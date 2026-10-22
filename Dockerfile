FROM python:3.13
WORKDIR /app
COPY . /app
RUN apt-get update
RUN apt-get install -y libdbus-1-dev libdbus-glib-1-dev
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["sh", "-c", "python -m coverage run -m unittest discover && coverage report"]
