# Linguly Core

Linguly Core is the core of Linguly hosting the Agents and serving the interfaces.
Here we define agents in YAML files and provide the list of available Agents for each interface.
Interfaces can login and send user specific messages to a selected Agent.
Linguly Core then proxy the message and return the response from the Agent to the interface.
In the initial version, connection to the Dbs (DB Proxy) and to the models (Model Proxy) will be handled in Linguly Core as well.


## Local Setup

### Prerequisites

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
pip install -r requirements-dev.txt
```

### Environment variables for local setup

To successfully running the app locally you need to create a `.env` file in the root folder and provide the following the parameters:

```t
BASIC_MODEL_URL= # your ollama api url e.g. http://localhost:11434
MONGODB_MAIN_URL=  # use your mongodb atlas uri or a local one
JWT_SECRET= # use a long and secure secret in production
```

### Run Ollama if required locally

- `ollama serve`

### Run it

- run the server

```bash
uvicorn src.main:app --reload --port 3001
```

- open the API documentation: [http://localhost:3001/docs](http://localhost:3001/docs)

## Formatting

- to install `pip install black`
- to run on all files `black .` or specify a file or folder instead of `.`