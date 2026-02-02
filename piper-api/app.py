from fastapi import FastAPI
from fastapi.responses import FileResponse, PlainTextResponse
from pydantic import BaseModel
import subprocess, tempfile, os
from starlette.background import BackgroundTask

VOICE_MODEL = os.environ.get("PIPER_MODEL", "/voices/ru_RU-irina-medium.onnx")
VOICE_CONFIG = os.environ.get("PIPER_CONFIG", "/voices/ru_RU-irina-medium.onnx.json")

app = FastAPI()

class TTSIn(BaseModel):
    text: str

def _cleanup(path: str):
    try:
        os.remove(path)
    except OSError:
        pass

@app.post("/tts")
def tts(payload: TTSIn):
    fd, out_path = tempfile.mkstemp(suffix=".wav")
    os.close(fd)

    try:
        subprocess.run(
            ["piper", "--model", VOICE_MODEL, "--config", VOICE_CONFIG, "--output_file", out_path],
            input=payload.text.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )

        return FileResponse(
            out_path,
            media_type="audio/wav",
            filename="tts.wav",
            background=BackgroundTask(_cleanup, out_path),
        )

    except subprocess.CalledProcessError as e:
        _cleanup(out_path)
        err = (e.stderr or b"").decode("utf-8", errors="ignore")
        return PlainTextResponse(f"Piper error:\n{err}", status_code=500)
