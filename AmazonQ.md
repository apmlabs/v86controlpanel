# Amazon Q - v86 Control Panel Context

**Last Updated**: 2026-02-23T10:37:00Z
**Working Directory**: `/home/ubuntu/mcpprojects/v86controlpanel/`
**Status**: ✅ Basic v86 working, control panel live

## Project: v86 Control Panel

Browser-based x86 VM control panel powered by v86 — boot OS images, run Doom, manage projects via SSH.

## Current Phase: Basic Control Panel Working

### What Works
- ✅ GitHub repo created: `github.com/apmlabs/v86controlpanel` (public)
- ✅ AGENTS.md, AmazonQ.md, README.md committed (not gitignored)
- ✅ v86 npm package installed, BIOS files downloaded
- ✅ FreeDOS boots in browser (720KB floppy image)
- ✅ Buildroot Linux boots in browser (6.3MB ISO)
- ✅ Control panel UI: start/stop/restart/save/restore/fullscreen
- ✅ Log panel for troubleshooting (download errors, events)
- ✅ systemd service `v86panel` on port 8087
- ✅ nginx reverse proxy at `/v86/` with basic auth
- ✅ Landing page at `https://54.80.204.92/` — Control Center with all project cards
- ✅ Doom on FreeDOS: 16MB HD image with DOOM.EXE + DOOM1.WAD, auto-launches
- ✅ xterm.js serial console for Linux profile
- ✅ fetch networking backend for Linux (wget works)

### What's Next
1. Add Doom on FreeDOS
2. Add xterm.js serial console for Linux
3. State persistence via IndexedDB
4. Networking (fetch backend)

---

## Session 1 - February 23, 2026

### Summary
Full project setup from zero to working v86 in browser.

### Research Completed
- v86 GitHub repo (copy/v86): 22k+ stars, BSD license
- Full API from v86.d.ts TypeScript definitions
- Networking docs: fetch, inbrowser, wsproxy, wisp backends
- npm package: `npm install v86`
- Compatible OS images: FreeDOS, Alpine, Buildroot, Arch32, Win98, KolibriOS
- Examples: basic.html, serial.html, save_restore.html, tcp_terminal.html
- Related projects: WebTerm (v86 + xterm.js), v86react, editor-v86

### Work Done
1. Created GitHub repo `apmlabs/v86controlpanel` (public)
2. Created AGENTS.md, AmazonQ.md, README.md, .gitignore
3. `npm init` + `npm install v86`
4. Downloaded BIOS files (seabios.bin, vgabios.bin)
5. Downloaded FreeDOS floppy image (720KB)
6. Downloaded Buildroot Linux ISO (6.3MB)
7. Built index.html control panel with:
   - Profile selector (FreeDOS / Linux)
   - Start/stop/restart/save/restore/fullscreen buttons
   - VGA canvas screen
   - Log panel with color-coded events
8. Created systemd service `v86panel` on port 8087
9. Added v86panel upstream to nginx config
10. Created Control Center landing page at `/var/www/cc/index.html`
11. Fixed nginx root page (moved `root`/`index` to server level)

### Issues Fixed
- **Linux black screen**: Missing linux.iso — downloaded from i.copy.sh
- **FreeDOS screen persisted on profile switch**: Added clearScreen() on stop/switch
- **nginx root showed "Welcome to nginx"**: `location = /` with `root` doesn't work — moved `root`/`index` to server level
- **git divergent branches**: Set `git config --global pull.rebase true`
- **Waze/Reus "unable to load data"**: Frontend JS used absolute `/api/...` paths — changed to relative `api/...` so nginx proxy subpath works
- **WebWars dev showed old UI**: Dev server serves from `build/wasm/bin/` which had stale HTML — copied `web/*.html` → `build/wasm/bin/`

### Decisions Made
1. Static HTML approach (no framework)
2. v86 npm package for embedding
3. AGENTS.md + AmazonQ.md committed to git (not gitignored)
4. FreeDOS for Doom, Buildroot Linux for terminal
5. systemd service for dev server (not ad-hoc python)
6. Port 8087 for v86panel
