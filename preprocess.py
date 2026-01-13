import multiprocessing
from multiprocessing import Pool, cpu_count
from pathlib import Path
from tqdm import tqdm
from src import converter

# CONFIG
BASE_DIR = Path(__file__).parent
INPUT_DIR = BASE_DIR / "data" / "raw_pdfs"
OUTPUT_DIR = BASE_DIR / "data" / "processed_papers"

def run_processing():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    pdf_files = [str(p) for p in INPUT_DIR.rglob("*.pdf")]

    if not pdf_files:
        print(f"⚠️ No PDFs found in {INPUT_DIR}")
        return

    print(f"🚀 Found {len(pdf_files)} PDFs. Starting Refinery...")

    # Test One
    print("Running diagnostic on 1 file...")
    try:
        converter.process_one(pdf_files[0], OUTPUT_DIR)
        print("Diagnostic: Success")
    except Exception as e:
        print(f"❌ Diagnostic Failed: {e}")
        return

    # Run Batch
    workers = max(1, cpu_count() - 2) 
    print(f"Starting batch with {workers} workers...")

    tasks = [(f, OUTPUT_DIR) for f in pdf_files]

    with Pool(processes=workers) as pool:
        for _ in tqdm(pool.imap_unordered(converter.process_one_wrapper, tasks, chunksize=5), total=len(tasks)):
            pass

    print("\n✅ Processing Complete.")

if __name__ == "__main__":
    multiprocessing.freeze_support() 
    run_processing()
