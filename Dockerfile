# syntax=docker/dockerfile:1

# Utiliser une image Python minimale
FROM python:3.11.5-slim

# Désactiver les fichiers pyc et activer l'affichage immédiat des logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Définir le répertoire de travail
WORKDIR /app

# Installer wget et autres dépendances système si nécessaire
RUN apt-get update && apt-get install -y wget ca-certificates && rm -rf /var/lib/apt/lists/*

# Copier les dépendances et les installer
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copier le script et le code
COPY . .

# Rendre le script Bash exécutable
RUN chmod +x download_and_extract_and_run.sh

# Commande par défaut pour exécuter le script
CMD ["./download_and_extract_and_run.sh"]
