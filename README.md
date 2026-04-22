***voice ai appointment system

**overview
this project is a voice based ai system that allows users to book cancel reschedule and check doctor appointments using voice input  

**features
 speech to text using whisper  
 multilingual support  
 ai agent for intent detection  
 appointment booking system  
 session memory  
 text to speech  
 websocket real time  

**how it works
1 user gives voice input  
2 speech converted to text  
3 language detection and translation  
4 ai agent processes request  
5 tool orchestrator calls services  
6 scheduling system executes  
7 response generated  
8 text converted to speech  

**run project
uvicorn backend.api.main:app --reload  

**example
input:  
book cardiologist tomorrow  

output:  
your appointment with dr sharma is booked  

**technologies
python fastapi whisper websocket  


**run the project

1 open terminal

2 go to project folder

3 run command

uvicorn backend.api.main:app --reload

4 open browser

http://127.0.0.1:8000/docs


**websocket testing

connect using websocket:

ws://127.0.0.1:8000/ws

send message example:

book cardiologist tomorrow

you will receive:

your appointment with dr sharma is booked for tomorrow at 10:30 am