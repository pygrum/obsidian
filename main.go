package main

import (
	"encoding/json"
	"fmt"
	"os"
	"sync"
)


// An array of attack targets
type Targets struct {
	Targets []Target `json:"targets"`
	//soon to add proxy support
	Replace_str string `json:"replace-string"`
	LHOST string `json:"lhost"`
	LPORT string `json:"lport"`
}

type Target struct {
	ID string `json:"id"`
	URI string `json:"URI"`
	Endpoints []Endpoint `json:"endpoints"`
}

type Endpoint struct {
	Port string `json:"port"`
	Path string `json:"endpoint"`
	Http_verb string `json:"method"`
	Params [][]string `json:"params"`
	Headers [][]string `json:"headers"`
	Cookies []Cookie `json:"cookies"`
	Body Body `json:"post"`
	Type string `json:"type"`
	Mgmt string `json:"management"`
}

type Cookie struct {
	Name string `json:"name"`
	Value string `json:"value"`
	MaxAge int `json:"max-age"`
}

type Body struct {
	Json string `json:"json"`
	FormData string `json:"form-data"`
}

type Payload struct {
	ID string `json:"id"`
	Payload string `json:"payload"`
}

var wg sync.WaitGroup

// Function to fetch payloads from payload config file
func GetPayloads(payloadFile string) ([]Payload, error) {
	jsonFile, err := os.ReadFile(payloadFile)
	if err != nil {
		return nil, fmt.Errorf("Failed to load json file: %v",err)
	}
	var payloads []Payload
	err = json.Unmarshal(jsonFile, &payloads)
	if err != nil {
		return nil, fmt.Errorf("Failed to unmarshal payload json file: %v",err)
	}
	return  payloads, nil
}


// Function to fetch targets from target config file
func (targets *Targets) GetTargets(targetFile string) error {
	jsonFile, err := os.ReadFile(targetFile) 
	if err != nil {
		return fmt.Errorf("Failed to load target json file: %v",err)
	}
	err = json.Unmarshal(jsonFile, targets)
	if err != nil {
		return fmt.Errorf("Failed to unmarshal target json file: %v",err)
	}
	return nil
}

func TestTargets(targets *Targets, payloads *[]Payload) {
	replace_string = targets.Replace_str
	
	for _, target := range targets.Targets {
		for _, endpoint := range target.Endpoints {
			for _, payload := range *payloads {
				wg.Add(1)
				go BuildReq(&target, &endpoint, &payload) // function from sender.go (same package (main) while local)
			}
		}
	}
}

//Host connection details
var lhost string
var lport string

//Payload replace-string details
var replace_string string


func main() {
	title := `		       __        __                 
	_____  ______ |__| ____ |  | __ ___________ 
	\__  \ \____ \|  |/ ___\|  |/ // __ \_  __ \
	 / __ \|  |_> >  \  \___|    <\  ___/|  | \/
	(____  /   __/|__|\___  >__|_ \\___  >__|   
	     \/|__|           \/     \/    \/       
	`
	fmt.Println(title)	
	targets := Targets{}

	//array of payloads struct
	payloads, err := GetPayloads("payloads.json")
	if err != nil {
		fmt.Println(err)
		return
	}
	err = targets.GetTargets("targets.json")
	if err != nil {
		fmt.Println(err)
		return
	}
	lhost = targets.LHOST
	lport = targets.LPORT
	
	if lhost == "" || lport == "" {
		fmt.Println("Warning: Local host and / or local port has not been provided.")
		fmt.Println("Some payloads may not work correctly.")
	}

	TestTargets(&targets, &payloads)
	wg.Wait()
	return
}
