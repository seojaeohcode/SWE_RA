#!/usr/bin/env python3
"""
MONAI 데이터셋을 SWE-bench 형식으로 변환
"""

import json
from pathlib import Path
from datasets import load_from_disk

def load_monai_info():
    """MONAI 정보를 로드합니다."""
    # 1. 완전한 정보 파일 시도
    info_file = "own_code/monai_complete_info.json"
    try:
        with open(info_file, 'r') as f:
            monai_info = json.load(f)
        print(f"✅ 완전한 MONAI 정보 로드 완료")
        return monai_info
    except FileNotFoundError:
        pass
    
    # 2. 테스트 정보만 시도
    test_info_file = "own_code/monai_test_info.json"
    try:
        with open(test_info_file, 'r') as f:
            test_info = json.load(f)
        print(f"✅ 테스트 정보 로드 완료: FAIL_TO_PASS {len(test_info['FAIL_TO_PASS'])}개, PASS_TO_PASS {len(test_info['PASS_TO_PASS'])}개")
        return {
            "test_info": test_info,
            "test_patch": "",
            "version": "1.0.0",
            "environment_setup_commit": ""
        }
    except FileNotFoundError:
        print("⚠️ MONAI 정보 파일이 없습니다. 기본값으로 설정합니다.")
        return {
            "test_info": {"FAIL_TO_PASS": [], "PASS_TO_PASS": []},
            "test_patch": "",
            "version": "1.0.0",
            "environment_setup_commit": ""
        }

def convert_monai_to_swebench_format():
    """MONAI 데이터셋을 SWE-bench 형식으로 변환"""
    
    # MONAI 정보 로드
    monai_info = load_monai_info()
    
    # MONAI 데이터셋 로드
    dataset_path = "data/monai_dataset/own_code__monai_dataset__style-3__fs-bm25"
    dataset = load_from_disk(dataset_path)
    
    # SWE-bench 형식으로 변환
    swebench_instances = []
    
    for item in dataset['train']:
        # SWE-bench 형식으로 변환
        swebench_instance = {
            "instance_id": item['instance_id'],
            "repo": "Project-MONAI/MONAI",  # MONAI 저장소
            "base_commit": item['base_commit'],
            "problem_statement": item['problem_statement'],
            "patch": item['patch'],  # 실제 패치 (gold)
            "test_patch": monai_info['test_patch'],  # 생성된 테스트 패치
            "version": monai_info['version'],  # 실제 버전
            "FAIL_TO_PASS": monai_info['test_info']['FAIL_TO_PASS'],  # 실제 테스트 정보
            "PASS_TO_PASS": monai_info['test_info']['PASS_TO_PASS'],  # 실제 테스트 정보
            "environment_setup_commit": monai_info['environment_setup_commit'],  # 환경 설정 커밋
        }
        swebench_instances.append(swebench_instance)
    
    # JSON 파일로 저장
    output_file = "monai_swebench_format.json"
    with open(output_file, 'w') as f:
        json.dump(swebench_instances, f, indent=2)
    
    print(f"✅ {len(swebench_instances)}개 인스턴스를 {output_file}로 변환 완료")
    print(f"📊 인스턴스 ID들: {[inst['instance_id'] for inst in swebench_instances[:5]]}...")
    print(f"📊 사용된 정보:")
    print(f"  - 테스트 패치: {len(monai_info['test_patch'])} 문자")
    print(f"  - 버전: {monai_info['version']}")
    print(f"  - FAIL_TO_PASS: {len(monai_info['test_info']['FAIL_TO_PASS'])}개")
    print(f"  - PASS_TO_PASS: {len(monai_info['test_info']['PASS_TO_PASS'])}개")
    print(f"  - 환경 커밋: {monai_info['environment_setup_commit']}")
    
    return output_file

if __name__ == "__main__":
    convert_monai_to_swebench_format() 