# Entra ID Authenticationを利用するため、
# Azureポータルでアプリケーションを登録する:
# Azureポータルにサインインし、「Microsoft Entra ID」>「アプリの登録」に移動します。
#「新規登録」をクリックし、アプリケーションの名前を入力して登録します。
# AZURE_CLIENT_IDを取得する:
# 登録したアプリケーションの「概要」ページで、「アプリケーション (クライアント) ID」を確認し、これがAZURE_CLIENT_IDになります。
# AZURE_TENANT_IDを取得する:
#「Azure Active Directory」の「概要」ページで、「ディレクトリ (テナント) ID」を確認し、これがAZURE_TENANT_IDになります。
# AZURE_CLIENT_SECRETを生成する:
# アプリケーションの「証明書とシークレット」セクションに移動し、「新しいクライアント シークレット」を作成します。
# シークレットの値をコピーし、これがAZURE_CLIENT_SECRETになります。シークレットの値は一度しか表示されないので、必ず記録しておいてください。

# そのまま実行するとエラーになる
# azure.core.exceptions.ClientAuthenticationError: (PermissionDenied) The principal `9c5b2c13-c3d4-43aa-982b-b4ce6c556fac` lacks the required data action `Microsoft.CognitiveServices/accounts/OpenAI/deployments/chat/completions/action` to perform `POST /openai/deployments/{deployment-id}/chat/completions` operation.
# Code: PermissionDenied
# Message: The principal `9c5b2c13-c3d4-43aa-982b-b4ce6c556fac` lacks the required data action `Microsoft.CognitiveServices/accounts/OpenAI/deployments/chat/completions/action` to perform `POST /openai/deployments/{deployment-id}/chat/completions` operation.

# API のアクセス許可を設定する
# Entra IDのアプリケーション登録後にAPIのアクセス許可を設定するには、以下の手順を実行してください：
# Azureポータルにアクセス:
# Azureポータルにサインインし、「Azure Active Directory」>「アプリの登録」に移動します。
# アプリケーションを選択:
# 設定したいアプリケーションを選択します。
# APIアクセス許可の設定:
# 左側のメニューから「APIアクセス許可」を選択します。
# 「アクセス許可の追加」をクリックします。
# 「マイ組織が使用するAPI」から「Microsoft Cognitive Services」を検索し、選択します。
# 「委任されたアクセス許可」を選択し、「Cognitive Services APIへのアクセスを組織のユーザーとして行う」チェックボックスをオンにします。
# 「アクセス許可の追加」をクリックします。
# 管理者の同意を付与:
# 「APIアクセス許可」ページで「管理者の同意を付与」を選択し、確認します。

# リソース側の許可を設定する
# 1. リソース（Azure OpenAIリソース）へ「ロール割り当て」を追加
# Azure Portalにサインインします。
# サービス（Cognitive Services/OpenAI）リソースのページに移動します。(Azure OpenAI > AI Foundry > モデルがデプロイされている作業場所[AI Fdoundryポータルの左上の名称])
# 左側のメニューから「アクセス制御 (IAM)」を選びます。
# 「ロールの割り当て」 > 「追加」 > 「ロールの割り当ての追加」をクリックします。
# ロールを選択します:
# 必要なアクション（chat/completions/action）には、以下のいずれかのロールが必要です。
# Cognitive Services OpenAI User
# Cognitive Services Contributor（より広い権限ですが、Userで十分な場合はUser推奨）
# 「メンバーの選択」で、問題のprincipal（サービスプリンシパル・アプリ）を検索し、追加します。
# 保存して反映されるのを待ちます。

# DefultAzureCredential
# ローカル開発シナリオでは、 DefaultAzureCredential は使用可能な認証ソースを順番にチェックすることによって機能します。 具体的には、次のツールでアクティブなセッションを検索します。
# Azure CLI (az login)
# Azure PowerShell (Connect-AzAccount)
# Azure Developer CLI (azd auth login)
# 開発者がこれらのツールのいずれかを使用して Azure にサインインしている場合、 DefaultAzureCredential はセッションを自動的に検出し、
# それらの資格情報を使用して Azure サービスでアプリケーションを認証します。 
# これにより、開発者は、シークレットを格納したり、さまざまな環境のコードを変更したりすることなく、安全に認証できます。
# https://learn.microsoft.com/ja-jp/azure/developer/python/sdk/authentication/local-development-dev-accounts?tabs=azure-cli%2Csign-in-azure-cli#4---implement-defaultazurecredential-in-your-application


# 実際に使用するときはAzure Portalから環境変数として設定する
# このソースを実行するときは、ターミナルで以下を打ち込み環境変数をセットする
# export AZURE_CLIENT_ID="<AZURE_CLIENT_ID>"
# export AZURE_TENANT_ID="<AZURE_TENANT_ID>"
# export AZURE_CLIENT_SECRET="<AZURE_CLIENT_SECRET>"



# pip install azure.identity
# pip install azure-ai-inference
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.identity import DefaultAzureCredential

# Azure AI Foundryから設定する
endpoint = "https://pakue-m5503fdl-eastus.cognitiveservices.azure.com/openai/deployments/gpt-4o"
model_name = "gpt-4o"

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential(), # Acquire a credential object
    credential_scopes=["https://cognitiveservices.azure.com/.default"]
)

response = client.complete(
    messages=[
        SystemMessage(content="あなたは親切なアシスタントです。"),
        UserMessage(content="パリに行く予定です。何を見ればいいですか？")
    ],
    max_tokens=4096,
    temperature=1.0,
    top_p=1.0,
    model=model_name
)

print(response.choices[0].message.content)