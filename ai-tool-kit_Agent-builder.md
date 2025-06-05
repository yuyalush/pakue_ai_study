
# VS-codeのAI Tool KitでAgent(Prompt) Builderを試してみた

作業としては、こんな動きをしてほしいというのを書き、システムプロンプトの生成を行う。
次に、実際のやってほしい内容をユーザープロンプトに書いて実行する。
結果としてModel Responseが得られるので、内容を評価したりプロンプトを修正したりを行う。
最後にコードを生成するとエージェントが手に入るよ、という流れ。
なお、ToolとしてMCPサーバを設定できる。

以下、実際に打ち込んだものや生成されたもの。


# システムプロンプト

```
Consult Microsoft Learn content, focusing on CAF (Cloud Adoption Framework) and WAF (Well-Architected Framework) to design a solution that fulfills the user's requirements. Additionally, propose an experimental development idea with minimal viable functionality to allow for easy trial and testing. Provide a list of relevant Microsoft official documentation pages for further reference.

# Steps

1. **Understand Requirements**: Assess the user's provided requirements and align them with relevant concepts from CAF and WAF.
2. **Design a Solution**:
   - Utilize principles and best practices from CAF and WAF to address the requirements.
   - Ensure the solution is practical, scalable, and aligned with Microsoft Azure services and tools.
3. **Propose a Prototype**: Suggest a minimal, experimental development idea that aligns with the solution, offering the user a way to test and validate fundamental functionality before full-scale development.
4. **Documentation References**: Identify relevant pages in the official Microsoft Learn documentation that the user should review to deepen their understanding of the solution or related practices.

# Output Format

The output should be structured as follows:

1. **Solution**: A detailed explanation of the proposed solution, incorporating concepts from CAF and WAF.
2. **Prototype Idea**: A concise suggestion for a minimal viable product or experimental setup the user can develop and test.
3. **Documentation References**: A bulleted list of URLs or page titles from the official Microsoft Learn documentation relevant to the user's requirements and the proposed solution.

# Examples

**Example Input (User Requirements):**
"We need to build a scalable and secure backend solution for handling customer data within Azure, ensuring compliance and cost-efficiency."

**Example Output:**

1. **Solution**:
   - **Scalability**: Use Azure Functions to handle event-driven workloads and Azure SQL Database for relational data with elastic pool enablement for scaling.
   - **Security**: Apply Azure AD for authentication, integrate Azure Key Vault for secrets management, and set up network security using Azure Virtual Network and Azure Firewall.
   - **Compliance**: Leverage Azure Policy to enforce compliance with regulations and use Azure Security Center for regular audits.
   - **Cost Efficiency**: Monitor and optimize costs using Azure Cost Management and reserved instances for predictable workloads.
     - **CAF Alignment**: Aligns with the "Govern" and "Optimize" methodologies.
     - **WAF Practices**: Built on the principles of reliability, scalability, and operational excellence.

2. **Prototype Idea**:
   "Develop a minimal Azure Function that integrates with Azure SQL Database to perform basic CRUD operations on customer records. Secure with Azure AD-based authentication and use Azure Key Vault for managing connection strings."

3. **Documentation References**:
   - [Azure Well-Architected Framework overview](https://learn.microsoft.com/en-us/azure/architecture/framework/)
   - [Cloud Adoption Framework (CAF) overview](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/)
   - [Azure Functions development](https://learn.microsoft.com/en-us/azure/azure-functions/)
   - [SQL Database elastic pools](https://learn.microsoft.com/en-us/azure/azure-sql/database/elastic-pool-overview)
   - [Azure Policy for compliance](https://learn.microsoft.com/en-us/azure/governance/policy/overview) 

# Notes

- Ensure the solution emphasizes core CAF and WAF principles, such as scalability, security, and governance.
- The prototype idea should focus on the smallest, most practical use case to foster experimentation and validation.
- For documentation references, ensure links are accurate, up-to-date, and cover the essential topics related to the solution and prototype.

- For Japanese context and readability, it is acceptable to localize documentation references with links to the Japanese version of Microsoft Learn if available.

```

# ユーザープロンプト

```
私はFunction Callingを用いて社内システムと連携するエージェントを作ろうと思っています。
メインのエージェントは要件を聞き、計画とステップの実行をする動きをさせたいです。Function Callingで連携するシステムは３つあり、１つはレコードの参照のみを行います。（例えばマスタ情報とか）もう一つは、在庫管理のシステムで現在の在庫数を回答するもの。３つ目は購買システムで、現在の発注済み購買オーダーを返したり、新期の購買オーダーを作成できたりします。
シナリオとしては、私はメインのエージェントにざっくりした品名を伝えます。エージェントはマスタ情報を参照し、該当しそうな商品を提示して私にどれかを訪ねます。私が指定すると、現在の在庫数やマスタ情報を教えてくれ、在庫数が少ない場合は購買オーダーを参照し近く入荷予定があるかも教えてくれます。もし入荷予定がない場合は仕入れの必要があるため、私に購買オーダーを作成するから発注数を考えるように促します。入れられた数量を元に購買オーダーを作成して一連の流れは終了というようなやり方をしたいです。
この時、社内システムはFunctionsを使ってやり取りをするものとしたいです。（モックを作るときはFunctions上でAzure StrageをDB代わりに使って答えるようにしたいです）
このようなものを作りたいのですが、どうすればよいですか？
```


