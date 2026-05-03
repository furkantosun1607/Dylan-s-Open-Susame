import os
from faster_whisper import WhisperModel

class STTService:
    def __init__(self, model_size="base", device="cpu", compute_type="int8"):
        """
        faster-whisper kullanarak sesten metne (Speech-to-Text) çeviri yapar.
        Varsayılan olarak CPU üzerinde ve int8 kuantizasyonu ile çalışır.
        """
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)

    def transcribe(self, audio_file_path: str) -> str:
        """
        Verilen ses dosyasını metne çevirir.
        """
        segments, info = self.model.transcribe(audio_file_path, beam_size=5)
        text = " ".join([segment.text for segment in segments])
        return text.strip()
