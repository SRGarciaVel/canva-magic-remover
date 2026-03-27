import torch
from PIL import Image
from transformers import AutoModelForImageSegmentation
from torchvision import transforms
import numpy as np
import cv2

device = "cuda" if torch.cuda.is_available() else "cpu"

# Cargamos el modelo
model = AutoModelForImageSegmentation.from_pretrained(
    "ZhengPeng7/BiRefNet", 
    trust_remote_code=True
)
model.to(device).float()
model.eval()

def remove_background(input_path, output_path):
    # 1. Cargar imagen original
    img_pil = Image.open(input_path).convert("RGB")
    w, h = img_pil.size
    
    # 2. Pre-procesamiento: Mejoramos el contraste local (CLAHE)
    # Esto ayuda a la IA a distinguir el fondo beige de la piel beige
    img_np = np.array(img_pil)
    img_lab = cv2.cvtColor(img_np, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(img_lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    l = clahe.apply(l)
    img_enhanced = cv2.merge((l,a,b))
    img_enhanced = cv2.cvtColor(img_enhanced, cv2.COLOR_LAB2RGB)
    img_pil_enhanced = Image.fromarray(img_enhanced)

    # 3. Preparar para la IA (Letterbox para no deformar)
    scale = 1024 / max(w, h)
    new_w, new_h = int(w * scale), int(h * scale)
    img_resized = img_pil_enhanced.resize((new_w, new_h), Image.Resampling.BILINEAR)
    
    input_canvas = Image.new("RGB", (1024, 1024), (0, 0, 0))
    input_canvas.paste(img_resized, ((1024 - new_w) // 2, (1024 - new_h) // 2))
    
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    input_tensor = transform(input_canvas).unsqueeze(0).to(device)

    # 4. Inferencia
    with torch.no_grad():
        preds = model(input_tensor)[-1].sigmoid().cpu()

    # 5. Post-procesamiento balanceado
    mask = preds[0].squeeze().numpy()
    
    # Recortar padding
    mask = mask[
        (1024 - new_h) // 2 : (1024 - new_h) // 2 + new_h,
        (1024 - new_w) // 2 : (1024 - new_w) // 2 + new_w
    ]
    
    # Redimensionar al tamaño original con alta fidelidad
    mask = cv2.resize(mask, (w, h), interpolation=cv2.INTER_LANCZOS4)

    # --- REFINAMIENTO PARA DISEÑO GRÁFICO ---
    # En lugar de borrar, ajustamos el contraste de la máscara.
    # Esto hace que las zonas "casi fondo" desaparezcan y las letras se mantengan.
    mask = np.clip((mask - 0.05) / (1.0 - 0.05), 0, 1) # Limpia neblina base
    mask = np.power(mask, 1.3) # Oscurece dudas sin matar bordes finos
    
    mask_uint8 = (mask * 255).astype(np.uint8)

    # 6. Aplicar máscara y guardar
    result = Image.open(input_path).convert("RGBA")
    mask_final_pil = Image.fromarray(mask_uint8)
    result.putalpha(mask_final_pil)
    
    result.save(output_path, "PNG", optimize=True)

print("--- Procesador Versión Final: Letras y Huecos Corregidos ---")