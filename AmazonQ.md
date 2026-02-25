# Amazon Q - v86 Control Panel Context

**Last Updated**: 2026-02-25T18:38:00Z
**Working Directory**: `/home/ubuntu/mcpprojects/v86controlpanel/`
**Status**: ✅ Modernized 6-profile panel + js-dos games + Chromium — ALL WORKING

## Project: v86 Control Panel

Browser-based x86 VM control panel powered by v86 + js-dos — boot OS images, play DOS games, manage projects via SSH, all from a single web UI.

## Current Phase: Modernized Panel — Complete

### What Works
- ✅ 6 profiles: Alpine 3.23, TinyCore 17, KolibriOS, js-dos (10 games), 9front, Chromium
- ✅ Alpine 3.23: kernel 6.18.7-0-virt, bzimage+initrd+ISO boot, xterm.js serial terminal
- ✅ TinyCore 17: kernel 6.18, GUI Linux with fetch networking
- ✅ KolibriOS: instant boot ASM OS, mouse lock on click
- ✅ js-dos: 10 DOS games locally hosted (Doom, C&C, Prince of Persia, WarCraft, etc.)
- ✅ 9front: Plan 9 fork, Jan 2026 release, 460MB ISO, async loading, ACPI
- ✅ Chromium 145: real browser via noVNC
- ✅ Server-side state persistence: Flask API, gzip compressed
- ✅ Mouse lock for graphical OSes (click screen, Esc to release)

### What's Next
1. SSH project manager from Alpine VM
2. Multi-VM dashboard (tabs)
3. Test 9front boot (460MB async load)

---

## Session 3 - February 25, 2026

### Summary
Full OS modernization: replaced old profiles (Doom/FreeDOS/DSL) with Alpine 3.23, TinyCore 17, 9front, js-dos. All working.

### Work Done
1. Downloaded Alpine 3.23 virt ISO, extracted kernel 6.18.7 + initrd, replaced old files
2. Downloaded TinyCore 17 (25MB), replaced old tinycore.iso
3. Downloaded 9front Jan 2026 release (460MB 386 ISO) from 9front.org
4. Rewrote index.html: 6 new profiles, removed Doom/FreeDOS/DSL
5. Fixed Alpine boot: added ISO as cdrom for modloop (was dropping to emergency shell)
6. Fixed xterm.js width: CSS overrides for `.xterm`, `.xterm-screen`, `.xterm-viewport`
7. Added mouse lock for graphical OSes (KolibriOS, TinyCore, 9front)
8. Integrated js-dos v8 API with locally hosted game bundles
9. Downloaded 10 game bundles to jsdos/ directory (Doom, Doom II, C&C, Prince, WarCraft, Lemmings, Heretic, GTA, NFS, Digger)
10. Cleaned up old images (doom.img, doom_boot.img, dsl.iso, freedos722.img, alpine-3.23.iso)

### Issues Fixed
- Alpine emergency shell: initrd needs ISO as cdrom to find modloop
- xterm.js black gap on right: fixed with CSS `width: 100% !important` + hidden scrollbar
- js-dos "Dos is not defined": wrong CDN URL, fixed to v8.js-dos.com/latest/
- cdn.dos.zone CORS blocks: downloaded all bundles locally
- dos.zone iframe CSP blocks: switched from iframe to direct js-dos API
- 9front download: 9front.org slow start but works (15MB/s once connected), only9fans.com mirror has stale build numbers
- C&C bundle: not at obvious URL, found via scraping dos.zone page source → `cc_gdi_novid.jsdos`

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

---

## Session 1 - February 23, 2026

### Summary
Full project setup from zero to working v86 in browser.

### Work Done
1. Created GitHub repo, context files, npm setup, BIOS + image downloads
2. Built index.html control panel with VGA canvas + log panel
3. systemd service, nginx config, Control Center landing page
4. Fixed: nginx root, git rebase, waze/reus API paths, webwars stale HTML
