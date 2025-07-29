#!/usr/bin/env python3
"""
MONAI 저장소에서 모든 필요한 정보를 생성
"""

import os
import json
import subprocess
from pathlib import Path

def run_script(script_name):
    """스크립트를 실행합니다."""
    print(f"🔄 {script_name} 실행 중...")
    try:
        result = subprocess.run(["python3", script_name], 
                              capture_output=True, text=True, cwd=".")
        if result.returncode == 0:
            print(f"✅ {script_name} 완료")
            return True
        else:
            print(f"❌ {script_name} 실패: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {script_name} 실행 오류: {e}")
        return False

def load_file_content(filename):
    """파일 내용을 로드합니다."""
    try:
        with open(filename, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""

def main():
    """메인 함수"""
    print("🚀 MONAI 정보 생성 시작")
    
    # 1. 테스트 정보 수집
    if run_script("collect_monai_tests.py"):
        test_info_file = "monai_test_info.json"
        if os.path.exists(test_info_file):
            with open(test_info_file, 'r') as f:
                test_info = json.load(f)
            print(f"✅ 테스트 정보 로드: FAIL_TO_PASS {len(test_info['FAIL_TO_PASS'])}개, PASS_TO_PASS {len(test_info['PASS_TO_PASS'])}개")
        else:
            test_info = {"FAIL_TO_PASS": [], "PASS_TO_PASS": []}
    else:
        test_info = {"FAIL_TO_PASS": [], "PASS_TO_PASS": []}
    
    # 2. 테스트 패치 생성
    if run_script("generate_test_patch.py"):
        test_patch = load_file_content("monai_test_patch.diff")
        print(f"✅ 테스트 패치 생성: {len(test_patch)} 문자")
    else:
        test_patch = ""
    
    # 3. 버전 정보 추출
    if run_script("get_monai_version.py"):
        version = load_file_content("monai_version.txt")
        print(f"✅ 버전 정보: {version}")
    else:
        version = "1.0.0"
    
    # 4. 환경 설정 커밋 찾기 (이미 생성된 파일이 있으면 사용)
    env_commit_file = "monai_environment_commit.txt"
    if os.path.exists(env_commit_file):
        env_commit = load_file_content(env_commit_file)
        print(f"✅ 기존 환경 설정 커밋 로드: {env_commit}")
    else:
        # 새로 생성
        if run_script("find_environment_commit.py"):
            env_commit = load_file_content(env_commit_file)
            print(f"✅ 환경 설정 커밋 생성: {env_commit}")
        else:
            env_commit = "67023b85c41d23d6c6d69812a41b207c4f8a9331"
            print(f"⚠️ 환경 커밋 생성 실패, 기본값 사용: {env_commit}")
    
    # 5. 모든 정보를 통합하여 저장
    monai_info = {
        "test_info": test_info,
        "test_patch": test_patch,
        "version": version,
        "environment_setup_commit": env_commit
    }
    
    with open("monai_complete_info.json", "w") as f:
        json.dump(monai_info, f, indent=2)
    
    print("✅ 모든 MONAI 정보 생성 완료: monai_complete_info.json")
    print(f"📊 요약:")
    print(f"  - FAIL_TO_PASS: {len(test_info['FAIL_TO_PASS'])}개")
    print(f"  - PASS_TO_PASS: {len(test_info['PASS_TO_PASS'])}개")
    print(f"  - 테스트 패치: {len(test_patch)} 문자")
    print(f"  - 버전: {version}")
    print(f"  - 환경 커밋: {env_commit}")

if __name__ == "__main__":
    main() 