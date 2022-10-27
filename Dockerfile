FROM golang:latest

RUN groupadd --gid 1000 runner \
    && useradd --uid 1000 --gid 1000 -m runner

WORKDIR "/home/runner/obsidian"

COPY . .

RUN chown -R runner:runner ../obsidian 

RUN ls -al ..

RUN go build -o obsidian .

CMD [ "./obsidian" ]
