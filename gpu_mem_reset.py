#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GPU 메모리 초기화 스크립트
- PyTorch 캐시 비우기
- Python 객체 참조 제거
- 가비지 컬렉션 실행
- PyTorch IPC 객체 정리
- 정리 전후 메모리 정보 출력
"""

import torch
import gc
import sys

def print_memory(title=""):
    allocated = torch.cuda.memory_allocated() / 1024**3
    reserved  = torch.cuda.memory_reserved()  / 1024**3
    print(f"{title} GPU 메모리 사용량:")
    print(f"- allocated : {allocated:.2f} GB")
    print(f"- reserved  : {reserved:.2f} GB\n")

def clear_gpu_memory():
    print_memory("[BEFORE]")

    # 객체 참조 제거
    for name in dir():
        if not name.startswith("_"):
            del globals()[name]

    # 가비지 수집 및 캐시 비우기
    gc.collect()
    torch.cuda.empty_cache()
    torch.cuda.ipc_collect()
    torch.cuda.reset_peak_memory_stats()

    print_memory("[AFTER]")

if __name__ == "__main__":
    if torch.cuda.is_available():
        clear_gpu_memory()
    else:
        print("CUDA 사용 불가: GPU가 감지되지 않았습니다.")
