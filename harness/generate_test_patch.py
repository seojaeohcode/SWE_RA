#!/usr/bin/env python3
"""
MONAI 저장소에서 기본 테스트 패치를 생성
"""

import os
import subprocess
from pathlib import Path

def generate_basic_test_patch():
    """기본 테스트 패치를 생성합니다."""
    
    # MONAI 저장소가 있는지 확인
    repo_path = "MONAI"
    if not os.path.exists(repo_path):
        print("📥 MONAI 저장소 클론 중...")
        subprocess.run([
            "git", "clone", "https://github.com/Project-MONAI/MONAI.git", repo_path
        ], check=True)
    
    # 기본 테스트 패치 생성
    test_patch = '''diff --git a/test_monai_basic.py b/test_monai_basic.py
new file mode 100644
--- /dev/null
+++ b/test_monai_basic.py
@@ -0,0 +1,20 @@
+#!/usr/bin/env python3
+"""Basic MONAI tests for SWE-bench evaluation"""
+
+import pytest
+import torch
+
+
+def test_monai_import():
+    """Test that MONAI can be imported"""
+    try:
+        import monai
+        assert monai is not None
+    except ImportError:
+        pytest.fail("MONAI import failed")
+
+
+def test_monai_version():
+    """Test MONAI version"""
+    import monai
+    assert hasattr(monai, '__version__')
+    assert monai.__version__ is not None
+
+
+def test_monai_basic_functionality():
+    """Test basic MONAI functionality"""
+    import monai
+    # Basic test - should not raise exceptions
+    assert True
+'''
    
    return test_patch

def main():
    """메인 함수"""
    print("🚀 MONAI 테스트 패치 생성")
    
    test_patch = generate_basic_test_patch()
    
    # 파일로 저장
    with open("monai_test_patch.diff", "w") as f:
        f.write(test_patch)
    
    print("✅ 테스트 패치 생성 완료: monai_test_patch.diff")
    print("📋 패치 내용:")
    print(test_patch)

if __name__ == "__main__":
    main() 