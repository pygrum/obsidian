.PHONY: build run clean start

build:
	sudo docker build -t obsidian .

run:
	sudo docker run -it --rm --name obsidian-runtime obsidian

clean:
	sudo docker image rm obsidian
start:
	make clean 2>/dev/null; make build && make run
