# Azure OpenAI サンプルコード集

このディレクトリには、Azure OpenAI サービスを利用するための複数のサンプルコードが含まれています。  
それぞれ異なるSDKや認証方式を利用しているため、用途や環境に応じて使い分けてください。

---

## 1. simplellmcall1.py

**使用SDK:**  
- [`openai`](https://pypi.org/project/openai/)（Azure OpenAI対応）

**特徴:**  
- Azure OpenAIのREST APIを`openai`パッケージ経由で利用します。
- APIキー認証を使用します。
- エンドポイントやAPIバージョン、デプロイ名などを手動で設定します。

**主な用途:**  
- シンプルなAPIキー認証での利用
- Azure OpenAIの基本的な呼び出し

**注意点**
- このソースコードでは、環境設定について直接ソースコードに埋め込む方法を使っています。APIキーの漏洩に気を付けてください。

---

## 2. simplellmcall2.py

**使用SDK:**  
- [`azure-ai-inference`](https://pypi.org/project/azure-ai-inference/)

**特徴:**  
- Azureが公式に提供する新しいAI推論SDKです。
- `AzureKeyCredential`を使ったAPIキー認証方式です。
- ストリーミング応答に対応しています。

**主な用途:**  
- Azure OpenAIのAPIキー認証での利用
- ストリーミング応答の取得

**注意点**
- このソースコードでは、環境設定について直接ソースコードに埋め込む方法を使っています。APIキーの漏洩に気を付けてください。

---

## 3. simplellmcall3.py

**使用SDK:**  
- [`azure-ai-inference`](https://pypi.org/project/azure-ai-inference/)
- [`azure-identity`](https://pypi.org/project/azure-identity/)

**特徴:**  
- Azure Entra ID（旧Azure AD）による認証（サービスプリンシパルやマネージドID）を利用します。
- `DefaultAzureCredential`を使うことで、ローカル開発やAzure上の各種認証方式に自動対応します。
- よりセキュアな認証方式が必要な場合や、APIキーを使いたくない場合に推奨されます。

**主な用途:**  
- Entra ID認証によるセキュアなAPI利用
- 開発・運用環境での統一的な認証管理

---

## 参考

- [Azure OpenAI Service ドキュメント](https://learn.microsoft.com/ja-jp/azure/ai-services/openai/)
- [azure-ai-inference SDK ドキュメント](https://learn.microsoft.com/ja-jp/python/api/overview/azure/ai-inference-readme)
- [azure-identity SDK ドキュメント](https://learn.microsoft.com/ja-jp/python/api/overview/azure/identity-readme)

---

## 注意

- Entra ID認証（simplellmcall3.py）を利用する場合は、Azure Portalでアプリ登録・APIアクセス許可・リソースへのロール割り当てが必要です。
- APIキー認証（simplellmcall1.py, simplellmcall2.py）は、キーの漏洩に注意してください。
