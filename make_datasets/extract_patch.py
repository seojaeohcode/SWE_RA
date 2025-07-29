import os
import json
import subprocess

# 저장소 루트 디렉토리
REPO_PATH = "/mnt/c/Users/USER/Documents/MONAI"
PATCH_OUTPUT_DIR = "patches"

# 출력 디렉토리 생성
os.makedirs(PATCH_OUTPUT_DIR, exist_ok=True)

# PR 목록 로딩
with open("filtered_prs.json", "r", encoding="utf-8") as f:
    prs = json.load(f)

# 변경사항 임시 보관
try:
    subprocess.run(["git", "stash", "-u"], cwd=REPO_PATH, check=True)
    print("변경사항 stash 처리 완료")
except subprocess.CalledProcessError as e:
    print(f"stash 실패: {e}")

# 각 PR에 대해 patch 생성
for pr in prs:
    pr_number = pr["number"]
    base_sha = pr["base_sha"]
    merge_sha = pr["merge_commit_sha"]
    patch_file = os.path.join(PATCH_OUTPUT_DIR, f"pr_{pr_number}.patch")

    try:
        # base로 체크아웃
        subprocess.run(["git", "checkout", base_sha], cwd=REPO_PATH, check=True)

        # patch 추출
        with open(patch_file, "w", encoding="utf-8") as f:
            subprocess.run(
                ["git", "diff", f"{base_sha}..{merge_sha}"],
                cwd=REPO_PATH, check=True, stdout=f
            )

        print(f"PR #{pr_number} 패치 생성 완료")

    except subprocess.CalledProcessError as e:
        print(f"PR #{pr_number} 처리 실패: {e}")
        continue

# 마지막에 main 브랜치로 되돌리기
try:
    subprocess.run(["git", "checkout", "main"], cwd=REPO_PATH, check=True)
    print("🔄 main 브랜치로 복귀 완료")
except subprocess.CalledProcessError:
    print("⚠️ main 브랜치 복귀 실패 (직접 확인 필요)")