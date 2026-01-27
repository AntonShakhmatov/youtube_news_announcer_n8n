## instalation of piper-tts: 
* pip install -U piper-tts

## Posibly installation of venv to the project:
*  sudo apt update
*  sudo apt install -y python3-full python3-venv

*  python3 -m venv .venv
*  source .venv/bin/activate

## connectint two containers to one net(important):
* sudo docker network connect youtube_announcer_default n8n


## Start a temporary Cloudflare tunnel:

```bash
cloudflared tunnel --url http://localhost:5678
```