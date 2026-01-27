from fastapi import FastAPI, Response
from pydantic import BaseModel
import subprocess
import tempfile
import os

VOICE_MODEL = os.environ.get("PIPER_MODEL", "/voices/ru_RU-irina-medium.onnx")
VOICE_CONFIG = os.environ.get("PIPER_CONFIG", "/voices/ru_RU-irina-medium.onnx.json")

app = FastAPI()

class TTSIn(BaseModel):
    text: str

@app.post("/tts")
def tts(payload: TTSIn):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        out_path = f.name

    try:
        proc = subprocess.run(
            ["piper", "--model", VOICE_MODEL, "--config", VOICE_CONFIG, "--output_file", out_path],
            input=payload.text.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        wav_bytes = open(out_path, "rb").read()
        return Response(content=wav_bytes, media_type="audio/wav")
    except subprocess.CalledProcessError as e:
        err = (e.stderr or b"").decode("utf-8", errors="ignore")
        return Response(content=f"Piper error:\n{err}", media_type="text/plain", status_code=500)
    finally:
        try:
            os.remove(out_path)
        except OSError:
            pass
