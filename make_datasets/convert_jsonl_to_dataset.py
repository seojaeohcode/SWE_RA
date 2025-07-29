#!/usr/bin/env python3

"""
JSONL 파일을 HuggingFace Dataset 형식으로 변환하는 스크립트
"""

import json
import os
from pathlib import Path
from datasets import Dataset, DatasetDict

def convert_jsonl_to_dataset(jsonl_file, output_dir):
    """
    JSONL 파일을 HuggingFace Dataset으로 변환
    
    Args:
        jsonl_file (str): 입력 JSONL 파일 경로
        output_dir (str): 출력 디렉토리 경로
    """
    # JSONL 파일 읽기
    data = []
    with open(jsonl_file, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line.strip()))
    
    print(f"📄 {len(data)}개의 인스턴스를 로드했습니다")
    
    # Dataset 생성
    dataset = Dataset.from_list(data)
    dataset_dict = DatasetDict({"train": dataset})
    
    # 저장
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    dataset_dict.save_to_disk(output_path)
    
    print(f"Dataset을 {output_path}에 저장했습니다")
    print(f"Dataset 정보:")
    print(f"   - Train split: {len(dataset)} 인스턴스")
    print(f"   - 컬럼: {list(dataset.column_names)}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="JSONL을 HuggingFace Dataset으로 변환")
    parser.add_argument("--input", required=True, help="입력 JSONL 파일 경로")
    parser.add_argument("--output", required=True, help="출력 디렉토리 경로")
    
    args = parser.parse_args()
    
    convert_jsonl_to_dataset(args.input, args.output) 