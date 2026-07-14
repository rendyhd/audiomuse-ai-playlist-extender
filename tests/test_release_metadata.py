# AudioMuse-AI - https://github.com/NeptuneHub/AudioMuse-AI
# Copyright (C) 2025 NeptuneHub
# SPDX-License-Identifier: AGPL-3.0-only
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License v3.0. See the LICENSE file
# in the project root or <https://github.com/NeptuneHub/AudioMuse-AI/blob/main/LICENSE>

"""Focused publication checks for Playlist Curator.

Main Features:
* Verifies Lumae authorship and the catalog feature description.
* Keeps the Lumae header and visible Clear Workbench actions regression-tested.
"""

import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "PlaylistCurator"


class ReleaseMetadataTests(unittest.TestCase):
    def test_catalog_identity_and_description(self):
        catalog = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
        metadata = json.loads((PLUGIN / "plugin.json").read_text(encoding="utf-8"))

        for entry in (catalog["plugins"][0], metadata):
            self.assertEqual(entry["author"], "Lumae")
            self.assertIn("Smart Search", entry["description"])
            self.assertIn("Playlist Expander", entry["description"])

        self.assertEqual(metadata["versions"][0]["version"], "0.1.2")

    def test_header_uses_lumae_branding(self):
        topbar = (
            PLUGIN / "templates" / "playlist_curator" / "_curator_topbar.html"
        ).read_text(encoding="utf-8")

        self.assertIn("Lumae · Curate", topbar)
        self.assertNotIn("AudioMuse · Curate", topbar)

    def test_clear_workbench_actions_are_visible_and_wired(self):
        template = (
            PLUGIN / "templates" / "playlist_curator" / "_curator_workbench.html"
        ).read_text(encoding="utf-8")
        shared_js = (
            PLUGIN / "static" / "playlist_curator" / "curator-shared.js"
        ).read_text(encoding="utf-8")

        for button_id in ("curator-wb-clear-btn", "curator-sheet-clear-btn"):
            button = re.search(
                rf'<button[^>]+id="{button_id}"[^>]*>(.*?)</button>',
                template,
                re.DOTALL,
            )
            self.assertIsNotNone(button)
            self.assertIn("Clear Workbench", button.group(1))
            self.assertIn(button_id, shared_js)

        self.assertIn("Clear the entire Workbench?", shared_js)


if __name__ == "__main__":
    unittest.main()
