FROM python:3-alpine

WORKDIR /urs/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./cli_wordle.py" ]
