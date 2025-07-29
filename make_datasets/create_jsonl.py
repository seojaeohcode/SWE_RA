# ---------------------------------------------------------------------
# MONAI PR → SWE‑bench‑lite JSONL 생성 스크립트 (수정 버전)
# - problem_statement  : SWE‑bench 프롬프트용 텍스트
# - base_commit        : checkout 에 사용될 SHA
# ---------------------------------------------------------------------

import os
import json

# 디렉토리 및 파일 경로 설정
PATCH_DIR = "patches"
BM25_RESULT_FILE = "bm25_text_results.jsonl"
FILTERED_PR_FILE = "filtered_prs.json"
OUTPUT_FILE = "monai_swe_lite.jsonl"

# BM25 결과 불러오기 (instance_id → hits 매핑)
bm25_map = {}
with open(BM25_RESULT_FILE, "r", encoding="utf-8") as f:
    for line in f:
        item = json.loads(line)
        # instance_id에서 pr_number 추출 (MONAI_123 → 123)
        pr_number = int(item["instance_id"].split("_")[-1])
        bm25_map[pr_number] = item["hits"]

# PR 정보 로딩
with open(FILTERED_PR_FILE, "r", encoding="utf-8") as f:
    prs = json.load(f)

# 최종 인스턴스 생성
with open(OUTPUT_FILE, "w", encoding="utf-8") as out_f:
    for pr in prs:
        pr_number = pr["number"]
        patch_path = os.path.join(PATCH_DIR, f"pr_{pr_number}.patch")

        if not os.path.exists(patch_path):
            print(f"⚠️ 패치 누락: PR #{pr_number}")
            continue

        if pr_number not in bm25_map:
            print(f"⚠️ BM25 결과 누락: PR #{pr_number}")
            continue

        # 패치 파일 로딩
        with open(patch_path, "r", encoding="utf-8") as pf:
            patch_content = pf.read()

        # SWE‑bench 호환 인스턴스 생성
        instance = {
            "instance_id": f"Project-MONAI/MONAI/{pr_number}",
            "repo": "Project-MONAI/MONAI",

            # ↓ SWE‑bench 필수 컬럼 --------------------------
            "problem_statement": (
                (pr.get("title") or "") + "\n\n" + (pr.get("body") or "")
            ),
            "base_commit": pr.get("base_sha", ""),
            # ----------------------------------------------

            # 기타 정보(선택) -------------------------------
            "issue_number": pr_number,
            "issue_title": pr.get("title", ""),
            "issue_body": pr.get("body", ""),
            # ----------------------------------------------

            "patch": patch_content,
            "hits": bm25_map[pr_number]  # BM25 hits 저장 (create_instance.py에서 사용)
        }

        # 📄 JSONL로 저장
        out_f.write(json.dumps(instance, ensure_ascii=False) + "\n")
        print(f"✅ PR #{pr_number} 인스턴스 저장 완료")
