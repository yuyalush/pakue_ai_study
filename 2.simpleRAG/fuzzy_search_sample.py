import json
from difflib import SequenceMatcher

# データファイル読み込み
with open("simplerag2.json", encoding="utf-8") as f:
    docs = json.load(f)

# ユーザーの検索クエリ
query = "図書館の話"

# あいまい検索（タイトル・紹介文の両方を対象、類似度しきい値0.5以上）
def fuzzy_search(docs, query, threshold=0.5):
    results = []
    for doc in docs:
        title_ratio = SequenceMatcher(None, query, doc["title"]).ratio()
        summary_ratio = SequenceMatcher(None, query, doc["summary"]).ratio()
        if max(title_ratio, summary_ratio) >= threshold:
            results.append({
                "title": doc["title"],
                "summary": doc["summary"],
                "score": max(title_ratio, summary_ratio)
            })
    return sorted(results, key=lambda x: x["score"], reverse=True)

hits = fuzzy_search(docs, query)

print("検索クエリ:", query)
print("検索結果:")
for hit in hits:
    print(f"- {hit['title']} ({hit['score']:.2f}) : {hit['summary']}")