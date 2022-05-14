from fastapi import FastAPI, UploadFile
import main

app = FastAPI()

@app.get("/")
async def home():
    if main.in_motion():
        if main.in_motion() in [main.success(), main.alert()]:
            return main.in_motion()
        return main.return_saved_image()
    else:
        return 0

@app.post("/upload/{name}")
def upload(name: str, file: UploadFile):
    main.upload_img(name, file)

@app.get("/train_data")
async def train():
    main.create_encoding_dataset()
    return ""


@app.post("/")
async def data(file: UploadFile):
    print(main.process_data(file.file.read()))