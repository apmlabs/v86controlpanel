# Amazon Q - v86 Control Panel Context

**Last Updated**: 2026-02-23T09:53:00Z
**Working Directory**: `/home/ubuntu/mcpprojects/v86controlpanel/`
**Status**: 🔲 Research & Setup

## Project: v86 Control Panel

Browser-based x86 VM control panel powered by v86 — boot OS images, run Doom, manage projects via SSH.

## Current Phase: Research & Setup

### What Works
- ✅ GitHub repo created: `github.com/apmlabs/v86controlpanel` (public)
- ✅ AGENTS.md created with full v86 API docs, architecture, lessons from other projects
- ✅ AmazonQ.md created (this file)
- ✅ README.md created

### What's Next
1. `npm init` + `npm install v86`
2. Create index.html with basic v86 embed (boot FreeDOS)
3. Add control panel UI (start/stop/reset buttons)
4. Add serial console (xterm.js)
5. Boot Alpine Linux with terminal
6. Add Doom on FreeDOS
7. State save/restore via IndexedDB
8. Networking (fetch backend)

### Known Constraints
- v86 is 32-bit x86 only (no 64-bit)
- Disk images are large (gitignored)
- BIOS files needed (seabios.bin, vgabios.bin)
- WASM file must be served as static asset for bundlers

---

## Session 1 - February 23, 2026

### Summary
Project initialization. Researched v86 thoroughly, created repo and context files.

### Research Completed
- v86 GitHub repo (copy/v86): 22k+ stars, BSD license, active development
- Full API documented from v86.d.ts TypeScript definitions
- Networking docs: fetch, inbrowser, wsproxy, wisp backends
- npm package: `npm install v86` (official, published from master)
- Compatible OS images: FreeDOS, Alpine, Buildroot, Arch32, Win98, KolibriOS
- Examples studied: basic.html, serial.html, save_restore.html, tcp_terminal.html
- Related projects: WebTerm (v86 + xterm.js), v86react, editor-v86

### Decisions Made
1. **Static HTML approach** (no framework) — matches webwars/wazetracker pattern
2. **npm package for v86** — easier than building from source
3. **AGENTS.md + AmazonQ.md committed to git** (not gitignored like webwars)
4. **FreeDOS for Doom** — known working, tiny, instant boot
5. **Alpine Linux for terminal** — minimal, good serial console support
6. **fetch backend for networking** — no proxy server needed for basic HTTP

### Files Created
- `AGENTS.md` — Full architecture, v86 API, lessons from other projects
- `AmazonQ.md` — This session log
- `README.md` — User-facing docs
- `.gitignore` — Ignore images, states, node_modules, build artifacts

### Key v86 API Findings
- Constructor takes bios, vga_bios, disk images, screen_container, serial_console
- `serial_console: { type: "xtermjs", container: el }` for xterm.js integration
- `net_device: { type: "virtio", relay_url: "fetch" }` for HTTP networking
- `save_state()` / `restore_state()` for instant boot snapshots
- `initial_state: { url: "state.bin.zst" }` for pre-saved states
- `filesystem: {}` for 9p file sharing with guest
- Events: emulator-ready, emulator-started, emulator-stopped, serial0-output-byte
