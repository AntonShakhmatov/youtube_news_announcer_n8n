# YouTube Announcer (n8n workflow)

This repository contains an n8n workflow that listens to two Telegram channels, processes the content using AI, generates videos, and uploads them to YouTube.

---
### Demonstration:
![Application demo](images/workflow.gif)

### Result:
https://www.youtube.com/watch?v=tBjlZNHd-rI

## Workflow overview

### 1) Telegram triggers
There are **two Telegram Trigger** nodes (both listening to `channel_post`):

- `Telegram Trigger for ichine_novosti_ebta`
- `Telegram Trigger nashi_novosti_bled`

Both triggers start the same workflow logic, but the data is later routed to different branches.

### 2) Initial delay
After each trigger there is a `Wait` node.  
It is used to stabilize incoming data (anti-spam, ensure all data is written before further processing).

### 3) Data preparation and routing
Next nodes:

- `ichine_tables`
- `nashi_tables`

After that, data is passed to `Switch1 (mode: Rule)`, which selects the correct processing branch depending on the channel or defined rules.

### 4) AI processing (two parallel branches)
After `Switch1`, there are **two AI branches**:

- `AI Agent` (connected to `Google Gemini Chat Model` + `Postgres Chat Memory`)
- `AI Agent1` (connected to `Google Gemini Chat Model1` + `Postgres Chat Memory1`)

The AI prepares text, structure, and parameters for the future video and can use Postgres as a long-term memory.

### 5) Reading data from Postgres
In each branch, the next steps are:

- `Wait4` / `Wait5`
- `Select rows from a table` / `Select rows from a table1` (Postgres)

These nodes fetch the required rows (for example: templates, settings, queues, history, or configuration data).

### 6) External HTTP service call
Next:

- `Wait11` / `Wait8`
- `OHF_POST` / `OHF_POST1` (HTTP POST to a local service on port `:8000`)

This service usually performs heavy processing (asset preparation, TTS, prompt generation, pipeline assembly, etc.) and returns data or files for the next steps.

### 7) File system operations
After the HTTP call:

- `Read/Write Files from Disk`
- `Read/Write Files from Disk2`
- `Read/Write Files from Disk3`

These nodes handle reading and writing intermediate files (text, audio, JSON, images, video drafts).

### 8) Video generation (fal.ai)
Then:

- `Wait7` / `Wait9`
- `Generate a video` / `Generate a video2`

These steps are responsible for video generation, typically via **fal.ai**.

### 9) Final processing and shell commands
Next:

- `Execute Command2`
- `Execute Command3`

Shell commands are executed here (for example: ffmpeg merging, audio normalization, subtitles overlay, final video assembly).

### 10) Upload to YouTube
Final nodes:

- `Upload a video`
- `Upload a video1`

Each branch ends with uploading the generated video to YouTube.

### 11) Telegram message cleanup (optional)
The workflow also contains:

- `Delete a chat message`
- `Delete a chat message1`

These nodes are used to remove temporary or service messages in Telegram (usually after `Wait2` / `Wait3`) to keep the channel or chat clean.

---

## Installation of piper-tts
* `pip install -U piper-tts`

## Installation of fal-ai
* `npm install --save @fal-ai/client`

## Optional: virtual environment setup
```bash
sudo apt update
sudo apt install -y python3-full python3-venv

python3 -m venv .venv
source .venv/bin/activate

Connecting two containers to the same network (important)
sudo docker network connect youtube_announcer_default n8n

Start a temporary Cloudflare tunnel
cloudflared tunnel --url http://localhost:5678

sudo docker network create stack_net

Liveportrait Node Execute Command:
* python inference_animals.py \
    -s ../n8n-data/tmp/avatar/avatar.jpg \
    -d assets/examples/driving/wink.pkl \
    --driving_multiplier 1.75 \
    --no_flag_stitching

## Working principle

1. A news message is sent to the Telegram bot.
2. The message is saved to the database.
3. The original message is deleted from the Telegram bot to keep the chat clean.
4. Data from the database is processed by AI, which creates satirical content based on the news.
5. The generated text is sent via an HTTP request to a service that produces a WAV audio file (TTS).
6. An avatar (video or image sequence) is generated.
7. `ffmpeg` merges the generated audio and video files into a single video.
8. **Result:** a cute cat avatar reads the news aloud 🎥🐱