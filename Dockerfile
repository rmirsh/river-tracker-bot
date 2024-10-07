FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

CMD ["sh", "-c", "sleep 5 && python bot/run.py"]
