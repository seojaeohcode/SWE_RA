from datasets import load_dataset

# SWE-bench_bm25_13K 다운로드
bench_dataset = load_dataset(
    "princeton-nlp/SWE-bench_bm25_13K",
    cache_dir="./data/SWE-bench_bm25_13K"
)
print("=== SWE-bench_bm25_13K ===")
for split in bench_dataset:
    print(f"✅ Split '{split}' downloaded: {len(bench_dataset[split])} samples")

# SWE-bench_Lite_bm25_13K 다운로드
lite_dataset = load_dataset(
    "princeton-nlp/SWE-bench_Lite_bm25_13K",
    cache_dir="./data/SWE-bench_Lite_bm25_13K"
)
print("\n=== SWE-bench_Lite_bm25_13K ===")
for split in lite_dataset:
    print(f"✅ Split '{split}' downloaded: {len(lite_dataset[split])} samples")