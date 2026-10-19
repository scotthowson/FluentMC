# usage: buildpack.py <cache_dir> <out_dir> <prism_instance_dir>
import json, sys, os, hashlib, shutil, zipfile, urllib.request, urllib.parse, concurrent.futures as cf
cache, out, inst = map(os.path.abspath, sys.argv[1:4])
os.makedirs(cache, exist_ok=True)
MC, LOADER, INSTALLER = "26.3", "0.20.0", "1.1.2"
NAME, VER = "FluentMC", "1.0.10"

CLIENT = """sodium iris sodium-extra reeses-sodium-options immediatelyfast entityculling moreculling badoptimizations
dynamic-fps continuity lambdynamiclights lambdabettergrass modmenu placeholder-api xaeros-minimap xaeros-world-map
inventory-profiles-next libipn mouse-tweaks zoomify not-enough-animations visuality presence-footsteps ambientsounds
creativecore sound-physics-remastered entity-model-features entitytexturefeatures chat-heads controlling searchables
status-effect-bars fastquit bobby dynamiccrosshair durability-tooltip supermartijn642s-config-lib pick-up-notifier
overflowing-bars better-mount-hud boat-item-view legendary-tooltips advancement-plaques prism-lib item-highlighter lighty auth-me dark-loading-screen smooth-scrolling-refurbished fast-ip-ping tool-stats
ambient-environment particle-rain sodium-shadowy-path-blocks wavey-capes mob-plaques chunks-fade-in autohud beautified-chat-client hey-wiki stendhal better-clouds wakes cherished-worlds""".split()
BOTH = """fabric-api fabric-language-kotlin cloth-config lithium ferrite-core krypton balm waystones
farmers-delight-refabricated puzzles-lib forge-config-api-port travelersbackpack better-combat player-animation-library
naturalist resourceful-lib friends-and-foes lithostitched terralith enderscape structory structory-towers cristel-lib
towns-and-towers dungeons-and-taverns hopo-better-mineshaft hopo-better-ruined-portals hopo-better-underwater-ruins
moogs-structure-lib mes-moogs-end-structures formations formations-overworld formations-nether lootr polymer universal-graves
trade-cycling veinminer fallingtree carry-on easy-anvils easy-magic leaves-be-gone jei mezzconfig jade appleskin clumps prickle
enchantment-descriptions shulkerboxtooltip ping-wheel spark
shogi natures-compass explorers-compass crafting-tweaks iceberg diagonal-fences diagonal-walls diagonal-windows visual-workbench easy-shulker-boxes
trashslot armor-statues debugify toms-storage camerapture
macaws-furniture macaws-bridges macaws-roofs macaws-windows macaws-doors macaws-trapdoors macaws-fences-and-walls
macaws-lights-and-lamps macaws-paths-and-pavings macaws-stairs macaws-paintings
amplified-nether dungeons-and-taverns-ancient-city-overhaul dungeons-and-taverns-nether-fortress-overhaul
dungeons-and-taverns-pillager-outpost-overhaul dungeons-and-taverns-stronghold-overhaul dungeons-and-taverns-swamp-hut-overhaul
repurposed-structures-fabric midnightlib wilder-wild frozenlib ecologics fish-of-thieves promenade
endrem better-archeology architectury-api resourceful-config stoneworks elytra-trims serene-seasons biomes-o-plenty terrablender glitchcore
mutant-monsters crawl friendly-fire xp-tome do-a-barrel-roll cicada universal-enchants spawn-animations collective yacl enchantment-lore incendium""".split()
SERVER = ["servercore", "chunky", "alternate-current", "ksyxis", "netherportalfix", "tabtps", "ledger",
          "essential-commands", "sit", "otterlib", "mob-heads", "lib-5555ff", "pet-names", "styled-chat", "brewery"]
SHADERS = ["complementary-unbound", "complementary-reimagined", "bsl-shaders", "photon-shader"]
RESOURCEPACKS = ["fresh-animations"]

