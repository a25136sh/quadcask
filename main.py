from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/hello")
async def hello():
    return {"message": "Hello World!!!"}


app.mount(
    "/",
    StaticFiles(directory="frontend/dist", html=True),
    name="static"
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("__main__:app", reload=True)
