FROM python:3.11-slim

RUN apt-get update && apt-get install -y wget gnupg libglib2.0-0 libnss3 libgconf-2-4 \
  libfontconfig1 libxss1 libasound2 libx11-xcb1 libxcomposite1 libxdamage1 \
  libxrandr2 libgtk-3-0 libgbm1

RUN pip install flask playwright && playwright install --with-deps

WORKDIR /app
COPY . .

CMD ["python", "server.py"]
