# Agent Status Tracking - v86 Control Panel

## 🎯 PROJECT GOAL

**Browser-based x86 VM control panel** — boot OS images, run Doom, manage projects via SSH, all from a single web UI. Mix of client-side v86 emulation and server-side Chromium via noVNC.

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

---

## Current Status
Last updated: 2026-02-23T18:30:00Z

### Project Status
- **Phase**: Full control panel with 7 OS profiles + Chromium browser + DOOM WORKING
- **Last Action**: Fixed Doom — geometry, BPB, preloading all resolved
- **Current Blocker**: None — Ctrl key (shoot) intercepted by browser in Doom
- **Target**: SSH project manager, multi-VM dashboard

### Implementation Tracks
| Track | Component | Status | Next Action |
|-------|-----------|--------|-------------|
| A | Repo & Context Files | ✅ COMPLETE | AGENTS.md, AmazonQ.md, README.md |
| B | v86 Integration | ✅ COMPLETE | v86 npm package, multiple OS profiles |
| C | Control Panel UI | ✅ COMPLETE | 7 profiles, start/stop/save/restore/fullscreen |
| D | nginx + Landing Page | ✅ COMPLETE | /v86/ route, /novnc/ route, Control Center at / |
| E | Doom on FreeDOS | ✅ COMPLETE | Boots, runs, plays — Ctrl (shoot) intercepted by browser |
| F | Serial Terminal | ✅ COMPLETE | xterm.js via v86 serial_container_xtermjs for Alpine |
| G | Project Manager | 🔲 TODO | SSH into dev server, manage projects |
| H | State Persistence | ✅ COMPLETE | Server-side Flask API, gzip compressed, cross-browser |
| I | Networking | ✅ COMPLETE | fetch backend for Alpine, DSL, TinyCore |
| J | Chromium noVNC | ✅ COMPLETE | Real Chromium via Xvfb + x11vnc + websockify + noVNC |
| K | Graphical OSes | ✅ COMPLETE | DSL, TinyCore, KolibriOS profiles added |

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

### Chromium noVNC Stack
```
User browser → nginx (/novnc/) → websockify (ws→vnc) → x11vnc → Xvfb :99 → Chromium 145
```
- **Xvfb**: Virtual framebuffer at 1280x720x24
- **x11vnc**: VNC server on localhost:5900
- **websockify**: WebSocket-to-VNC bridge on port 6080, serves noVNC static files
- **Chromium**: Real browser with full modern JS support
- **systemd**: `chromium-vnc.service` with respawn loop for Chromium

### Server (server.py — Flask)
- Serves static files (index.html, images, bios, node_modules)
- State API:
  - `GET /api/states` — list all saved states with sizes
  - `GET /api/states/<profile>` — download state (gzip compressed)
  - `PUT /api/states/<profile>` — upload state (raw → gzip on server)
  - `DELETE /api/states/<profile>` — delete state
- States stored in `states/` directory, gzip compressed
- Max upload: 500MB (nginx `client_max_body_size 500m`)

### v86 API (key methods)
```javascript
const emulator = new V86({
    wasm_path: "build/v86.wasm",
    bios: { url: "bios/seabios.bin" },
    vga_bios: { url: "bios/vgabios.bin" },
    screen_container: document.getElementById("screen"),
    memory_size: 64 * 1024 * 1024,
    vga_memory_size: 8 * 1024 * 1024,
    autostart: true,
    // Disk options:
    cdrom: { url: "images/linux.iso" },
    hda: { url: "images/disk.img", async: true, size: SIZE_BYTES },
    fda: { url: "images/floppy.img" },
    bzimage: { url: "images/bzImage" },
    initrd: { url: "images/rootfs.cpio" },
    cmdline: "console=ttyS0 quiet",
    // Serial console (v86 creates xterm.js internally):
    serial_container_xtermjs: document.getElementById("terminal-el"),
    // Networking:
    net_device: { type: "virtio", relay_url: "fetch" },
});

// Control: run(), stop(), restart(), destroy()
// State: save_state() → ArrayBuffer, restore_state(buf)
// Serial: serial0_send("cmd\n"), add_listener("serial0-output-byte", fn)
// Screen: screen_go_fullscreen()
```

