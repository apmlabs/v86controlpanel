# Agent Status Tracking - v86 Control Panel

## 🎯 PROJECT GOAL

**Browser-based x86 VM control panel** — boot OS images, run Doom, manage projects via SSH, all from a single web UI. Zero server-side compute; everything runs client-side using v86 (x86-to-WASM JIT emulator).

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
Last updated: 2026-02-23T10:08:00Z

### Project Status
- **Phase**: Basic v86 working, control panel UI live
- **Last Action**: FreeDOS boots, Linux boots, nginx landing page fixed
- **Current Blocker**: None
- **Target**: Working v86 control panel with Doom + SSH + project management

### Implementation Tracks
| Track | Component | Status | Next Action |
|-------|-----------|--------|-------------|
| A | Repo & Context Files | ✅ COMPLETE | AGENTS.md, AmazonQ.md, README.md |
| B | v86 Integration | ✅ COMPLETE | v86 npm package, FreeDOS + Linux boot working |
| C | Control Panel UI | ✅ BASIC | Start/stop/reset/save/restore, VGA canvas, log panel |
| D | nginx + Landing Page | ✅ COMPLETE | /v86/ route, Control Center landing page at / |
| E | Doom on FreeDOS | 🔲 TODO | FreeDOS image + DOOM.WAD, boot & play |
| F | SSH / Terminal | 🔲 TODO | Alpine Linux image + xterm.js serial console |
| G | Project Manager | 🔲 TODO | SSH into dev server, manage projects |
| H | State Persistence | 🔲 TODO | Save/restore VM state via IndexedDB |
| I | Networking | 🔲 TODO | fetch backend for HTTP, wisp for TCP |

### Infrastructure
- **Public IP**: 54.80.204.92
- **Landing page**: https://54.80.204.92/ (Control Center with all project cards)
- **v86 panel**: https://54.80.204.92/v86/
- **Auth**: basic auth (same as all other projects)
- **Dev server**: systemd service `v86panel` on port 8087
- **nginx**: `/etc/nginx/sites-available/dev-proxy` — v86panel upstream added

---

## 🏗️ ARCHITECTURE

### v86 Engine (copy/v86)
- **Repo**: https://github.com/copy/v86 (22k+ stars, BSD license)
- **npm**: `npm install v86`
- **What it does**: x86 PC emulator + JIT compiler (x86 → WebAssembly at runtime)
- **Emulated hardware**: CPU (~Pentium 4 + SSE3), FPU, VGA/SVGA, PS/2 keyboard/mouse, PIT, PIC, APIC, RTC, PCI, IDE, floppy, NE2000 NIC, virtio (fs/net/balloon), SoundBlaster 16
- **Limitations**: 32-bit x86 only, no 64-bit, no multicore, emulation speed (not native)

### v86 API (key methods)
```javascript
const emulator = new V86({
    wasm_path: "build/v86.wasm",
    bios: { url: "bios/seabios.bin" },
    vga_bios: { url: "bios/vgabios.bin" },
    screen_container: document.getElementById("screen"),
    memory_size: 64 * 1024 * 1024,  // 64MB default
    vga_memory_size: 8 * 1024 * 1024,
    autostart: true,
    // Disk options (pick one or more):
    cdrom: { url: "images/linux.iso" },
    hda: { url: "images/disk.img", async: true, size: SIZE_BYTES },
    fda: { url: "images/floppy.img" },
    bzimage: { url: "images/bzImage" },
    initrd: { url: "images/rootfs.cpio" },
    // Serial console:
    serial_console: { type: "xtermjs", container: el },
    // Networking:
    net_device: { type: "virtio", relay_url: "fetch" },
    // 9p filesystem (share files with guest):
    filesystem: { baseurl: "path/", basefs: "fs.json" },
    // State restore (instant boot from snapshot):
    initial_state: { url: "state.bin.zst" },
});

// Control
emulator.run();
emulator.stop();
emulator.restart();
emulator.destroy();
emulator.is_running();

// State save/restore
const state = await emulator.save_state();  // → ArrayBuffer
await emulator.restore_state(state);

// Serial I/O
emulator.serial0_send("ls -la\n");
emulator.add_listener("serial0-output-byte", (byte) => { ... });

// Keyboard
emulator.keyboard_send_text("hello");
emulator.keyboard_send_scancodes([0x1C]); // Enter

// Screen
emulator.screen_make_screenshot();
emulator.screen_set_scale(2, 2);
emulator.screen_go_fullscreen();

// 9p filesystem
await emulator.create_file("/tmp/test.txt", new Uint8Array([...]));
const data = await emulator.read_file("/tmp/test.txt");

// Disk swap at runtime
await emulator.set_cdrom({ url: "new.iso" });
emulator.eject_cdrom();

// Events
emulator.add_listener("emulator-ready", () => { ... });
emulator.add_listener("emulator-started", () => { ... });
emulator.add_listener("emulator-stopped", () => { ... });
emulator.add_listener("download-error", (e) => { ... });
emulator.add_listener("download-progress", (e) => { ... });
```

### Networking Backends
| Backend | URL | What it does | Proxy needed? |
|---------|-----|-------------|---------------|
| **fetch** | `fetch` | HTTP via browser fetch() API | Optional CORS proxy |
| **inbrowser** | `inbrowser` | VM-to-VM in same browser (BroadcastChannel) | No |
| **wsproxy** | `wss://host/` | Raw ethernet over WebSocket | Yes (websockproxy) |
| **wisp** | `wisps://host/` | TCP/UDP over WISP protocol | Yes (wisp-js) |

fetch backend special: `http://<port>.external` → localhost:<port> on host.

