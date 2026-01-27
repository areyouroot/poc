import time
import subprocess
import os
import sys
from playwright.sync_api import sync_playwright

def run_e2e():
    # Paths
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    backend_dir = os.path.join(root_dir, "backend")
    # frontend_dir = os.path.join(root_dir, "frontend")
    dist_dir = os.path.join(root_dir, "frontend", "dist", "frontend", "browser")
    evidence_dir = os.path.join(root_dir, "evidence")
    os.makedirs(evidence_dir, exist_ok=True)

    print(f"Starting Backend from {backend_dir}...")
    env = os.environ.copy()
    env["PYTHONPATH"] = root_dir
    backend_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"],
        cwd=root_dir,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    print(f"Starting Frontend Static Server from {dist_dir}...")
    frontend_proc = subprocess.Popen(
        [sys.executable, "-m", "http.server", "4200", "--directory", dist_dir],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    try:
        # Wait for services
        print("Waiting for services (5s)...")
        time.sleep(5)

        with sync_playwright() as p:
            print("Launching browser...")
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            print("Navigating to app...")
            try:
                page.goto("http://localhost:4200", timeout=30000)
            except Exception as e:
                print(f"Failed to load page: {e}")
                raise

            # Fill Config
            print("Filling config...")
            # We need to wait for inputs to appear
            page.wait_for_selector("input")

            # Maps Key is first input
            page.locator("input").nth(0).fill("TEST_MAPS_KEY")
            # Search Key is second
            page.locator("input").nth(1).fill("TEST_SEARCH_KEY")
            # CX
            page.locator("input").nth(2).fill("TEST_CX")

            # Click Save
            page.click("button:has-text('Save & Start')")

            print("Waiting for main UI...")
            page.wait_for_selector(".app-container")

            # Click Scan
            print("Clicking Scan...")
            page.click("button:has-text('Scan Companies')")

            # Wait a bit
            time.sleep(5)

            # Take screenshot
            screenshot_path = os.path.join(evidence_dir, "final_screenshot.png")
            page.screenshot(path=screenshot_path)
            print(f"Screenshot saved to {screenshot_path}")

            browser.close()

    finally:
        print("Stopping services...")
        backend_proc.terminate()
        frontend_proc.terminate()
        try:
            backend_proc.wait(timeout=5)
            frontend_proc.wait(timeout=5)
        except:
            backend_proc.kill()
            frontend_proc.kill()

if __name__ == "__main__":
    run_e2e()
