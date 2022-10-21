.PHONY: build run clean

build:
	sudo docker build -t obsidian-be .

run:
	sudo docker run -it --rm --name obsidian-be-runtime obsidian-be

clean:
	sudo docker image rm obsidian-be
start:
	make clean 2>/dev/null; make build && make run
