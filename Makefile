.PHONY: run
run: main
	./apicker

main: *.go go.mod
	go build -o obsidian .

.PHONY: all
all: main
