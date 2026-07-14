# AudioMuse-AI Playlist Extender

An installable AudioMuse-AI plugin for searching, extending, previewing, deduplicating, and saving playlists from an analyzed music library.

## Install

In AudioMuse-AI, open **Plugins > Repositories** and add:

```text
https://raw.githubusercontent.com/rendyhd/audiomuse-ai-playlist-extender/main/manifest.json
```

Refresh the catalog, install **Playlist Curator**, and select **Apply now (restart)**.

## Features

- Smart Search across artist, album, genre, mood, BPM, energy, key, scale, year, and rating metadata.
- Playlist Extender based on a weighted centroid of AudioMuse analysis embeddings.
- Normal, Boost, Strong, and Focus influence levels for seed tracks.
- Duplicate review for search results, extender results, and the shared Workbench.
- Credential-safe audio previews proxied through AudioMuse.
- Playlist loading and saving for Jellyfin, Emby, Plex, Navidrome, and Lyrion.

MPD playlist loading and audio previews are intentionally unsupported.

## Compatibility

The plugin requires AudioMuse-AI 2.6.2 or newer and runs in the Flask/web process. It has no additional Python dependencies.

The extender intentionally imports `find_nearest_neighbors_by_vector` and `get_vector_by_id` directly from `tasks.ivf_manager`. Those are internal AudioMuse interfaces, so a future core refactor may require a matching plugin update.

## Development

Plugin source is under `plugins/PlaylistCurator`. Build the deterministic code-only archive with:

```shell
python scripts/build_playlist_curator_plugin.py
```

The archive excludes `plugin.json`, as required by the AudioMuse plugin installer. Pushes to `main` rebuild the archive and update its URL and checksum automatically.

## License

AGPL-3.0-only. See [LICENSE](LICENSE).
