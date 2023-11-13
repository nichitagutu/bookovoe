import logging


logging.basicConfig(filename="example.log", encoding="utf-8", level=logging.DEBUG)

import json
import urllib.request

from file_handling import save_words_from_text


import rowordnet as rwn
from cube.api import Cube
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import redis

from dotenv import load_dotenv

load_dotenv()


redis_client = redis.StrictRedis(host="localhost", port=6379, db=0)


WORDNET = rwn.RoWordNet()

CUBE = Cube(verbose=True)
CUBE.load("ro")

app = FastAPI()

origins = [
    "http://localhost:1422",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def add_entry(word, definition, value):
    key = json.dumps({"word": word, "definition": definition})
    redis_client.set(key, value)


def exists(word, definition):
    key = json.dumps({"word": word, "definition": definition})
    return redis_client.exists(key)


def get_value(word, definition):
    key = json.dumps({"word": word, "definition": definition})
    return redis_client.get(key)


def request(action, **params):
    return {"action": action, "params": params, "version": 6}


def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode("utf-8")
    response = json.load(
        urllib.request.urlopen(
            urllib.request.Request("http://127.0.0.1:8765", requestJson)
        )
    )
    if len(response) != 2:
        raise Exception("response has an unexpected number of fields")
    if "error" not in response:
        raise Exception("response is missing required error field")
    if "result" not in response:
        raise Exception("response is missing required result field")
    if response["error"] is not None:
        raise Exception(response["error"])
    return response["result"]


def add_definitions_to_anki(definitions, deck_name):
    invoke("createDeck", deck=deck_name)
    notes = []

    for word, definitions_list in definitions.items():
        for definition in definitions_list:
            if exists(word, definition):
                continue

            add_entry(word, definition, 1)
            notes.append(
                {
                    "deckName": deck_name,
                    "modelName": "Basic",
                    "fields": {
                        "Front": word,
                        "Back": definition,
                    },
                    "options": {
                        "allowDuplicate": True,
                        "duplicateScope": "deck",
                        "duplicateScopeOptions": {
                            "deckName": deck_name,
                            "checkChildren": False,
                            "checkAllModels": False,
                        },
                    },
                }
            )

    invoke(
        "addNotes",
        notes=notes,
    )

    logging.info("Successfully added notes to Anki")
    logging.info(len(notes))


@app.post("/text")
async def upload_text(
    text: str, language: str = "ro", deck_name: str = "Romanian_slovoed"
):
    definitions = save_words_from_text(CUBE, WORDNET, text)
    add_definitions_to_anki(definitions, deck_name)

    return {"text": text, "definitions_length": len(definitions)}


@app.post("/file")
async def upload_file(
    file: UploadFile, language: str = "ro", deck_name: str = "Romanian_slovoed"
):
    allowed_extensions = {"txt", "pdf", "epub", "fb2"}

    filename = file.filename
    file_extension = filename.rsplit(".", 1)[1].lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="File format not supported")

    contents = await file.read()
    text = contents.decode("utf-8")
    definitions = save_words_from_text(CUBE, WORDNET, text)

    add_definitions_to_anki(definitions, deck_name)

    return {"filename": file.filename, "definitions_length": len(definitions)}
