import os
import torch
from transformers import AutoModelForImageSegmentation

def download():
    print("Iniciando descarga de modelos de IA...")
    try:
        # Esto descarga los pesos y los deja en la cache local
        model = AutoModelForImageSegmentation.from_pretrained(
            "ZhengPeng7/BiRefNet", 
            trust_remote_code=True
        )
        print("✅ BiRefNet descargado correctamente.")
    except Exception as e:
        print(f"❌ Error descargando: {e}")

if __name__ == "__main__":
    download()