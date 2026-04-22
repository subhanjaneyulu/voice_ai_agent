****setup instructions

first make sure python is installed in your system

open terminal in the project folder

create virtual environment
python -m venv venv

activate virtual environment

for windows
venv\scripts\activate

for mac or linux
source venv/bin/activate

install required packages
pip install fastapi uvicorn faster-whisper deep-translator

run the server
run the server
uvicorn backend.api.main:app --reload

open the application in browser
open api documentation
http://127.0.0.1:8000/docs

4 websocket endpoint
ws://127.0.0.1:8000/ws
______________________________________________________________________________________________________________

***architectural decisions
________________________
the system is designed using a modular approach where each component has a clear responsibility. speech to text is handled using whisper model. language detection and translation convert all input into english. the ai agent extracts intent doctor date and time. the tool orchestrator decides which backend service to call. the scheduling system handles booking availability cancel and reschedule. text to speech converts the final response into audio. this structure makes the system easy to maintain and scalable.
__________________________________________________________________________________________

***memory design
_________________
the system uses session based memory to store user context such as doctor date and time. this helps when the user gives incomplete input. for example if the user first says book appointment and then says tomorrow the system remembers previous data and completes the request. currently memory is stored in runtime and will reset when the server restarts.

____________________________________________________________________________________________________________________
****latency breakdown
speech to text takes the most time depending on audio length. agent processing is fast because it uses simple logic. tool execution is very fast as it uses in memory data. text to speech adds a small delay. overall the system responds quickly and supports near real time interaction.
___________________________________________________________________________________________________________________ 
***tradeoffs
the system uses an in memory database instead of a real database to keep it simple. rule based logic is used instead of complex ai models for faster performance. only a limited set of doctor specialties is supported. cpu based processing is used instead of gpu to keep the system lightweight. these decisions improve speed but limit scalability.
___________________________________________________________________________________________________________________ 
****known limitations
tamil speech recognition may not be highly accurate. data is not stored permanently and will be lost after restart. the system supports only limited doctor types. time understanding is basic and may not handle complex sentences. there is no user authentication implemented.
_________________________________________________________________________________________________________________________