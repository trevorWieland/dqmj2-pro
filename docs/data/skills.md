# Skills

Index entries: `skill_records`. Confidence: **proven-by-code** for layout, **unknown** for
the table base.

## Skill record — layout from `native_main_0207adb0`

`src/mechanics_save/20261029_skill_entry_member.c` is a matched accessor over a skill
record. Its own typedef is the layout evidence:

```c
typedef struct { u8 id; u8 inputs[3]; } NativeSkillAction;
typedef struct { u8 threshold[10]; NativeSkillAction actions[10]; u8 features[10]; } NativeSkillRecord;
```

| offset | width | type | name | confidence |
| --- | --- | --- | --- | --- |
| 0 | 10 | u8[10] | threshold | inferred |
| 10 + 4·i (i<10) | 1 | u8 | actions[i].id | proven-by-code |
| 11 + 4·i (i<10) | 3 | u8[3] | actions[i].inputs | proven-by-code |
| 50 | 10 | u8[10] | features | inferred |

Stride 60 bytes (10 + 10·4 + 10). The function body proves the indexing, not just the
typedef:

```c
NativeSkillAction *entry = record->actions + index;
if (entry->id != 0) return entry->inputs[member];
```

So `actions` is an array of 4-byte entries indexed by a skill slot, `id == 0` means
"empty slot", and `inputs` holds three per-member values. `threshold` and `features` are
marked **inferred**, not proven: `native_main_0207adb0` never reads them, they appear only
in the file's typedef.

## Base address

`unknown`. The record is passed by pointer; no matched function takes its address or
indexes a global array, so neither the base nor the record count is proven. The
`docs/data/index.json` entry therefore has `"address": "unknown"` and no dump is
possible for it.

## What is deliberately absent

Per-skill power/MP cost fields are **not** listed: nothing in the matched accessor reads
them, so they stay unknown even though they almost certainly exist somewhere in the
record.
