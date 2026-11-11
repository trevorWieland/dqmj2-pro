# Documentation index

Start with the [README](../README.md) for what the project is and the current numbers. This page
groups the rest by purpose. Every entry links the document itself; nothing here is required reading
in order.

## Mechanics and data

| document | what it answers |
| --- | --- |
| [data/index.json](data/index.json) | machine-readable data dictionary: tables, addresses, strides, field offsets, confidence |
| [data/species-and-rosters.md](data/species-and-rosters.md) | roster slot records and the species field |
| [data/skills.md](data/skills.md) | skill record layout (thresholds, action entries, features) |
| [data/items.md](data/items.md) | per-item descriptor fields proven by code |
| [data/save-format.md](data/save-format.md) | save money record, save bank header, saved monster record |
| [data/arm7-sound.md](data/arm7-sound.md) | ARM7 sound player and track views (WRAM structures) |
| [data/arm7-boot.md](data/arm7-boot.md) | measured ARM7 boot parameter blob |
| [data/misc-measured-data.md](data/misc-measured-data.md) | measured data blobs with unknown semantics |
| [2026-10-29-interpreted-script-inventory.md](2026-10-29-interpreted-script-inventory.md) | the SCR corpus census: 341 archives, 297 images, CFG scope |

## Scripts

| document | what it answers |
| --- | --- |
| [scripts/vm.md](scripts/vm.md) | the text-VM execution model: dispatch, opcodes, terminators, round-trip limits |
| [2026-10-29-interpreted-script-inventory.md](2026-10-29-interpreted-script-inventory.md) | interpreted SCR container and SYS dispatch (separate from the text VM) |

## Platform

| document | what it answers |
| --- | --- |
| [platform/contract.md](platform/contract.md) | hardware/SDK boundary, what a headless boot needs, and the blocker list |
| [2026-10-30-native-effect-policy-provenance.md](2026-10-30-native-effect-policy-provenance.md) | provenance for the status-byte writeback filter |

## Authoring and tooling

| document | what it answers |
| --- | --- |
| [source-units.md](source-units.md) | how `config/source_units.json` maps directories to compilation rules |
| [bytematch.md](bytematch.md) | how measurement works, badge scopes and the public number tables |
| [public-build.md](public-build.md) | building and checking the public tree without private inputs |
| [semantic-understanding.md](semantic-understanding.md) | how to do naming and meaning work without inventing |
| [2026-11-10-code-and-progress-policy.md](2026-11-10-code-and-progress-policy.md) | what counts as a contribution and what earns credit |
| [modding/example-title.md](modding/example-title.md) | the worked one-byte title patch with CRC fix-up |
| [closed-checkpoint-176.md](closed-checkpoint-176.md) | the historical closed-checkpoint proof scope (superseded as a status page) |

## Acceptance

| document | what it answers |
| --- | --- |
| [acceptance/2026-11-11-phase1.md](acceptance/2026-11-11-phase1.md) | independent end-to-end run of the five lens artifacts from a clean clone, with pass/fail and private-input map |

## Historical records

`docs/2026-*.md` are dated research and execution records, including explicit failures and open
questions. They are evidence of how the reconstruction reached its current state, not status pages;
the [README](../README.md) and the acceptance report are the current statements.
