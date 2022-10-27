# To run the container in this directory, do:
# sudo docker build -t obsidian-be .
# sudo docker run -it --rm --name obsidian-be-runtime obsidian-be

FROM python:3

WORKDIR /app

RUN groupadd --gid 1000 runner \
    && useradd --uid 1000 --gid 1000 -m runner

USER runner

ENV PATH="${PATH}:/home/runner/.local/bin"

COPY . .

RUN make main

CMD [ "./obsidian" ]
