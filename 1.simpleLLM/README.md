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
- [Microsoft ID プラットフォームのドキュメント](https://learn.microsoft.com/ja-jp/entra/identity-platform/)
- [Python 用 Azure ID クライアント ライブラリ](https://github.com/Azure/azure-sdk-for-python/tree/azure-ai-inference_1.0.0b5/sdk/identity/azure-identity)

---

## 注意

- Entra ID認証（simplellmcall3.py）を利用する場合は、Azure Portalでアプリ登録・APIアクセス許可・リソースへのロール割り当てが必要です。
- APIキー認証（simplellmcall1.py, simplellmcall2.py）は、キーの漏洩に注意してください。

---

## サービスプリンシパルとマネージドIDの違い

Azureでアプリケーションやサービスがリソースへアクセスする際の「ID」には主に以下の2種類があります。

### サービスプリンシパル（Service Principal）

- **概要**:  
  Azure AD（Entra ID）にアプリケーションを登録して作成するIDです。  
  アプリやスクリプトなど「人間以外」がAzureリソースにアクセスするために使います。

- **特徴**:  
  - クライアントID・テナントID・シークレット（または証明書）を自分で管理・設定する必要があります。
  - ローカルPCやオンプレミス、他クラウドなど、Azure外からも利用可能です。
  - シークレットの管理やローテーションが必要です。

- **例**:  
  - GitHub ActionsやJenkinsなど、Azure外部のCI/CDツールからAzureリソース（例：OpenAI、Storage、Key Vaultなど）にアクセスしたい場合
  - ローカルPCやオンプレミスサーバーからAzureのAPIを呼び出すバッチ処理


### マネージドID（Managed Identity）

- **概要**:  
  Azure上のリソース（VM、App Service、Functionsなど）に自動的に割り当てられるIDです。  
  AzureがIDの発行・管理を自動で行い、シークレット管理が不要です。

- **特徴**:  
  - Azureリソースに割り当てるだけで利用可能（手動でシークレットを管理しなくてよい）
  - システム割り当てIDとユーザー割り当てIDの2種類があります
  - Azure上のリソースからのみ利用可能（ローカルPCや他クラウドからは利用不可）

- **例**:  
  - Azure FunctionsやApp Service、VMなどからKey VaultやOpenAIなどのAzureリソースに安全にアクセスしたい場合
  - Azure Data Factoryのパイプラインからストレージやデータベースにアクセスする場合


### 比較表

| 項目                | サービスプリンシパル         | マネージドID                |
|---------------------|-----------------------------|-----------------------------|
| シークレット管理    | 必要（手動で管理）           | 不要（Azureが自動管理）     |
| 利用できる場所      | どこからでも利用可能         | Azureリソース上のみ         |
| 主な用途            | 汎用的な自動化・外部連携     | Azure内の安全な自動化       |

**どちらもAzureリソースへのアクセス権（RBACロール割り当て）が必要です。**  
セキュリティや運用の観点から、Azure上のリソースからアクセスする場合はマネージドIDの利用が推奨されます。
