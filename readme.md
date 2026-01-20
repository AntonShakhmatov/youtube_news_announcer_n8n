## WorkFlow:

## 🗺 Content Factory Map (n8n)

### 1. News Sources (Input)

```
[Local Sources]        [Foreign Sources]
     |                       |
     |                       |
HTTP API / Telegram   HTTP API / Telegram
     |                       |
     +----------+------------+
                |
```

---

### 2. Trigger Layer (n8n)

```
[Webhook / Telegram Trigger]
            |
            v
      [Source Router]
      (local / foreign)
```

---

### 3. Normalization & Quality Control

```
[Normalize News]
  - text cleanup
  - language detection
  - format standardization
        |
        v
[Deduplicate]
  - hash
  - storage (Redis / DB)
        |
        v
[Filter]
  - length
  - relevance
  - absurdity score
```

---

### 4. AI Script Engine (Core)

```
[Persona Selector]
  - local persona
  - foreign persona
        |
        v
[LLM Script Generator]
  (satirical monologue
   30–45 seconds)
```

---

### 5. Virtual Anchor Generation

```
[Voice / Avatar Router]
        |
        +--> [TTS]
        |      - ElevenLabs
        |      - OpenAI TTS
        |
        +--> [Video Avatar]
               - D-ID
               - HeyGen
```

---

### 6. Final Content Assembly

```
[Audio / Video Output]
        |
        v
[Post-processing]
 - cover / thumbnail
 - subtitles
 - formatting
```

---

### 7. Publishing & Distribution

```
[Scheduler]
        |
        v
[Distribution]
 - Telegram
 - YouTube Shorts
 - TikTok
 - Instagram Reels
```

---

### 8. Feedback Loop (Optional)

```
[Metrics]
 - views
 - engagement
        |
        v
[AI Optimization]
 - persona tuning
 - topic filtering
```

---

### 🎭 Personas (Examples)

* Local → “Tired regional journalist”
* Foreign → “Cynical international analyst”

---

### 🧠 Key Principle

> **One LLM = one finished script**
> No LLM → LLM → LLM chains

---

If you want, I can convert this map into **Mermaid / draw.io / PNG**, or break down **a single n8n workflow node by node**.
