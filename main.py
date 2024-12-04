import uvicorn
from fastapi import FastAPI
from midnite.routers import events

app = FastAPI()


@app.get("/lives")
def is_lives():
    return 1


app.include_router(events.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
