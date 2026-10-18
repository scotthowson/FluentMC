# Hosting a FluentMC server

Requirements: Java 25 (GraalVM or any JDK 25), 6 GB RAM, one open port (TCP + UDP, default 25565). Voice chat rides on the same port.

## Pelican / Pterodactyl

1. Admin → Eggs → Import, pick `pelican/egg-fluentmc.json` from this repo.
2. Create a server from the egg. Image: `ghcr.io/scotthowson/graalvm-papermc:graalvm25`. Memory: 6144 MB or more. One allocation.
3. `MRPACK_URL` must be a direct link to the `.mrpack`. The default points at this repo's latest release, which only works while the repo is public. For a private repo, upload the `.mrpack` somewhere reachable and paste that link.
4. Start it. The panel asks you to accept the Mojang EULA, then the server boots.
5. In the console: `whitelist add <friend>` for each player, `op <you>` for yourself.

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
| | `view-distance=10`, `simulation-distance=8` | server does less; clients see far with Distant Horizons and Bobby |
| | `allow-flight=true` | stops kicks from Waystones teleports and backpack hovering |
| | `max-tick-time=-1` | the watchdog would kill the server during heavy Terralith generation |
| | `sync-chunk-writes=false` | faster chunk saving on Linux |
| | `spawn-protection=0` | everyone can build at spawn |
| `config/voicechat/voicechat-server.properties` | `port=-1` | voice chat uses the Minecraft port, no second allocation |

Everything else runs on mod defaults. ServerCore, Lithium, Krypton and FerriteCore need no tuning. Chunky is installed for pre-generating: `chunky radius 2000` then `chunky start` after the first boot gives new players instant chunks.

## Ports and firewall

Open the Minecraft port for **both TCP and UDP**. UDP carries voice chat.

## Players

Players import `FluentMC-<version>.mrpack` into Prism Launcher (Add Instance → Import) or the Modrinth App, then add the server address. Clients need 8 to 10 GB of RAM and Java 25, which Prism downloads automatically.
