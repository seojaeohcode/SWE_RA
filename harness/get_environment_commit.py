#!/usr/bin/env python3
"""
MONAI 저장소에서 환경 설정 커밋을 찾기
"""

import os
import subprocess
import re
from pathlib import Path

def get_environment_setup_commit():
    """환경 설정 커밋을 찾습니다."""
    
    # MONAI 저장소가 있는지 확인
    repo_path = "MONAI"
    if not os.path.exists(repo_path):
        print("📥 MONAI 저장소 클론 중...")
        subprocess.run([
            "git", "clone", "https://github.com/Project-MONAI/MONAI.git", repo_path
        ], check=True)
    
    # 저장소 디렉토리로 이동
    os.chdir(repo_path)
    
    try:
        # 환경 설정 관련 파일들의 최근 커밋 찾기
        env_files = [
            "requirements.txt",
            "setup.py", 
            "pyproject.toml",
            "environment.yml",
            "Dockerfile",
            ".github/workflows/",
            "docker/"
        ]
        
        latest_commit = None
        for file_path in env_files:
            if os.path.exists(file_path):
                # 파일의 최근 커밋 해시 찾기
                result = subprocess.run([
                    "git", "log", "--oneline", "-1", "--", file_path
                ], capture_output=True, text=True)
                
                if result.stdout:
                    commit_hash = result.stdout.split()[0]
                    if not latest_commit:
                        latest_commit = commit_hash
                    else:
                        # 더 최근 커밋 선택
                        result2 = subprocess.run([
                            "git", "log", "--oneline", "--format=%H", "-1", "--", file_path
                        ], capture_output=True, text=True)
                        if result2.stdout:
                            latest_commit = result2.stdout.strip()
        
        if latest_commit:
            return latest_commit
        
        # 기본값: 최근 커밋
        result = subprocess.run([
            "git", "log", "--oneline", "-1", "--format=%H"
        ], capture_output=True, text=True)
        
        if result.stdout:
            return result.stdout.strip()
        
    except Exception as e:
        print(f"⚠️ 커밋 찾기 실패: {e}")
    
    # 기본값
    return "67023b85c41d23d6c6d69812a41b207c4f8a9331"

def main():
    """메인 함수"""
    print("🚀 MONAI 환경 설정 커밋 찾기")
    
    commit = get_environment_setup_commit()
    print(f"✅ 환경 설정 커밋: {commit}")
    
    # 파일로 저장
    with open("monai_env_commit.txt", "w") as f:
        f.write(commit)
    
    print(f"✅ 커밋 정보를 monai_env_commit.txt에 저장 완료")

if __name__ == "__main__":
    main() 