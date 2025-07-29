from datasets import load_from_disk
import json
import re

# 생성된 HuggingFace Dataset 로드
dataset = load_from_disk("../data/monai_dataset/own_code__monai_dataset__style-3__fs-bm25")

def format_text_field(text_content):
    if not text_content:
        return "No text available"
    
    # 태그별로 구분해서 출력
    lines = text_content.split('\n')
    formatted_sections = []
    
    current_section = ""
    current_tag = ""
    
    for line in lines:
        if line.strip() == "":
            continue
            
        if line.startswith('<issue>'):
            current_tag = "issue"
            current_section = "🐛 ISSUE SECTION:\n" + "="*50 + "\n"
        elif line.startswith('</issue>'):
            formatted_sections.append(current_section)
            current_section = ""
            current_tag = ""
        elif line.startswith('<code>'):
            current_tag = "code"
            current_section = "\n📁 CODE SECTION:\n" + "="*50 + "\n"
        elif line.startswith('</code>'):
            formatted_sections.append(current_section)
            current_section = ""
            current_tag = ""
        elif line.startswith('<patch>'):
            current_tag = "patch"
            current_section = "\n🔧 PATCH EXAMPLE:\n" + "="*50 + "\n"
        elif line.startswith('</patch>'):
            formatted_sections.append(current_section)
            current_section = ""
            current_tag = ""
        elif line.startswith('[start of'):
            current_section += f"\n📄 {line}\n"
        elif line.startswith('[end of'):
            current_section += f"{line}\n"
        elif current_tag == "issue":
            current_section += f"{line}\n"
        elif current_tag == "code":
            current_section += f"{line}\n"
        elif current_tag == "patch":
            current_section += f"{line}\n"
        else:
            current_section += f"{line}\n"
    
    return "\n".join(formatted_sections)

# 상위 n개 출력
n = 1
for i in range(n):
    print(f"\n{'='*80}")
    print(f"📋 TEXT FIELD PREVIEW - Instance {i}")
    print(f"{'='*80}")
    
    instance = dataset['train'][i]
    
    # 기본 정보
    print(f"🆔 Instance ID: {instance.get('instance_id', 'N/A')}")
    print(f"📊 Text Length: {len(instance.get('text', '')):,} characters")
    print(f"🔧 Patch Length: {len(instance.get('patch', '')):,} characters")
    
    # hits 정보
    hits = instance.get('hits', [])
    print(f"🔍 BM25 Hits: {len(hits)} files")
    if hits:
        print("   Files included:")
        for j, hit in enumerate(hits[:5]):
            print(f"   {j+1}. {hit.get('docid', 'N/A')}")
    
    print(f"\n{'='*80}")
    print("📄 FULL TEXT CONTENT:")
    print("="*80)
    
    # text 필드 가독성 좋게 출력
    text_content = instance.get('text', '')
    formatted_text = format_text_field(text_content)
    print(formatted_text)
    
    print(f"\n{'='*80}")
    print("📄 RAW TEXT CONTENT (first 2000 chars):")
    print("="*80)
    print(text_content[:2000])
    if len(text_content) > 2000:
        print(f"\n... (truncated, total length: {len(text_content):,} characters)")
    
    print(f"\n{'='*80}")
