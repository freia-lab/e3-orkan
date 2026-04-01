import sys
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

# ------------------------------------------------------------
# Command‑line argument: IP address
# ------------------------------------------------------------
if len(sys.argv) < 2:
    print("Usage: python3 program.py <ip_addr>")
    sys.exit(1)

IP_ADDR = sys.argv[1]
BASE = f"http://{IP_ADDR}"
FORM_PAGE = urljoin(BASE, "/ip_en.html")
DEFAULT_ACTION = "/ok.html"

HEADERS = {
    "User-Agent": "python-requests/2.x",
    "Referer": FORM_PAGE,
}

# ------------------------------------------------------------
# Parse the form fields
# ------------------------------------------------------------
def parse_form(html):
    soup = BeautifulSoup(html, "html.parser")

    # Find the form whose action is ok.html
    form = None
    for f in soup.find_all("form"):
        action = (f.get("action") or "").strip()
        if action == "/ok.html":
            form = f
            break

    if form is None:
        raise RuntimeError("Cannot find form with action /ok.html")

    action = form.get("action") or DEFAULT_ACTION
    method = (form.get("method") or "GET").upper()

    data = {}

    # Inputs
    for inp in form.find_all("input"):
        name = inp.get("name")
        if not name:
            continue
        itype = (inp.get("type") or "").lower()

        if itype in ("checkbox", "radio"):
            if inp.has_attr("checked"):
                data[name] = inp.get("value", "on")
        elif itype == "submit":
            # EXCLUDE "post" field
            continue
        else:
            data[name] = inp.get("value", "")

    # Selects
    for sel in form.find_all("select"):
        name = sel.get("name")
        if not name:
            continue
        chosen = sel.find("option", selected=True) or sel.find("option")
        if chosen:
            data[name] = chosen.get("value", chosen.text)

    # Remove unwanted field if present
    data.pop("lgo", None)   # remove logout button field if parsed

    return action, method, data


# ------------------------------------------------------------
# Main logic
# ------------------------------------------------------------
def reload_form(simulate_new_value=False, safe_echo_first=True):
    print(f"[INFO] Connecting to device at {IP_ADDR}")

    s = requests.Session()
    s.headers.update(HEADERS)

    # 1) GET the form
    r = s.get(FORM_PAGE, timeout=10)
    r.raise_for_status()

    # 2) Parse fields
    action, method, form_data = parse_form(r.text)
    post_url = urljoin(BASE, action)

    print("[INFO] Form action:", post_url)
    print("[INFO] Fields parsed:", form_data)

    # 3) Optionally change a value
    if simulate_new_value and "lca" in form_data:
        form_data["lca"] = "192.168.10.99"
        print("[INFO] Changing Device IP to 192.168.10.99 (simulate)")

    # 4) Safe echo test
    if safe_echo_first:
        print("[INFO] Sending payload to https://httpbin.org/post (safe test)")
        er = s.post("https://httpbin.org/post", data=form_data, timeout=10)
        er.raise_for_status()
        print("[INFO] Echo server reply (first 500 bytes):")
        print(er.text[:800])

    # 5) Real POST — remains commented out for safety
    rr = s.post(post_url, data=form_data, timeout=10)
    print("Device returned:", rr.status_code)
    # print(rr.text[:500])


if __name__ == "__main__":
    # Safe defaults
    reload_form(simulate_new_value=False, safe_echo_first=False)