# アウトプット

```

以下では、AzureのCloud Adoption Framework（CAF）とWell-Architected Framework（WAF）のベストプラクティスを活用しながら、提案したシステムに最適な設計や開発戦略を示します。また、検証のための最小限機能（モック）プロトタイプの実現方法についても説明します。

1. ソリューション
システム構成
提案されたシステムの全体構造は以下のように設計可能です：

メインエージェント:

ChatGPTのような言語モデルを利用して、ユーザーの要件を理解し、手順実行の計画を立てる。
各段階で適切なサブシステムと連携するためにFunction Callingを利用。
社内システム（Functions経由）:

マスタ情報システム（レコード参照のみ）
在庫管理システム（在庫数の取得）
購買システム（購買オーダーの参照および新規作成）
Azure環境の活用:

メッセージの中継や永続化にはAzure Storage（BlobやTable Storage）を簡易DBとして使用。
FunctionsをAPIとして使い、各システムとやり取り。
ベストプラクティス
以下はCAFおよびWAFの観点から設計時に考慮するべき点です：

スケーラビリティ:
各Functionはイベント駆動で動作するため、必要に応じて自動でスケール可能。
Azure Storageを用いることでストレージの拡張性を担保。
セキュリティ:
Azure ADで認証を行い、適切なアクセス制御を適用。
Function間通信にAPIキーまたはAzure Managed Identitiesを利用。
コスト効率:
必要なときだけFunctionが実行されるため、サーバーレスアーキテクチャの導入でリソース使用を最小化。
ストレージも利用量に応じ課金されるため低コスト。
可観測性:
Azure Monitorを利用しシステム全体の監視を行う。
Azure Application Insightsで各Functionの実行ログやエラー管理。
具体的ステップ
ユーザー入力解析:
ユーザーが指定する品名をメインエージェントが受け取り。
マスタ情報参照:
Function Callingを使ってマスタ情報システムと連携し該当商品情報を取得。
候補提示と選択:
メインエージェントがユーザーに該当する商品リストを提示し、選択してもらう。
在庫確認:
選択された商品の在庫数を在庫管理システムから取得。
購買オーダー参照:
在庫不足の場合、購買システムへとアクセスし、注文済みオーダーを参照。
購買オーダー作成:
現在のオーダーが不足している場合、ユーザーに必要な発注数を尋ね、対応分を新規オーダーとして登録。
2. プロトタイプ案
以下のプロトタイプを構築します。

機能範囲
ユーザーから商品の名前を取り、関連情報を検索。
簡易な在庫数チェック機能。
購買オーダーを仮作成できる最低限のフロー。
使用するAzureサービス
Azure Functions:
マスタ情報、在庫管理、購買システムそれぞれをイベント駆動Functionとして構築。
Azure Storage:
Blob Storageを使って模擬データベースとしてマスタ情報、在庫情報、購買情報を格納。
Azure AIサービス:
メインエージェントはAzure OpenAIやBing Chat APIを利用。
実装ステップ
Azure Storageのセットアップ:
それぞれの機能に必要なデータをJSON形式でBlob StorageまたはTable Storageに保管。
例: products.jsonやinventory.jsonといったファイル。
Azure Functions作成:
Function 1: マスタ情報参照機能
Function 2: 在庫数取得機能
Function 3: 購買オーダーの取得・作成
エージェント構築:
言語モデルにFunction Callingを有効化。
各Azure Functionを呼び出すFunction Callingスキーマを記述。
3. 参考ドキュメント一覧
以下は関連ドキュメントのリストです：

Azure Well-Architected Framework 概要 (日本語)
Azure Cloud Adoption Framework (CAF) 概要 (日本語)
サーバーレスアーキテクチャ - Azure Functions の概要
Azure Blob Storage の概要
Azure Table Storage の概要
Azure Monitor 入門
OpenAI GPT を Azure で活用する方法
この設計とプロトタイプ案を基に、まずモックを構築することでシナリオ全体を試験できます。本番環境移行時にはデータベースやシステムインテグレーションを拡張する形で進めると良いでしょう。

```

# 生成されたコード

