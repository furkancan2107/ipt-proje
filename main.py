
from fastapi import FastAPI
import databases
import sqlalchemy



DATABASE_URL = "sqlite:///./test.db"


app = FastAPI()


database = databases.Database(DATABASE_URL)


metadata = sqlalchemy.MetaData()

# Örnek bir tablo oluştur
notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)

@app.on_event("startup")
async def startup():
    await database.connect()
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
async def read_root():
    return {"message": "Hello FastAPI"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)

