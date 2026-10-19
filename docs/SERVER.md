# Hosting a FluentMC server

Requirements: Java 25 (GraalVM or any JDK 25), 6 GB RAM, one open port (TCP + UDP, default 25565).

## Pelican / Pterodactyl

1. Admin → Eggs → Import, pick `pelican/egg-fluentmc.json` from this repo.
2. Create a server from the egg. Image: `ghcr.io/scotthowson/graalvm-papermc:graalvm25`. Memory: 6144 MB or more. One allocation.
3. `MRPACK_URL` must be a direct link to the `.mrpack`. The default points at this repo's latest release, which only works while the repo is public. For a private repo, upload the `.mrpack` somewhere reachable and paste that link.
4. **Fresh server only.** If the server folder already holds a `world/` from Paper or an older Minecraft, rename or delete it first. 26.3 cannot open it and stops with `Overworld settings missing` (the installer prints a warning when it sees this).
5. Start it. The panel asks you to accept the Mojang EULA, then the server boots. First boot generates the world and takes a minute or two.
6. In the console: `whitelist add <friend>` for each player, `op <you>` for yourself.

Updating: change `MRPACK_URL` if needed and click **Reinstall**. The installer replaces `mods/` and re-downloads Fabric, verifies every file hash, and leaves your world, `server.properties` and tuned configs alone.

## Bare metal

```bash
unzip FluentMC-<version>-server.zip && cd server
./start.sh            # stops once and writes eula.txt
sed -i 's/eula=false/eula=true/' eula.txt   # only if you agree to https://aka.ms/MinecraftEULA
./start.sh
```

`start.sh` uses GraalVM at `/usr/lib/jvm/graalvm-jdk-25` when present, otherwise `java` from PATH, with a fixed 6 GB heap and ZGC.

## What is preconfigured

| File | Setting | Why |
|---|---|---|
| `server.properties` | `white-list=true`, `enforce-whitelist=true` | friends only |
| | `difficulty=normal`, PvP on | vanilla defaults, as chosen |
| | `view-distance=12`, `simulation-distance=8` | server does less; clients see far with Bobby |
| | `allow-flight=true` | stops kicks from Waystones teleports and backpack hovering |
| | `max-tick-time=-1` | the watchdog would kill the server during heavy Terralith generation |
| | `sync-chunk-writes=false` | faster chunk saving on Linux |
| | `spawn-protection=0` | everyone can build at spawn |

| `config/universal-graves/config.json` | graves expire after 7 real days | abandoned graves drop their items and clean up |
| `config/EssentialCommands.properties` | 5 homes, 1 s teleport cooldown, `/back` after death | friends-server travel |
| `mods/fluentmc-rules-<ver>.jar` | `players_sleeping_percentage 1` on every world load | one sleeper skips the night, also in singleplayer |

Distant Horizons is not in the pack. On 26.3 its OpenGL engine (forced whenever Iris is installed) fails to load levels on multiplayer servers, its Blaze3D engine refuses to start with Iris, and its server-side generator deadlocked chunk generation. Bobby caches chunks past the server view distance instead.

Everything else runs on mod defaults. ServerCore, Lithium, Krypton, FerriteCore, Alternate Current and Ksyxis need no tuning.

## Admin tools on the server

- **TabTPS**: `/tps`, `/mspt`, `/memory`, and `/tabtps toggle tab` puts TPS in the tab list.
- **Ledger**: who broke, placed or took what. `/lg search action:block-break range:20` or `/lg inspect`, then `/lg rollback range:20 time:1h` to undo griefing.
- **Spark**: `/spark profiler start` for 30 seconds of lag diagnosis, `/spark health`.
- **Chunky**: `/chunky radius 2000` then `/chunky start` pre-generates the world so new players never wait on Terralith.
- **Nether Portal Fix** links portals correctly between dimensions; nothing to configure.

Backups: use Pelican's built-in backup schedule (Server → Backups). No backup mod is bundled.

Optional Discord chat bridge: [Discord-MC-Chat](https://modrinth.com/mod/discord-mc-chat) has a 26.3 server build, but it needs a bot token and is still beta, so it is not bundled. Drop its jar into `mods/` on the server and follow its README if you want join/leave and chat mirrored into your Discord. Chunky is installed for pre-generating: `chunky radius 2000` then `chunky start` after the first boot gives new players instant chunks.

## Ports and firewall

Open the Minecraft port (TCP). Nothing in the pack needs a second port.

## Players

Players import `FluentMC-<version>.mrpack` into Prism Launcher (Add Instance → Import) or the Modrinth App, then add the server address. Clients need 8 to 10 GB of RAM and Java 25, which Prism downloads automatically.
