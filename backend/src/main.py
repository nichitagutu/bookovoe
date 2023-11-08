import logging

logging.basicConfig(filename="example.log", encoding="utf-8", level=logging.DEBUG)

import rowordnet as rwn
from cube.api import Cube
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv

load_dotenv()

from db.connection import Database
from models.word import Word
from models.user_review import UserReview
from models.definition import Definition

WORDNET = rwn.RoWordNet()

CUBE = Cube(verbose=True)
CUBE.load("ro")

Database.initialize()

# allow origin localhost:1420


app = FastAPI()

origins = [
    "http://localhost:1420",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/words")
def get_all_words():
    return {"words": Word.get_all_words()}


@app.get("/word/{word_id}/definition")
def get_definition(word_id: int):
    return {"definition": Definition.get_definition(word_id)}


@app.post("/review")
def add_review(user_id: int, word_id: int, review_quality: int, review_date: str):
    user_review = UserReview(user_id, word_id, review_date)
    user_review.update_review(review_quality)
    return {"review_id": user_review.review_id}


@app.post("/file")
async def upload_file(file: UploadFile):
    contents = await file.read()
    text = contents.decode("utf-8")
    definitions = Word.save_words_from_text(CUBE, WORDNET, text)

    return {"filename": file.filename, "definitions": definitions}
