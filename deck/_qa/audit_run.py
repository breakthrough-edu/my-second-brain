#!/usr/bin/env python3
"""Run the deterministic collision auditor on one slide and print its JSON report.
Usage: python3 audit_run.py <slide.html>
Prints compact JSON: {clean, overlaps[], oob[], tileOverlaps[], textCount}.
Chrome hangs after --dump-dom (and macOS has no `timeout`), so we launch it in
its own process group, read stdout in a thread until the DOM appears, then kill.
"""
import sys, os, re, html, json, subprocess, signal, threading, time

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
QA_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIT = os.path.join(QA_DIR, "audit.html")

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "error": "usage: audit_run.py <slide.html>"})); return 2
    slide = sys.argv[1]
    slide_abs = slide if os.path.isabs(slide) else os.path.abspath(slide)
    if not os.path.exists(slide_abs):
        alt = os.path.join(os.path.dirname(QA_DIR), "slides", os.path.basename(slide))
        if os.path.exists(alt): slide_abs = alt
    if not os.path.exists(slide_abs):
        print(json.dumps({"status": "error", "error": "slide not found: " + slide})); return 2

    url = "file://" + AUDIT + "?src=" + "file://" + slide_abs
    prof = subprocess.run(["mktemp", "-d"], capture_output=True, text=True).stdout.strip()
    args = [CHROME, "--headless=new", "--disable-gpu",
            "--allow-file-access-from-files", "--disable-web-security",
            "--virtual-time-budget=12000", "--run-all-compositor-stages-before-draw",
            "--user-data-dir=" + prof, "--dump-dom", url]
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                         text=True, start_new_session=True)
    buf = {"dom": ""}
    def reader():
        try: buf["dom"] = p.stdout.read()
        except Exception: pass
    th = threading.Thread(target=reader, daemon=True); th.start()

    dom = ""; t0 = time.time(); deadline = 16
    while time.time() - t0 < deadline:
        time.sleep(0.5)
        # peek: reader fills buf only on full read; also poll process exit
        if p.poll() is not None:
            th.join(2); dom = buf["dom"]; break
    else:
        pass
    # if still running, kill and take whatever the reader captured (dump-dom
    # flushes the full DOM before the hang, so a clean read usually completes on exit)
    try:
        os.killpg(os.getpgid(p.pid), signal.SIGKILL)
    except Exception:
        pass
    th.join(3)
    if not dom:
        dom = buf["dom"]
    subprocess.run(["rm", "-rf", prof])

    matches = re.findall(r'<pre id="report">(.*?)</pre>', dom, re.S)
    if not matches:
        print(json.dumps({"status": "error", "error": "no report node in dom", "domlen": len(dom)})); return 1
    raw = html.unescape(matches[-1])   # last = the populated report
    try:
        rep = json.loads(raw)
    except Exception as e:
        print(json.dumps({"status": "error", "error": "bad json: " + str(e), "raw": raw[:300]})); return 1
    print(json.dumps(rep, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    sys.exit(main())
