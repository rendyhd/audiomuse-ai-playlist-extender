# AudioMuse-AI - https://github.com/NeptuneHub/AudioMuse-AI
# Copyright (C) 2025 NeptuneHub
# SPDX-License-Identifier: AGPL-3.0-only
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License v3.0. See the LICENSE file
# in the project root or <https://github.com/NeptuneHub/AudioMuse-AI/blob/main/LICENSE>

"""Build a deterministic, code-only AudioMuse Playlist Curator plugin archive.

Main Features:
* Excludes plugin.json and Python cache files from the install package.
* Produces reproducible archives and reports their MD5 checksum.
"""

import argparse
import copy
import hashlib
import json
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = REPO_ROOT / "plugins" / "PlaylistCurator"


def _manifest():
    return json.loads((PLUGIN_ROOT / "plugin.json").read_text(encoding="utf-8"))


def _members():
    for path in sorted(PLUGIN_ROOT.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(PLUGIN_ROOT)
        if relative == Path("plugin.json"):
            continue
        if "__pycache__" in relative.parts or path.suffix == ".pyc":
            continue
        yield path, relative.as_posix()


def build(output_dir):
    manifest = _manifest()
    version = str(manifest["versions"][0]["version"])
    plugin_id = manifest["id"]
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / f"{plugin_id}_{version}.zip"

    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for source, archive_name in _members():
            info = zipfile.ZipInfo(archive_name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, source.read_bytes())

    checksum = hashlib.md5(output.read_bytes(), usedforsecurity=False).hexdigest()
    return output, checksum


def write_local_catalog(output_dir, archive, checksum, base_url):
    """Write install metadata for an HTTP server rooted at output_dir."""
    manifest = copy.deepcopy(_manifest())
    base_url = base_url.rstrip('/')
    manifest['versions'][0]['sourceUrl'] = f"{base_url}/{archive.name}"
    manifest['versions'][0]['checksum'] = checksum
    (output_dir / 'plugin.json').write_text(
        json.dumps(manifest, indent=2) + '\n', encoding='utf-8', newline='\n'
    )
    catalog = {
        'plugins': [{
            'id': manifest['id'],
            'name': manifest['name'],
            'author': manifest['author'],
            'description': manifest['description'],
            'pluginUrl': f"{base_url}/plugin.json",
        }]
    }
    (output_dir / 'manifest.json').write_text(
        json.dumps(catalog, indent=2) + '\n', encoding='utf-8', newline='\n'
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=REPO_ROOT / "dist" / "playlist_curator",
    )
    parser.add_argument(
        "--base-url",
        help="Also write plugin.json and manifest.json for this served directory URL.",
    )
    args = parser.parse_args()
    output, checksum = build(args.output_dir.resolve())
    if args.base_url:
        write_local_catalog(args.output_dir.resolve(), output, checksum, args.base_url)
    print(output)
    print(f"md5 {checksum}")


if __name__ == "__main__":
    main()
