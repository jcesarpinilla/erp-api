from fastapi import FastAPI, Header, HTTPException

app = FastAPI()

API_KEY = "P@ssw0rdapi$"

@app.get("/")
def home():
    return {"status": "API funcionando"}

@app.post("/upload")
def upload_data(data: dict, x_api_key: str = Header(None)):

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return {
        "status": "ok",
        "empresa": data.get("empresa_id"),
        "modulo": data.get("modulo"),
        "registros": len(data.get("data", []))
    }
