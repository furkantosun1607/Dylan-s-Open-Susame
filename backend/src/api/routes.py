import os
import uuid
import asyncio
from fastapi import APIRouter, UploadFile, File, HTTPException
from src.services.stt_service import STTService
from src.core.agent import DylanAgent
from src.services.tts_service import TTSService
from src.services.image_service import ImageService

router = APIRouter()

# Servisleri ayağa kaldıralım (Sadece bir kere başlatılacaklar)
stt_service = STTService()
agent = DylanAgent()
tts_service = TTSService()
image_service = ImageService()

TEMP_DIR = "temp"

@router.get("/status")
def get_status():
    return {"status": "ok", "service": "Bob Dylan AI Backend"}

@router.post("/knock")
async def knock_door(file: UploadFile = File(...)):
    """
    1) Ses dosyasını alır.
    2) STT ile metne çevirir.
    3) DylanAgent ile Duygu, Şiir ve Kapı betimlemesi üretir.
    4) TTS ve ImageGen servislerini PARALEL çalıştırarak süreyi kısaltır.
    5) Oluşan içerik ve dosyaların URL'lerini frontend'e döner.
    """
    try:
        # 1. Gelen ses dosyasını geçici olarak kaydet
        audio_filename = f"input_{uuid.uuid4()}_{file.filename}"
        input_audio_path = os.path.join(TEMP_DIR, audio_filename)
        
        with open(input_audio_path, "wb") as f:
            f.write(await file.read())
            
        # 2. STT: Sesi metne çevir
        # faster-whisper CPU üzerinde biraz zaman alabilir, event loop'u bloklamaması için to_thread kullanabiliriz,
        # ancak basitlik açısından doğrudan da çağrılabilir. Yine de asenkron ortamı rahatlatmak için to_thread iyi olur.
        transcribed_text = await asyncio.to_thread(stt_service.transcribe, input_audio_path)
        
        if not transcribed_text:
            transcribed_text = "I couldn't say a word, I just stood there in silence."
            
        # 3. Agent: Duygu, Şiir ve Görsel Promptunu Üret
        agent_result = await asyncio.to_thread(agent.generate_response, transcribed_text)
        
        poem = agent_result["poem"]
        emotion = agent_result["emotion"]
        image_prompt = agent_result["image_prompt"]
        
        # 4. Paralel İşlem: TTS ve ImageGen
        # ImageService senkron olduğu için to_thread, TTS asenkron olduğu için doğrudan veriyoruz.
        image_task = asyncio.to_thread(image_service.generate_image, image_prompt)
        tts_task = tts_service.generate_audio(poem)
        
        # İkisinin de bitmesini aynı anda bekle (Süre yarı yarıya düşer)
        image_path, audio_path = await asyncio.gather(image_task, tts_task)
        
        # Frontend için URL'leri formatla (Windows backslash sorununu düzeltmek için)
        image_url = f"/{image_path.replace(os.sep, '/')}"
        audio_url = f"/{audio_path.replace(os.sep, '/')}"
        
        return {
            "text_transcribed": transcribed_text,
            "emotion": emotion,
            "poem": poem,
            "audio_url": audio_url,
            "image_url": image_url
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
