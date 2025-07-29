import json
import matplotlib.pyplot as plt
from collections import Counter

# JSON 로딩
with open("princeton-nlp__SWE-Llama-7b.swe_llama7b_bm25_eval.json", "r") as f:
    data = json.load(f)

submitted_ids = data.get("submitted_ids", [])
project_counts = Counter()

for sid in submitted_ids:
    if "__" in sid:
        project = sid.split("__")[0]
        project_counts[project] += 1

# 상위 N개 + 기타 묶기
top_n = 10
common_projects = project_counts.most_common(top_n)
other_count = sum(project_counts.values()) - sum(count for _, count in common_projects)

labels = [f"{proj} ({count})" for proj, count in common_projects]
sizes = [count for _, count in common_projects]
if other_count > 0:
    labels.append(f"Other ({other_count})")
    sizes.append(other_count)

# 색상 설정 (matplotlib 3.4 호환)
cmap = plt.get_cmap("tab20")
colors = [cmap(i / len(labels)) for i in range(len(labels))]

# 퍼센트 항상 표시
def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct * total / 100.0))
        return f'{pct:.1f}%'
    return my_autopct

# 그래프 그리기
fig, ax = plt.subplots(figsize=(10, 8))
wedges, texts, autotexts = ax.pie(
    sizes,
    labels=labels,
    autopct=make_autopct(sizes),
    startangle=140,
    colors=colors,
    pctdistance=0.75,
    labeldistance=1.1
)

# 폰트 크기 조정
for text in texts:
    text.set_fontsize(10)
for autotext in autotexts:
    autotext.set_fontsize(9)

# 제목 및 저장
plt.title("Project-wise Submission Distribution (SWE-Llama-7B BM25 Eval)", pad=40)
plt.subplots_adjust(top=0.85)
plt.axis("equal")
plt.tight_layout()
plt.savefig("submitted_projects_distribution_fixed.png", dpi=300)
plt.close()
