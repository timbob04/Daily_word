def createLaunchAgent(dep, executable_name="Controller"):

  # Launch agent path
  launch_agents = dep.pathlib.Path.home() / "Library" / "LaunchAgents"
  plist_file = launch_agents / f"com.myapp.{executable_name}.plist"
  
  # Only create launch agent if this script is running as an executable
  if getattr(dep.sys, 'frozen', False):

    root_dir, _ = dep.getBaseDir(dep.sys, dep.os)

    # ── paths & label ─────────────────────────────────────────────
    app_path = dep.os.path.join(root_dir, 'bin', executable_name + '.app') # .app path
    exe_path = dep.os.path.join(app_path, "Contents", "MacOS", executable_name) # inner binary path
    label = "com.myapp." + executable_name # label for the launch agent
    
    # Ensure the binary is executable
    exe_path = dep.pathlib.Path(exe_path)
    exe_path.chmod(exe_path.stat().st_mode | dep.stat.S_IXUSR | dep.stat.S_IXGRP | dep.stat.S_IXOTH)

    # Strip any Gatekeeper quarantine flags
    dep.subprocess.run(["xattr", "-r", "-d", "com.apple.quarantine", str(app_path)],
                  check=False)

    # Give the bundle an ad-hoc code signature (launchd accepts this)
    dep.subprocess.run(["codesign", "--force", "--deep", "--sign", "-", str(app_path)],
                  check=True)

    # Write the plist file and create the launch agent
    plist_text = dep.textwrap.dedent(f"""\
        <?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
          "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
        <plist version="1.0">
          <dict>
            <key>Label</key>            <string>{label}</string>
            <key>ProgramArguments</key> <array>
                                          <string>{exe_path}</string>
                                          <string>--from-launchagent</string>
                                        </array>
            <key>RunAtLoad</key>        <true/>
            <key>KeepAlive</key>        <false/>
          </dict>
        </plist>
    """)

    launch_agents.mkdir(exist_ok=True)
    plist_file.write_text(plist_text)

    print("✔ Plist written. It will auto-start at next login / reboot.")

def deleteLaunchAgent(dep, label="com.myapp.Controller"):
    plist = f"{dep.pathlib.Path.home()}/Library/LaunchAgents/{label}.plist"
    dep.subprocess.run(["rm", "-f", plist], check=False)
    print(f"✔ {label}: plist removed.")