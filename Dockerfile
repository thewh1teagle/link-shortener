FROM python:3.9-slim-bullseye
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
ENTRYPOINT [ "python", "main.py" ]