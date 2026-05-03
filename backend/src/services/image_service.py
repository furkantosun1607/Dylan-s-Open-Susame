import os
import uuid
import requests
import urllib.parse
from src.core.config import settings

class ImageService:
    def __init__(self, output_dir="temp"):
        """
        Hugging Face Inference API su anda genel erisim sorunlari yasattigi (404 Error) icin,
        fallback olarak ucretsiz ve sinirsiz Pollinations AI (Stable Diffusion tabanli) kullanilmaktadir.
        """
        self.output_dir = output_dir
        
        # Temp klasörü yoksa oluştur
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)

    def generate_image(self, prompt: str) -> str:
        """
        Verilen prompt'a göre görsel üretir, temp klasörüne kaydeder ve dosya yolunu döner.
        """
        encoded_prompt = urllib.parse.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"
        response = requests.get(url)
        
        if response.status_code != 200:
            raise Exception(f"ImageGen API Error: {response.status_code} - {response.text}")
        filename = f"{uuid.uuid4()}.png"
        output_path = os.path.join(self.output_dir, filename)
        
        with open(output_path, "wb") as f:
            f.write(response.content)
            
        return output_path
