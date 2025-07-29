from github import Github
import json
import time

# 🔐 GitHub 토큰 입력
gh = Github("")

try:
    # 사용자 정보 확인
    user = gh.get_user()
    print(f"로그인된 사용자: {user.login}")
    
    # 저장소 접근
    repo = gh.get_repo("Project-MONAI/MONAI")
    print(f"저장소 이름: {repo.full_name}")

    # 첫 번째 PR 샘플 테스트 (PaginatedList는 인덱싱 필요)
    sample_prs = repo.get_pulls(state="closed", sort="updated", direction="desc")
    pr_list = list(sample_prs[:1])
    if pr_list:
        pr = pr_list[0]
        print(f"📄 PR 샘플 확인 - #{pr.number} 제목: {pr.title}")
    else:
        print("닫힌 PR이 없습니다.")

    # 전체 닫힌 PR 수집
    print("\n전체 PR 수집 중 (잠시 시간이 걸릴 수 있습니다)...")
    prs = list(repo.get_pulls(state="closed"))
    print(f"총 닫힌 PR 수: {len(prs)}")

    # 필터 조건 정의
    def is_valid_pr(pr):
        print(f"▶ PR #{pr.number} 검사 중...", end=" ")

        if not pr.merged:
            print("❌ 병합되지 않음")
            return False
        if "fixes #" not in (pr.body or "").lower():
            print("❌ 이슈 링크 없음")
            return False
        try:
            files = pr.get_files()
        except Exception:
            print("❌ 파일 목록 불러오기 실패 (API 제한 가능성)")
            return False
        if not any("test" in f.filename.lower() for f in files):
            print("❌ 테스트 코드 없음")
            return False
        if pr.commits > 1:
            print("❌ 커밋 수 > 1")
            return False

        print("✅ 통과")
        return True

    # 필터링된 PR 저장
    valid_prs = []
    for pr in prs:
        try:
            if is_valid_pr(pr):
                valid_prs.append(pr)
            time.sleep(0.3)  # API rate limit 방지
        except Exception as e:
            print(f"⚠️ 예외 발생: {e}")
            continue

    print(f"\n유효한 PR 개수: {len(valid_prs)}")

    # 💾 JSON 저장
    result = []
    for pr in valid_prs:
        result.append({
            "number": pr.number,
            "title": pr.title,
            "body": pr.body,
            "base_sha": pr.base.sha,
            "merge_commit_sha": pr.merge_commit_sha,
            "url": pr.html_url
        })

    with open("filtered_prs.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print("\n저장 완료: filtered_prs2.json")

except Exception as e:
    print(f"\n전역 오류 발생: {e}")
