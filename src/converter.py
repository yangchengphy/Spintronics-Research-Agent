import pymupdf4llm
from pathlib import Path

def process_one(pdf_path_str, output_dir):
    try:
        pdf_path = Path(pdf_path_str)
        output_path = output_dir / f"{pdf_path.stem}.md"
        if output_path.exists(): return "Skipped"
        md_text = pymupdf4llm.to_markdown(pdf_path_str)
        output_path.write_text(md_text, encoding="utf-8")
        return "Success"
    except Exception as e: return f"Error: {str(e)[:50]}"

def process_one_wrapper(args):
    return process_one(*args)
