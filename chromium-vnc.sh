#!/bin/bash
export DISPLAY=:99

# Start Xvfb
Xvfb :99 -screen 0 1280x720x24 &
sleep 1

# Start x11vnc
x11vnc -display :99 -nopw -listen 127.0.0.1 -forever -shared -rfbport 5900 -noxdamage &
sleep 1

# Start Chromium (respawn if it dies)
while true; do
    chromium-browser --no-sandbox --disable-gpu --disable-software-rasterizer \
      --no-first-run --start-maximized --disable-dev-shm-usage \
      "https://google.com" 2>/dev/null
    sleep 2
done &

# websockify in foreground (keeps service alive)
exec websockify --web /usr/share/novnc 6080 127.0.0.1:5900
