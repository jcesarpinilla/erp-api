from fastapi import FastAPI, Header, HTTPException
import psycopg2
import os

app = FastAPI()

# API KEY desde entorno
API_KEY = os.getenv("P@ssw0rdapi$")

# FUNCIÓN DE CONEXIÓN
def get_conn():
    return psycopg2.connect(
        host="https://lfybdquesopbadahgvps.supabase.co",
        database="postgres",
        user="postgres",
        password="TsvmBnMuFq4zgZIw",
        port="5432"
    )

@app.get("/")
def home():
    return {"status": "API funcionando con BD"}

@app.post("/upload")
def upload_data(data: dict, x_api_key: str = Header(None)):

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    conn = get_conn()
    cur = conn.cursor()

    empresa_id = data.get("empresa_id")
    modulo = data.get("modulo")

    # =========================
    # VENTAS
    # =========================
    if modulo == "ventas":
        for item in data.get("data", []):
            cur.execute("""
                INSERT INTO ventas (
                    empresa_id, fecha, cliente_id, cliente,
                    producto_id, producto, cantidad, precio, costo, total
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                empresa_id,
                item["fecha"],
                item["cliente_id"],
                item["cliente"],
                item["producto_id"],
                item["producto"],
                item["cantidad"],
                item["precio"],
                item["costo"],
                item["total"]
            ))

    conn.commit()
    cur.close()
    conn.close()

    return {"status": "ok", "modulo": modulo}
