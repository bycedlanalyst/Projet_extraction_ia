from groq import Groq

# Mets la clé ici
client = Groq(api_key="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")

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "user", "content": "Bonjour, peux-tu me résumer ce texte : Le chat mange une pomme."}
    ]
)

print(response.choices[0].message.content)
