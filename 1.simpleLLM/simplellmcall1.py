# Install dependencies: pip install openai
from openai import AzureOpenAI

# Azure AI Foundryでモデルをデプロイし、詳細から情報をコピペする
targetURI = "<ターゲットURIをコピペする>"
subscription_key = "<キーをコピペする>"
model_name = "<モデル名をコピペする>"

# ターゲットURIから、エンドポイント、APIバージョン、配置名を抜き出す
endpoint = targetURI.split("/", 3)[0] + "//" + targetURI.split("/", 3)[2] + "/"
api_version = targetURI.split("api-version=")[-1].split("&")[0]
deployment = targetURI.split("/deployments/")[1].split("/")[0]


# Azure OpenAI SDKを使う
client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)

# プロンプトを設定し、Streamで回答の受け取りを始める
response = client.chat.completions.create(
    stream=True,
    messages=[
        {
            "role": "system",
            "content": "あなたは親切なアシスタントです。",
        },
        {
            "role": "user",
            "content": "パリに行く予定です。何を見ればいいですか？",
        }
    ],
    max_tokens=4096,
    temperature=1.0,
    top_p=1.0,
    model=deployment,
)

# 受け取った回答を順次表示していく
for update in response:
    if update.choices:
        print(update.choices[0].delta.content or "", end="")

client.close()