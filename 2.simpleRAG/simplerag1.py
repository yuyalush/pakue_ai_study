# 必要なパッケージ: pip install openai
# ※このサンプルは「APIキー認証」でAzure OpenAIを利用します

import os
from openai import AzureOpenAI

# --- 事前準備 ---
# 1. Azure OpenAIでモデルをデプロイし、APIキー・エンドポイント・デプロイ名を取得
# 2. 簡易RAGのため、検索対象ドキュメントをPythonリストで用意（本格運用は検索サービスやベクタDB推奨）

# --- 設定 ---
api_key = "<YOUR_API_KEY>"
endpoint = "<YOUR_ENDPOINT>"  # 例: https://xxxx.openai.azure.com/
deployment = "<YOUR_DEPLOYMENT_NAME>"  # 例: gpt-35-turbo

api_key = "DRusskedxOeUV3ehyNdYIF1iCk0pi1ZibuybKIHCWlSekWlX2zkJJQQJ99ALACYeBjFXJ3w3AAAAACOGO8lU"
endpoint = "https://pakue-m5503fdl-eastus.cognitiveservices.azure.com/"
deployment = "gpt-4o"

# --- 簡易ドキュメントコーパス ---
documents = [
    "パスワードを忘れた場合は、パスワードリセットページから再設定できます。",
    "システムメンテナンスは毎週土曜日の午前2時から行われます。",
    "サポートへのお問い合わせはメールまたはチャットで可能です。"
]

# --- ユーザーからの質問 ---
query = "パスワードを忘れたときはどうすればいいですか？"

# --- シンプルな検索（キーワード一致） ---
relevant_docs = [doc for doc in documents if "パスワード" in doc]

# --- RAGプロンプト作成 ---
context = "\n".join(relevant_docs)
prompt = f"""以下は参考情報です:
{context}

ユーザーの質問: {query}
この情報を参考に、できるだけ正確に日本語で答えてください。
"""

print("\nRAGプロンプト:\n", prompt)

# --- Azure OpenAI呼び出し（RAG回答） ---
client = AzureOpenAI(
    api_key=api_key,
    azure_endpoint=endpoint,
    api_version="2024-02-15-preview"
)

response = client.chat.completions.create(
    messages=[
        {"role": "system", "content": "あなたは親切なアシスタントです。"},
        {"role": "user", "content": prompt}
    ],
    model=deployment,
    max_tokens=512,
    temperature=0.2,
)

print("\n回答:\n", response.choices[0].message.content)

# --- 補足 ---
# 本格的なRAGを行う場合は、Azure Cognitive Searchやベクターデータベース（例: Azure AI Search, Pinecone, Qdrant等）を使い、
# ドキュメントの検索部分を強化してください。