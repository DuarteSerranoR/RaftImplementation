# Raft Implementation
Project for Fault Tolerance in Distributed Systems - Lib developed for learning.

<h2><b>BEFORE USING</b></h2>
<h3>For the database:</h2>
<p>You need to check the following pre-requisites:</p>
<ol>
    <li>Have PostgreSQL Installed in your local machine;</li>
    <li>Have the replicas file filled with the desired ip addresses;</li>
    <li>Have the desired databases created in PostgreSQL</li>
</ol>

<h3>For the PostgreSQL Databases creation:</h3>
<ul>
    <li>-driver -> PostgreSQL</li>
    <li>-server -> localhost</li>
    <li>-dbname -> {program name passed as an argument}-raft-logs</li>
    <li>-uname -> dev</li>
    <li>-pwd -> passwd</li>
</ul>

<h2>Other installation and Usage instructions</h2>
<p>To launch the application, with all the pre-requisites checked out,
You only run the main.py with the following arguments:</p>
```sh
main.py {number of the replica starting at index 0} {program name passed to the database creation}
```
<p>Following this logic, for the replica 0, with the database raft0-raft-logs, you run:</p>
```sh
main.py 0 raft0
```
