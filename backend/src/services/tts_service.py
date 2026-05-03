import os
import uuid
import edge_tts

class TTSService:
    def __init__(self, voice="en-US-ChristopherNeural", output_dir="temp"):
        """
        edge-tts kullanarak metinden sese (Text-to-Speech) çeviri yapar.
        Varsayılan olarak derin bir erkek sesi (Christopher) kullanılır.
        """
        self.voice = voice
        self.output_dir = output_dir
        
        # Temp klasörü yoksa oluştur
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)

    async def generate_audio(self, text: str) -> str:
        """
        Verilen metni ses dosyası olarak kaydeder ve dosya yolunu döner.
        """
        filename = f"{uuid.uuid4()}.mp3"
        output_path = os.path.join(self.output_dir, filename)
        
        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(output_path)
        
        return output_path
