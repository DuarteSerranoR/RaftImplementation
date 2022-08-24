package lib

import "io/ioutil"

type Replica struct {
	id   int
	host string
	port int
	//client Client
}

func LoadReplicas(path string) []Replica {
	b, _ := ioutil.ReadFile("./replicas")
	// TODO - catch err
	s := string(b)
	print(s)
	return make([]Replica, 0)
}
