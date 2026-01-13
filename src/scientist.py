import datetime
from google import genai
from google.genai import types
from sentence_transformers import SentenceTransformer, util
from src.config import *
from src.utils import compress_giant_file

print("📥 Loading Embedding Model...")
embedder = SentenceTransformer(EMBEDDING_MODEL_NAME)
current_cache = None

def find_files_by_vector(question_text, top_n=500):
    print(f"🧠 Understanding Question: '{question_text}'...")
    q_vec = embedder.encode(question_text, convert_to_tensor=True)
    all_files = list(DATA_DIR.rglob("*.md"))

    if not all_files:
        print("⚠️ No .md files found! Run preprocess.py first.")
        return []

    scored_files = []
    batch_size = 100
    for i in range(0, len(all_files), batch_size):
        batch = all_files[i : i+batch_size]
        texts = []
        valid_batch = []
        for p in batch:
            try:
                texts.append(p.read_text(encoding='utf-8')[:1000])
                valid_batch.append(p)
            except: continue
        if not texts: continue
        embeddings = embedder.encode(texts, convert_to_tensor=True)
        scores = util.cos_sim(q_vec, embeddings)[0]
        for p, score in zip(valid_batch, scores):
            if score.item() > 0.30: scored_files.append((p, score.item()))

    scored_files.sort(key=lambda x: x[1], reverse=True)
    return [f[0] for f in scored_files[:top_n]]

def ask_expert(question):
    global current_cache
    if not API_KEY: return "❌ No API Key found."
    client = genai.Client(api_key=API_KEY)

    # Always refresh cache for new context
    if current_cache:
        try: client.caches.delete(name=current_cache)
        except: pass

    files = find_files_by_vector(question)
    if not files: return "❌ No relevant papers found."

    full_text = ""
    for p in files:
        text = p.read_text(encoding="utf-8")
        if len(text) > GIANT_FILE_THRESHOLD: text = compress_giant_file(text, question, p.name)
        else: text = f"\n\n--- FILE: {p.name} ---\n{text}\n"
        if len(full_text) + len(text) > MAX_CACHE_SIZE: break
        full_text += text

    ttl_seconds = int(datetime.timedelta(hours=CACHE_TTL_HOURS).total_seconds())
    try:
        cache = client.caches.create(
            model=TARGET_MODEL,
            config=types.CreateCachedContentConfig(
                contents=[types.Content(role='user', parts=[types.Part(text=full_text)])],
                system_instruction=f"Answer strictly based on these papers. Context: {question}",
                ttl=f"{ttl_seconds}s"
            )
        )
        current_cache = cache.name
        response = client.models.generate_content(
            model=TARGET_MODEL,
            contents=[types.Content(role='user', parts=[types.Part(text=question)])],
            config=types.GenerateContentConfig(cached_content=cache.name, temperature=0.3)
        )
        return response.text
    except Exception as e: return f"❌ API Error: {e}"
