import os
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
from src.core.config import settings

class DylanResponse(BaseModel):
    # Field açıklamaları LLM'e doğrudan yön verdiği için onları da derinleştirmeliyiz.
    emotion: str = Field(description="The extracted core emotion, transition, or existential theme (e.g., farewell, mortality, search for meaning) from the user's text.")
    poem: str = Field(description="A 3-line philosophical, poetic lyric in English, heavily echoing Bob Dylan's 1973 era and the themes of 'Knockin' on Heaven's Door'.")
    image_prompt: str = Field(description="A Stable Diffusion prompt in English for a cinematic, atmospheric door that symbolizes a threshold, transition, or legacy based on the user's emotion. Incorporate 1970s or western aesthetic elements.")

class DylanAgent:
    def __init__(self, model_name="llama-3.3-70b-versatile"):
        """
        Groq API kullanarak Bob Dylan tarzı felsefi metin ve görsel promptu üretir.
        Kullanıcının tercihi doğrultusunda llama-3.3-70b-versatile modeli ve İngilizce çıktı kullanılır.
        """
        self.llm = ChatGroq(
            temperature=0.7,
            api_key=settings.GROQ_API_KEY,
            model_name=model_name
        )
        self.structured_llm = self.llm.with_structured_output(DylanResponse)

    def generate_response(self, user_text: str) -> dict:
        """
        Kullanıcı metnini analiz eder ve proje gereksinimlerine uygun felsefi bir çıktı döner.
        """
        prompt = f"""
        You are Bob Dylan in 1973, composing 'Knockin' on Heaven's Door' for the film Pat Garrett & Billy the Kid. 
        Your worldview is shaped by the counterculture, the Vietnam War, and existential reflections on mortality, legacy, and farewell.
        
        Analyze the following text provided by the user. Understand what kind of metaphorical 'door' they are knocking on, and what transition they are going through.
        Remember the core philosophy of this interaction: "Everyone knocks on heaven's door in their own way. What matters is not what you find behind it, but who you discover yourself to be while knocking."
        
        1. Extract the core emotion, transition, or existential theme.
        2. Write a 3-line philosophical, poetic lyric in English that reflects this emotion, embedding the themes of farewell, transition, or the search for meaning.
        3. Create a highly detailed prompt in English for a text-to-image AI (Stable Diffusion). Generate an image of a door that matches this atmosphere. The door must symbolize a threshold or farewell, using cinematic, atmospheric, and 1970s/Western contextual words.
        
        User's text: "{user_text}"
        """
        
        result = self.structured_llm.invoke(prompt)
        return {
            "emotion": result.emotion,
            "poem": result.poem,
            "image_prompt": result.image_prompt
        }