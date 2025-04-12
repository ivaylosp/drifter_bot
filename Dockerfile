FROM python:3.12.6-slim-bookworm

ARG YOUR_ENV

ENV YOUR_ENV=${YOUR_ENV}

WORKDIR /app

RUN apt-get update

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#CMD [ "python", "bot.py" ]
ENTRYPOINT ["tail", "-f", "/dev/null"]