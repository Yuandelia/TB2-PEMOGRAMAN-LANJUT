from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
from database import conn

app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define Buku class
class Buku(BaseModel):
    judul: str
    penulis: str
    penerbit: str = None
    tahun_terbit: int = None
    konten: str = None
    iktisar: str = None

    def read(self, halaman: int):
        konten_halaman = self.konten.split('\n')[:halaman]
        for halaman_konten in konten_halaman:
            print(halaman_konten)

    def __str__(self):
        return f"{self.judul} by {self.penulis}"

@app.post("/buku/", response_model=Buku)
def post_buku(buku: Buku):
    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO buku (judul, penulis, penerbit, tahun_terbit, konten, iktisar) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (buku.judul, buku.penulis, buku.penerbit, buku.tahun_terbit, buku.konten, buku.iktisar))
        conn.commit()
        buku.id = cursor.lastrowid
        cursor.close()
        logger.info(f"Buku '{buku.judul}' berhasil disimpan.")
        return buku
    except Exception as e:
        logger.error(f"Terjadi kesalahan: {e}")
        raise HTTPException(status_code=500, detail="Terjadi kesalahan pada server.")

@app.get("/buku/{buku_id}", response_model=Buku)
def get_buku(buku_id: int):
    cursor = conn.cursor()
    query = "SELECT id, judul, penulis, penerbit, tahun_terbit, konten, iktisar FROM buku WHERE id=%s"
    cursor.execute(query, (buku_id,))
    buku = cursor.fetchone()
    cursor.close()
    if buku is None:
        raise HTTPException(status_code=404, detail="Buku tidak ditemukan")
    return {
        "id": buku[0],
        "judul": buku[1],
        "penulis": buku[2],
        "penerbit": buku[3],
        "tahun_terbit": buku[4],
        "konten": buku[5],
        "iktisar": buku[6]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
