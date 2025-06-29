from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import decoder_token
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://localhost",
        "http://localhost:8000",
    "http://127.0.0.1",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Load(BaseModel):
    token: str
# POST
@app.post("/post_token")
def post_token(load: Load):
     header_token, payload_token = decoder_token.decode_jwt(load.token)
     print(json.dumps(payload_token, indent=4))
     return {"decode_token":json.dumps(payload_token, indent=4)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
