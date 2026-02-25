# Agent Status Tracking - v86 Control Panel

## 🎯 PROJECT GOAL

**Browser-based x86 VM control panel** — boot OS images, play DOS games, manage projects via SSH, all from a single web UI. Mix of client-side v86 emulation, js-dos for DOS games, and server-side Chromium via noVNC.

---

## 📚 DOCUMENTATION STRUCTURE

### Core Files (NEVER DELETE, COMMITTED TO GIT)
- **AGENTS.md** (this file) - Permanent knowledge, architecture, lessons learned
- **AmazonQ.md** - Current status, session history, progress tracking
- **README.md** - User-facing quick start guide

---

## ⚠️ AGENT RULES

1. **Always update AGENTS.md and AmazonQ.md** after significant changes, then push to GitHub
2. **When user says "remember"** — write that info into AGENTS.md
3. **Never use sed to edit files** — read files fully with cat/fs_read, then write with fs_write
4. **Read files before editing** — always read the full file first, plan changes, then write
5. **Step back and plan** before making changes — don't rush into edits
6. **Push to GitHub** after updating context files
7. **Never use curl -s (silent)** — always show download progress
8. **Never pipe and wait** — show output to user

---

## Current Status
Last updated: 2026-02-25T18:38:00Z

### Project Status
- **Phase**: Modernized 6-profile panel + js-dos games + Chromium
- **Last Action**: Full profile modernization — Alpine 3.23, TinyCore 17, 9front, js-dos with 10 games
- **Current Blocker**: None
- **Target**: SSH project manager, multi-VM dashboard

### Implementation Tracks
| Track | Component | Status | Next Action |
|-------|-----------|--------|-------------|
| A | Repo & Context Files | ✅ COMPLETE | AGENTS.md, AmazonQ.md, README.md |
| B | v86 Integration | ✅ COMPLETE | v86 npm package, multiple OS profiles |
| C | Control Panel UI | ✅ COMPLETE | 6 profiles, start/stop/save/restore/fullscreen |
| D | nginx + Landing Page | ✅ COMPLETE | /v86/ route, /novnc/ route, Control Center at / |
| E | js-dos Games | ✅ COMPLETE | 10 DOS games, locally hosted bundles |
| F | Serial Terminal | ✅ COMPLETE | xterm.js via v86 serial_container_xtermjs for Alpine |
| G | Project Manager | 🔲 TODO | SSH into dev server, manage projects |
| H | State Persistence | ✅ COMPLETE | Server-side Flask API, gzip compressed, cross-browser |
| I | Networking | ✅ COMPLETE | fetch backend for Alpine, TinyCore |
| J | Chromium noVNC | ✅ COMPLETE | Real Chromium via Xvfb + x11vnc + websockify + noVNC |
| K | OS Modernization | ✅ COMPLETE | Alpine 3.23, TinyCore 17, 9front Jan 2026 |
| L | Mouse Lock | ✅ COMPLETE | Click VGA screen to lock mouse for graphical OSes |

### Infrastructure
- **Public IP**: 54.80.204.92
- **Landing page**: https://54.80.204.92/ (Control Center with all project cards)
- **v86 panel**: https://54.80.204.92/v86/
- **noVNC**: https://54.80.204.92/novnc/ (Chromium remote desktop)
- **Auth**: basic auth (same as all other projects)
- **Services**:
  - `v86panel` — Flask server on port 8087 (static files + state API)
  - `chromium-vnc` — Xvfb + x11vnc + Chromium + websockify on ports 5900/6080
- **nginx**: `/etc/nginx/sites-available/dev-proxy` — v86panel + novnc upstreams

---

## 🏗️ ARCHITECTURE

### v86 Engine (copy/v86)
- **Repo**: https://github.com/copy/v86 (22k+ stars, BSD license)
- **npm**: `npm install v86`
- **What it does**: x86 PC emulator + JIT compiler (x86 → WebAssembly at runtime)
- **Emulated hardware**: CPU (~Pentium 4 + SSE3), FPU, VGA/SVGA, PS/2 keyboard/mouse, PIT, PIC, APIC, RTC, PCI, IDE, floppy, NE2000 NIC, virtio (fs/net/balloon), SoundBlaster 16
- **Limitations**: 32-bit x86 only, no 64-bit, no multicore, emulation speed (not native)