### OS Profiles
| Profile | Image | Size | Display | Networking | Notes |
|---------|-------|------|---------|------------|-------|
| 💀 Doom | doom_boot.img + doom.img | 720KB + 16MB | VGA | None | FreeDOS boot floppy + HD |
| 🖥️ FreeDOS | freedos722.img | 720KB | VGA | None | Plain DOS |
| 🐧 Alpine | alpine-bzimage + alpine-initrd | 13MB | xterm.js serial | fetch | `console=ttyS0`, login as root |
| 🖼️ DSL | dsl.iso | 50MB | VGA | fetch | X11 + Fluxbox, Dillo/Firefox |
| 🐧 TinyCore | tinycore.iso | 24MB | VGA | fetch | X11 + FLWM |
| 💎 KolibriOS | kolibri.img | 1.4MB | VGA | None | Native GUI, built-in browser |
| 🌐 Chromium | noVNC iframe | N/A | noVNC | Native | Real Chromium 145 on server |

### Networking Backends
| Backend | URL | What it does | Proxy needed? |
|---------|-----|-------------|---------------|
| **fetch** | `fetch` | HTTP via browser fetch() API | No |
| **inbrowser** | `inbrowser` | VM-to-VM in same browser | No |
| **wsproxy** | `wss://host/` | Raw ethernet over WebSocket | Yes |
| **wisp** | `wisps://host/` | TCP/UDP over WISP protocol | Yes |

