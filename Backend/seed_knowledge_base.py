import os
import Backend.rag_engine as rag_engine

SEED_DIR = os.path.join(os.path.dirname(__file__), "seed_data")

FILE_CATEGORY_MAP = {
    "courses.txt": "Academics",
    "admissions.txt": "Admissions",
    "exam_policy.txt": "Exams",
    "library.txt": "Library",
    "hostel_life.txt": "Hostel & Campus Life",
    "scholarships.txt": "Scholarships & Fees",
    "placement_cell.txt": "Placements & Career",
}

def run():
    if not rag_engine.is_empty():
        print("[seed] Knowledge base already populated, skipping seed load.")
        return

    print("[seed] Knowledge base is empty, loading sample education content...")
    total_chunks = 0
    for filename, category in FILE_CATEGORY_MAP.items():
        path = os.path.join(SEED_DIR, filename)
        if not os.path.exists(path):
            continue
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        n = rag_engine.add_document(source=filename, category=category, raw_text=text)
        total_chunks += n
        print(f"  - {filename} ({category}): {n} chunks")

    print(f"[seed] Done. {total_chunks} total chunks loaded.")

if __name__ == "__main__":
    run()