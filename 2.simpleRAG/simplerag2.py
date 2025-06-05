import json
from difflib import SequenceMatcher
from openai import AzureOpenAI

# 設定
api_key = "<YOUR_API_KEY>"
endpoint = "<YOUR_ENDPOINT>"
deployment = "<YOUR_DEPLOYMENT_NAME>"

# データファイル読み込み
with open("simplerag2.json", encoding="utf-8") as f:
    docs = json.load(f)

# ユーザーの質問
query = input("どんな本を探していますか？: ")

# LLMでキーワード抽出
keyword_prompt = f"""
次の質問から検索に使うべき日本語のキーワードを1つか2つ、カンマ区切りで抽出してください。キーワードのみを出力してください。

質問: {query}
"""

client = AzureOpenAI(
    api_key=api_key,
    azure_endpoint=endpoint,
    api_version="2024-02-15-preview"
)

keyword_response = client.chat.completions.create(
    messages=[
        {"role": "system", "content": "あなたは検索エンジンのキーワード抽出器です。"},
        {"role": "user", "content": keyword_prompt}
    ],
    model=deployment,
    max_tokens=20,
    temperature=0.0,
)

keywords_raw = keyword_response.choices[0].message.content.strip()
keywords = keywords_raw.replace("、", ",").split(",")
keywords = [k.strip() for k in keywords if k.strip()]

print("抽出されたキーワード:", keywords)

# あいまい検索（タイトル・紹介文の両方を対象、類似度しきい値0.5以上 or キーワード一致）
def fuzzy_search(docs, query, keywords, threshold=0.5):
    results = []
    for doc in docs:
        title_ratio = SequenceMatcher(None, query, doc["title"]).ratio()
        summary_ratio = SequenceMatcher(None, query, doc["summary"]).ratio()
        keyword_hit = any(k in doc["title"] or k in doc["summary"] for k in keywords)
        score = max(title_ratio, summary_ratio)
        if score >= threshold or keyword_hit:
            results.append({
                "title": doc["title"],
                "summary": doc["summary"],
                "score": score
            })
    return sorted(results, key=lambda x: x["score"], reverse=True)

hits = fuzzy_search(docs, query, keywords)

# RAGプロンプト作成
context = "\n".join([f"{doc['title']}: {doc['summary']}" for doc in hits[:5]])  # 上位5件
rag_prompt = f"""以下は蔵書データの一部です:
{context}

ユーザーの質問: {query}
この情報を参考に、あなたが図書館のレコメンドエージェントとして最適な本を日本語で案内してください。
"""

print("\nRAGプロンプト:\n", rag_prompt)

# 回答生成
response = client.chat.completions.create(
    messages=[
        {"role": "system", "content": "あなたは親切な図書館のレコメンドエージェントです。"},
        {"role": "user", "content": rag_prompt}
    ],
    model=deployment,
    max_tokens=512,
    temperature=0.2,
)

print("\nおすすめの本:\n", response.choices[0].message.content)