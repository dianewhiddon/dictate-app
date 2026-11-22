# Changelog

## 0.1.5 — 2026-11-22

- Publish Dictate from a new GitHub repository.
- Update the Windows OpenTelemetry API dependency to address CVE-2026-126360.

## 0.1.4 — 2026-11-03

Windows lifecycle reliability.

- The native key watcher releases its Windows registration, joins on shutdown, and falls back to polling if its wait fails. An unused second-launch event path inherited from another app was removed.
- Queue work is ignored after shutdown begins, and the recorder watcher, tray and Tk window are cleaned up when the main loop exits.
- Added a regression using the actual initialized application and Tk event loop, so worker dispatch is exercised without the fallback timer.
- Recognition, cleanup choices, microphone behavior, hotkeys, dependencies and the contributed macOS code are unchanged.

## 0.1.3 — 2026-11-03

Battery. Windows only; the macOS port is unchanged.

- Dictate no longer checks your hold keys 50 times a second, all the time. It sleeps until Windows Raw Input reports a key change, looks every 20 milliseconds only while your two keys are down, and keeps a once-a-second check for keyboards that do not report through Raw Input. If Raw Input cannot register, the 20-millisecond polling returns. Raw Input is not a keyboard hook: it sits beside your typing, not in the path of every keystroke, so a busy Dictate cannot delay or drop one. Idle use measured on the maintainer's laptop fell from about 0.73% to about 0.08% of one processor core.
- The window's action queue wakes when work is posted instead of looking 25 times a second, with a slow 250-millisecond safety check.
- No change to recording, transcription, cleanup, insertion, Recents, dependencies or the installer.

## 0.1.2 — 2026-10-23

Security update. Install it in place of 0.1.1.

- certifi 2026.7.22 → 2026.10.19 in the Windows, macOS and development locks. It removes the distrusted emSign roots; certifi now has a matching minimum in both `requirements.txt` files.
- Pillow 12.3.0 → 13.0.0 in the Windows lock, with a 13.0.0 minimum.
- Development tool uv 0.13.1 → 0.13.4.
- No change to dictation, insertion, Recents or installer behavior. The macOS port, its bundle identifier and AUTHORS.md are unchanged.

## 0.1.1 — 2026-10-16

- Apply the shared gold action and light-gold accent palette on neutral gray surfaces.
- Separate action, selection and focus colors; preserve native controls and workflows.
- Refresh design documentation and release screenshots. Dependencies and installation behavior are unchanged.


## 0.1.0 · October 15, 2026

First personal-profile public source release, based on the previously prepared member edition.

- Neutral gray, white, teal and blue Windows tray/Recents styling; larger readable text, keyboard log action and generated microphone icon.
- Cloud cleanup off by default, bounded output budget and HTTP-client cleanup even when SDK construction fails.
- Bounded audio capture; dropped, overlong or interrupted captures retain their WAV instead of appearing complete. Destination menus block Windows insertion.
- Hash-locked runtime and development dependencies; Windows/macOS automated checks and documented release verification.
- Diane Green's macOS port preserved and credited. Added its missing sound module; history now precedes paste; incomplete cleanup falls back; modifier/clipboard failure cleanup is guarded; Quit/Restart target only this installation and wait for work to save; installer/bundle avoid broad process kills and recursive bundle deletion. Removed unused macOS GUI dependencies.
- Separate public repository and shortcut names; no personal installation data, API keys, recordings or private history included.

## Earlier member-edition history

## Unreleased

Windows public-release candidate, pending owner approval.

- Port clipboard-free Unicode insertion and explicit Recents copying from the daily-use application.
- Capture the foreground destination before recording; retain text before insertion.
- Replace the global keyboard library with native held-key polling.
- Keep configuration reload and Quit from interrupting active work.
- Validate local configuration overrides without overwriting shipped defaults.
- Bound history reads and preserve multiline entries; rotate diagnostic logs.
- Reject incomplete cleanup responses, close API clients, and omit provider bodies from transcription errors.
- Use single-pass literal snippet replacement.
- Add regression tests, hashed Windows dependencies and release/development documentation.
- Use explicit system-certificate TLS contexts instead of a global certificate monkeypatch.
- Preserve the credited macOS implementation as a separate community port.

### Migrating an existing Windows starter

Quit the old app first. Back up your own configuration, snippets, keys and history privately.
Reconcile customized `config.toml` with the new defaults and move overrides into `config.local.toml`.
Remove `paste_combo` and `restore_clipboard` from Windows settings: normal insertion no longer uses either.
Keep personal snippets outside tracked `snippets.md` and point to them from your local configuration.
Run the installer to update dependencies, then test in a text editor.

Existing Markdown history is readable; multiline entries written by older versions may already have lost their boundaries. Nothing reconstructs missing text. Your installed personal edition is a separate repository and does not update from this starter.
