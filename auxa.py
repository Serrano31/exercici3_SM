import os
import tempfile
from google.cloud import speech_v1
from google.cloud import storage

def transcribe_audio(event, context):
    # Obtiene el nombre del archivo de audio desde los datos del evento
    file_name = event['name']
    
    # Descarga el archivo de audio desde Cloud Storage
    temp_dir = tempfile.mkdtemp()
    local_audio_path = os.path.join(temp_dir, file_name)
    bucket_name = event['bucket']
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.download_to_filename(local_audio_path)
    
    # Inicializa el cliente de Speech-to-Text
    client = speech_v1.SpeechClient()

    # Lee el contenido del archivo de audio
    with open(local_audio_path, "rb") as audio_file:
        content = audio_file.read()

    # Especifica la configuración para la transcripción
    config = {
        "language_code": "es-ES",  # Cambia a tu idioma preferido
        "sample_rate_hertz": 16000,
    }
    audio = {"content": content}

    # Realiza la transcripción
    response = client.recognize(config=config, audio=audio)

    # Obtiene el texto transcrito
    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript + "\n"

    # Devuelve el texto transcrito y el archivo de audio original
    return {
        'transcript.txt': transcript,
        'original_audio.mp3': local_audio_path
    }
