# JetBrains Plugins Fetcher

Automatically fetches and publishes JetBrains IDE plugin compatibility data organized by IDE and version.

## Overview

This repository tracks the latest plugin compatibility information for all JetBrains IDEs, running daily at 6 AM UTC via GitHub Actions.

## 📥 Download Plugins

Visit the [Releases](https://github.com/yashbiyani/jetbrains-plugins-fetcher/releases) page to download plugin data:

- **Latest Release** (`latest-plugins`): Contains zipped plugin data for each version
- Each version includes XML files organized by IDE
- Files are structured as: `{version}/{IDE-Name}/{IDE-Code}-{BUILD}.xml`

### Directory Structure

```
2026.1.3/
├── IntelliJ IDEA Ultimate/
│   └── IU-261.25134.95.xml
├── PyCharm/
│   └── PY-261.25134.203.xml
├── WebStorm/
│   └── WS-261.25134.101.xml
└── ... (other IDEs)
```

## 🔍 IDE Codes

| Code | IDE |
|------|-----|
| IU | IntelliJ IDEA Ultimate |
| PS | PhpStorm |
| WS | WebStorm |
| PY | PyCharm |
| RM | RubyMine |
| CL | CLion |
| GO | GoLand |
| DB | DataGrip |
| RD | Rider |
| RR | RustRover |

## 📋 Manifest File

Each version includes a `manifest.json` that indexes all IDE data:

```json
{
  "fetched_at": "2026-07-02T11:16:49.735538+00:00",
  "version": "2026.1.3",
  "products": {
    "IU": {
      "build": "261.25134.95",
      "ide": "IntelliJ IDEA Ultimate",
      "file": "releases/2026.1.3/IntelliJ IDEA Ultimate/IU-261.25134.95.xml"
    }
  }
}
```

## 🔄 Update Frequency

- **Scheduled**: Daily at 6 AM UTC
- **Manual**: Trigger via [Actions](https://github.com/yashbiyani/jetbrains-plugins-fetcher/actions) > "Track JetBrains Plugins by Build" > "Run workflow"

## 📦 Release Contents

Each release contains:
- Version-specific zip files (e.g., `2026.1.3.zip`)
- Plugin XML files for each IDE
- `manifest.json` for each version
- `RELEASES.md` with summary of all IDE builds

## 🛠 Usage

1. Download the zip file for your target version from [Releases](https://github.com/yashbiyani/jetbrains-plugins-fetcher/releases)
2. Extract and locate the XML file for your IDE
3. Use the XML data for plugin compatibility analysis

## 📝 License

This project is open source. See LICENSE for details.