def api(path):
    return json.load(urllib.request.urlopen("https://api.modrinth.com/v2/" + path, timeout=60))

def resolve(slug, loader):
    q = urllib.parse.urlencode({"game_versions": f'["{MC}"]', "loaders": f'["{loader}"]'})
    v = api(f"project/{slug}/version?{q}")
    assert v, f"{slug}: no {loader} build for {MC}"
    v = v[0]
    f = next((x for x in v["files"] if x["primary"]), v["files"][0])
    return {"slug": slug, "pid": v["project_id"], "version": v["version_number"], "file": f,
            "deps": [d["project_id"] for d in v["dependencies"] if d["dependency_type"] == "required"]}

def fetch(m):
    p = os.path.join(cache, m["file"]["filename"])
    if not (os.path.exists(p) and hashlib.sha512(open(p, "rb").read()).hexdigest() == m["file"]["hashes"]["sha512"]):
        data = urllib.request.urlopen(m["file"]["url"], timeout=120).read()
        assert hashlib.sha512(data).hexdigest() == m["file"]["hashes"]["sha512"], f"{m['slug']}: hash mismatch"
        open(p, "wb").write(data)
    return p

# (slugs, modrinth loader, install dir, client env, server env)
GROUPS = [(CLIENT, "fabric", "mods", "required", "unsupported"),
          (BOTH, "fabric", "mods", "required", "required"),
          (SERVER, "fabric", "mods", "unsupported", "required"),
          (SHADERS, "iris", "shaderpacks", "required", "unsupported"),
          (RESOURCEPACKS, "minecraft", "resourcepacks", "required", "unsupported")]

def resolve_item(item):
    slug, loader, directory, client_env, server_env = item
    return {**resolve(slug, loader), "dir": directory, "client": client_env, "server": server_env}

items = [(slug, *group[1:]) for group in GROUPS for slug in group[0]]
with cf.ThreadPoolExecutor(12) as ex:
    mods = list(ex.map(resolve_item, items))
    list(ex.map(fetch, mods))

have = {m["pid"] for m in mods}
missing = {d for m in mods for d in m["deps"] if d not in have} - {"1vrSzlao", "qvIfYCYJ"}  # kotlin-lang-forge: Forge only; qsl: Quilt only (Fabric API covers it)
for d in missing:
    who = [m["slug"] for m in mods if d in m["deps"]]
    print(f"MISSING DEP {d} ({api('project/'+d)['slug']}) needed by {who}")

# staging dirs
build = os.path.join(out, "build"); shutil.rmtree(build, ignore_errors=True)
client, server = os.path.join(build, "client"), os.path.join(build, "server")
for m in mods:
    for side, root in (("client", client), ("server", server)):
        if m[side] != "unsupported":
            d = os.path.join(root, m["dir"]); os.makedirs(d, exist_ok=True)
            shutil.copy(os.path.join(cache, m["file"]["filename"]), d)

filename = {m["slug"]: m["file"]["filename"] for m in mods}
shader, fa = filename["complementary-unbound"], filename["fresh-animations"]
os.makedirs(os.path.join(client, "config"), exist_ok=True)
open(os.path.join(client, "config", "iris.properties"), "w").write(
    f"#Iris Config\nshaderPack={shader}\nenableShaders=false\ndisableUpdateMessage=true\n")
OPTS = {"renderDistance": "16", "simulationDistance": "10", "entityDistanceScaling": "1.0",
        "resourcePacks": json.dumps(["vanilla", f"file/{fa}"]),
        "incompatibleResourcePacks": json.dumps([f"file/{fa}"]),
        "key_gui.xaero_new_waypoint": "key.keyboard.n", "key_key.toms_storage.open_terminal": "key.keyboard.h",
        "key_key.travelersbackpack.cycle_tool": "key.keyboard.v",
        "key_key.heywiki.open": "key.keyboard.j", "key_key.heywiki.open_search": "key.keyboard.comma"}
