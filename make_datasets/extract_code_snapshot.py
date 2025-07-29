import os
import json
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils import ingest_directory_contents  # 절대 임포트로 수정
import subprocess

# 설정
REPO_PATH = "/mnt/c/Users/USER/Documents/MONAI"
OUTPUT_DIR = "code_snapshots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# PR 목록 불러오기
with open("filtered_prs.json", "r", encoding="utf-8") as f:
    prs = json.load(f)

# 각 PR마다 base commit 기준으로 전체 코드 수집
for pr in prs:
    pr_number = pr["number"]
    base_sha = pr["base_sha"]
    snapshot_file = os.path.join(OUTPUT_DIR, f"pr_{pr_number}_code.json")

    try:
        # base commit으로 이동
        subprocess.run(["git", "checkout", base_sha], cwd=REPO_PATH, check=True)

        # 전체 코드 수집 (테스트 코드는 제외)
        code_corpus = ingest_directory_contents(REPO_PATH, include_tests=False)

        # 저장
        with open(snapshot_file, "w", encoding="utf-8") as f:
            json.dump(code_corpus, f, indent=2, ensure_ascii=False)

        print(f"PR #{pr_number} 코드 스냅샷 저장 완료")

    except Exception as e:
        print(f"PR #{pr_number} 코드 수집 실패: {e}")
