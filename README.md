# Obsidian

## Testing the tool

You may wish to run a simple test for the tool. This can be run using the image provided by @christophetd and test for log4shell using https://log4shell.huntress.com.

1. Pull the vulnerable docker image and tag it with `docker build -t vuln-app -f VulnImage .`

2. Run the image (as a background process) with `docker run -it --rm --name vuln-app vuln-app &`

3. Run `docker inspect vuln-app | grep IPAddress` to find the IP address of the running image.

4. In the `targets.json` file, there is already a target there with the endpoint to test on configured (X-Api-Version). Replace the IP in the URI with the IP of the vulnerable container.

5. Visit https://log4shell.huntress.com and retrieve your unique ID to test for log4shell (a string of letters and numbers, separated by '-'. Then in the `payloads.json` file, replace the unique ID that's already there with your own. Save your changes.

6. In the repo base directory, run `make start`. You should see a log of the request made and it's response. check 'view connections' in https://log4shell.huntress.com. An entry should appear.