open(os.path.join(client, "options.txt"), "w").write("".join(f"{k}:{v}\n" for k, v in OPTS.items()))

# server files
shutil.copytree(os.path.join(out, "server", "config"), os.path.join(server, "config"), dirs_exist_ok=True)
if os.path.isdir(os.path.join(out, "client", "config")):
    shutil.copytree(os.path.join(out, "client", "config"), os.path.join(client, "config"), dirs_exist_ok=True)

# tiny code-less Fabric mod whose datapack sets friends-server gamerules on every world load
rules_jar = f"fluentmc-rules-{VER}.jar"
with zipfile.ZipFile(os.path.join(cache, rules_jar), "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("fabric.mod.json", json.dumps({"schemaVersion": 1, "id": "fluentmc_rules", "version": VER,
        "name": "FluentMC Rules", "description": "Sets FluentMC gamerules on world load.", "environment": "*"}))
    z.writestr("data/fluentmc_rules/function/load.mcfunction", "gamerule players_sleeping_percentage 1\n")
    z.writestr("data/minecraft/tags/function/load.json", json.dumps({"values": ["fluentmc_rules:load"]}))
data = open(os.path.join(cache, rules_jar), "rb").read()
mods.append({"slug": "fluentmc-rules", "pid": None, "version": VER, "dir": "mods", "client": "required", "server": "required",
             "file": {"filename": rules_jar, "size": len(data), "url": f"https://github.com/scotthowson/{NAME}/releases/download/v{VER}/{rules_jar}",
                      "hashes": {"sha1": hashlib.sha1(data).hexdigest(), "sha512": hashlib.sha512(data).hexdigest()}}})
for root in (client, server):
    shutil.copy(os.path.join(cache, rules_jar), os.path.join(root, "mods"))
launcher = f"fabric-server-mc.{MC}-loader.{LOADER}-launcher.{INSTALLER}.jar"
open(os.path.join(server, launcher), "wb").write(urllib.request.urlopen(
    f"https://meta.fabricmc.net/v2/versions/loader/{MC}/{LOADER}/{INSTALLER}/server/jar").read())
open(os.path.join(server, "server.properties"), "w").write(f"""motd=\\u00a7b{NAME}\\u00a7r - Fabric {MC}
max-players=10
view-distance=12
simulation-distance=8
difficulty=normal
spawn-protection=0
allow-flight=true
max-tick-time=-1
sync-chunk-writes=false
enable-status=true
online-mode=true
white-list=true
enforce-whitelist=true
""")
open(os.path.join(server, "start.sh"), "w").write(f"""#!/usr/bin/env sh
# Needs Java 25. Uses GraalVM if present, else whatever 'java' is on PATH.
cd "$(dirname "$0")"
JAVA="${{JAVA:-$(command -v java)}}"
[ -x /usr/lib/jvm/graalvm-jdk-25/bin/java ] && JAVA=/usr/lib/jvm/graalvm-jdk-25/bin/java
exec "$JAVA" -Xms6G -Xmx6G -XX:+UseZGC -XX:+AlwaysPreTouch -Dfile.encoding=UTF-8 -jar {launcher} nogui
""")
os.chmod(os.path.join(server, "start.sh"), 0o755)
open(os.path.join(server, "README.txt"), "w").write(f"""{NAME} {VER} server (Minecraft {MC}, Fabric {LOADER})
1. Install Java 25 (GraalVM or any JDK 25).
2. ./start.sh  -> it stops once and writes eula.txt; set eula=true in it if you agree to Mojang's EULA, then run again.
3. Whitelist is ON: add friends with  /whitelist add <name>  in the console.
4. Players need the {NAME}-{VER}.mrpack (import into Prism Launcher or the Modrinth App) and your IP/port 25565.
""")

