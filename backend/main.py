from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import shutil
import os
import uuid

from processor import remove_background
from database import SessionLocal, engine, Base
from models import ImageHistory

# Crear tablas en Supabase si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

OUTPUT_DIR = "outputs"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

app.mount("/outputs", StaticFiles(directory=OUTPUT_DIR), name="outputs")

@app.post("/process/")
async def process_image(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    temp_path = f"temp_{file.filename}"
    output_filename = f"result_{file_id}.png"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Procesamiento (Detección auto GPU/CPU interna en processor.py)
    remove_background(temp_path, output_path)
    os.remove(temp_path)

    # Guardar registro en Supabase
    db = SessionLocal()
    db_img = ImageHistory(original_name=file.filename, file_path=output_filename)
    db.add(db_img)
    db.commit()
    db.close()

    return {"url": f"http://localhost:8000/outputs/{output_filename}"}

@app.get("/history/")
def get_history():
    db = SessionLocal()
    history = db.query(ImageHistory).order_by(ImageHistory.id.desc()).limit(20).all()
    db.close()
    return history