### js-dos (DOS Games)
- **Repo**: https://github.com/caiiiycuk/js-dos (MIT license)
- **What it does**: DOSBox compiled to WebAssembly, runs DOS games in browser
- **CDN**: `https://v8.js-dos.com/latest/js-dos.js` + `js-dos.css`
- **API**: `Dos(element, { url: "path/to/game.jsdos" })`
- **Bundles**: .jsdos files = ZIP archives containing game files + dosbox.conf
- **Bundle sources**: cdn.dos.zone/custom/dos/ (1900+ games), v8.js-dos.com/bundles/
- **CORS issue**: cdn.dos.zone blocks cross-origin requests — must host bundles locally
- **Architecture**: DOSBox→WASM in Web Worker, renders to canvas, sound via Web Audio API

### Chromium noVNC Stack
```
User browser → nginx (/novnc/) → websockify (ws→vnc) → x11vnc → Xvfb :99 → Chromium 145
```

### Server (server.py — Flask)
- Serves static files (index.html, images, jsdos, bios, node_modules)
- State API: GET/PUT/DELETE /api/states/<profile>
- States stored in `states/` directory, gzip compressed
- Max upload: 500MB (nginx `client_max_body_size 500m`)

### OS Profiles (Current — 6 profiles)
| Profile | Tech | Image | Size | Display | Notes |
|---------|------|-------|------|---------|-------|
| 🐧 Alpine 3.23 | v86 | bzimage+initrd+iso | 66MB | xterm.js serial | Kernel 6.18.7, login root (no pw) |
| 🐧 TinyCore 17 | v86 | tinycore.iso | 25MB | VGA | Kernel 6.18, GUI Linux, fetch net |
| 💎 KolibriOS | v86 | kolibri.img | 1.5MB | VGA | ASM OS, instant boot, click to lock mouse |
| 🎮 js-dos | DOSBox→WASM | .jsdos bundles | varies | js-dos player | 10 games, locally hosted |
| 🔷 9front | v86 | 9front.iso | 460MB | VGA | Plan 9 fork, Jan 2026, async load, ACPI |
| 🌐 Chromium | noVNC | N/A | N/A | noVNC iframe | Real Chromium 145 on server |

### js-dos Game Bundles (locally hosted in jsdos/)
| Game | File | Size |
|------|------|------|
| Doom | doom.jsdos | 5.4MB |
| Doom II | doom2.jsdos | 6.7MB |
| Command & Conquer | cnc.jsdos | 68MB |
| Prince of Persia | prince.jsdos | 362KB |
| WarCraft | warcraft.jsdos | 5.3MB |
| Lemmings | lemmings.jsdos | 2.1MB |
| Heretic | heretic.jsdos | 11MB |
| GTA | gta.jsdos | 31MB |
| Need for Speed | nfs.jsdos | 46MB |
| Digger | digger.jsdos | 27KB |

### Project Structure
```
v86controlpanel/
├── AGENTS.md              # Agent context (committed)
├── AmazonQ.md             # Session history (committed)
├── README.md              # User docs
├── .gitignore
├── index.html             # Main control panel UI (6 profiles)
├── server.py              # Flask server (static files + state API)
├── chromium-vnc.sh        # Launcher for Chromium noVNC stack
├── package.json           # npm deps (v86)
├── states/                # Saved VM states (gitignored)
├── bios/                  # SeaBIOS + VGA BIOS (gitignored)
│   ├── seabios.bin
│   └── vgabios.bin
├── jsdos/                 # DOS game bundles (gitignored)
│   ├── doom.jsdos
│   ├── doom2.jsdos
│   ├── cnc.jsdos
│   ├── prince.jsdos
│   ├── warcraft.jsdos
│   ├── lemmings.jsdos
│   ├── heretic.jsdos
│   ├── gta.jsdos
│   ├── nfs.jsdos
│   └── digger.jsdos
└── images/                # OS disk images (gitignored)
    ├── alpine.iso         # 51MB Alpine 3.23 virt ISO (boot media for modloop)
    ├── alpine-bzimage     # 7.6MB Alpine 3.23 kernel (6.18.7-0-virt)
    ├── alpine-initrd      # 7.4MB Alpine 3.23 initramfs
    ├── tinycore.iso       # 25MB TinyCore 17 (kernel 6.18)
    ├── kolibri.img        # 1.5MB KolibriOS floppy
    └── 9front.iso         # 460MB 9front Jan 2026 release (386)
```

---

## 🧠 LESSONS LEARNED

