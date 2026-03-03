import requests
import json

r = requests.get(
    'https://openrouter.ai/api/v1/models',
    headers={'Authorization': 'Bearer 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'}
)

models = r.json().get('data', [])
step_model = [m for m in models if 'step-3.5-flash' in m.get('id', '').lower()]

if step_model:
    print("Step-3.5-Flash 模型信息:")
    print(json.dumps(step_model[0], indent=2, ensure_ascii=False))
else:
    print("Model not found")
