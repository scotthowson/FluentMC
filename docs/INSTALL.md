# Installing FluentMC

FluentMC is a Fabric modpack for **Minecraft 26.3**. You need a Minecraft: Java Edition account, **Java 25** (the launchers below download it for you), and **8 to 10 GB of RAM** given to the game. Download `FluentMC-<version>.mrpack` from the [latest release](https://github.com/scotthowson/FluentMC/releases/latest).

Pick one launcher. Prism Launcher is the recommended route and the one the pack was built with.

## Prism Launcher (recommended)

1. Install [Prism Launcher](https://prismlauncher.org/download/) and sign in with your Microsoft account (top right → Accounts).
2. **Add Instance** → **Import** → choose the downloaded `.mrpack` → OK.
3. Prism downloads Fabric, every mod, shader and resource pack. First import takes a minute or two.
4. Right-click the instance → **Edit** → **Settings** → **Java**: tick *Memory*, set **Maximum memory allocation** to **8192 MiB** (10240 if you have 32 GB or more). Prism picks Java 25 automatically.
5. Launch. The first start builds caches and can take a few minutes; later starts are quicker.

**Updating**: Add Instance → Import the new `.mrpack` as a fresh instance (your singleplayer worlds live inside the old instance; copy `saves/` across if you need them). For the server, nothing else is needed: worlds live on the server.

## Modrinth App

1. Install the [Modrinth App](https://modrinth.com/app) and sign in with Microsoft.
2. **Create profile** → **From file** → choose the `.mrpack`.
3. Open the profile → **Options** → **Java and memory** → set memory to **8192 MB** or more.
4. **Play**.

**Updating**: drag the new `.mrpack` onto the app, or create a new profile from it.

## Vanilla Minecraft Launcher

The official launcher can't read `.mrpack` files, so two steps: install Fabric, then copy the pack's files in. You need Python 3 for the helper script, or do the file step by hand.

1. Run the [Fabric installer](https://fabricmc.net/use/installer/) → **Client** tab → Minecraft version **26.3**, Loader **0.20.0** → **Install**. This adds a `fabric-loader-0.20.0-26.3` profile to the launcher.
2. Make a dedicated game folder, for example `~/FluentMC` (Windows: `%APPDATA%\FluentMC`). Keeping it separate from `.minecraft` avoids mixing other mods in.
3. Fill it from the pack:
   ```bash
   python3 tools/install_vanilla.py FluentMC-<version>.mrpack ~/FluentMC
   ```
   (`tools/install_vanilla.py` is in this repo. It downloads every client file with hash checks, then copies the pack's default options and configs in. Re-run it with a new `.mrpack` to update.)
   Doing it by hand instead: unzip the `.mrpack`, open `modrinth.index.json`, download each `downloads` URL whose `env.client` is not `unsupported` into the listed `path` under your game folder, then copy the contents of `client-overrides/` over the game folder.
4. In the launcher, **Installations** → edit the `fabric-loader-0.20.0-26.3` profile:
   - **Game directory**: your `~/FluentMC` folder.
   - **JVM arguments**: change `-Xmx2G` to `-Xmx8G`.
   - Java: leave the launcher's bundled runtime; it is Java 25 for 26.3.
5. Play that profile.

## After installing, on any launcher

- Shaders are bundled but off. Press **K** in game to turn Complementary Unbound on, or pick another pack under Options → Video Settings → Shader Packs.
- Keys that differ from vanilla are listed in [KEYBINDS.md](KEYBINDS.md). Most important: **B** opens the backpack, **N** sets a waypoint, **J** opens the wiki for whatever you're looking at.
- To join the server, ask for the address and make sure you've been whitelisted.

## Troubleshooting

- **"Out of memory" or stutter**: raise memory to 10240 MiB. Below 6 GB the pack will not run well.
- **Game won't start after you added a mod**: remove it. Every mod in the pack was tested together; extras are on you.
- **Low FPS with shaders**: press K to turn them off, or switch to Complementary Reimagined in the shader list, which is lighter.
- **Linux, AMD GPU**: keep Mesa current. The pack runs on radeonsi with no extra flags.
- **Java version errors**: the game needs Java 25. Prism and Modrinth install it automatically; on the vanilla launcher use the bundled runtime, not a system Java 17 or 21.
