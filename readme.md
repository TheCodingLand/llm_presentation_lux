# Zero shot classification from scratch with llama3


## Démarrage des llm avec docker:

```bash
docker-compose up -d
docker exec -it ollama_presentation ollama run llama3:instruct
```

## Installer l'environnement python:

Installer conda ou Mambaforge et faire

mamba env create -f conda_env.yml

conda activate presentation

et enfin python live_demo.py

