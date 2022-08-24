package main

import (
	"log"
	"os"
	"raft_algorithm/client"
	"raft_algorithm/server"
)

func main() {
	//args := os.Args[1:]

	t := ""
	if len(os.Args) >= 2 {
		t = os.Args[1]
	}

	if t == "server" {
		server.Main()
	} else if t == "client" {
		client.Main()
	} else {
		log.Fatalln("Arg[1] neither server or client !!")
	}
}