### Compatible OS Images
From v86 demos (known working):
- **FreeDOS** — perfect for Doom, tiny, instant boot
- **Alpine Linux** — minimal Linux, good for SSH/terminal
- **Buildroot Linux** — custom minimal images (we use this: linux.iso 6.3MB)
- **Arch Linux 32** — fuller Linux experience
- **Windows 98/95** — retro computing
- **KolibriOS** — tiny graphical OS

### State Images (Instant Boot)
- Save VM state → compressed .bin.zst file
- Restore = instant boot (skip BIOS/kernel boot)
- Store in IndexedDB for persistence across page reloads
- Caveat: MAC address randomized on restore (need driver reload or preserve_mac_from_state_image)

### Screen Container HTML Structure
```html
<div id="screen_container">
    <div style="white-space: pre; font: 14px monospace; line-height: 14px"></div>
    <canvas style="display: none"></canvas>
</div>
```

### Project Structure
```
v86controlpanel/
├── AGENTS.md              # Agent context (committed)
├── AmazonQ.md             # Session history (committed)
├── README.md              # User docs
├── .gitignore
├── index.html             # Main control panel UI
├── package.json           # npm deps (v86)
├── bios/                  # SeaBIOS + VGA BIOS (gitignored, downloaded)
│   ├── seabios.bin        # 128KB from v86 repo
│   └── vgabios.bin        # 36KB from v86 repo
└── images/                # OS disk images (gitignored, downloaded)
    ├── freedos722.img     # 720KB FreeDOS floppy
    └── linux.iso          # 6.3MB Buildroot Linux
```

---

## 🎮 FEATURE PLANS

### 1. Doom on FreeDOS
- Boot FreeDOS image in v86
- Include DOOM1.WAD (shareware, freely distributable)
- VGA canvas output, keyboard input
- Save state after Doom loads for instant restart

### 2. Linux Terminal (Alpine)
- Boot Alpine Linux with serial console
- xterm.js terminal in control panel
- Package manager (apk), basic tools
- 9p filesystem to share files with browser

### 3. SSH Project Manager
- From Alpine VM, SSH to dev server
- Or: use fetch backend networking to reach localhost services
- Manage projects (webwars, wazetracker, etc.) from browser

### 4. Multi-VM Dashboard
- Run multiple VMs simultaneously (v86 supports this)
- Tab-based UI: switch between Doom, Linux terminal, etc.
- Each VM has its own state save/restore

---

## 🧠 LESSONS LEARNED

### From this project
- v86 npm package works out of the box — just need bios files + disk images
- BIOS files: download from `https://github.com/copy/v86/raw/master/bios/`
- Demo images: download from `https://i.copy.sh/{freedos722.img,linux.iso,...}`
- Screen container needs exact HTML structure (div + canvas)
- `emulator.destroy()` to fully clean up, but must also clear canvas manually
- nginx `location = /` with `root` doesn't serve index.html — use server-level `root` + `index` instead
- **Never use sed to edit config files** — read fully, write cleanly

### From webwars (Hedgewars WASM port)
- Emscripten/WASM builds need careful memory management
- Asset caching via nginx Cache-Control headers (7d for .wasm/.data, 1h for .js, no-cache for .html)
- Download progress bars essential for large files
- systemd services for production deployment
- Admin panel pattern: Flask + Leaflet for monitoring

### From wazetracker
- Single-file frontend (index.html) with Leaflet maps works great for dashboards
- SQLite for local persistence
- Simple Flask API backend

### From onyxpoker
- AGENTS.md + AmazonQ.md pattern is essential for agent continuity
- Git tags for milestones (v1.0-gold pattern)
- Client/server split with clear API boundaries

### Common Patterns Across All Projects
- **AGENTS.md**: Architecture, permanent knowledge, never delete
- **AmazonQ.md**: Session log, current status, progress tracking
- **README.md**: User-facing docs
- **.gitignore**: Keep build artifacts, large binaries, secrets out of git
- **Single-page frontends**: HTML + JS, no framework overhead for demos
- **Production**: nginx reverse proxy, HTTPS, systemd services

---

## 🔧 TECHNICAL NOTES

### v86 npm Package
```bash
npm install v86
```
Includes libv86.js + v86.wasm. Python http.server serves it fine for dev.

### BIOS Files Required
```bash
curl -sL -o bios/seabios.bin "https://github.com/copy/v86/raw/master/bios/seabios.bin"
curl -sL -o bios/vgabios.bin "https://github.com/copy/v86/raw/master/bios/vgabios.bin"
```

### Disk Image Sources
```bash
curl --compressed -sL -o images/freedos722.img "https://i.copy.sh/freedos722.img"
curl --compressed -sL -o images/linux.iso "https://i.copy.sh/linux.iso"
```

### systemd Service
```
/etc/systemd/system/v86panel.service
WorkingDirectory=/home/ubuntu/mcpprojects/v86controlpanel
ExecStart=/usr/bin/python3 -m http.server 8087
```

### nginx Config
- Upstream: `v86panel` → `127.0.0.1:8087`
- Location: `/v86/` → `proxy_pass http://v86panel/`
- Landing page: `/var/www/cc/index.html` served at `/`
- Config file: `/etc/nginx/sites-available/dev-proxy`

### IndexedDB for Persistence
- Store VM state snapshots (can be large, 50-200MB)
- Store writable disk overlay
- Use .zst compression (v86 has built-in zstd decompressor)

### Performance Tips
- Use `initial_state` for instant boot (skip BIOS/kernel)
- `fastboot: true` skips BIOS menu
- VirtIO devices faster than legacy emulation
- Memory: 64MB default, increase for heavier OSes
