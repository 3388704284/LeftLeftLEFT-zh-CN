#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build the Simplified Chinese patch for Left! Left! LEFT! Playtest.
Requires: Python 3.10+ and UnityPy (pip install UnityPy)
Usage: python build_patch.py --game "D:\\steam\\steamapps\\common\\Left! Left! LEFT! Playtest" [--out build]
The script never writes to the game directory.
"""
import argparse, hashlib, json, os, shutil, struct, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
TEXT_MAP = PROJECT / "translation" / "zh_CN.json"
TEXTS = PROJECT / "source" / "texts.json"
TARGET_FONT_PATH_ID = 32  # ShareTechMono-Regular SDF, used by nearly all UI labels

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def replace_serialized_string(raw, old, new):
    old_b, new_b = old.encode("utf-8"), new.encode("utf-8")
    pat = struct.pack("<I", len(old_b)) + old_b
    pos = raw.find(pat)
    if pos < 0:
        raise RuntimeError("m_text not found: %r" % old)
    if raw.find(pat, pos + 1) >= 0:
        raise RuntimeError("m_text occurs more than once: %r" % old)
    old_total = 4 + len(old_b)
    new_total = 4 + len(new_b)
    old_pad = (-old_total) % 4
    new_pad = (-new_total) % 4
    if raw[pos + old_total:pos + old_total + old_pad] != b"\0" * old_pad:
        raise RuntimeError("unexpected string padding: %r" % old)
    return (raw[:pos] + struct.pack("<I", len(new_b)) + new_b + b"\0" * new_pad
            + raw[pos + old_total + old_pad:])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True)
    ap.add_argument("--out", default=str(PROJECT / "build"))
    args = ap.parse_args()
    game = Path(args.game)
    data = game / "LeftLeftLEFT_Data"
    out = Path(args.out)
    patch_data = out / "patch" / "LeftLeftLEFT_Data"
    if out.exists():
        shutil.rmtree(out)
    patch_data.mkdir(parents=True)
    os.makedirs(out / "source", exist_ok=True)

    if not (data / "resources.assets").exists():
        sys.exit("game data not found: %s" % data)
    tr = json.loads(TEXT_MAP.read_text(encoding="utf-8"))
    texts = json.loads(TEXTS.read_text(encoding="utf-8"))

    import UnityPy

    # 1) Switch the ShareTechMono TMP font asset to Dynamic OS and use Microsoft YaHei.
    # The family name has the same byte length as "Share Tech Mono", so no object resize is needed.
    env = UnityPy.load(str(data / "sharedassets0.assets"))
    obj = next(o for o in env.objects if o.path_id == TARGET_FONT_PATH_ID)
    raw = bytearray(obj.get_raw_data())
    old_family = b"Share Tech Mono"
    new_family = b"Microsoft YaHei"
    if raw.count(old_family) != 1 or len(old_family) != len(new_family):
        raise RuntimeError("unexpected TMP font family string")
    raw = raw.replace(old_family, new_family)
    path_pos = raw.find(b"C:\\Unity")
    if path_pos < 0:
        raise RuntimeError("TMP source path not found")
    path_len = struct.unpack("<I", raw[path_pos - 4:path_pos])[0]
    mode_pos = path_pos + path_len + (-(4 + path_len)) % 4
    if raw[mode_pos:mode_pos + 4] != struct.pack("<I", 1):
        raise RuntimeError("unexpected atlas population mode")
    raw[mode_pos:mode_pos + 4] = struct.pack("<I", 2)  # DynamicOS
    raw[mode_pos + 4] = 1  # InternalDynamicOS
    obj.set_raw_data(bytes(raw))
    env.save(out_path=str(patch_data))
    print("font: ShareTechMono-Regular SDF -> DynamicOS / Microsoft YaHei")

    # 2) Replace TMP text in the four scene files.
    for idx, fname in [(10, "level0"), (9, "level1"), (8, "level2"), (7, "level3")]:
        env = UnityPy.load(str(data / fname))
        objs = {o.path_id: o for o in env.objects}
        changed = 0
        for item in texts:
            if item["idx"] != idx:
                continue
            new = tr.get(item["text"], item["text"])
            if new == item["text"]:
                continue
            o = objs.get(item["id"])
            if o is None:
                raise RuntimeError("object missing: %s/%s" % (fname, item["id"]))
            raw = o.get_raw_data()
            o.set_raw_data(replace_serialized_string(raw, item["text"], new))
            changed += 1
        env.save(out_path=str(patch_data))
        print("%s: %d text components translated" % (fname, changed))

    # 3) Manifest with hashes.
    manifest = {"game": "Left! Left! LEFT! Playtest", "appid": 5425110, "steam_buildid": "26172243",
                "unity_version": "6000.3.16f1", "platform": "Windows x64",
                "tested_at": "2026-10-24", "files": {}}
    for fname in ["level0", "level1", "level2", "level3", "sharedassets0.assets"]:
        src = data / fname
        dst = patch_data / fname
        manifest["files"][fname] = {"original_sha256": sha256(src), "original_size": src.stat().st_size,
                                    "patched_sha256": sha256(dst), "patched_size": dst.stat().st_size}
    rp = data / "resources.assets"
    manifest["files"]["resources.assets"] = {"original_sha256": sha256(rp), "original_size": rp.stat().st_size,
                                                "untouched": True}
    (out / "PATCH_MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out / "source" / "texts.json").write_text(json.dumps(texts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out / "source" / "zh_CN.json").write_text(json.dumps(tr, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("built:", out)

if __name__ == "__main__":
    main()
