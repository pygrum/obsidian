# To run the container in this directory, do:
# sudo docker build -t obsidian-be .
# sudo docker run -it --rm --name obsidian-be-runtime obsidian-be

FROM python:3

WORKDIR /app

COPY requirements.txt requirements.txt

RUN groupadd --gid 1000 runner \
    && useradd --uid 1000 --gid 1000 -m runner

USER runner

ENV PATH="${PATH}:/home/runner/.local/bin"

RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python","./main.py" ]
