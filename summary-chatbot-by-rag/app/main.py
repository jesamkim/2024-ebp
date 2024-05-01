import os

import aiofiles
from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from os.path import abspath, dirname, join

import generator
import helpers.document_helper as doc_helper
import uploader

app = FastAPI()

dir_path = os.path.dirname(os.path.realpath(__file__))
static_dir = os.path.join(dir_path, "ui/static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

templates = Jinja2Templates(directory="ui")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"id": id}
    )
    # return templates.TemplateResponse("index.html", {"request": request, "id": id})
    # # return templates.TemplateResponse(
    # #     name="index.html", context={"request": request, "id": id}
    # # )


@app.get("/health")
async def root():
    return {"message": "Healthy"}


class Claude2Data(BaseModel):
    modelId: str
    maxTokens: int
    temperature: float
    topP: float
    topK: int
    prompt: str


@app.post("/answer/{filename}")
async def get_answer(data: Claude2Data, filename: str):
    # print(data)
    #
    # result = {}
    # filepath = join(dirname(abspath(__file__)), "tmp", filename)
    # result['result'] = generator.generate_summary(filepath=filepath, question=question, max_tokens=data.maxTokens,
    #                                               temperature=data.temperature, top_p=data.topP, top_k=data.topK)
    # result['question'] = question
    # return result

    print(data)
    question = ""

    result = {}
    filepath = join(dirname(abspath(__file__)), "tmp", filename)
    result['result'] = generator.generate_summary(filepath=filepath, question=question, max_tokens=data.maxTokens,
                                                  temperature=data.temperature, top_p=data.topP, top_k=data.topK, prompt=data.prompt)
    result['question'] = question
    return result


@app.post("/answer/{filename}/{question}")
async def get_answer_with_retrieval(data: Claude2Data, filename: str, question: str):
    print(data)

    result = {}
    filepath = join(dirname(abspath(__file__)), "tmp", filename)
    result['result'] = generator.generate_summary(filepath=filepath, question=question, max_tokens=data.maxTokens,
                                                  temperature=data.temperature, top_p=data.topP, top_k=data.topK, prompt=data.prompt)
    result['question'] = question
    return result


@app.get("/documents")
async def get_documents(request: Request):
    return uploader.get_filelist()


@app.post("/documents/{document}")
async def upload_document(file: UploadFile, document: str):
    print(f"File Name: {file.filename}", flush=True)
    print(f"Document Name: {document}", flush=True)
    await uploader.save_file(file, document)
    return {"status": 200}


@app.delete("/documents/{document}")
async def delete_documents(document: str):
    await uploader.delete_file(document)
    return {
        "result": 200
    }