# .mrpack
index = {"formatVersion": 1, "game": "minecraft", "versionId": VER, "name": NAME,
         "summary": f"Fabric {MC}: Sodium/Iris + Distant Horizons, Complementary shaders, Waystones, Farmer's Delight, Terralith, structures, building QoL.",
         "files": [{"path": f"{m['dir']}/{m['file']['filename']}", "hashes": {"sha1": m["file"]["hashes"]["sha1"], "sha512": m["file"]["hashes"]["sha512"]},
                    "env": {"client": m["client"], "server": m["server"]}, "downloads": [m["file"]["url"]], "fileSize": m["file"]["size"]} for m in mods],
         "dependencies": {"minecraft": MC, "fabric-loader": LOADER}}
mrpack = os.path.join(out, f"{NAME}-{VER}.mrpack")
with zipfile.ZipFile(mrpack, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("modrinth.index.json", json.dumps(index, indent=2))
    for root, _, files in os.walk(os.path.join(client, "config")):
        for f in files:
            full = os.path.join(root, f)
            z.write(full, "client-overrides/" + os.path.relpath(full, client))
    z.write(os.path.join(client, "options.txt"), "client-overrides/options.txt")
    z.write(os.path.join(server, "server.properties"), "server-overrides/server.properties")
    for root, _, files in os.walk(os.path.join(server, "config")):
        for f in files:
            full = os.path.join(root, f)
            z.write(full, "server-overrides/" + os.path.relpath(full, server))
shutil.make_archive(os.path.join(out, f"{NAME}-{VER}-server"), "zip", build, "server")

# sync Prism instance
mc = os.path.join(inst, ".minecraft")
shutil.rmtree(os.path.join(mc, "mods"))
for d in ("mods", "shaderpacks", "resourcepacks", "config"):
    shutil.copytree(os.path.join(client, d), os.path.join(mc, d), dirs_exist_ok=True)
op = os.path.join(mc, "options.txt")
lines = [l for l in open(op).read().splitlines() if l.split(":", 1)[0] not in OPTS]
open(op, "w").write("\n".join(lines + [f"{k}:{v}" for k, v in OPTS.items()]) + "\n")

# MODLIST.md from Modrinth project metadata (one bulk call)
ids = json.dumps([m["pid"] for m in mods if m["pid"]])
titles = {p["id"]: p for p in api("projects?ids=" + urllib.parse.quote(ids))}
titles[None] = {"title": "FluentMC Rules", "project_type": "mod", "slug": "", "description": "Pack-local gamerules (one player sleeping skips the night)."}
side = {("required", "required"): "both", ("required", "unsupported"): "client", ("unsupported", "required"): "server"}
with open(os.path.join(out, "MODLIST.md"), "w") as f:
    f.write(f"# {NAME} {VER} mod list\n\nMinecraft {MC}, Fabric Loader {LOADER}. Generated by build.py from Modrinth.\n\n")
    for directory, heading in (("mods", "Mods"), ("shaderpacks", "Shader packs"), ("resourcepacks", "Resource packs")):
        f.write(f"## {heading}\n\n| Name | Version | Side | Summary |\n|---|---|---|---|\n")
        for m in sorted((m for m in mods if m["dir"] == directory), key=lambda m: titles[m["pid"]]["title"].lower()):
            t = titles[m["pid"]]
            link = f"[{t['title']}](https://modrinth.com/{t['project_type']}/{t['slug']})" if t["slug"] else t["title"]
            f.write(f"| {link} | {m['version']} | {side[(m['client'], m['server'])]} | {t['description'].replace('|', '/')} |\n")
        f.write("\n")

print(f"\n{len(mods)} items; client mods={len(os.listdir(os.path.join(client,'mods')))} server mods={len(os.listdir(os.path.join(server,'mods')))}")
for m in sorted(mods, key=lambda m: (m["dir"], m["client"], m["slug"])): print(f"  {m['dir']:13} c={m['client']:11} s={m['server']:11} {m['slug']:30} {m['version']}")
