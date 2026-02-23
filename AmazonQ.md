# Amazon Q - v86 Control Panel Context

**Last Updated**: 2026-02-23T18:30:00Z
**Working Directory**: `/home/ubuntu/mcpprojects/v86controlpanel/`
**Status**: ✅ Full control panel with 7 profiles + Chromium + server-side state + DOOM WORKING

## Project: v86 Control Panel

Browser-based x86 VM control panel powered by v86 — boot OS images, run Doom, manage projects via SSH.

## Current Phase: Full Control Panel + Chromium

### What Works
- ✅ 7 OS profiles: Doom, FreeDOS, Alpine, DSL, TinyCore, KolibriOS, Chromium
- ✅ Doom on FreeDOS: boot floppy + MBR-partitioned HD (sector 63 CHS), preloaded, plays!
- ✅ Alpine Linux: bzimage+initrd boot, xterm.js serial terminal
- ✅ DSL + TinyCore: graphical X11 desktops with fetch networking
- ✅ KolibriOS: native GUI with built-in browser
- ✅ Chromium 145: real browser via noVNC (Xvfb + x11vnc + websockify)
- ✅ Server-side state persistence: Flask API, gzip compressed, cross-browser
- ✅ systemd services: v86panel (Flask:8087), chromium-vnc (VNC:5900, WS:6080)
- ✅ nginx: /v86/ + /novnc/ routes with WebSocket upgrade

### What's Next
1. SSH project manager from Alpine VM
2. Multi-VM dashboard (tabs)

---

## Session 2 - February 23, 2026 (continued)

### Summary
Major expansion: 7 OS profiles, Chromium via noVNC, server-side state persistence, graphical OSes.

### Work Done
1. Fixed Doom boot: created doom_boot.img (stripped FreeDOS floppy + AUTOEXEC->C:\DOOM\DOOM.EXE)
2. Fixed Alpine: switched from ISO (ISOLINUX hang) to bzimage+initrd direct boot
3. Fixed serial terminal: v86 serial_container_xtermjs with console=ttyS0 kernel cmdline
4. Added graphical OS profiles: DSL (50MB), TinyCore (24MB), KolibriOS (1.4MB)
5. Added fetch networking to DSL and TinyCore
6. Built Chromium noVNC stack: Xvfb + x11vnc + Chromium 145 + websockify + noVNC
7. Replaced python http.server with Flask (server.py) for state API
8. Server-side state save/restore: PUT/GET /api/states/<profile>, gzip compressed
9. Rebuilt Doom HD image with MBR partition table, sector 63 start (CHS)

### Issues Fixed
- All JS broken: Duplicate const profile in same function scope - script fails silently
- Alpine ISOLINUX hang: Switched to bzimage+initrd
- Doom Invalid drive C: No partition table - rebuilt with MBR
- Doom Error reading from drive C: Sector 2048 start - rebuilt with sector 63
- Doom "suspect partition" + read errors: MBR CHS and BPB geometry didn't match v86's hardcoded 16H/63S
- Doom extremely slow init: async disk = HTTP per sector read; preload fixes it
- Flask crash: str_replace merged two lines - fixed newline

---

## Session 1 - February 23, 2026

### Summary
Full project setup from zero to working v86 in browser.

### Work Done
1. Created GitHub repo, context files, npm setup, BIOS + image downloads
2. Built index.html control panel with VGA canvas + log panel
3. systemd service, nginx config, Control Center landing page
4. Fixed: nginx root, git rebase, waze/reus API paths, webwars stale HTML
