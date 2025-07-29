#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
BM25 기반으로 PR 설명과 코드 스냅샷을 매칭해 가장 관련 높은 파일 Top‑K를 찾습니다.
"""

import json
import os
import sys
import re
from collections import defaultdict
import math

# BM25 구현
class BM25Retriever:
    def __init__(self, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.documents = []
        self.doc_freq = defaultdict(int)  # term -> number of docs containing term
        self.term_freq = []  # list of dicts, each dict is doc_id -> term_freq
        self.doc_lengths = []
        self.avg_doc_length = 0
        self.N = 0  # total number of documents
        
    def fit(self, documents):
        """
        documents: list of dicts with 'docid' and 'content' keys
        """
        self.documents = documents
        self.N = len(documents)
        
        # Calculate document frequencies and lengths
        for doc in documents:
            doc_id = doc['docid']
            content = doc['content']
            
            # Tokenize content (simple word splitting)
            terms = re.findall(r'\b\w+\b', content.lower())
            
            # Calculate term frequencies for this document
            term_freq = defaultdict(int)
            for term in terms:
                term_freq[term] += 1
                self.doc_freq[term] += 1
            
            self.term_freq.append(term_freq)
            self.doc_lengths.append(len(terms))
        
        # Calculate average document length
        self.avg_doc_length = sum(self.doc_lengths) / self.N if self.N > 0 else 0
    
    def search(self, query, top_k=20):
        """
        query: string to search for
        top_k: number of top results to return
        """
        # Tokenize query
        query_terms = re.findall(r'\b\w+\b', query.lower())
        
        scores = []
        for i, doc in enumerate(self.documents):
            score = 0
            doc_length = self.doc_lengths[i]
            
            for term in query_terms:
                if term in self.doc_freq:
                    # Calculate IDF with safety check
                    df = self.doc_freq[term]
                    if df > 0 and df < self.N:
                        idf = math.log((self.N - df + 0.5) / (df + 0.5))
                    else:
                        idf = 0  # Skip terms that appear in all or no documents
                    
                    # Calculate TF
                    tf = self.term_freq[i].get(term, 0)
                    
                    # Calculate BM25 score
                    numerator = tf * (self.k1 + 1)
                    denominator = tf + self.k1 * (1 - self.b + self.b * (doc_length / self.avg_doc_length))
                    
                    if denominator > 0:
                        score += idf * (numerator / denominator)
            
            scores.append((i, score))
        
        # Sort by score (descending) and return top_k results
        scores.sort(key=lambda x: x[1], reverse=True)
        
        results = []
        for doc_idx, score in scores[:top_k]:
            results.append({
                'docid': self.documents[doc_idx]['docid'],
                'score': score
            })
        
        return results

def main():
    # Load filtered PRs
    with open('filtered_prs.json', 'r') as f:
        filtered_prs = json.load(f)
    
    # Process each PR
    results = []
    for pr in filtered_prs:
        pr_number = pr['number']
        
        # Load code corpus for this specific PR
        code_snapshot_file = f'code_snapshots/pr_{pr_number}_code.json'
        
        # Skip if code snapshot doesn't exist
        if not os.path.exists(code_snapshot_file):
            print(f"Warning: Code snapshot not found for PR {pr_number}, skipping...")
            continue
            
        with open(code_snapshot_file, 'r') as f:
            code_corpus = json.load(f)
        
        # Convert code_corpus to list format for BM25
        documents = []
        for file_path, content in code_corpus.items():
            documents.append({
                'docid': file_path,
                'content': content
            })
        
        # Skip if no documents
        if not documents:
            print(f"Warning: No documents found for PR {pr_number}, skipping...")
            continue
        
        # Initialize and fit BM25 for this PR
        retriever = BM25Retriever(k1=1.5, b=0.75)
        retriever.fit(documents)
        
        # Create query from PR title and body
        title = pr.get('title', '')
        body = pr.get('body', '')
        query = f"{title} {body}".strip()
        
        # Skip if no query content
        if not query:
            print(f"Warning: No query content for PR {pr_number}, skipping...")
            continue
        
        # Tokenize query for file path matching
        query_terms = re.findall(r'\b\w+\b', query.lower())
        
        # Search for relevant files
        hits = retriever.search(query, top_k=20)  # 3에서 10으로 증가 - 더 많은 후보
        
        # 파일 경로에 가중치 부여 (더 관련성 높은 파일 우선)
        for hit in hits:
            file_path = hit['docid']
            # 패치가 수정하는 파일이면 우선순위 높임
            if any(term.lower() in file_path.lower() for term in query_terms):
                hit['score'] *= 2.0  # 가중치 증가
            # 파일 경로에 키워드가 포함되어 있으면 추가 가중치
            if any(keyword in file_path.lower() for keyword in ['test', 'example', 'demo']):
                hit['score'] *= 0.5  # 테스트 파일은 낮은 우선순위
        
        # 상위 5개만 선택
        hits = sorted(hits, key=lambda x: x['score'], reverse=True)[:5]
        
        # Create result entry
        result = {
            'instance_id': f"MONAI_{pr_number}",
            'hits': hits
        }
        results.append(result)
    
    # Save results
    with open('bm25_text_results.jsonl', 'w') as f:
        for result in results:
            f.write(json.dumps(result) + '\n')

if __name__ == "__main__":
    main()
