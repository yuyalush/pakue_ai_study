# pakue_ai_study
AI関連の勉強ソース集

1. シンプルLLM呼び出し：simpleLLM

    - simplellmcall1.py : Azure OpenAI SDK + API Key認証を使ったパターン
    - simplellmcall2.py : Azure AI Inference SDK + API Key認証を使ったパターン
    - simplellmcall3.py : Azure AI Inference SDK + Microsoft ID プラットフォーム(サービスプリンシパル)による認証と承認を使ったパターン
    - [READMEはこちら](./simpleLLM/README.md)

2. シンプルRAGサンプル：2.simpleRAG

    - simplerag1.py : Pythonリスト＋キーワード一致によるRAGサンプル
    - simplerag2.py : JSONデータ＋LLMキーワード抽出＋あいまい検索によるRAGサンプル
    - simplerag2.json : 架空の本のタイトルと紹介文データ（検索対象）
    - fuzzy_search_sample.py : あいまい検索部分のサンプル
    - [READMEはこちら](./2.simpleRAG/README.md)

---

整理前のメモなど

- [VS CodeのAI Tool KitでAgent Builderを試したメモ](ai-tool-kit_Agent-builder.md)