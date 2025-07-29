import json
import matplotlib.pyplot as plt
from collections import Counter, defaultdict

# 분석할 평가 결과 json 파일명
EVAL_JSON = "princeton-nlp__SWE-Llama-7b.swe_llama7b_bm25_eval.json"

# 프로젝트 이름 추출 함수
def get_project(instance_id):
    return instance_id.split('__')[0] if '__' in instance_id else instance_id

# 평가 결과 로드
def load_eval_json(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)

data = load_eval_json(EVAL_JSON)

# 전체 제출/해결 인스턴스 id
submitted_ids = data.get('submitted_ids', [])
resolved_ids = set(data.get('resolved_ids', []))

# 프로젝트별 제출/해결 카운트
submitted_counts = defaultdict(int)
resolved_counts = defaultdict(int)

for iid in submitted_ids:
    proj = get_project(iid)
    submitted_counts[proj] += 1
    if iid in resolved_ids:
        resolved_counts[proj] += 1

# 모든 프로젝트 이름 정렬
projects = sorted(submitted_counts.keys())

# 해결 비율 계산
resolved_ratios = [
    (resolved_counts.get(proj, 0) / submitted_counts[proj]) * 100 for proj in projects
]

# 그래프 생성
fig, ax = plt.subplots(figsize=(max(8, len(projects)), 4))
bars = ax.bar(projects, resolved_ratios, color='#f4b942', label='Resolved %')

# y축 범위 자동 조정 (최대 5% 이상이면 10%까지)
max_ratio = max(resolved_ratios) if resolved_ratios else 1
ax.set_ylim(0, max(5, min(10, max_ratio + 2)))
ax.set_ylabel('% Resolved')
ax.set_title(f'{EVAL_JSON} - % Resolved per Project')
ax.legend()

# x축 라벨 회전 및 레이아웃 조정
plt.xticks(rotation=45)
plt.tight_layout()

# 파일로 저장
plt.savefig("swe_llama_resolved_rates.png", dpi=300)
