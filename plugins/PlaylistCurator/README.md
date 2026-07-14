# Playlist Curator

Playlist Curator is a Lumae plugin for AudioMuse-AI with Smart Search and Playlist Expander for building playlists from the analyzed music library.

## Features

- Smart Search across artist, album, genre, mood, BPM, energy, key, scale, year, and rating metadata.
- Playlist Expander using a weighted centroid of analysis embeddings.
- Per-track Normal, Boost, Strong, and Focus influence levels.
- Duplicate discovery in search results, extender results, and the shared Workbench.
- Audio preview proxied through AudioMuse so media-server credentials stay server-side.
- Loading and saving playlists through Jellyfin, Emby, Plex, Navidrome, and Lyrion.

MPD playlist loading and audio preview are intentionally unsupported.

## Compatibility

The plugin requires AudioMuse-AI 2.6.0 or newer and runs only in the Flask/web process. It uses AudioMuse's built-in packages and does not require plugin-installed pip dependencies.

The extender intentionally imports `find_nearest_neighbors_by_vector` and `get_vector_by_id` from `tasks.ivf_manager`. These are internal AudioMuse APIs, so a future core refactor may require a matching plugin update.

## Build and local installation

From the repository root, build the code-only archive with:

```shell
python scripts/build_playlist_curator_plugin.py
```

To also generate install metadata for a locally served directory:

```shell
python scripts/build_playlist_curator_plugin.py --base-url http://YOUR_HOST:8000
python -m http.server 8000 --directory dist/playlist_curator
```

Use an address the AudioMuse container can reach, then add `http://YOUR_HOST:8000/manifest.json` under Plugins > Repositories. The generated zip correctly excludes `plugin.json`; AudioMuse reads that metadata separately through the catalog.

After installing or updating, use **Apply now (restart)** on the Plugins page.
