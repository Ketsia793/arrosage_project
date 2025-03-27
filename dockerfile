FROM python:3.9

# Installer les dépendances nécessaires pour psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential \
    wget

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de requirements
COPY requirements.txt /app/

# Mettre à jour pip et installer les dépendances
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install python-dotenv

# Copier le script wait-for-it.sh
COPY scripts/wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# Copier le reste du code
COPY . /app/

# Exposer le port sur lequel l'application Django va écouter
EXPOSE 8000

# Utiliser wait-for-it pour attendre que PostgreSQL soit prêt
CMD ./wait-for-it.sh db:5432 -- python manage.py runserver 0.0.0.0:8000
