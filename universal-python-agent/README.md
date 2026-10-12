# 🛡️ Humanpowers for Python (LangChain, AutoGen, CrewAI)

Python asosidagi agentlar uchun Humanpowers kutubxonasi.

## Ishga tushirish:
```bash
python example.py
```

## Foydalanish:
```python
from craftsman import CraftsmanAgent

agent = CraftsmanAgent(persona="software_architect", min_passing_score=95)
result = agent.execute("Vazifa matni...")
print(result["final_output"])
```
