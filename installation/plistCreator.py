import pathlib, textwrap, subprocess

exe_path = "/Users/tim/Projects/DailyWordDefinition_v2/dist/main_Controller.app/Contents/MacOS/main_Controller"
label      = "com.myapp.main_controller"                                       # any unique name you like

plist_text = textwrap.dedent(f"""\
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>Label</key>            <string>{label}</string>
    <key>ProgramArguments</key> <array><string>{exe_path}</string></array>
    <key>RunAtLoad</key>        <false/>   <!-- auto-start at login?  true/false -->
    <key>KeepAlive</key>        <false/>   <!-- restart if it quits?  true/false -->
  </dict>
</plist>
""")

launch_agents = pathlib.Path.home() / "Library" / "LaunchAgents"
launch_agents.mkdir(exist_ok=True)
plist_file = launch_agents / f"{label}.plist"
plist_file.write_text(plist_text)

subprocess.run(["launchctl", "load", "-w", str(plist_file)], check=True)  # register it once

print('Completed plist creation')
