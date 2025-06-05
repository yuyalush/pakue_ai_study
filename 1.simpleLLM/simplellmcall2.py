
# pip install azure-ai-inference
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

model_name = "gpt-4o"

# Create a client to connect to the Azure OpenAI service
# Replace the endpoint and API key with your actual values
client = ChatCompletionsClient(
    endpoint="https://sample.openai.azure.com/openai/deployments/gpt-4o",
    credential=AzureKeyCredential("<API_KEY>")  
)

response = client.complete(
    stream=True,
    messages=[
        SystemMessage(content="あなたは親切なアシスタントです。"),
        UserMessage(content="パリに行く予定です。何を見ればいいですか？")
    ],
    max_tokens=4096,
    temperature=1.0,
    top_p=1.0,
    model=model_name
)

for update in response:
    if update.choices:
        print(update.choices[0].delta.content or "", end="")

client.close()