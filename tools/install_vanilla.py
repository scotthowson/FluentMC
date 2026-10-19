#!/usr/bin/env python3
"""Install FluentMC client files from an .mrpack into a game folder for the vanilla launcher.

usage: python3 install_vanilla.py FluentMC-x.y.z.mrpack /path/to/game/folder
Downloads every client-side file in the pack (hash-verified) into <folder>/mods, shaderpacks,
resourcepacks, then applies overrides and client-overrides. Re-run to update: mods/ is replaced,
everything else is kept.
"""
import hashlib, json, os, shutil, sys, urllib.request, zipfile

mrpack, dest = sys.argv[1], os.path.abspath(sys.argv[2])
with zipfile.ZipFile(mrpack) as z:
    index = json.loads(z.read("modrinth.index.json"))
    files = [f for f in index["files"] if f.get("env", {}).get("client", "required") != "unsupported"]
    shutil.rmtree(os.path.join(dest, "mods"), ignore_errors=True)
    for f in files:
        path = os.path.join(dest, f["path"])
        os.makedirs(os.path.dirname(path), exist_ok=True)
        data = urllib.request.urlopen(f["downloads"][0], timeout=120).read()
        if hashlib.sha512(data).hexdigest() != f["hashes"]["sha512"]:
            sys.exit(f"hash mismatch for {f['path']}, aborting")
        open(path, "wb").write(data)
        print(" +", f["path"])
    for prefix in ("overrides/", "client-overrides/"):
        for name in z.namelist():
            if name.startswith(prefix) and not name.endswith("/"):
                target = os.path.join(dest, name[len(prefix):])
                os.makedirs(os.path.dirname(target), exist_ok=True)
                open(target, "wb").write(z.read(name))
                print(" =", name[len(prefix):])
print(f"\nDone. Minecraft {index['dependencies']['minecraft']}, Fabric Loader {index['dependencies']['fabric-loader']}, {len(files)} files in {dest}")
