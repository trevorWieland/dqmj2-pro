# Semantic investigation alongside matching

Byte matching establishes a compiler result under measured placement and interfaces. It does not establish a function's game-level meaning. Naming and documentation are independent work queues, following the evidence-driven methods in [pokebw2's naming workflow](https://github.com/fuddlesworth/pokebw2/blob/main/.agents/skills/name-symbols/SKILL.md) and [naming report](https://github.com/fuddlesworth/pokebw2/blob/main/tools/decomp/naming_report.py).

Investigate disjoint function families and their callers, callees, constants, tables, string references and consumed layouts. Record a proposed descriptive alias, the exact observed contract, evidence, confidence, unanswered questions and all affected identities. An offset-derived field name is appropriate while its meaning is unresolved. Do not widen fields to introduce an enum or invent game concepts from a suggestive branch pattern.

Keep canonical address identities stable. Document descriptive aliases first; migrate source names and interfaces only through a separate, fully revalidated change. Frozen accepted source and packet inputs must retain their hashes. A naming claim never increases matched bytes. A portable implementation, native platform replacement and hardware-facing matching source have different proof obligations.

`python naming_report.py --revision HEAD --output work/semantic-naming/report.json` scans selected committed sources and authored quoted includes. It lists placeholder arguments/locals, unknown or offset-derived identifiers, numeric switch cases and numeric comparisons. Comments and strings are excluded. These are investigation leads, not defects or a semantic-completion percentage. Shared-header findings may belong to multiple families; global totals deduplicate files.

An initial measured example is host ARM9 OV001 `0x021f1414`: its `u32(s32)` contract maps 0 to 0, 1 to 1 and every other argument to 2. OV001 `0x021f1438` consumes that value with a `u32(u32)` interface; values 0–2 forward constants 4–6 to main `0x02085320`, while other values are returned unchanged. This establishes a concrete value flow. The game-level purpose of that selector and the provider's role remain unresolved.

Another example separates storage facts from meaning: a 12-byte resource entry stride and an 8-byte consumed prefix can both be correct. Likewise, a scene field and cursor field may denote the same physical RAM word. Document the observed alias and consumed widths before choosing conceptual type boundaries or portable ownership.
