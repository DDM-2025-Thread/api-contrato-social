from google import genai
from google.genai import types
from app.schemas.social_contract_squema import ContratoSocial
import os
import uuid
from io import BytesIO
import json

class GeminiService:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.model_name = "gemini-2.5-flash"
        self.prompt_context = (
            "Given the text of a social contract, extract key information and return it in the provided JSON format. Discuss in Portuguese(BR)"
        )

    def upload_pdf_for_processing(self, pdf_file_bytes: bytes) -> types.File:
        pdf_stream = BytesIO(pdf_file_bytes)
        file_name = f"upload-{uuid.uuid4()}.pdf"
        uploaded_file = self.client.files.upload(
            file=pdf_stream,
            config={
                "display_name": file_name,
                "mime_type": "application/pdf"
            }
        )
        return uploaded_file

    def get_contract_data(self, uploaded_file: types.File) -> dict:
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[uploaded_file, self.prompt_context],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=ContratoSocial,
                )
            )
            return json.loads(response.text)
        except json.JSONDecodeError as e:
             print(f"Erro ao analisar o JSON do Gemini: {e}")
             raise ValueError(f"Resposta inválida do modelo: {response.text}") from e
