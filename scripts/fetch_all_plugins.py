import requests, json, datetime, os
from concurrent.futures import ThreadPoolExecutor, as_completed

PRODUCTS = ["IU", "IC", "PS", "WS", "PY", "PC", "RM", "CL",
            "GO", "DB", "RD", "AI", "RR", "QA"]

def latest_build(code):
    url = f"https://data.services.jetbrains.com/products/releases?code={code}&type=release&latest=true"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    data = r.json()
    key = next(iter(data))
    return data[key][0]["build"], data[key][0]["version"]

def fetch_one(code):
    build, version = latest_build(code)
    url = f"https://plugins.jetbrains.com/plugins/list/?build={code}-{build}"
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    os.makedirs("data", exist_ok=True)
    fname = f"data/{code}-{build}.xml"
    with open(fname, "w") as f:
        f.write(r.text)
    return code, build, version, fname

def main():
    manifest = {"fetched_at": datetime.datetime.utcnow().isoformat(), "products": {}}
    with ThreadPoolExecutor(max_workers=8) as pool:  # parallel, but capped to be polite
        futures = {pool.submit(fetch_one, code): code for code in PRODUCTS}
        for fut in as_completed(futures):
            code = futures[fut]
            try:
                code, build, version, fname = fut.result()
                manifest["products"][code] = {"build": build, "version": version, "file": fname}
                print(f"{code}: build {build} ({version}) done")
            except Exception as e:
                print(f"{code}: FAILED — {e}")

    with open("data/manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)

if __name__ == "__main__":
    main()