fetch backend = HTTP only (wget/curl work, SSH/ping don't).

### Project Structure
```
v86controlpanel/
├── AGENTS.md              # Agent context (committed)
├── AmazonQ.md             # Session history (committed)
├── README.md              # User docs
├── .gitignore
├── index.html             # Main control panel UI (7 profiles)
├── server.py              # Flask server (static files + state API)
├── chromium-vnc.sh        # Launcher for Chromium noVNC stack
├── package.json           # npm deps (v86)
├── states/                # Saved VM states (gitignored, server-side)
├── bios/                  # SeaBIOS + VGA BIOS (gitignored)
│   ├── seabios.bin        # 128KB
│   └── vgabios.bin        # 36KB
└── images/                # OS disk images (gitignored)
    ├── freedos722.img     # 720KB FreeDOS floppy
    ├── doom.img           # 16MB FreeDOS HD (MBR + FAT16, sector 63 start)
    ├── doom_boot.img      # 720KB FreeDOS boot floppy (AUTOEXEC→C:\DOOM\DOOM.EXE)
    ├── linux.iso          # 6.3MB Buildroot Linux
    ├── alpine.iso         # 46MB Alpine Linux ISO (source)
    ├── alpine-bzimage     # 6.3MB Alpine kernel (from ISO)
    ├── alpine-initrd      # 6.7MB Alpine initramfs (from ISO)
    ├── dsl.iso            # 50MB Damn Small Linux
    ├── tinycore.iso       # 24MB Tiny Core Linux
    └── kolibri.img        # 1.4MB KolibriOS floppy
```

---

## 🎮 FEATURE PLANS

### 1. Doom on FreeDOS ✅ WORKING
- Boot FreeDOS floppy, HD as C: with DOOM.EXE + DOOM1.WAD
- AUTOEXEC.BAT: `C:\ → CD DOOM → DOOM.EXE -nomusic -nosfx`
- **HD image geometry must match v86 hardcoded 16 heads / 63 SPT**
- **BPB must have matching geometry + hidden sectors = partition offset**
- **Remove `async: true` from hda config** — preload image for fast disk I/O
- Save state after Doom loads for instant restart
- Only issue: Ctrl (shoot) intercepted by browser — use mouse click or fullscreen

### 2. Linux Terminal (Alpine)
- Boot via bzimage+initrd (not ISO — avoids ISOLINUX hang)
- `console=ttyS0` for serial output to xterm.js
- Login as `root` (no password), then:
  - `setup-interfaces -a` → DHCP via fetch backend
  - `apk add curl` → install tools

### 3. SSH Project Manager (TODO)
- From Alpine VM, SSH to dev server
- Or: use fetch backend to reach localhost services

### 4. Multi-VM Dashboard (TODO)
- Run multiple VMs simultaneously
- Tab-based UI

---

## 🧠 LESSONS LEARNED

### From this project
- v86 npm package works out of the box — just need bios files + disk images
- BIOS files: `https://github.com/copy/v86/raw/master/bios/`
- Demo images: `https://i.copy.sh/{freedos722.img,linux.iso,dsl-4.11.rc2.iso,kolibri.img}`
- Screen container needs exact HTML structure (div + canvas)
- `serial_container_xtermjs` — pass DOM element, v86 creates Terminal internally (needs `window.Terminal` from xterm.js CDN)
- Alpine: boot via bzimage+initrd, NOT ISO (ISOLINUX hangs in v86)
- **FreeDOS HD images MUST have MBR partition table** — raw FAT16 without partition table = "Invalid drive C:"
- **Partition must start at sector 63** (classic CHS) — sector 2048 (modern) causes "Error reading from drive C:"
- **v86 ide.js hardcodes geometry: 16 heads, 63 sectors/track** — image size must be exact multiple of cylinder size (16×63×512 = 516096 bytes)
- **MBR partition CHS values must match v86 geometry** — sfdisk writes wrong CHS with its own geometry assumption
- **FAT16 BPB must match v86 geometry** — use `mkfs.fat -h 63 -g 16/63` to set heads=16, SPT=63, hidden=63
- **Remove `async: true` for game disk images** — async = HTTP fetch per sector read = extremely slow; preload = instant RAM reads
- **Duplicate `const` declarations in same function scope** = entire `<script>` block fails silently
- Chromium in v86 is impossible (32-bit, single-core, too slow) — use noVNC + real Chromium instead
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

### Building Doom HD Image
```bash
# v86 hardcodes 16 heads, 63 SPT — image must match exactly
HEADS=16; SPT=63; CYLS=32
TOTAL=$((CYLS * HEADS * SPT))  # 32256 sectors = 16515072 bytes
dd if=/dev/zero of=doom_hd.img bs=512 count=$TOTAL

# Write MBR with python (sfdisk uses wrong geometry)
python3 -c "
import struct
with open('doom_hd.img','r+b') as f:
    h,sc,c = 1, 0x01, 0x00  # start CHS 0/1/1
    eh,esc,ec = 15, 0x3f, 0x1f  # end CHS 31/15/63
    f.seek(0x1BE)
    f.write(struct.pack('<BBBBBBBBII',0x80,h,sc,c,0x06,eh,esc,ec,63,32193))
    f.seek(0x1FE); f.write(b'\x55\xAA')
"

# Format with matching BPB geometry
LOOP=$(sudo losetup --find --show --offset 32256 --sizelimit $((32193*512)) doom_hd.img)
sudo mkfs.fat -F 16 -h 63 -g 16/63 -n DOOM $LOOP
sudo mount $LOOP /mnt/doom
# Copy KERNEL.SYS, COMMAND.COM from FreeDOS floppy
# Copy DOOM/DOOM.EXE, DOOM/DOOM1.WAD
# Create AUTOEXEC.BAT: C:\ / CD DOOM / DOOM.EXE -nomusic -nosfx
```

### Image Sources
```bash
curl -sL -o images/freedos722.img "https://i.copy.sh/freedos722.img"
curl -sL -o images/dsl.iso "https://i.copy.sh/dsl-4.11.rc2.iso"
curl -sL -o images/kolibri.img "https://i.copy.sh/kolibri.img"
curl -sL -o images/tinycore.iso "http://tinycorelinux.net/15.x/x86/release/TinyCore-current.iso"
curl -sL -o images/alpine.iso "https://dl-cdn.alpinelinux.org/alpine/v3.19/releases/x86/alpine-virt-3.19.1-x86.iso"
# Extract Alpine kernel/initrd: mount ISO, copy boot/vmlinuz-virt + boot/initramfs-virt
```
