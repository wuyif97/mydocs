import requests

r = requests.get(
    'https://openrouter.ai/api/v1/models',
    headers={'Authorization': 'Bearer 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'}
)

models = r.json().get('data', [])
free_models = [m for m in models if 'free' in m.get('id', '').lower()]

print('可用免费模型:')
for m in free_models[:10]:
    print(f"  - {m['id']}")