### From this project
- v86 npm package works out of the box — just need bios files + disk images
- BIOS files: `https://github.com/copy/v86/raw/master/bios/`
- Screen container needs exact HTML structure (div + canvas)
- `serial_container_xtermjs` — pass DOM element, v86 creates Terminal internally
- Alpine: boot via bzimage+initrd, needs ISO as cdrom for modloop
- Alpine 3.23 initrd requires boot media (ISO) to find modloop — without it drops to emergency shell
- **9front ISO**: 460MB, use `async: true` + `acpi: true`, 128MB RAM, load as hda not cdrom
- **9front download**: 9front.org is slow but works; only9fans.com mirror has stale nightly numbers
- **js-dos v8 API**: `Dos(element, { url: "bundle.jsdos" })` — simplest integration
- **js-dos CDN URLs**: `https://v8.js-dos.com/latest/js-dos.js` + `js-dos.css`
- **js-dos bundles**: .jsdos = ZIP with game files + .jsdos/dosbox.conf
- **cdn.dos.zone CORS**: Blocks cross-origin requests — must download bundles and serve locally
- **dos.zone iframe CSP**: frame-ancestors blocks embedding — can't use iframe approach
- **Bundle URL pattern**: `cdn.dos.zone/custom/dos/{game}.jsdos` — not all games available
- **C&C bundle**: Found via scraping dos.zone page source: `cc_gdi_novid.jsdos`
- **xterm.js width issue**: xterm renders at fixed column width, doesn't auto-resize; CSS fix with `width: 100% !important` on `.xterm`, `.xterm-screen`, `.xterm-viewport`
- **Mouse lock for graphical OSes**: `emulator.lock_mouse()` on screen click, Esc to release
- **curl -s hides errors** — never use silent mode, always show progress
- **mv -f needed** for read-only files in non-interactive shell
- Chromium in v86 is impossible (32-bit, single-core, too slow) — use noVNC + real Chromium
- Flask replaces python http.server when you need API endpoints
- nginx `client_max_body_size` needed for large uploads (VM states)
- **Never use sed to edit config files** — read fully, write cleanly
- **Frontend API paths must be relative** when behind nginx reverse proxy at subpath

### From other projects
- Single-page frontends (HTML + JS) work great for dashboards
- systemd services for production deployment
- nginx reverse proxy pattern: upstream + location + proxy_pass
- AGENTS.md + AmazonQ.md pattern essential for agent continuity

---

## 🔧 TECHNICAL NOTES

### systemd Services
```
# v86 Control Panel (Flask)
/etc/systemd/system/v86panel.service
WorkingDirectory=/home/ubuntu/mcpprojects/v86controlpanel
ExecStart=/usr/bin/python3 server.py
Port: 8087

# Chromium noVNC
/etc/systemd/system/chromium-vnc.service
ExecStart=/home/ubuntu/mcpprojects/v86controlpanel/chromium-vnc.sh
Ports: 5900 (VNC), 6080 (websockify)
```

### nginx Config
- Upstream: `v86panel` → `127.0.0.1:8087`, `novnc` → `127.0.0.1:6080`
- Location: `/v86/` → `proxy_pass http://v86panel/` (client_max_body_size 500m)
- Location: `/novnc/` → `proxy_pass http://novnc/`
- Location: `/novnc/websockify` → WebSocket upgrade
- Config file: `/etc/nginx/sites-available/dev-proxy`

### Image Sources
```bash
# Alpine 3.23
curl -sL -o images/alpine.iso "https://dl-cdn.alpinelinux.org/alpine/v3.23/releases/x86/alpine-virt-3.23.3-x86.iso"
# Extract kernel/initrd: mount ISO, copy boot/vmlinuz-virt + boot/initramfs-virt

# TinyCore 17
curl -sL -o images/tinycore.iso "http://tinycorelinux.net/17.x/x86/release/TinyCore-current.iso"

# KolibriOS
curl -sL -o images/kolibri.img "https://i.copy.sh/kolibri.img"

# 9front (Jan 2026 release, 386)
curl -L -o images/9front.iso.gz "http://9front.org/iso/9front-11554.386.iso.gz" && gunzip images/9front.iso.gz

# js-dos bundles
curl -sL -o jsdos/doom.jsdos "https://cdn.dos.zone/custom/dos/doom.jsdos"
curl -sL -o jsdos/cnc.jsdos "https://cdn.dos.zone/custom/dos/cc_gdi_novid.jsdos"
# etc.
```
