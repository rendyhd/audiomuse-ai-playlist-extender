# AudioMuse-AI Playlist Extender

An installable AudioMuse-AI plugin by Lumae with Smart Search and Playlist Expander for discovering, extending, previewing, deduplicating, and saving playlists.

## Install

In AudioMuse-AI, open **Plugins > Repositories** and add:

```text
https://raw.githubusercontent.com/rendyhd/audiomuse-ai-playlist-extender/main/manifest.json
```

Refresh the catalog, install **Playlist Curator**, and select **Apply now (restart)**.

## Features

- Smart Search across artist, album, genre, mood, BPM, energy, key, scale, year, and rating metadata.
- Playlist Expander based on a weighted centroid of AudioMuse analysis embeddings.
- Normal, Boost, Strong, and Focus influence levels for seed tracks.
- Duplicate review for search results, extender results, and the shared Workbench.
- Credential-safe audio previews proxied through AudioMuse.
- Playlist loading and saving for Jellyfin, Emby, Plex, Navidrome, and Lyrion.

## Compatibility

The plugin requires AudioMuse-AI 2.6.0 or newer and runs in the Flask/web process. It has no additional Python dependencies.

## Development

Plugin source is under `plugins/PlaylistCurator`. Build the deterministic code-only archive with:

```shell
python scripts/build_playlist_curator_plugin.py
```

The archive excludes `plugin.json`, as required by the AudioMuse plugin installer. Pushes to `main` rebuild the archive and update its URL and checksum automatically.

## License

AGPL-3.0-only. See [LICENSE](LICENSE).
