#!/usr/bin/env python3
"""render.py <slide.html> <out.png>
Headless-Chrome screenshot of a 1920x1080 slide. Chrome will NOT exit after
writing the PNG (known hang), and macOS has no `timeout`, so we launch it in its
own process group, poll until the PNG is written and its size is stable (fonts
loaded via --virtual-time-budget), then kill the group. Never waits on exit.
"""
import sys, os, time, signal, subprocess

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

def render(html_path, out_png, deadline=55):
    html_path = os.path.abspath(html_path)
    out_png = os.path.abspath(out_png)
    if os.path.exists(out_png):
        os.remove(out_png)
    prof = subprocess.run(["mktemp", "-d"], capture_output=True, text=True).stdout.strip()
    args = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
            "--force-device-scale-factor=1", "--window-size=1920,1080",
            "--virtual-time-budget=20000", "--run-all-compositor-stages-before-draw",
            "--font-render-hinting=none", "--user-data-dir=" + prof,
            "--screenshot=" + out_png, "file://" + html_path]
    p = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                         start_new_session=True)
    t0 = time.time(); last = -1; stable = 0
    while time.time() - t0 < deadline:
        time.sleep(0.5)
        if os.path.exists(out_png):
            sz = os.path.getsize(out_png)
            if sz > 0 and sz == last:
                stable += 1
                if stable >= 2:   # size unchanged across two polls => fully written
                    break
            else:
                stable = 0
            last = sz
        if p.poll() is not None:   # chrome exited on its own
            break
    try:
        os.killpg(os.getpgid(p.pid), signal.SIGKILL)
    except Exception:
        pass
    subprocess.run(["rm", "-rf", prof])
    if os.path.exists(out_png) and os.path.getsize(out_png) > 0:
        try:
            from PIL import Image
            w, h = Image.open(out_png).size
            print("OK %s %dx%d" % (out_png, w, h))
            return (w, h) == (1920, 1080)
        except Exception as e:
            print("OK(no-PIL) " + out_png); return True
    print("FAIL no PNG for " + html_path)
    return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: render.py <slide.html> <out.png>"); sys.exit(2)
    sys.exit(0 if render(sys.argv[1], sys.argv[2]) else 1)
