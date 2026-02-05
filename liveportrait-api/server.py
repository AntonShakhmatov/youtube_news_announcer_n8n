from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import os
from pathlib import Path
import uuid

app = FastAPI(title="LivePortrait API", version="1.0")

class AnimateRequest(BaseModel):
    source_path: str # Path for what we planing animate
    driving_path: str # Path for how animation will looks like
    driving_multiplier: float = 1.75
    no_flag_stitching: bool = True 
    output_dir: str = "/files/final/"

class AnimateResponse(BaseModel):
    ok: bool
    output_dir: str
    stdout: str
    stderr: str

def _safe_path(p: str, allowed_prefixes=("/files/", "/app/")) -> str:
    p = os.path.abspath(p)
    if not any(p.startswith(os.path.abspath(pref)) for pref in allowed_prefixes):
        raise ValueError(f"Path not allowed: {p}")
    return p


@app.get("/health")
def health():
    return {"ok": True}

@app.post("/animate", response_model=AnimateResponse)
def animate(req: AnimateRequest):
    try:
        source = _safe_path(req.source_path)
        driving = _safe_path(req.driving_path)
        out_dir = _safe_path(req.output_dir, allowed_prefixes=("/files/",))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    job_id = uuid.uuid4().hex[:10]
    job_out = Path(out_dir) / job_id
    job_out.mkdir(parents=True, exist_ok=True)

    cmd = [
        "python", "/app/inference_animals.py",
        "-s", source,
        "-d", driving,
        "--driving_multiplier", str(req.driving_multiplier),
        "--output_dir", str(job_out),
    ]
    if req.no_flag_stitching:
        cmd.append("--no_flag_stitching")
    
    try:
        p = subprocess.run(
            cmd,
            cwd="/app",
            capture_output=True,
            text=True,
            check=False,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to run inference: {e}")
    
    if p.returncode != 0:
        raise HTTPException(status_code=500, detail=f"Inference error: {p.stderr[-2000:]}")

    return AnimateResponse(
        ok=True,
        output_dir=str(job_out),
        stdout=p.stdout[-4000:],
        stderr=p.stderr[-4000:],
    )
