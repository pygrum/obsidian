.PHONY: run
run: main
	./obsidian

main: 
	go build -o obsidian .

.PHONY: all
all: main
