.PHONY: build run clean

build:
	sudo docker build -t obsidian-be .

run:
	sudo docker run -it --rm --name obsidian-be-runtime obsidian-be

clean:
	sudo docker image rm obsidian-be
