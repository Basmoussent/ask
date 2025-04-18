FROM python:3.10-slim

# Installer les dépendances système nécessaires à Qt
RUN apt-get update && apt-get install -y \
    libegl1 \
    libglib2.0-0 \
    libx11-6 \
    libxext6 \
    libxrender1 \
    libxcb1 \
    libxkbcommon-x11-0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxi6 \
    libxtst6 \
    libnss3 \
    libdbus-1-3 \
    libfontconfig1 \
    libfreetype6 \
    libxrandr2 \
    libxcursor1 \
    libxinerama1 \
    libsm6 \
    x11-apps \
	libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . /app
WORKDIR /app

# Démarrer l'application
CMD ["python", "main.py"]
