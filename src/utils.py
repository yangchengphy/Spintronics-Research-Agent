from google import genai
from src.config import API_KEY, COMPRESSOR_MODEL

def compress_giant_file(text, context, filename):
    print(f"   ✂️ Compressing giant file ({len(text):,} chars): {filename}...")
    if not API_KEY: return text[:10000]

    client = genai.Client(api_key=API_KEY)
    try:
        response = client.models.generate_content(
            model=COMPRESSOR_MODEL,
            contents=[f"Extract experimental data regarding '{context}' from this text:", text]
        )
        return f"--- SUMMARY: {filename} ---\n{response.text}\n"
    except: return ""
