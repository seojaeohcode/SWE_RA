#!/usr/bin/env python3
"""
MONAI 저장소에서 버전 정보를 추출
"""

import os
import subprocess
import re
from pathlib import Path

def get_monai_version():
    """MONAI 버전을 추출합니다."""
    
    # MONAI 저장소가 있는지 확인
    repo_path = "MONAI"
    if not os.path.exists(repo_path):
        print("📥 MONAI 저장소 클론 중...")
        subprocess.run([
            "git", "clone", "https://github.com/Project-MONAI/MONAI.git", repo_path
        ], check=True)
    
    # setup.py에서 버전 추출
    setup_py_path = os.path.join(repo_path, "setup.py")
    if os.path.exists(setup_py_path):
        with open(setup_py_path, 'r') as f:
            content = f.read()
            # version = "1.3.0" 패턴 찾기
            version_match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
            if version_match:
                return version_match.group(1)
    
    # __init__.py에서 버전 추출
    init_py_path = os.path.join(repo_path, "monai", "__init__.py")
    if os.path.exists(init_py_path):
        with open(init_py_path, 'r') as f:
            content = f.read()
            # __version__ = "1.3.0" 패턴 찾기
            version_match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
            if version_match:
                return version_match.group(1)
    
    # pyproject.toml에서 버전 추출
    pyproject_path = os.path.join(repo_path, "pyproject.toml")
    if os.path.exists(pyproject_path):
        with open(pyproject_path, 'r') as f:
            content = f.read()
            # version = "1.3.0" 패턴 찾기
            version_match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
            if version_match:
                return version_match.group(1)
    
    # 기본값 반환
    return "1.0.0"

def main():
    """메인 함수"""
    print("🚀 MONAI 버전 추출")
    
    version = get_monai_version()
    print(f"✅ MONAI 버전: {version}")
    
    # 파일로 저장
    with open("monai_version.txt", "w") as f:
        f.write(version)
    
    print(f"✅ 버전 정보를 monai_version.txt에 저장 완료")

if __name__ == "__main__":
    main() 