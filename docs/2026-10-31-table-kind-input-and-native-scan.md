# Table-kind caller and original lookup - 2026-10-31

Main ARM0207D708 is a new68-byte ordinary-C candidate. Replay: `python match_mechanics_save_20261031_lane_table_kind.py`. Normal and parent-directory Python `-I -S` runs reproduce canonical SHA ec9fff52dade5b8408a606ec7268fb4a6d34685adb52b49cbdbe55b113610bd4. The dedicated static profile retains the historical2.0/base compiler and complete O2 flags. Objects are checked against current genuine Metrowerks link provenance; source and native identities are separately pinned.

The historical near differed only in the final conditional-move ordering. A positive equality branch resolves it; a compact typed pointer view independently gives the same full native bytes. The preferred source also explicitly forwards the incoming word to0207D2C8, avoiding incidental R0 retention. No opcode/register forcing is used. Registration/module/ROM acceptance belongs to the integrator.

The native lookup reads the pointer at021C6BF4 and compares full incoming R0 with byte keys at eight-byte intervals. This proof supplies disposable table backing and executes the original getter with zero providers. After a matching nonzero key, the caller reads row+3:4 returns21,8 returns25,and all other values return0. Key0 returns0 only after lookup, without reading row+3.

The apparent native stop check compares a zero-extended byte withFFFFFFFF. ByteFF does not terminate the measured scan; a table startingFF still returns a later matching key. Absent keys, full-word keys outside the byte domain and null backing stop at logical/unmapped read guards. Five profiles on original/source give ten excluded stops, no actual-return credit or post-fault state claim. No handled empty-table/error path is established.

The1,287 supported pairs yield2,574 actual top returns and separately2,574 original getter returns. All256 kind bytes, keys0/1/127/128/255, prefix lengths0..2, duplicate-first selection and incoming-register variation are covered. All17 own instruction addresses are fetched. Every invocation uses fresh Unicorn state, requires actual return/SP/callee-saved restoration, checks ordered reads and rejects nonstack writes. Data remains unchanged.

Three whole compiled wrong-C controls change the byte offset, collapse raw21/25 returns to1,or skip lookup for key0. Their90 pairs yield180 real returns,38 independent rejections and52 observational positives. Early-zero is rejected by omitted native reads/getter return even where R0 stays0. Full vectors are deterministic gzip sidecars.

The pointer view describes measured accesses only. Table loading/extent/lifetime, ordinary scene reachability, semantic labels and save/bank chronology remain unproved. Original inputs, application files and accepted source remain untouched.
