from groq import Groq

client = Groq(api_key="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")

models = client.models.list()
for m in models.data:
    print(m.id)
