FROM python:3.13-slim

WORKDIR /nerd-nest-api

COPY app/ /nerd-nest-api/app/
COPY requirements.txt run.py /nerd-nest-api/

RUN pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["run:app", "-b", "0.0.0.0:5000"]

ENTRYPOINT ["gunicorn"]
