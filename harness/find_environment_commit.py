#!/usr/bin/env python3
"""
MONAI 저장소에서 환경 설정 커밋을 정확히 찾기
"""

import os
import subprocess
import re
from pathlib import Path
from datetime import datetime

def clone_monai_repo():
    """MONAI 저장소를 클론합니다."""
    repo_path = "MONAI"
    if not os.path.exists(repo_path):
        print("📥 MONAI 저장소 클론 중...")
        subprocess.run([
            "git", "clone", "https://github.com/Project-MONAI/MONAI.git", repo_path
        ], check=True)
        print("✅ MONAI 저장소 클론 완료")
    else:
        print("✅ MONAI 저장소 이미 존재")
    return repo_path

def get_file_commit_info(repo_path, file_path):
    """파일의 커밋 정보를 가져옵니다."""
    try:
        # 파일이 존재하는지 확인
        full_path = os.path.join(repo_path, file_path)
        if not os.path.exists(full_path):
            return None
        
        # 파일의 최근 커밋 정보 가져오기
        result = subprocess.run([
            "git", "log", "--oneline", "--format=%H|%an|%ad|%s", "-1", "--", file_path
        ], capture_output=True, text=True, cwd=repo_path)
        
        if result.stdout.strip():
            commit_hash, author, date, message = result.stdout.strip().split('|', 3)
            return {
                'hash': commit_hash,
                'author': author,
                'date': date,
                'message': message,
                'file': file_path
            }
    except Exception as e:
        print(f"⚠️ {file_path} 커밋 정보 가져오기 실패: {e}")
    
    return None

def find_environment_commits(repo_path):
    """환경 설정 관련 커밋들을 찾습니다."""
    
    # 환경 설정 관련 파일들
    env_files = [
        "requirements.txt",
        "setup.py",
        "pyproject.toml", 
        "environment.yml",
        "Dockerfile",
        "docker/Dockerfile",
        ".github/workflows/ci.yml",
        ".github/workflows/test.yml",
        "setup.cfg",
        "MANIFEST.in",
        "tox.ini",
        "pytest.ini"
    ]
    
    print("🔍 환경 설정 파일들의 커밋 정보 찾는 중...")
    
    commits = []
    for file_path in env_files:
        commit_info = get_file_commit_info(repo_path, file_path)
        if commit_info:
            commits.append(commit_info)
            print(f"  ✅ {file_path}: {commit_info['hash'][:8]} - {commit_info['message']}")
    
    return commits

def find_most_recent_commit(commits):
    """가장 최근 커밋을 찾습니다."""
    if not commits:
        return None
    
    # 날짜 기준으로 정렬
    def parse_date(date_str):
        try:
            return datetime.strptime(date_str, '%a %b %d %H:%M:%S %Y %z')
        except:
            return datetime.min
    
    sorted_commits = sorted(commits, key=lambda x: parse_date(x['date']), reverse=True)
    return sorted_commits[0]

def find_setup_related_commits(repo_path):
    """설정 관련 커밋들을 찾습니다."""
    try:
        # "setup", "requirements", "environment" 관련 커밋들 찾기
        result = subprocess.run([
            "git", "log", "--oneline", "--format=%H|%an|%ad|%s", 
            "--grep=setup", "--grep=requirements", "--grep=environment", "--grep=docker",
            "-10"
        ], capture_output=True, text=True, cwd=repo_path)
        
        if result.stdout.strip():
            commits = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    parts = line.split('|', 3)
                    if len(parts) == 4:
                        commits.append({
                            'hash': parts[0],
                            'author': parts[1], 
                            'date': parts[2],
                            'message': parts[3]
                        })
            return commits
    except Exception as e:
        print(f"⚠️ 설정 관련 커밋 찾기 실패: {e}")
    
    return []

def main():
    """메인 함수"""
    print("🚀 MONAI 환경 설정 커밋 찾기")
    
    # 1. 저장소 클론
    repo_path = clone_monai_repo()
    
    # 2. 환경 설정 파일들의 커밋 찾기
    env_commits = find_environment_commits(repo_path)
    
    # 3. 가장 최근 커밋 선택
    most_recent = find_most_recent_commit(env_commits)
    
    # 4. 설정 관련 커밋들도 확인
    setup_commits = find_setup_related_commits(repo_path)
    
    # 5. 최종 선택
    final_commit = None
    if most_recent:
        final_commit = most_recent['hash']
        print(f"\n✅ 선택된 환경 커밋: {final_commit}")
        print(f"   파일: {most_recent['file']}")
        print(f"   메시지: {most_recent['message']}")
        print(f"   날짜: {most_recent['date']}")
    else:
        # 기본값
        final_commit = "67023b85c41d23d6c6d69812a41b207c4f8a9331"
        print(f"\n⚠️ 환경 커밋을 찾을 수 없어 기본값 사용: {final_commit}")
    
    # 6. 결과 저장
    with open("monai_environment_commit.txt", "w") as f:
        f.write(final_commit)
    
    print(f"\n📊 요약:")
    print(f"  - 환경 설정 파일 커밋: {len(env_commits)}개")
    print(f"  - 설정 관련 커밋: {len(setup_commits)}개")
    print(f"  - 최종 선택: {final_commit}")
    
    # 7. 상세 정보 저장
    commit_details = {
        "selected_commit": final_commit,
        "environment_file_commits": env_commits,
        "setup_related_commits": setup_commits[:5]  # 상위 5개만
    }
    
    with open("monai_environment_commit_details.json", "w") as f:
        import json
        json.dump(commit_details, f, indent=2, default=str)
    
    print(f"✅ 상세 정보를 monai_environment_commit_details.json에 저장 완료")

if __name__ == "__main__":
    main() 