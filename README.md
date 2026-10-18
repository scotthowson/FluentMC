# FluentMC

A Fabric modpack for Minecraft 26.3 that keeps vanilla's feel but makes it smoother, prettier and better to explore with friends.

- **Smooth**: Sodium, Iris, Lithium, FerriteCore, ImmediatelyFast, Entity Culling, More Culling, Krypton, Dynamic FPS, Distant Horizons, Bobby.
- **Pretty**: Complementary Unbound shaders enabled out of the box (Reimagined, BSL and Photon included), Fresh Animations, Presence Footsteps, AmbientSounds, Sound Physics, Visuality, Not Enough Animations, LambDynamicLights, Continuity.
- **Fresh world**: Terralith terrain, Nullscape end, Structory, Towns & Towers, Dungeons and Taverns, Hopo's better structures, Formations, Moog's End Structures, Naturalist and Friends & Foes mobs.
- **Play together**: Waystones, Simple Voice Chat, Ping Wheel, Lootr (per-player loot), Universal Graves, Farmer's Delight, Traveler's Backpack, Better Combat, Nature's and Explorer's Compass, VeinMiner, FallingTree, Carry On, Easy Anvils / Easy Magic, Trade Cycling.
- **QoL**: JEI, Jade, AppleSkin, Xaero's Minimap + World Map, Inventory Profiles Next, Mouse Tweaks, Crafting Tweaks, Dynamic Crosshair, Zoomify, Controlling, Enchantment Descriptions, Durability Tooltip, Legendary Tooltips, Advancement Plaques, Item Highlighter, Pick Up Notifier, Overflowing Bars, Better Mount HUD, Boat Item View, Lighty, Shulker Box Tooltip, Chat Heads, Status Effect Bars, Mod Menu.

Full list with versions and sides: [MODLIST.md](MODLIST.md). Hosting guide: [docs/SERVER.md](docs/SERVER.md).

Requires **Java 25**. Give the client 8 to 10 GB of RAM.

## Play

Import `FluentMC-<version>.mrpack` into [Prism Launcher](https://prismlauncher.org) (Add Instance → Import) or the Modrinth App. Four shader packs are bundled and off by default: press **K** in game to toggle Complementary Unbound, or pick another under Video Settings → Shader Packs.

## Host a server

- **Bare metal**: download `FluentMC-<version>-server.zip` from Releases, unzip, `./start.sh`, accept the EULA in `eula.txt`, run again. The whitelist is on: `/whitelist add <name>`.
- **Pelican / Pterodactyl**: import `pelican/egg-fluentmc.json`. It runs on `ghcr.io/scotthowson/graalvm-papermc:graalvm25`. `MRPACK_URL` defaults to this repo's latest `FluentMC-latest.mrpack` release asset (the repo must be public, or point it at any other direct link); the install script fetches Fabric and every server-side mod from Modrinth and verifies hashes. Voice chat shares the Minecraft port, so one allocation is enough. Reinstalling updates mods but never overwrites your tuned `server.properties` or configs.

## Update or change the pack

Edit the mod lists at the top of `build.py`, then:

```bash
python3 -I build.py cache . ~/.local/share/PrismLauncher/instances/"Minecraft 26.3 Fabric"
```

It resolves the newest 26.3 Fabric build of every mod from Modrinth, verifies SHA-512 hashes, writes the `.mrpack` and server zip, and syncs the local Prism instance. Bump `VER` in the script for a new release, then publish the `.mrpack` (also as `FluentMC-latest.mrpack`) and server zip:

```bash
gh release create vX.Y.Z FluentMC-X.Y.Z.mrpack FluentMC-X.Y.Z-server.zip FluentMC-latest.mrpack
```
