import pathlib, textwrap, subprocess, os, stat

# ── paths & label ─────────────────────────────────────────────
app_path = pathlib.Path("/Users/tim/Projects/DailyWordDefinition_v2/bin/main_Controller.app")
exe_path = app_path / "Contents" / "MacOS" / "main_Controller"      # inner binary
label    = "com.myapp.main_controller"

# ── 0.  make the bundle launch-safe  ───────────────────────────
# a) ensure the binary is executable
exe_path.chmod(exe_path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

# b) strip any Gatekeeper quarantine flags
subprocess.run(["xattr", "-r", "-d", "com.apple.quarantine", str(app_path)],
               check=False)

# c) give the bundle an ad-hoc code signature (launchd accepts this)
subprocess.run(["codesign", "--force", "--deep", "--sign", "-", str(app_path)],
               check=True)

# ── 1. remove any previous plist ───────────────────────────────
user_uid      = os.getuid()
domain_target = f"gui/{user_uid}"
launch_agents = pathlib.Path.home() / "Library" / "LaunchAgents"
plist_file    = launch_agents / f"{label}.plist"

if plist_file.exists():
    subprocess.run(["launchctl", "bootout", domain_target, str(plist_file)],
                   check=False)          # ignore if not loaded
    plist_file.unlink()

# ── 2. write the new plist (RunAtLoad = true) ──────────────────
plist_text = textwrap.dedent(f"""\
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
      "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
      <dict>
        <key>Label</key>            <string>{label}</string>
        <key>ProgramArguments</key> <array>
                                       <string>{exe_path}</string>
                                    </array>
        <key>RunAtLoad</key>        <true/>
        <key>KeepAlive</key>        <false/>
      </dict>
    </plist>
""")

launch_agents.mkdir(exist_ok=True)
plist_file.write_text(plist_text)

print("✔ Plist written. It will auto-start at next login / reboot.")
