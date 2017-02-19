Project Title:-

Trigger RESTFULL application running on minion server to execute list of shell commands.

Prerequisites:-

1. Passwordless authentication enabled between client and servers.
   This can be done either by injectig ssh key into server from cloud manager
2. Assuming vendor docker images are available in vendor private repository. 
3. pyhton verson less then 3
4. Cloud environment firewall rules updated with required ports. 

Dependency:-

1. Server application container should be spawned before client container.


Installing:-

Separate containers should be created for client and server respectively.
It is not mandatory for client container creation since it involvs static installation tools.
A pyhton image from Docker hub is used as a base image. 


SERVER -

Step 1:
Download the server tar bundle from the deliver_repo from the GIT and untar the same
>tar -xzvf docker_server.tar.gz
docker_server/
			-dependency.txt
			-script_cmd.py
			-minion_server_app.py
			-Dockerfile

note: description of above files can be found in Activity_description_guide.docx document.

Step 2:
Build image
>cd docker_server/
>docker build -t minion_server:latest .

Step 3:
Spawn container
>docker run -d -p 5000:5000 minion_server

CLIENT -

Step 1:
Download the client tar bundle from the deliver_repo from the GIT and untar the same
>tar -xzvf docker_client.tar.gz
docker_server/
			-dependency.txt
			-action_list.json
			-operator_input_file.yaml
			-minion_client_app.py
			-Dockerfile

note: description of above files can be found in minion_activity.docx document.

Step 2:
Build image
>cd docker_client/
>docker build -t minion_client:latest .

Step 3:
Spawn container
>docker run -d minion_client

Built With:-
Flask - Webframework library from python
pyaml - yaml parser library from python

Improvements:-
Both server and client tools can be improvised for robustness and error handling.


Versioning:-
1.0

Authors:-
Pradeep Kumar D S (ppradeepkumards@gmail.com)




	
   
