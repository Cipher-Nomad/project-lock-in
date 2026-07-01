#!/usr/bin/env python3
"""
apply_patch.py — Generic Project Lock In save-game patch applier.

Reads a patch file (see PATCH_PROTOCOL.md for format) and applies it to
data/*.yaml. Works for ANY session, not just one hardcoded session, as
long as the patch follows the strict schema.

Usage:
    python3 apply_patch.py <patch.yaml> <data-dir>

Patch file format:
    patch:
      player.yaml:
        set:
          player.overall.level: 1
          player.overall.experience.current: 110
        append:
          progress.missionsCompleted: [PF-M1-MSN2]
          mentalModelsUnlocked: [MM-006, MM-007]
        append_text:
          mentorAssessment.overall.understanding: null   # (not used here, example only)
        remove:
          quests.active: [PF-M1-MSN2]

Operations:
  set          - dot.path: value        -> overwrite value at path (creates path if needed)
  append       - dot.path: [items]      -> append each item to the list at path.
                                            Scalars are de-duplicated (skipped if already present).
                                            Dicts are always appended (sessions/entries are unique).
  append_text  - dot.path: "more text"  -> join onto existing string with "\n" (creates if absent)
  remove       - dot.path: [items]      -> remove each item from the list at path if present (no-op if absent)

After writing each file, it is re-parsed to confirm the YAML is valid.
If parsing fails, the write is rolled back and reported.
"""
import sys
import shutil
from pathlib import Path
from ruamel.yaml import YAML

yaml_rt = YAML()
yaml_rt.preserve_quotes = True
yaml_rt.width = 4096


def get_parent(data, dotted_path, create=True):
    parts = dotted_path.split(".")
    node = data
    for p in parts[:-1]:
        if p not in node or node[p] is None:
            if not create:
                raise KeyError(f"Path segment '{p}' not found in '{dotted_path}'")
            node[p] = {}
        node = node[p]
    return node, parts[-1]


def op_set(data, path, value):
    parent, key = get_parent(data, path)
    parent[key] = value


def op_append(data, path, items):
    parent, key = get_parent(data, path)
    if key not in parent or parent[key] is None:
        parent[key] = []
    target = parent[key]
    if not isinstance(items, list):
        items = [items]
    for item in items:
        if isinstance(item, dict):
            target.append(item)
        else:
            if item not in target:
                target.append(item)


def op_append_text(data, path, text):
    parent, key = get_parent(data, path)
    existing = parent.get(key)
    if existing:
        parent[key] = existing.rstrip("\n") + "\n" + text
    else:
        parent[key] = text


def op_remove(data, path, items):
    parent, key = get_parent(data, path, create=False)
    if key not in parent or parent[key] is None:
        return
    target = parent[key]
    if not isinstance(items, list):
        items = [items]
    for item in items:
        if item in target:
            target.remove(item)


def apply_file_patch(filepath: Path, ops: dict):
    backup = filepath.with_suffix(filepath.suffix + ".bak")
    shutil.copy(filepath, backup)

    with open(filepath) as f:
        data = yaml_rt.load(f)

    for path, value in (ops.get("set") or {}).items():
        op_set(data, path, value)
    for path, items in (ops.get("append") or {}).items():
        op_append(data, path, items)
    for path, text in (ops.get("append_text") or {}).items():
        op_append_text(data, path, text)
    for path, items in (ops.get("remove") or {}).items():
        op_remove(data, path, items)

    with open(filepath, "w") as f:
        yaml_rt.dump(data, f)

    # Validate: re-parse with a plain YAML loader to catch structural errors
    try:
        import yaml as pyyaml
        with open(filepath) as f:
            pyyaml.safe_load(f)
    except Exception as e:
        shutil.copy(backup, filepath)
        raise RuntimeError(f"Patch produced invalid YAML for {filepath.name}, rolled back. Error: {e}")

    backup.unlink()


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 apply_patch.py <patch.yaml> <data-dir>")
        sys.exit(1)

    patch_path = Path(sys.argv[1])
    data_dir = Path(sys.argv[2])

    with open(patch_path) as f:
        patch_doc = yaml_rt.load(f)

    patch = patch_doc.get("patch", {})
    if not patch:
        print("No 'patch:' key found at top level of patch file.")
        sys.exit(1)

    for filename, ops in patch.items():
        filepath = data_dir / filename
        if not filepath.exists():
            print(f"  SKIP {filename}: not found in {data_dir}")
            continue
        try:
            apply_file_patch(filepath, ops)
            print(f"  OK   {filename}")
        except Exception as e:
            print(f"  FAIL {filename}: {e}")
            sys.exit(1)

    print("Patch applied successfully.")


if __name__ == "__main__":
    main()