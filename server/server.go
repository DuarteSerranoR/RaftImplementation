package server

import "raft_algorithm/lib"

// TODO - register server and then do some kind of listener/handler for requests
func Main() {
	replicas := lib.LoadReplicas("../replicas")
	print(replicas)
	/*
		arguments := os.Args
		if len(arguments) == 1 {
			fmt.Println("Please provide port number")
			return
		}

		PORT := ":" + arguments[1]
		l, err := net.Listen("tcp", PORT)
		if err != nil {
			fmt.Println(err)
			return
		}
		defer l.Close()

		c, err := l.Accept()
		if err != nil {
			fmt.Println(err)
			return
		}

		for {
			netData, err := bufio.NewReader(c).ReadString('\n')
			if err != nil {
				fmt.Println(err)
				return
			}
			if strings.TrimSpace(string(netData)) == "STOP" {
				fmt.Println("Exiting TCP server!")
				return
			}

			fmt.Print("-> ", string(netData))
			t := time.Now()
			myTime := t.Format(time.RFC3339) + "\n"
			c.Write([]byte(myTime))
		}
	*/
}
