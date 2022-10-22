package main

import (
	"encoding/json"
	"fmt"
	"os"
	"flag"
)


// An array of attack targets
type Targets struct {
	Targets []Target `json:"targets"`
	//soon to add proxy support
	Replace_str string `json:"replace-string"`
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

// An array of payloads

type Payload struct {
	ID string `json:"id"`
	Payload string `json:"payload"`
}

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

func SendRequest() error {
return nil
}

//func TestTargets(targets *Targets, payloads *Payloads) {
//	replace_string := targets.Replace_str
//	replace_id := payloads.Replace_string

//	for _, target := range targets.Targets {
//		for _, endpoint := range targets.Endpoints {
//			for _, payload := range payloads.Payloads {
//				wg.Add(1)
				//go SendRequest()
//			}
//		}
//	}
//}

//Host connection details
var lhost string
var lport string


func main() {
	title := `		       __        __                 
	_____  ______ |__| ____ |  | __ ___________ 
	\__  \ \____ \|  |/ ___\|  |/ // __ \_  __ \
	 / __ \|  |_> >  \  \___|    <\  ___/|  | \/
	(____  /   __/|__|\___  >__|_ \\___  >__|   
	     \/|__|           \/     \/    \/       
	`
	fmt.Println(title)
	flag.StringVar(&lhost, "l", "", "specify the local IP address, which will replace LHOST in payloads")
	flag.StringVar(&lport, "p", "", "specify the local port, which will replace LPORT in payloads")
	boolPtr := flag.Bool("h", false, "show this help message and exit")

	for _, arg := range os.Args {
		if arg == "-h" {
			*boolPtr = true
			break
		}
	}

	flag.Parse()
	if *boolPtr == true{
		flag.PrintDefaults()
		return
	}
	
	if lhost == "" || lport == "" {
		fmt.Println("Warning: Local host and/or local port not specified, payloads requiring either may not run correctly.")
	}
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
	fmt.Println(payloads)
	//TestTargets(&targets, &payloads)
	//wg.Wait()
	return
}
