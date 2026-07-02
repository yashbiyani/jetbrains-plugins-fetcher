import requests, json, datetime, os, shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import timezone
from collections import defaultdict

PRODUCTS = {
    "IU": "IntelliJ IDEA Ultimate",
    "PS": "PhpStorm",
    "WS": "WebStorm",
    "PY": "PyCharm",
    "RM": "RubyMine",
    "CL": "CLion",
    "GO": "GoLand",
    "DB": "DataGrip",
    "RD": "Rider",
    "RR": "RustRover"
}

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
    
    # Organize by version and IDE name
    ide_name = PRODUCTS[code]
    release_dir = f"releases/{version}/{ide_name}"
    os.makedirs(release_dir, exist_ok=True)
    
    fname = f"{release_dir}/{code}-{build}.xml"
    with open(fname, "w") as f:
        f.write(r.text)
    
    return code, build, version, ide_name, fname

def main():
    # Clean previous releases directory
    if os.path.exists("releases"):
        shutil.rmtree("releases")
    
    version_products = defaultdict(dict)
    release_summary = {}
    
    with ThreadPoolExecutor(max_workers=8) as pool:  # parallel, but capped to be polite
        futures = {pool.submit(fetch_one, code): code for code in PRODUCTS}
        for fut in as_completed(futures):
            code = futures[fut]
            try:
                code, build, version, ide_name, fname = fut.result()
                version_products[version][code] = {
                    "build": build,
                    "ide": ide_name,
                    "file": fname
                }
                print(f"{code}: build {build} ({version}) done")
            except Exception as e:
                print(f"{code}: FAILED — {e}")
    
    # Create manifests for each version and generate release summary
    for version in sorted(version_products.keys(), reverse=True):
        # Version-specific manifest
        manifest = {
            "fetched_at": datetime.datetime.now(timezone.utc).isoformat(),
            "version": version,
            "products": version_products[version]
        }
        
        manifest_path = f"releases/{version}/manifest.json"
        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=2)
        
        # Build release summary
        ide_list = []
        for code in sorted(version_products[version].keys()):
            product = version_products[version][code]
            ide_list.append(f"- **{product['ide']}** ({code}): Build {product['build']}")
        
        release_summary[version] = "\n".join(ide_list)
    
    # Create release summary file
    summary_text = "# JetBrains Plugins by Version\n\n"
    for version in sorted(release_summary.keys(), reverse=True):
        summary_text += f"## Version {version}\n\n{release_summary[version]}\n\n"
    
    with open("releases/RELEASES.md", "w") as f:
        f.write(summary_text)
    
    print("\nRelease structure created under releases/ directory")

if __name__ == "__main__":
    main()