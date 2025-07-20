# Linguly Core

Linguly Core is the core of [Linguly](https://github.com/Linguly). To learn more about Linguly Check [our documentation](https://docs.linguly.io/) or this [one pager](https://github.com/Linguly?view_as=public#linguly-language-learning-platform).


- Linguly core hosts the Agents and serving the interfaces.
- Here we define agents in YAML files and provide the list of available Agents for each interface.
- Interfaces can login and send user specific messages to a selected Agent.
- Linguly Core then proxy the message and return the response from the Agent to the interface.
- Currently connection to the Dbs (DB Proxy) and to the models (Model Proxy) are also handled in Linguly Core.


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

- install pre-commit to always format the files before commit:

```bash
pre-commit install
```

And to disable it:

```bash
pre-commit uninstall
```

### Environment variables for local setup

To successfully running the app locally you need to create a `.env` file in the root folder and provide the following the parameters:

```t
OLLAMA_URL= # your ollama api url e.g. http://localhost:11434
OPENAI_API_KEY= # your openAI API key if available
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


## Disable connectors when testing

In order to reduce cost and complexity while testing, we can disable all connectors and use the echo model instead.
For that just add the following to your `.env` file.
```
ECHO_MODEL_ENABLED=true
```

## Formatting

- to install `pip install black`
- to run on all files `black .` or specify a file or folder instead of `.`