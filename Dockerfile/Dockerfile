# stage: downloading static ffmpeg
FROM alpine:3.19 AS ffmpeg
RUN apk add --no-cache curl tar xz
RUN curl -L -o /tmp/ffmpeg.tar.xz https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz \
  && mkdir -p /opt/ffmpeg \
  && tar -xJf /tmp/ffmpeg.tar.xz -C /opt/ffmpeg --strip-components=1 \
  && chmod +x /opt/ffmpeg/ffmpeg /opt/ffmpeg/ffprobe

# stage: n8n
FROM docker.n8n.io/n8nio/n8n:2.4.6
USER root
COPY --from=ffmpeg /opt/ffmpeg/ffmpeg /usr/local/bin/ffmpeg
COPY --from=ffmpeg /opt/ffmpeg/ffprobe /usr/local/bin/ffprobe
USER node