package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"strings"
)

func SendReq(req *http.Request, endpoint *Endpoint) {

	// client := &http.Client{}
	// client.Do(req)
	return
}

func BuildReq(target *Target, endpoint *Endpoint, payload string) error {
	defer wg.Done()
	// Code goes here
	target_url := target.URI + ":" + endpoint.Port + endpoint.Path
	var body io.Reader

	//Replacing lhost lport in payload
	payload_str := strings.Replace(payload, "lhost", lhost, -1)
	payload_str = strings.Replace(payload_str, "lport", lport, -1)

	// Replacing any rstrings with payload_str
	jsondata := strings.Replace(endpoint.Body.Json, replace_string, payload_str, -1)
	formdata := strings.Replace(endpoint.Body.FormData, replace_string, payload_str, -1)

	data, err := json.Marshal(jsondata)
	if err != nil {
		return fmt.Errorf("Failed to marshal json post data: %v", err)
	}
	form, err := url.ParseQuery(formdata)
	if err != nil {
		return fmt.Errorf("Failed to parse http form query: %v", err)
	}
	if len(form) == 0 {
		body = bytes.NewReader(data)
	} else {
		body = strings.NewReader(form.Encode())
	}
	req, err := http.NewRequest(endpoint.Http_verb, target_url, body)

	// Replacing any rstrings with payload
	if len(endpoint.Headers) != 0 {
		for i, header := range endpoint.Headers {
			if len(header) != 2 {
				fmt.Println("Header", i+1, "is invalid (for '", target_url, "')")
			} else {
				val := strings.Replace(header[1], replace_string, payload_str, -1)
				req.Header.Add(header[0], val)
			}
		}
	}

	for _, cookie := range endpoint.Cookies {
		c := &http.Cookie{
			Name:   cookie.Name,
			Value:  cookie.Value,
			MaxAge: 0,
		}
		req.AddCookie(c)
	}

	q := req.URL.Query()
	if len(endpoint.Params) != 0 {
		for i, param := range endpoint.Params {
			if len(param) != 2 {
				fmt.Println("Parameter", i+1, "is invalid (for '", target_url, "')")
			} else {
				val := strings.Replace(param[1], replace_string, payload_str, -1)
				q.Add(param[0], val)
			}
		}
	}
	req.URL.RawQuery = q.Encode()

	SendReq(req, endpoint)
	return nil
}
