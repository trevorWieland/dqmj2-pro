# Relative-include transport repair for SSID280 — 2026-11-01

The source/compiler/native proof in the frozen161 packet passed its tests, but the integrator correctly refused registration: the repository dependency resolver follows quoted includes relative to source.parent and does not use compiler -i search paths. Its three dependency checks returned false. No native bytes or source credit were accepted through that failed preparation.

This replacement preserves161 and the shared resolver unchanged. A new source directory, src/arm7/20261101_wl_ssid280_include, changes exactly one quoted include to ../20261101_wl_counter504/wl_complete_types.h. Every other C byte, compiler flag, native target hash and all four shared-header hashes remain identical. The unchanged resolver now returns true for all three rows. provenance/arm7-sdk180-ssid280-include-repair-20261101.json records those checks and the complete frozen-original manifest identity.

The new180 source/profile/policy/compiler/matcher/validator paths replay the full proof independently. The validator also traverses quoted includes from each actual source parent and requires the complete four-file declared closure. It does not modify or replace the shared resolver.

Run python validate_arm7_sdk180_ssid280_20261101.py. This performs genuine source compilation and MWLD comparison for all280 initialized bytes,10,500 owned original/recompiled returns,32,706 source-linked reader returns,2,308 original fill returns and all79 original controls. Constructor return credit stays zero. The functions retain the typed u16/u8/pointer domains and limitations described in the earlier dated SSID280 source note; the272-byte inexact setter remains excluded.

The old161 source, report, producer, validator, profiles and headers remain frozen historical evidence. Adoption must select this replacement once and must not add duplicate byte, function, header, data, assembly or denominator credit. Integration and module acceptance remain with the coordinator.
