class CreateLaunchAgent():
  def __init__(self, dep, executable_name):
    # Parameters
    self.dep = dep
    self.executable_name = executable_name
    # Default values
    self.plist_file = None
    self.domain_target = None
    
    # Always set up paths, even if just for cleanup
    user_uid = self.dep.os.getuid()
    self.domain_target = f"gui/{user_uid}"
    launch_agents = self.dep.pathlib.Path.home() / "Library" / "LaunchAgents"
    self.plist_file = launch_agents / f"com.myapp.{self.executable_name}.plist"
    
    # Only create plist if running as executable
    if getattr(self.dep.sys, 'frozen', False):
      self.createPlist()

  def createPlist(self):
    
    # Return if not running as an executable
    if not getattr(self.dep.sys, 'frozen', False):
      return

    root_dir, _ = self.dep.getBaseDir(self.dep.sys, self.dep.os)

    # ── paths & label ─────────────────────────────────────────────
    app_path = self.dep.os.path.join(root_dir, 'bin', self.executable_name + '.app')
    exe_path = self.dep.os.path.join(app_path, "Contents", "MacOS", self.executable_name)      # inner binary
    label    = "com.myapp." + self.executable_name

    # ── 0.  make the bundle launch-safe  ───────────────────────────
    # a) ensure the binary is executable
    exe_path = self.dep.pathlib.Path(exe_path)
    exe_path.chmod(exe_path.stat().st_mode | self.dep.stat.S_IXUSR | self.dep.stat.S_IXGRP | self.dep.stat.S_IXOTH)

    # b) strip any Gatekeeper quarantine flags
    self.dep.subprocess.run(["xattr", "-r", "-d", "com.apple.quarantine", str(app_path)],
                  check=False)

    # c) give the bundle an ad-hoc code signature (launchd accepts this)
    self.dep.subprocess.run(["codesign", "--force", "--deep", "--sign", "-", str(app_path)],
                  check=True)

    # ── 1. remove any previous plist ───────────────────────────────
    user_uid      = self.dep.os.getuid()
    self.domain_target = f"gui/{user_uid}"
    launch_agents = self.dep.pathlib.Path.home() / "Library" / "LaunchAgents"
    self.plist_file    = launch_agents / f"{label}.plist"

    self.unlinkPlist()

    # ── 2. write the new plist (RunAtLoad = true) ──────────────────
    plist_text = self.dep.textwrap.dedent(f"""\
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
    self.plist_file.write_text(plist_text)

    print("✔ Plist written. It will auto-start at next login / reboot.")

  def unlinkPlist(self):
    # Return if not running as an executable
    print(f"\nAttempting to unlink plist:")
    print(f"Running as executable: {getattr(self.dep.sys, 'frozen', False)}")
    print(f"Plist file: {self.plist_file}")
    
    if self.plist_file.exists():
      print("Found plist file, attempting to unlink")
      self.dep.subprocess.run(["launchctl", "bootout", self.domain_target, str(self.plist_file)],
                    check=False)          # ignore if not loaded
      self.plist_file.unlink()
      print("Plist unlinked")
    else:
      print("No plist file found to unlink")

def checkIfRunningFromLaunchAgent(dep, executable_name):
    user_uid = dep.os.getuid()
    domain_target = f"gui/{user_uid}"
    launch_agents = dep.pathlib.Path.home() / "Library" / "LaunchAgents"
    plist_file = launch_agents / f"com.myapp.{executable_name}.plist"
    
    print(f"\nChecking launch agent status:")
    print(f"Looking for plist file at: {plist_file}")
    print(f"Running as executable: {getattr(dep.sys, 'frozen', False)}")
    
    # Check if plist exists and is loaded
    if plist_file.exists():
        print("✓ Plist file exists")
        # Check if the launch agent is actually loaded
        result = dep.subprocess.run(["launchctl", "print", domain_target], 
                                  capture_output=True, text=True, check=False)
        print(f"Launch agent status output:\n{result.stdout}")
        is_loaded = f"com.myapp.{executable_name}" in result.stdout
        print(f"Launch agent is {'loaded' if is_loaded else 'not loaded'}")
        return is_loaded
    else:
        print("✗ Plist file does not exist")
        return False      