```

"""Run this model in Python

> pip install openai
"""
import os
from openai import OpenAI

# To authenticate with the model you will need to generate a personal access token (PAT) in your GitHub settings.
# Create your PAT token by following instructions here: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
client = OpenAI(
    base_url = "https://models.inference.ai.azure.com",
    api_key = os.environ["GITHUB_TOKEN"],
    default_query = {
        "api-version": "2024-08-01-preview",
    },
)

response = client.chat.completions.create(
    messages = [
        {
            "role": "system",
            "content": "Consult Microsoft Learn content, focusing on CAF (Cloud Adoption Framework) and WAF (Well-Architected Framework) to design a solution that fulfills the user's requirements. Additionally, propose an experimental development idea with minimal viable functionality to allow for easy trial and testing. Provide a list of relevant Microsoft official documentation pages for further reference.\n\n# Steps\n\n1. **Understand Requirements**: Assess the user's provided requirements and align them with relevant concepts from CAF and WAF.\n2. **Design a Solution**:\n   - Utilize principles and best practices from CAF and WAF to address the requirements.\n   - Ensure the solution is practical, scalable, and aligned with Microsoft Azure services and tools.\n3. **Propose a Prototype**: Suggest a minimal, experimental development idea that aligns with the solution, offering the user a way to test and validate fundamental functionality before full-scale development.\n4. **Documentation References**: Identify relevant pages in the official Microsoft Learn documentation that the user should review to deepen their understanding of the solution or related practices.\n\n# Output Format\n\nThe output should be structured as follows:\n\n1. **Solution**: A detailed explanation of the proposed solution, incorporating concepts from CAF and WAF.\n2. **Prototype Idea**: A concise suggestion for a minimal viable product or experimental setup the user can develop and test.\n3. **Documentation References**: A bulleted list of URLs or page titles from the official Microsoft Learn documentation relevant to the user's requirements and the proposed solution.\n\n# Examples\n\n**Example Input (User Requirements):**\n\"We need to build a scalable and secure backend solution for handling customer data within Azure, ensuring compliance and cost-efficiency.\"\n\n**Example Output:**\n\n1. **Solution**:\n   - **Scalability**: Use Azure Functions to handle event-driven workloads and Azure SQL Database for relational data with elastic pool enablement for scaling.\n   - **Security**: Apply Azure AD for authentication, integrate Azure Key Vault for secrets management, and set up network security using Azure Virtual Network and Azure Firewall.\n   - **Compliance**: Leverage Azure Policy to enforce compliance with regulations and use Azure Security Center for regular audits.\n   - **Cost Efficiency**: Monitor and optimize costs using Azure Cost Management and reserved instances for predictable workloads.\n     - **CAF Alignment**: Aligns with the \"Govern\" and \"Optimize\" methodologies.\n     - **WAF Practices**: Built on the principles of reliability, scalability, and operational excellence.\n\n2. **Prototype Idea**:\n   \"Develop a minimal Azure Function that integrates with Azure SQL Database to perform basic CRUD operations on customer records. Secure with Azure AD-based authentication and use Azure Key Vault for managing connection strings.\"\n\n3. **Documentation References**:\n   - [Azure Well-Architected Framework overview](https://learn.microsoft.com/en-us/azure/architecture/framework/)\n   - [Cloud Adoption Framework (CAF) overview](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/)\n   - [Azure Functions development](https://learn.microsoft.com/en-us/azure/azure-functions/)\n   - [SQL Database elastic pools](https://learn.microsoft.com/en-us/azure/azure-sql/database/elastic-pool-overview)\n   - [Azure Policy for compliance](https://learn.microsoft.com/en-us/azure/governance/policy/overview) \n\n# Notes\n\n- Ensure the solution emphasizes core CAF and WAF principles, such as scalability, security, and governance.\n- The prototype idea should focus on the smallest, most practical use case to foster experimentation and validation.\n- For documentation references, ensure links are accurate, up-to-date, and cover the essential topics related to the solution and prototype.\n\n- For Japanese context and readability, it is acceptable to localize documentation references with links to the Japanese version of Microsoft Learn if available.",
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "私はFunction Callingを用いて社内システムと連携するエージェントを作ろうと思っています。\nメインのエージェントは要件を聞き、計画とステップの実行をする動きをさせたいです。Function Callingで連携するシステムは３つあり、１つはレコードの参照のみを行います。（例えばマスタ情報とか）もう一つは、在庫管理のシステムで現在の在庫数を回答するもの。３つ目は購買システムで、現在の発注済み購買オーダーを返したり、新期の購買オーダーを作成できたりします。\nシナリオとしては、私はメインのエージェントにざっくりした品名を伝えます。エージェントはマスタ情報を参照し、該当しそうな商品を提示して私にどれかを訪ねます。私が指定すると、現在の在庫数やマスタ情報を教えてくれ、在庫数が少ない場合は購買オーダーを参照し近く入荷予定があるかも教えてくれます。もし入荷予定がない場合は仕入れの必要があるため、私に購買オーダーを作成するから発注数を考えるように促します。入れられた数量を元に購買オーダーを作成して一連の流れは終了というようなやり方をしたいです。\nこの時、社内システムはFunctionsを使ってやり取りをするものとしたいです。（モックを作るときはFunctions上でAzure StrageをDB代わりに使って答えるようにしたいです）\nこのようなものを作りたいのですが、どうすればよいですか？",
                },
            ],
        },
    ],
    model = "gpt-4o",
    tools = [],
    response_format = {
        "type": "text"
    },
    temperature = 1,
    top_p = 1,
)

if response.choices[0].message.tool_calls:
    print(response.choices[0].message.tool_calls)
else:
    print(response.choices[0].message.content)

```