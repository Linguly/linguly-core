# Linguly Core

Linguly Core is the core of Linguly hosting the Agents and serving the interfaces.
Here we define agents in YAML files and provide the list of available Agents for each interface.
Interfaces can login and send user specific messages to a selected Agent.
Linguly Core then proxy the message and return the response from the Agent to the interface.
In the initial version, connection to the Dbs (DB Proxy) and to the models (Model Proxy) will be handled in Linguly Core as well.


## Local Setup

- Setup venv
  - for Windows:

  ```bash
  python -m venv venv
  .\venv\Scripts\activate
  ```
  - for macOS/Linux:
  
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

- install dependencies
```bash
pip install -r requirements.txt
```

- run the server

```bash
uvicorn src.main:app --reload --port 3001
```

- or if you want to connect to a local ollama

```bash
BASIC_MODEL_URL=http://localhost:11434 uvicorn src.main:app --reload --port 3001
```

- open the API documentation: [http://localhost:3001/docs](http://localhost:3001/docs)

## Formatting

- to install `pip install black`
- to run on all files `black .` or specify a file or folder instead of `.`