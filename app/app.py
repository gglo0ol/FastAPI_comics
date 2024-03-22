from fastapi import FastAPI

from views import router
from core.db import init_db


app = FastAPI()
app.include_router(router)


@app.on_event("startup")
async def start_db():
    await init_db()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app=app, host="localhost", port=8000)
