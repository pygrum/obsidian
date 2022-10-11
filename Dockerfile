# To run the container in this directory, do:
# sudo docker build -t obsidian-be .
# sudo docker run --it --rm --name obsidian-be-runtime obsidian-be

FROM python:3

WORKDIR /app

COPY . .

CMD [ "python", "./main.py" ]