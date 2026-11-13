"""Verify the thirty main-module rows authored in the pass-2 lane.

Every row is recompiled with the source-unit rule its directory resolves to
(``src/main/r1_main_small`` -> p001 / mwccarm 2.0/base, ``src/main/r2_main_large``
-> p002 / mwccarm 2.0/sp1p5), its relocations are patched, and the whole measured
extent is compared with ``extract/arm9/arm9.bin`` at the row's ``binaryOffset``.

Compiler-runtime helpers (``_fflt``, ``_ffix`` ...) are linker-resolved symbols with
no address-bearing name. They are decoded from the measured call site the same way
``public_tools/repo_build.py`` recovers them and pinned as ``native_fn_<target>``.

For each row the check proves:

* the object's relocation table is exactly the pinned one - same offsets, kinds and
  externals - so a match cannot come from a hard-coded literal;
* every ``R_ARM_ABS32`` slot in the image equals the object's relocation target, so
  a pool word is checked against the image word, never against a symbol name;
* one whole-C negative control (a structural variant of the same source) compiles
  and differs from the image at the pinned offsets, so a match is not vacuous.

    python ops/verify_main_rows_2.py

Exit status 0 only when every positive check and every negative control passes.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / 'public_tools'))

import form_search  # noqa: E402
import source_units  # noqa: E402

MODULE = 'main'
LANE_DIRS = ('src/main/r1_main_small', 'src/main/r2_main_large')

# address, bytes, source, pinned relocations, control source, pinned control diff.
ROWS = (
    dict(address=0x02068590, bytes=4, source='native_main_02068590.c',
         relocations=[],
         control='#include "context.h"\nu32 native_main_02068590(u32 value) { return value + 1; }\n',
         controlDiff=(0, 1, 2, 3), dir='r1_main_small'),
    dict(address=0x02063fa0, bytes=12, source='native_main_02063fa0.c',
         relocations=[(8, 2, 'native_fn_02062650', 0)],
         control='/* Tail-call thunk: forward the call and return the callee result.\n   Unknowns: the callee 0x02062650 role and the thunk caller contract. */\n#include "context.h"\ntypedef unsigned char u8;\ntypedef signed char s8;\ntypedef unsigned short u16;\ntypedef signed short s16;\ntypedef unsigned int u32;\ntypedef signed int s32;\ntypedef unsigned long long u64;\ntypedef signed long long s64;\ntypedef float f32;\ntypedef double f64;\nextern u32 native_fn_02062650();\nu32 native_main_02063fa0(void) {\n    return (native_fn_02062650()) + 1;\n}',
         controlDiff=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), dir='r1_main_small'),
    dict(address=0x02063fac, bytes=12, source='native_main_02063fac.c',
         relocations=[(8, 2, 'native_fn_02062690', 0)],
         control='/* Tail-call thunk: forward the call and return the callee result.\n   Unknowns: the callee role and why a distinct thunk exists beside 0x02063fa0. */\n#include "context.h"\ntypedef unsigned char u8;\ntypedef signed char s8;\ntypedef unsigned short u16;\ntypedef signed short s16;\ntypedef unsigned int u32;\ntypedef signed int s32;\ntypedef unsigned long long u64;\ntypedef signed long long s64;\ntypedef float f32;\ntypedef double f64;\nextern u32 native_fn_02062690();\nu32 native_main_02063fac(void) {\n    return (native_fn_02062690()) + 1;\n}',
         controlDiff=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), dir='r1_main_small'),
    dict(address=0x020685bc, bytes=12, source='native_main_020685bc.c',
         relocations=[(8, 2, 'native_data_02063ea4', 0)],
         control='/* Tail-call thunk to the identity-profile pointer getter.\n   Unknowns: the profile block role and the caller contract. */\n#include "context.h"\nextern void *native_data_02063ea4(void);\nvoid *saved_identity_profile_pointer(void) { return (void *)((u8 *)(native_data_02063ea4()) + 1); }',
         controlDiff=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), dir='r1_main_small'),
    dict(address=0x020bf218, bytes=12, source='native_main_020bf218.c',
         relocations=[(8, 2, 'native_data_021d424c', 0)],
         control='/* Return the address of the 0x021d424c block.\n   Unknowns: the block contents and why the address is exposed. */\n#include "context.h"\ntypedef unsigned char u8;\ntypedef signed char s8;\ntypedef unsigned short u16;\ntypedef signed short s16;\ntypedef unsigned int u32;\ntypedef signed int s32;\ntypedef unsigned long long u64;\ntypedef signed long long s64;\ntypedef float f32;\ntypedef double f64;\nextern u8 native_data_021d424c[];\nu32 native_main_020bf218(void) {\n    return ((u32) native_data_021d424c) + 1;\n}',
         controlDiff=(0, 4, 5, 6, 7, 8, 9, 10, 11), dir='r1_main_small'),
    dict(address=0x020bf4ec, bytes=16, source='native_main_020bf4ec.c',
         relocations=[(12, 2, 'native_data_020e2cc0', 0)],
         control='/* Indexed word read from the 0x020e2cc0 table.\n   Unknowns: the table element meaning and its bounds. */\n#include "context.h"\ntypedef unsigned char u8;\ntypedef signed char s8;\ntypedef unsigned short u16;\ntypedef signed short s16;\ntypedef unsigned int u32;\ntypedef signed int s32;\ntypedef unsigned long long u64;\ntypedef signed long long s64;\ntypedef float f32;\ntypedef double f64;\nextern u8 native_data_020e2cc0[];\nu32 native_main_020bf4ec(s32 arg0) {\n    return (*(u32 *)(native_data_020e2cc0 + (arg0 * 4))) + 1;\n}',
         controlDiff=(0, 8, 9, 10, 11, 12, 13, 14, 15), dir='r1_main_small'),
    dict(address=0x020455c8, bytes=32, source='native_main_020455c8.c',
         relocations=[(28, 2, 'native_data_020f6ae4', 0)],
         control='/* Clear the requested bits of a global control word.\n   Unknowns: the block role and the bit meanings. */\n#include "context.h"\ntypedef unsigned short int u16;\nextern u16 native_data_020f6ae4;\nvoid native_main_020455c8(int timerNum);\nvoid native_main_020455c8 (int timerNum)\n{\n    native_data_020f6ae4 |= ~(1 << timerNum);\n}',
         controlDiff=(18, 19), dir='r1_main_small'),
    dict(address=0x02045b00, bytes=76, source='native_main_02045b00.c',
         relocations=[(32, 1, 'native_fn_02003e54', -8), (40, 1, 'native_fn_02003ea8', -8), (48, 1, 'native_fn_02003efc', -8), (56, 1, 'native_fn_02003ff4', -8), (64, 1, 'native_fn_02008430', -8)],
         control='/* Four-way dispatch on a small selector, defaulting to 0x02008430.\n   Unknowns: what the four branches produce and the selector domain. */\n#include "context.h"\nvoid native_fn_02008430(void);\nvoid native_fn_02004e58(const void *, u32, u32);\nvoid native_fn_02004f18(const void *, u32, u32);\nvoid native_fn_02004fd8(const void *, u32, u32);\nvoid native_fn_02005098(const void *, u32, u32);\nvoid native_fn_02004eb8(const void *, u32, u32);\nvoid native_fn_02004f78(const void *, u32, u32);\nvoid native_fn_02005038(const void *, u32, u32);\nvoid native_fn_020050f8(const void *, u32, u32);\nvoid *native_fn_020040ec(void);\nvoid *native_fn_02004140(void);\nvoid *native_fn_02004194(void);\nvoid *native_fn_02004224(void);\nvoid *native_fn_02004120(void);\nvoid *native_fn_02004174(void);\nvoid *native_fn_020041e4(void);\nvoid *native_fn_0200427c(void);\nvoid native_fn_02004b58(const void *, u32, u32);\nvoid native_fn_02004c18(const void *, u32, u32);\nvoid native_fn_02004cd8(const void *, u32, u32);\nvoid native_fn_02004d98(const void *, u32, u32);\nvoid native_fn_02004bb8(const void *, u32, u32);\nvoid native_fn_02004c78(const void *, u32, u32);\nvoid native_fn_02004d38(const void *, u32, u32);\nvoid native_fn_02004df8(const void *, u32, u32);\nvoid native_fn_02007308(const void *, u32);\n\nvoid *native_main_02045b00(u32 arg0) {\n    switch (arg0) {\n    case 0:\n        return native_fn_02003e54();\n    case 1:\n        return native_fn_02003ea8();\n    case 2:\n        return native_fn_02003efc();\n    case 3:\n        return native_fn_02003ff4();\n    default:\n        native_fn_02008470();\n        return 0U;\n    }\n}',
         controlDiff=(64,), dir='r1_main_small'),
    dict(address=0x02045b4c, bytes=76, source='native_main_02045b4c.c',
         relocations=[(32, 1, 'native_fn_02003e88', -8), (40, 1, 'native_fn_02003edc', -8), (48, 1, 'native_fn_02003f80', -8), (56, 1, 'native_fn_02004078', -8), (64, 1, 'native_fn_02008430', -8)],
         control='/* Four-way dispatch on a small selector, defaulting to 0x02008430.\n   Unknowns: what the four branches produce and the selector domain. */\n#include "context.h"\nvoid native_fn_02008430(void);\nvoid native_fn_02004e58(const void *, u32, u32);\nvoid native_fn_02004f18(const void *, u32, u32);\nvoid native_fn_02004fd8(const void *, u32, u32);\nvoid native_fn_02005098(const void *, u32, u32);\nvoid native_fn_02004eb8(const void *, u32, u32);\nvoid native_fn_02004f78(const void *, u32, u32);\nvoid native_fn_02005038(const void *, u32, u32);\nvoid native_fn_020050f8(const void *, u32, u32);\nvoid *native_fn_020040ec(void);\nvoid *native_fn_02004140(void);\nvoid *native_fn_02004194(void);\nvoid *native_fn_02004224(void);\nvoid *native_fn_02004120(void);\nvoid *native_fn_02004174(void);\nvoid *native_fn_020041e4(void);\nvoid *native_fn_0200427c(void);\nvoid native_fn_02004b58(const void *, u32, u32);\nvoid native_fn_02004c18(const void *, u32, u32);\nvoid native_fn_02004cd8(const void *, u32, u32);\nvoid native_fn_02004d98(const void *, u32, u32);\nvoid native_fn_02004bb8(const void *, u32, u32);\nvoid native_fn_02004c78(const void *, u32, u32);\nvoid native_fn_02004d38(const void *, u32, u32);\nvoid native_fn_02004df8(const void *, u32, u32);\nvoid native_fn_02007308(const void *, u32);\n\nvoid *native_main_02045b4c(u32 arg0) {\n    switch (arg0) {\n    case 0:\n        return native_fn_02003e88();\n    case 1:\n        return native_fn_02003edc();\n    case 2:\n        return native_fn_02003f80();\n    case 3:\n        return native_fn_02004078();\n    default:\n        native_fn_02008470();\n        return 0U;\n    }\n}',
         controlDiff=(64,), dir='r1_main_small'),
    dict(address=0x0204dd18, bytes=76, source='native_main_0204dd18.c',
         relocations=[(12, 1, 'native_fn_0221a0d8', -8), (16, 1, 'native_fn_02025a28', -8)],
         control='/* Scale a parameter into the context slot and advance the record cursor.\n   Unknowns: the parameter meaning, the bank/record roles and the caller contract. */\n#include "context.h"\ntypedef struct CommandRecord {\n    u32 position;\n    u8 reserved[3];\n    u8 status;\n    u8 padding[0x108];\n} CommandRecord;\ntypedef struct Context {\n    u8 reserved[3];\n    u8 bank;\n    u32 reservedWords[3];\n    float parameters[8];\n    u8 padding[0x440];\n    CommandRecord records[];\n} Context;\ntypedef struct Instruction {\n    u32 opcode;\n    u32 advance;\n    u8 payload[];\n} Instruction;\nextern u32 native_fn_02064000(void);\nextern void native_fn_02064038(u32);\nextern void native_fn_02040820(void);\nextern int native_fn_ov000_021e9aa0(void);\nextern void native_fn_0204071c(int);\nextern void native_fn_ov000_02208dcc(void);\nextern void native_fn_ov000_02209670(void);\nextern void native_fn_ov000_022096bc(void);\nextern void native_fn_ov000_02209554(void);\nextern void native_fn_0205e61c(void);\nextern void native_fn_0205e520(void);\nextern void native_fn_ov000_021f4110(int, u8);\nextern void native_fn_ov000_021f4174(int, int);\nextern int native_fn_0205c668(int, int);\nextern int native_fn_ov000_021e96cc(int, int, signed char, int);\nextern int native_fn_ov000_021e31f0(int, int);\nextern int native_fn_ov000_021e9738(int, int, int);\nextern int native_fn_0205d718(int);\nextern int native_fn_ov000_02221444(const void *);\nextern void native_fn_0205e3f0(u8);\nextern void native_fn_ov000_021e9df4(u8);\nextern void native_fn_ov000_021e9e4c(u8, u8);\nextern int native_fn_ov000_021e9794(int);\nextern void native_fn_ov000_021f3e5c(int, int *);\nextern int native_fn_ov000_021f3f68(int);\nextern void native_fn_ov000_021f3dac(int, int);\nextern int native_fn_ov000_021f3ec4(int, int);\nextern void native_fn_ov000_021f3fec(int, int, int, int);\nextern void native_fn_ov000_021e71a4(int, int);\n#define TO_FIXED(value) ((int)((value) > 0.0f ? 0.5f + 4096.0f * (value) : 4096.0f * (value) - 0.5f))\nextern void native_fn_0205bd6c(int,int,int,int,int,int,int,int,int,int,int,int,int,int,int,int,int,int);\nextern void native_fn_ov000_021e7940(int);\nextern void native_fn_020404f0(int);\nextern int native_fn_ov000_02210b98(int,int);\nextern u32 native_fn_02040424(void);\nextern void native_fn_0205e73c(int);\nextern int native_fn_ov000_021e7b9c(int);\nextern void native_fn_ov000_021e0bc4(int);\nextern int native_fn_0205c1e8(void);\nextern void native_fn_ov000_021e7bb0(int,int);\nextern int native_fn_0205f35c(int,int);\nextern void native_fn_0205f4bc(int,int,int);\nextern void native_fn_0205f404(int,int);\nextern void native_fn_0205f6a0(int,int,int);\n\nvoid native_main_0204dd18(Context *context, const Instruction *instruction)\n{\n    context->parameters[0] = (float)native_fn_0221a0d8();\n    context->records[context->bank].position += instruction->advance;\n    context->records[context->bank].status = 0;\n}',
         controlDiff=(25, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 40, 41, 42, 44, 46, 47, 48, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 69), dir='r2_main_large'),
    dict(address=0x020501f4, bytes=80, source='native_main_020501f4.c',
         relocations=[(12, 1, 'native_fn_02040424', -8), (16, 1, 'native_fn_021df3d0', -8), (20, 1, 'native_fn_02025a70', -8)],
         control='/* Scale a parameter into the context slot and advance the record cursor.\n   Unknowns: the parameter meaning, the bank/record roles and the caller contract. */\n#include "context.h"\ntypedef struct CommandRecord {\n    u32 position;\n    u8 reserved[3];\n    u8 status;\n    u8 padding[0x104];\n} CommandRecord;\ntypedef struct Context {\n    u8 reserved[3];\n    u8 bank;\n    u32 reservedWords[3];\n    float parameters[8];\n    u8 padding[0x440];\n    CommandRecord records[];\n} Context;\ntypedef struct Instruction {\n    u32 opcode;\n    u32 advance;\n    u8 payload[];\n} Instruction;\nextern u32 native_fn_02064000(void);\nextern void native_fn_02064038(u32);\nextern void native_fn_02040820(void);\nextern int native_fn_ov000_021e9aa0(void);\nextern void native_fn_0204071c(int);\nextern void native_fn_ov000_02208dcc(void);\nextern void native_fn_ov000_02209670(void);\nextern void native_fn_ov000_022096bc(void);\nextern void native_fn_ov000_02209554(void);\nextern void native_fn_0205e61c(void);\nextern void native_fn_0205e520(void);\nextern void native_fn_ov000_021f4110(int, u8);\nextern void native_fn_ov000_021f4174(int, int);\nextern int native_fn_0205c668(int, int);\nextern int native_fn_ov000_021e96cc(int, int, signed char, int);\nextern int native_fn_ov000_021e31f0(int, int);\nextern int native_fn_ov000_021e9738(int, int, int);\nextern int native_fn_0205d718(int);\nextern int native_fn_ov000_02221444(const void *);\nextern void native_fn_0205e3f0(u8);\nextern void native_fn_ov000_021e9df4(u8);\nextern void native_fn_ov000_021e9e4c(u8, u8);\nextern int native_fn_ov000_021e9794(int);\nextern void native_fn_ov000_021f3e5c(int, int *);\nextern int native_fn_ov000_021f3f68(int);\nextern void native_fn_ov000_021f3dac(int, int);\nextern int native_fn_ov000_021f3ec4(int, int);\nextern void native_fn_ov000_021f3fec(int, int, int, int);\nextern void native_fn_ov000_021e71a4(int, int);\n#define TO_FIXED(value) ((int)((value) > 0.0f ? 0.5f + 4096.0f * (value) : 4096.0f * (value) - 0.5f))\nextern void native_fn_02029c88(u8, u8, u8);\nextern int native_fn_ov000_02214a54(void);\nextern int native_fn_ov000_02214acc(void);\nextern u32 native_fn_0205bf9c(void);\nextern void native_fn_0205bf7c(u8);\nextern void native_fn_ov000_02218c24(u16);\nextern void native_fn_ov000_02218cb4(u16);\nextern void native_fn_ov000_02218d20(u16, int);\nextern int native_fn_0205e844(int);\nextern void native_fn_02040534(u32);\nextern void native_fn_02040518(u32);\nextern u32 native_fn_0205d8a4(u8);\nextern u32 native_fn_020d3fd0(void);\nextern void native_fn_020d3fbc(u8);\nextern int native_fn_020d3dc0(int, u8);\nextern u32 native_fn_020d3e80(int, u8);\nextern u32 native_fn_020d3738(void);\nextern int native_fn_020d38f0(u32);\nextern int native_fn_020d37f0(void);\nextern u32 native_fn_0205c278(void);\nextern void native_fn_ov000_022092b0(u8);\nextern u32 native_fn_ov000_02209244(const void *);\nextern void native_fn_ov000_022092e0(u32);\nextern const void *native_fn_0205dc70(int, int, u16);\nextern void native_fn_ov000_022093ec(u8, int);\nextern void native_fn_ov000_022094e8(u8);\n\nvoid native_main_020501f4(Context *context, const Instruction *instruction)\n{\n    context->parameters[0] = (float)native_fn_021df7d0(native_fn_02040424());\n    context->records[context->bank].position += instruction->advance;\n    context->records[context->bank].status = 0;\n}',
         controlDiff=(17,), dir='r2_main_large'),
    dict(address=0x02054608, bytes=84, source='native_main_02054608.c',
         relocations=[(16, 1, 'native_fn_020259b4', -8), (20, 1, 'native_fn_021e767c', -8), (24, 1, 'native_fn_02025a28', -8)],
         control='/* Scale a parameter into the context slot and advance the record cursor.\n   Unknowns: the parameter meaning, the bank/record roles and the caller contract. */\n#include "context.h"\ntypedef struct CommandRecord {\n    u32 position;\n    u8 reserved[3];\n    u8 status;\n    u8 padding[0x108];\n} CommandRecord;\ntypedef struct Context {\n    u8 reserved[3];\n    u8 bank;\n    u32 reservedWords[3];\n    float parameters[8];\n    u8 padding[0x440];\n    CommandRecord records[];\n} Context;\ntypedef struct Instruction {\n    u32 opcode;\n    u32 advance;\n    u8 payload[];\n} Instruction;\nextern u32 native_fn_02064000(void);\nextern void native_fn_02064038(u32);\nextern void native_fn_02040820(void);\nextern int native_fn_ov000_021e9aa0(void);\nextern void native_fn_0204071c(int);\nextern void native_fn_ov000_02208dcc(void);\nextern void native_fn_ov000_02209670(void);\nextern void native_fn_ov000_022096bc(void);\nextern void native_fn_ov000_02209554(void);\nextern void native_fn_0205e61c(void);\nextern void native_fn_0205e520(void);\nextern void native_fn_ov000_021f4110(int, u8);\nextern void native_fn_ov000_021f4174(int, int);\nextern int native_fn_0205c668(int, int);\nextern int native_fn_ov000_021e96cc(int, int, signed char, int);\nextern int native_fn_ov000_021e31f0(int, int);\nextern int native_fn_ov000_021e9738(int, int, int);\nextern int native_fn_0205d718(int);\nextern int native_fn_ov000_02221444(const void *);\nextern void native_fn_0205e3f0(u8);\nextern void native_fn_ov000_021e9df4(u8);\nextern void native_fn_ov000_021e9e4c(u8, u8);\nextern int native_fn_ov000_021e9794(int);\nextern void native_fn_ov000_021f3e5c(int, int *);\nextern int native_fn_ov000_021f3f68(int);\nextern void native_fn_ov000_021f3dac(int, int);\nextern int native_fn_ov000_021f3ec4(int, int);\nextern void native_fn_ov000_021f3fec(int, int, int, int);\nextern void native_fn_ov000_021e71a4(int, int);\n#define TO_FIXED(value) ((int)((value) > 0.0f ? 0.5f + 4096.0f * (value) : 4096.0f * (value) - 0.5f))\ntypedef short s16;\ntypedef struct RecordEntry { u8 value; u8 reserved; } RecordEntry;\ntypedef struct NativeRecord {\n    u8 reserved[0x14];\n    u32 field14;\n    s16 field18;\n    u8 field1a;\n    u8 field1b;\n    u8 reserved1c[2];\n    u8 field1e;\n    u8 reserved1f[0x5b];\n    RecordEntry entries[5];\n} NativeRecord;\nextern NativeRecord *native_fn_02062b00(void);\nextern u32 native_fn_02062a68(int);\nextern u32 native_fn_02062a78(int);\nextern NativeRecord *native_fn_02062a50(int);\nextern NativeRecord *native_fn_02062a88(int);\nextern int native_fn_02044dc4(s16, u8);\nextern int native_fn_02044cdc(s16);\nextern void native_fn_ov000_02229f68(int);\nextern void native_fn_ov000_02229fdc(int);\nextern void native_fn_ov000_0222a050(int);\nextern void native_fn_ov000_0222a0c4(int);\nextern void native_fn_ov000_0222a138(int);\nextern void native_fn_ov000_02229fb0(int);\nextern void native_fn_ov000_0222a024(int);\nextern void native_fn_ov000_0222a098(int);\nextern void native_fn_ov000_0222a10c(int);\nextern void native_fn_ov000_0222a17c(int);\nextern void native_fn_ov000_021e8dc0(int, int);\nextern void native_fn_ov000_021e8e6c(int, int);\nextern void native_fn_ov000_021e8cb4(int, int, int, int);\nextern void native_fn_ov000_021e8e1c(int, int);\nextern void native_fn_ov000_021e8e44(int, int);\nextern u32 native_fn_02063d6c(void);\nextern void native_fn_02008140(u32);\nextern int native_fn_ov000_021f3e28(int, int, int);\nextern int native_fn_ov000_021e770c(const void *);\nextern int native_fn_ov000_021f3b4c(int);\n\nvoid native_main_02054608(Context *context, const Instruction *instruction)\n{\n    context->parameters[0] = (float)native_fn_021e767c((int)context->parameters[0]);\n    context->records[context->bank].position += instruction->advance;\n    context->records[context->bank].status = 0;\n}',
         controlDiff=(33, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 48, 49, 50, 52, 54, 55, 56, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 77), dir='r2_main_large'),
    dict(address=0x0204ed3c, bytes=276, source='native_main_0204ed3c.c',
         relocations=[(24, 1, 'native_fn_0202537c', -8), (40, 1, 'native_fn_02025ab8', -8), (52, 1, 'native_fn_02024e0c', -8), (60, 1, 'native_fn_02025ab8', -8), (68, 1, 'native_fn_02025ca4', -8), (72, 1, 'native_fn_020259b4', -8), (88, 1, 'native_fn_0202537c', -8), (104, 1, 'native_fn_02025ab8', -8), (116, 1, 'native_fn_02024e0c', -8), (124, 1, 'native_fn_02025ab8', -8), (132, 1, 'native_fn_02025ca4', -8), (136, 1, 'native_fn_020259b4', -8), (152, 1, 'native_fn_0202537c', -8), (168, 1, 'native_fn_02025ab8', -8), (180, 1, 'native_fn_02024e0c', -8), (188, 1, 'native_fn_02025ab8', -8), (196, 1, 'native_fn_02025ca4', -8), (200, 1, 'native_fn_020259b4', -8), (212, 1, 'native_fn_021d8abc', -8)],
         control='/* Convert three parameters to fixed point and publish them to a helper.\n   Unknowns: the fixed-point consumer and the parameter meanings. */\n#include "context.h"\ntypedef struct CommandRecord {\n    u32 position;\n    u8 reserved[3];\n    u8 status;\n    u8 padding[0x108];\n} CommandRecord;\ntypedef struct Context {\n    u8 reserved[3];\n    u8 bank;\n    u32 reservedWords[3];\n    float parameters[8];\n    u8 padding[0x440];\n    CommandRecord records[];\n} Context;\ntypedef struct Instruction {\n    u32 opcode;\n    u32 advance;\n    u8 payload[];\n} Instruction;\nextern u32 native_fn_02064000(void);\nextern void native_fn_02064038(u32);\nextern void native_fn_02040820(void);\nextern int native_fn_ov000_021e9aa0(void);\nextern void native_fn_0204071c(int);\nextern void native_fn_ov000_02208dcc(void);\nextern void native_fn_ov000_02209670(void);\nextern void native_fn_ov000_022096bc(void);\nextern void native_fn_ov000_02209554(void);\nextern void native_fn_0205e61c(void);\nextern void native_fn_0205e520(void);\nextern void native_fn_ov000_021f4110(int, u8);\nextern void native_fn_ov000_021f4174(int, int);\nextern int native_fn_0205c668(int, int);\nextern int native_fn_ov000_021e96cc(int, int, signed char, int);\nextern int native_fn_ov000_021e31f0(int, int);\nextern int native_fn_ov000_021e9738(int, int, int);\nextern int native_fn_0205d718(int);\nextern int native_fn_ov000_02221444(const void *);\nextern void native_fn_0205e3f0(u8);\nextern void native_fn_ov000_021e9df4(u8);\nextern void native_fn_ov000_021e9e4c(u8, u8);\nextern int native_fn_ov000_021e9794(int);\nextern void native_fn_ov000_021f3e5c(int, int *);\nextern int native_fn_ov000_021f3f68(int);\nextern void native_fn_ov000_021f3dac(int, int);\nextern int native_fn_ov000_021f3ec4(int, int);\nextern void native_fn_ov000_021f3fec(int, int, int, int);\nextern void native_fn_ov000_021e71a4(int, int);\n#define TO_FIXED(value) ((int)((value) > 0.0f ? 0.5f + 4096.0f * (value) : 4096.0f * (value) - 0.5f))\nextern void native_fn_ov000_021e8c80(int, int);\nextern void native_fn_ov000_021e8d58(int, int, int);\nextern void native_fn_ov000_021e8d98(int, u8);\nextern void native_fn_ov000_021e8c34(int, u8);\nextern void native_fn_020c5750(short);\nextern void native_fn_ov000_02209d94(int,int,int);\nextern void native_fn_ov000_02210f20(int, int, int);\nextern u32 native_fn_ov000_02210880(int, u8);\nextern u32 native_fn_ov000_022108dc(int, u8);\nextern void native_fn_ov000_02210344(int, u8);\nextern void native_fn_ov000_0220ef24(int, u8);\nextern u32 native_fn_ov000_0220a060(int);\nextern void native_fn_02048094(int,int);\nextern void native_fn_ov000_0221a0bc(int);\nextern int native_fn_ov000_021e0d78(int,int,int);\nextern void native_fn_02047d40(int);\nextern int native_fn_ov000_02213cdc(int);\nextern int native_fn_ov000_021e5594(int);\nextern void native_fn_ov000_021e577c(int,u8);\nextern void native_fn_ov000_02219404(u8);\nextern void native_fn_0204b818(short,short);\nextern void native_fn_0204b79c(void);\nextern void native_fn_ov000_021e0b88(int);\nextern void native_fn_0205c218(u32,u8);\nextern void native_fn_ov000_021d8a08(int);\nextern void native_fn_020404f0(int);\ntypedef struct Words3 { int words[3]; } Words3;\ntypedef struct PrefixHalfwords { unsigned short field0; unsigned short field2; } PrefixHalfwords;\ntypedef struct OpaqueFields { u8 reserved0[0x70]; Words3 field70; u8 reserved1[0x94]; Words3 field110; } OpaqueFields;\nextern void native_fn_ov000_0220a078(int);\nextern PrefixHalfwords * native_fn_020c56b4(int);\nextern void native_fn_ov000_02210908(int);\nextern int native_fn_02041bdc(void);\nextern void native_fn_0204dd64(int);\nextern void native_fn_0205e3c0(short);\nextern void native_fn_020404f0(int);\nextern const Words3 * ov000_saved_world_position_get_021e07b8(int);\nextern const Words3 * native_fn_ov000_021e5744(int);\nextern void native_fn_ov000_021e0b88(int);\nextern int native_fn_0202818c(const Words3 *,const Words3 *);\nextern int native_fn_ov000_021e0d78(int,int,int);\nextern void native_fn_ov000_021d8b10(u8 *);\nextern u8 * native_fn_ov000_0221220c(short,short);\nextern const Words3 * native_fn_ov000_021d8aa0(int);\nextern const Words3 * native_fn_ov000_021d8a50(int);\nextern void native_fn_ov000_021d8c80(int);\nextern void native_fn_ov000_021d8a08(int);\nextern void native_fn_ov000_021d8a28(void);\nextern Words3 * native_fn_ov000_02210f08(int);\nextern void native_fn_02048034(int,int);\nextern int native_fn_0205dc70(u8,u8,unsigned short);\nextern void native_fn_ov000_021e0b60(int,int,int);\nextern OpaqueFields * native_fn_ov000_021e07ac(void);\ntypedef struct OpaqueState { u8 reserved0[0x98]; int field98; } OpaqueState;\nextern int native_fn_ov000_021e5528(int,int,int,int,int,u8);\nextern void native_fn_ov000_021e2ce8(const Words3 *,int);\nextern void native_fn_ov000_021d8a6c(const Words3 *);\nextern void native_fn_0205bf2c(int);\nextern void native_fn_0205bdfc(u8);\nextern void native_fn_0205bf04(int);\nextern void native_fn_0205be4c(int);\nextern void native_fn_0205be74(const Words3 *);\nextern void native_fn_0205bea4(int);\nextern void native_fn_0205bed4(int);\nextern OpaqueState * native_fn_ov000_021d8a44(void);\n\nvoid native_main_0204ed3c(Context *context,const Instruction *instruction)\n{\n    Words3 words;\n    words.words[0]=TO_FIXED(context->parameters[0]);\n    words.words[1]=TO_FIXED(context->parameters[1]);\n    words.words[2]=TO_FIXED(context->parameters[2]);\n    native_fn_021d8abc(&words);\n    context->records[context->bank].position+=instruction->advance;\n    context->records[context->bank].status=0;\n}',
         controlDiff=(217, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 232, 233, 234, 236, 238, 239, 240, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 261), dir='r2_main_large'),
    dict(address=0x02052720, bytes=288, source='native_main_02052720.c',
         relocations=[(20, 1, 'native_fn_0202537c', -8), (36, 1, 'native_fn_02025ab8', -8), (48, 1, 'native_fn_02024e0c', -8), (56, 1, 'native_fn_02025ab8', -8), (64, 1, 'native_fn_02025ca4', -8), (68, 1, 'native_fn_020259b4', -8), (84, 1, 'native_fn_0202537c', -8), (100, 1, 'native_fn_02025ab8', -8), (112, 1, 'native_fn_02024e0c', -8), (120, 1, 'native_fn_02025ab8', -8), (128, 1, 'native_fn_02025ca4', -8), (132, 1, 'native_fn_020259b4', -8), (148, 1, 'native_fn_0202537c', -8), (164, 1, 'native_fn_02025ab8', -8), (176, 1, 'native_fn_02024e0c', -8), (184, 1, 'native_fn_02025ab8', -8), (192, 1, 'native_fn_02025ca4', -8), (196, 1, 'native_fn_020259b4', -8), (208, 1, 'native_fn_020259e8', -8), (228, 1, 'native_fn_021e6114', -8)],
         control='/* Convert parameters to fixed point, publish them and advance the record.\n   Unknowns: the fixed-point consumer and the record bank roles. */\n#include "context.h"\ntypedef struct CommandRecord {\n    u32 position;\n    u8 reserved[3];\n    u8 status;\n    u8 padding[0x104];\n} CommandRecord;\ntypedef struct Context {\n    u8 reserved[3];\n    u8 bank;\n    u32 reservedWords[3];\n    float parameters[8];\n    u8 padding[0x440];\n    CommandRecord records[];\n} Context;\ntypedef struct Instruction {\n    u32 opcode;\n    u32 advance;\n    u8 payload[];\n} Instruction;\nextern u32 native_fn_02064000(void);\nextern void native_fn_02064038(u32);\nextern void native_fn_02040820(void);\nextern int native_fn_ov000_021e9aa0(void);\nextern void native_fn_0204071c(int);\nextern void native_fn_ov000_02208dcc(void);\nextern void native_fn_ov000_02209670(void);\nextern void native_fn_ov000_022096bc(void);\nextern void native_fn_ov000_02209554(void);\nextern void native_fn_0205e61c(void);\nextern void native_fn_0205e520(void);\nextern void native_fn_ov000_021f4110(int, u8);\nextern void native_fn_ov000_021f4174(int, int);\nextern int native_fn_0205c668(int, int);\nextern int native_fn_ov000_021e96cc(int, int, signed char, int);\nextern int native_fn_ov000_021e31f0(int, int);\nextern int native_fn_ov000_021e9738(int, int, int);\nextern int native_fn_0205d718(int);\nextern int native_fn_ov000_02221444(const void *);\nextern void native_fn_0205e3f0(u8);\nextern void native_fn_ov000_021e9df4(u8);\nextern void native_fn_ov000_021e9e4c(u8, u8);\nextern int native_fn_ov000_021e9794(int);\nextern void native_fn_ov000_021f3e5c(int, int *);\nextern int native_fn_ov000_021f3f68(int);\nextern void native_fn_ov000_021f3dac(int, int);\nextern int native_fn_ov000_021f3ec4(int, int);\nextern void native_fn_ov000_021f3fec(int, int, int, int);\nextern void native_fn_ov000_021e71a4(int, int);\n#define TO_FIXED(value) ((int)((value) > 0.0f ? 0.5f + 4096.0f * (value) : 4096.0f * (value) - 0.5f))\ntypedef struct NativeVec3 { int x; int y; int z; } NativeVec3;\ntypedef struct CommandContext {\n    u8 reserved[3];\n    u8 bank;\n    u32 reservedWords[3];\n    float parameters[16];\n    u8 padding[0x420];\n    CommandRecord records[];\n} CommandContext;\ntypedef struct TargetRecord {\n    u8 reserved00[9];\n    u8 state09;\n    u8 reserved0a[0x66];\n    u32 slot70[3];\n    u8 reserved7c[0x0c];\n    u32 slot88[3];\n    u8 reserved94[0x24];\n} TargetRecord;\nextern int native_fn_0205f2d8(int);\nextern int native_fn_0205f45c(int);\nextern void native_fn_0205e814(int,int,int);\nextern void native_fn_0205f7e0(int,int,int);\nextern void native_fn_0205f6a0(int,int,int);\nextern void native_fn_ov000_021e582c(u16,const NativeVec3 *,const NativeVec3 *,const NativeVec3 *,const NativeVec3 *,u8);\nextern void native_fn_ov000_021e58a0(u16);\nextern int native_fn_ov000_0221221c(int,int,int);\nextern void native_fn_ov000_022124e8(int,int,int);\nextern int native_fn_ov000_0221225c(int,int,int);\nextern void native_fn_ov000_02212518(int,int,int);\nextern void native_fn_ov000_0221229c(int,int,int);\nextern void native_fn_ov000_02211188(int,const NativeVec3 *,const NativeVec3 *,int);\nextern void native_fn_ov000_02212480(int,int,int);\nextern void native_fn_ov000_022124b4(int,int,int);\nextern void native_fn_ov000_022122dc(int,int,const NativeVec3 *,int);\nextern void native_fn_ov000_021e77f8(int,NativeVec3 *);\nextern int native_fn_ov000_021e784c(int);\nextern TargetRecord *native_fn_ov000_0221220c(short,short);\ntypedef struct CountRecord { u8 reserved[0x18]; short slot18; } CountRecord;\nextern void native_fn_ov000_0220a040(int,u8);\nextern void native_fn_ov000_021e5c88(u8,int,const void *,u8);\nextern int native_fn_02028158(int);\nextern void native_fn_ov000_021e5ec0(u8,int);\nextern void native_fn_ov000_021e5ffc(int,int,int,u8);\nextern int native_fn_0203d294(int);\nextern int native_fn_0206344c(void);\nextern int native_fn_0206349c(void);\nextern int native_fn_020629e0(void);\nextern int native_fn_02062aa0(void);\nextern int native_fn_02062ad0(void);\nextern CountRecord *native_fn_02062a50(int);\nextern CountRecord *native_fn_02062a88(int);\nextern int native_fn_02044cdc(int);\n\nvoid native_main_02052720(Context *context, const Instruction *instruction)\n{\n    int third;\n    int first = TO_FIXED(context->parameters[0]);\n    int second = TO_FIXED(context->parameters[1]);\n    u8 last;\n    third = TO_FIXED(context->parameters[2]);\n    last = (u32)context->parameters[7];\n    native_fn_021e6114(first,second,third,last);\n    context->records[context->bank].position += instruction->advance;\n    context->records[context->bank].status = 0;\n}',
         controlDiff=(204,), dir='r2_main_large'),
    dict(address=0x0204c8d4, bytes=316, source='native_main_0204c8d4.c',
         relocations=[(16, 1, 'native_fn_020259b4', -8), (44, 1, 'native_fn_0202537c', -8), (60, 1, 'native_fn_02025ab8', -8), (72, 1, 'native_fn_02024e0c', -8), (80, 1, 'native_fn_02025ab8', -8), (88, 1, 'native_fn_02025ca4', -8), (104, 1, 'native_fn_0202537c', -8), (120, 1, 'native_fn_02025ab8', -8), (132, 1, 'native_fn_02024e0c', -8), (140, 1, 'native_fn_02025ab8', -8), (148, 1, 'native_fn_02025ca4', -8), (164, 1, 'native_fn_0202537c', -8), (180, 1, 'native_fn_02025ab8', -8), (192, 1, 'native_fn_02024e0c', -8), (200, 1, 'native_fn_02025ab8', -8), (208, 1, 'native_fn_02025ca4', -8), (212, 1, 'native_fn_020259b4', -8), (224, 1, 'native_fn_020259b4', -8), (236, 1, 'native_fn_020259b4', -8), (256, 1, 'native_fn_021e8c50', -8)],
         control='/* Convert parameters to fixed point, publish them and advance the record.\n   Unknowns: the fixed-point consumer and the record bank roles. */\n#include "context.h"\ntypedef struct CommandRecord {\n    u32 position;\n    u8 reserved[3];\n    u8 status;\n    u8 padding[0x104];\n} CommandRecord;\ntypedef struct Context {\n    u8 reserved[3];\n    u8 bank;\n    u32 reservedWords[3];\n    float parameters[8];\n    u8 padding[0x440];\n    CommandRecord records[];\n} Context;\ntypedef struct Instruction {\n    u32 opcode;\n    u32 advance;\n    u8 payload[];\n} Instruction;\nextern u32 native_fn_02064000(void);\nextern void native_fn_02064038(u32);\nextern void native_fn_02040820(void);\nextern int native_fn_ov000_021e9aa0(void);\nextern void native_fn_0204071c(int);\nextern void native_fn_ov000_02208dcc(void);\nextern void native_fn_ov000_02209670(void);\nextern void native_fn_ov000_022096bc(void);\nextern void native_fn_ov000_02209554(void);\nextern void native_fn_0205e61c(void);\nextern void native_fn_0205e520(void);\nextern void native_fn_ov000_021f4110(int, u8);\nextern void native_fn_ov000_021f4174(int, int);\nextern int native_fn_0205c668(int, int);\nextern int native_fn_ov000_021e96cc(int, int, signed char, int);\nextern int native_fn_ov000_021e31f0(int, int);\nextern int native_fn_ov000_021e9738(int, int, int);\nextern int native_fn_0205d718(int);\nextern int native_fn_ov000_02221444(const void *);\nextern void native_fn_0205e3f0(u8);\nextern void native_fn_ov000_021e9df4(u8);\nextern void native_fn_ov000_021e9e4c(u8, u8);\nextern int native_fn_ov000_021e9794(int);\nextern void native_fn_ov000_021f3e5c(int, int *);\nextern int native_fn_ov000_021f3f68(int);\nextern void native_fn_ov000_021f3dac(int, int);\nextern int native_fn_ov000_021f3ec4(int, int);\nextern void native_fn_ov000_021f3fec(int, int, int, int);\nextern void native_fn_ov000_021e71a4(int, int);\n#define TO_FIXED(value) ((int)((value) > 0.0f ? 0.5f + 4096.0f * (value) : 4096.0f * (value) - 0.5f))\ntypedef short s16;\ntypedef struct RecordEntry { u8 value; u8 reserved; } RecordEntry;\ntypedef struct NativeRecord {\n    u8 reserved[0x14];\n    u32 field14;\n    s16 field18;\n    u8 field1a;\n    u8 field1b;\n    u8 reserved1c[2];\n    u8 field1e;\n    u8 reserved1f[0x5b];\n    RecordEntry entries[5];\n} NativeRecord;\nextern NativeRecord *native_fn_02062b00(void);\nextern u32 native_fn_02062a68(int);\nextern u32 native_fn_02062a78(int);\nextern NativeRecord *native_fn_02062a50(int);\nextern NativeRecord *native_fn_02062a88(int);\nextern int native_fn_02044dc4(s16, u8);\nextern int native_fn_02044cdc(s16);\nextern void native_fn_ov000_02229f68(int);\nextern void native_fn_ov000_02229fdc(int);\nextern void native_fn_ov000_0222a050(int);\nextern void native_fn_ov000_0222a0c4(int);\nextern void native_fn_ov000_0222a138(int);\nextern void native_fn_ov000_02229fb0(int);\nextern void native_fn_ov000_0222a024(int);\nextern void native_fn_ov000_0222a098(int);\nextern void native_fn_ov000_0222a10c(int);\nextern void native_fn_ov000_0222a17c(int);\nextern const int *native_fn_ov000_021e6a70(int, int);\nextern const int *native_fn_ov000_021e6a40(int, int);\nextern void native_fn_ov000_021e6bac(int, int, int, int);\nextern void native_fn_ov000_021e70b0(int, int, int, int);\nextern void native_fn_ov000_021e7108(int, int, int, int);\nextern void native_fn_ov000_021e6c70(int, int, int, int, int);\nextern void native_fn_ov000_021f3e88(int, int, int, int);\nextern int native_fn_ov000_021f3f1c(int, int, int, int);\nextern int native_fn_ov000_021f4234(int, int, int, int);\nextern void native_fn_020725c8(int, u32);\nextern u32 native_fn_0205be24(void);\nextern u32 native_fn_0205be14(void);\nextern int native_fn_0205be64(void);\nextern void native_fn_ov000_021e6b64(int, int);\nextern void native_fn_ov000_021e6bf4(int, int);\nextern void native_fn_ov000_021e6cd0(int, int, int);\nextern void native_fn_ov000_021e6d44(int, int, int);\nextern void native_fn_ov000_021e7160(int, int, int);\nextern int native_fn_ov000_021f3c48(int);\nextern void native_fn_ov000_021f3f88(int, int, int, int);\nextern int native_fn_ov000_021f3ef0(int, int);\nextern int native_fn_ov000_021f3af8(int, int);\nextern int native_fn_ov000_021f4208(int, int);\n\nvoid native_main_0204c8d4(Context *context, const Instruction *instruction)\n{\n    int object = (int)context->parameters[0];\n    float first = context->parameters[1];\n    float second = context->parameters[2];\n    float third = context->parameters[7];\n    native_fn_021e8c50(object, TO_FIXED(first), TO_FIXED(second), TO_FIXED(third));\n    context->records[context->bank].position += instruction->advance;\n    context->records[context->bank].status = 0;\n}',
         controlDiff=(20,), dir='r2_main_large'),
    dict(address=0x0202b2f0, bytes=56, source='native_main_0202b2f0.c',
         relocations=[(48, 1, 'native_fn_0202ae28', -8)],
         control='/* Frame-heap range check: align the span, reject under 0x4c bytes, else allocate.\n   Unknowns: the heap descriptor layout and the allocator contract. */\n#include "context.h"\nextern u32 native_fn_0202b54c(void *,u32,u32);\nextern u32 native_fn_0202b594(void *,u32,u32);\nextern u32 native_fn_0202b614(void *,u32,u32);\n\nu32 native_main_0202b2f0(u32 arg0, u32 arg1, u32 arg2) {\n    u32 temp_r0;\n    u32 temp_r1;\n\n    temp_r1 = (arg1 + arg0) & ~3;\n    temp_r0 = (arg0 + 3) & ~3;\n    if ((temp_r0 > temp_r1) || ((u32) (temp_r1 - temp_r0) < 0x50U)) {\n        return 0U;\n    }\n    return native_fn_0202ae28((void *) temp_r0, temp_r1, arg2);\n}',
         controlDiff=(32,), dir='r1_main_small'),
    dict(address=0x020c386c, bytes=152, source='native_main_020c386c.c',
         relocations=[(24, 1, 'native_fn_02008d78', -8), (40, 1, 'native_fn_02008d78', -8), (68, 1, 'native_fn_02062a10', -8), (100, 1, 'native_fn_02008e0c', -8), (132, 1, 'native_fn_020c3928', -8), (140, 2, 'native_data_021d4ef4', 0), (144, 2, 'native_data_021d4d58', 0), (148, 2, 'native_data_021d4cf4', 0)],
         control='/* Fill a roster cache from up to three ids and return the accepted count.\n   Unknowns: the record layout, the accepted-id predicate and the cache roles. */\n#include "context.h"\ntypedef unsigned char u8;\ntypedef signed char s8;\ntypedef unsigned short u16;\ntypedef signed short s16;\ntypedef unsigned int u32;\ntypedef signed int s32;\ntypedef unsigned long long u64;\ntypedef signed long long s64;\ntypedef float f32;\ntypedef double f64;\n#define ROTATE_RIGHT(value, amount) (((u32)(value) >> ((u32)(amount) & 31)) | ((u32)(value) << ((0U - (u32)(amount)) & 31)))\n#define NULL ((void *)0)\nextern void native_fn_02008d78(void *destination,int value,u32 bytes);\nextern void native_fn_02008e0c(const void *source,void *destination,u32 bytes);\nextern const u8 *native_fn_02062a10(u32 id);\nextern u32 native_fn_020c3928(u32 count);\nextern u8 native_data_021d4cf4[];\nextern u8 native_data_021d4d58[];\nextern u8 native_data_021d4ef4[];\nu32 native_main_020c386c(const u32 *arg0) {\n    const u8 *temp_r0;\n    u8 var_r7;\n    u8 var_r8;\n\n    var_r8 = 0;\n    native_fn_02008d78(native_data_021d4ef4, 0, 0x190);\n    native_fn_02008d78(native_data_021d4d58, 0, 0xC);\n    var_r7 = 0;\n    do {\n        temp_r0 = native_fn_02062a10(arg0[var_r7]);\n        if (temp_r0 != 0) {\n            M2C_FIELD((native_data_021d4cf4 + (var_r8 * 4)), s32 *, 0x64) = (s32) arg0[var_r7];\n            native_fn_02008e0c(temp_r0, (var_r8 * 0x84) + (s32) native_data_021d4ef4, 0x84);\n            var_r8 += 1;\n        }\n        var_r7 += 1;\n    } while ((u32) var_r7 < 3U);\n    return native_fn_020c3928(var_r8);\n}',
         controlDiff=(20, 21), dir='r1_main_small'),
    dict(address=0x02040534, bytes=32, source='native_main_02040534.c',
         relocations=[(28, 2, 'native_data_020f6054', 0)],
         control='/* Clear the requested bits of a global control word using orr+eor.\n   Unknowns: the block role and the bit meanings. */\n#include "context.h"\n#ifndef R1_MAIN_SMALL_CONTEXT_H\n#define R1_MAIN_SMALL_CONTEXT_H\n\n\n/* Byte-offset field access on a measured global block. The pool word stays the\n   block base address, so the field offset shows up in the instruction — which is\n   what the image holds; folding base+offset into one literal does not match. */\n\n#endif\n\nextern u8 native_data_020f6054[];\nu32 native_main_02040534(u32 mask) {\n    u32 old = M2C_FIELD(native_data_020f6054, u32 *, 0x34);\n    u32 both = old | mask;\n    M2C_FIELD(native_data_020f6054, u32 *, 0x38) = both ^ mask;\n    return old;\n}',
         controlDiff=(20,), dir='r1_main_small'),
    dict(address=0x020455ac, bytes=28, source='native_main_020455ac.c',
         relocations=[(24, 2, 'native_data_020f6ae4', 0)],
         control='/* Set bit N of a global halfword, where N is the caller selector.\n   Unknowns: the block role, the selector domain and the halfword owner. */\n#include "context.h"\n#ifndef R1_MAIN_SMALL_CONTEXT_H\n#define R1_MAIN_SMALL_CONTEXT_H\n\n\n/* Byte-offset field access on a measured global block. The pool word stays the\n   block base address, so the field offset shows up in the instruction — which is\n   what the image holds; folding base+offset into one literal does not match. */\n\n#endif\n\nextern u8 native_data_020f6ae4[];\nvoid native_main_020455ac(u32 bit) {\n    u32 old = M2C_FIELD(native_data_020f6ae4, u16 *, 0);\n    u32 value = old ^ (1 << bit);\n    M2C_FIELD(native_data_020f6ae4, u16 *, 0) = value;\n}',
         controlDiff=(14, 15), dir='r1_main_small'),
    dict(address=0x020191fc, bytes=24, source='native_main_020191fc.c',
         relocations=[(20, 2, 'native_data_027ffc30', 0)],
         control='/* Return the one-bit flag stored in byte 5 of the 0x027ffc30 block.\n   Unknowns: the block owner and what the flag gates. */\n#include "context.h"\n#ifndef R1_MAIN_SMALL_CONTEXT_H\n#define R1_MAIN_SMALL_CONTEXT_H\n\n\n/* Byte-offset field access on a measured global block. The pool word stays the\n   block base address, so the field offset shows up in the instruction — which is\n   what the image holds; folding base+offset into one literal does not match. */\n\n#endif\n\ntypedef struct { u8 pad[9]; u8 flag : 1; } T;\nextern u8 native_data_027ffc30[];\nu32 native_main_020191fc(void) {\n    return ((T *)native_data_027ffc30)->flag;\n}',
         controlDiff=(4,), dir='r1_main_small'),
    dict(address=0x0204448c, bytes=28, source='native_main_0204448c.c',
         relocations=[(24, 2, 'native_data_020f69c4', 0)],
         control='/* Increment byte 0x26 of the 0x020f69c4 block and return the new value.\n   Unknowns: the block role and why the counter increments. */\n#include "context.h"\n#ifndef R1_MAIN_SMALL_CONTEXT_H\n#define R1_MAIN_SMALL_CONTEXT_H\n\n\n/* Byte-offset field access on a measured global block. The pool word stays the\n   block base address, so the field offset shows up in the instruction — which is\n   what the image holds; folding base+offset into one literal does not match. */\n\n#endif\n\nextern u8 native_data_020f69c4[];\nu32 native_main_0204448c(void) {\n    u8 *p = native_data_020f69c4;\n    u32 v = (u32)p[0x26] + 1;\n    p[0x2a] = (u8)v;\n    return v & 0xff;\n}',
         controlDiff=(12,), dir='r1_main_small'),
    dict(address=0x0203915c, bytes=32, source='native_main_0203915c.c',
         relocations=[(28, 2, 'native_data_020f4c44', 0)],
         control='/* Publish two recorded words from the object reached through 0x020f4c44.\n   Unknowns: the record layout at +0x7c/+0x80 and the output owner. */\n#include "context.h"\n#ifndef R1_MAIN_SMALL_CONTEXT_H\n#define R1_MAIN_SMALL_CONTEXT_H\n\n\n/* Byte-offset field access on a measured global block. The pool word stays the\n   block base address, so the field offset shows up in the instruction — which is\n   what the image holds; folding base+offset into one literal does not match. */\n\n#endif\n\nextern u8 native_data_020f4c44[];\nvoid native_main_0203915c(u32 *out) {\n    u8 *p = *(u8 **)native_data_020f4c44;\n    u32 a = M2C_FIELD(p, volatile u32 *, 0x80);\n    u32 b = M2C_FIELD(p, volatile u32 *, 0x80);\n    out[0] = a;\n    out[1] = b;\n}',
         controlDiff=(8,), dir='r1_main_small'),
    dict(address=0x02034b18, bytes=20, source='native_main_02034b18.c',
         relocations=[],
         control='/* Pop one halfword through a caller cursor and advance it by two bytes.\n   Unknowns: the stream format and the cursor owner. */\n#include "context.h"\n#ifndef R1_MAIN_SMALL_CONTEXT_H\n#define R1_MAIN_SMALL_CONTEXT_H\n\n\n/* Byte-offset field access on a measured global block. The pool word stays the\n   block base address, so the field offset shows up in the instruction — which is\n   what the image holds; folding base+offset into one literal does not match. */\n\n#endif\n\nu32 native_main_02034b18(u16 **cursor) {\n    u16 *p = *cursor;\n    u16 value = *p++;\n    *cursor = p;\n    return (value) + 1;\n}',
         controlDiff=(12, 14, 15), dir='r1_main_small'),
    dict(address=0x02034bfc, bytes=20, source='native_main_02034bfc.c',
         relocations=[],
         control='/* Pop one byte through a caller cursor and advance it by one byte.\n   Unknowns: the stream format and the cursor owner. */\n#include "context.h"\n#ifndef R1_MAIN_SMALL_CONTEXT_H\n#define R1_MAIN_SMALL_CONTEXT_H\n\n\n/* Byte-offset field access on a measured global block. The pool word stays the\n   block base address, so the field offset shows up in the instruction — which is\n   what the image holds; folding base+offset into one literal does not match. */\n\n#endif\n\nu32 native_main_02034bfc(u8 **cursor) {\n    u8 *p = *cursor;\n    u8 value = *p++;\n    *cursor = p;\n    return (value) + 1;\n}',
         controlDiff=(12, 14, 15), dir='r1_main_small'),
    dict(address=0x0204ad90, bytes=20, source='native_main_0204ad90.c',
         relocations=[(16, 2, 'native_data_020d940c', 0)],
         control='/* Signed-byte table read with a four-byte stride from 0x020d940c.\n   Unknowns: the table contents and the index domain. */\n#include "context.h"\n#ifndef R1_MAIN_SMALL_CONTEXT_H\n#define R1_MAIN_SMALL_CONTEXT_H\n\n\n/* Byte-offset field access on a measured global block. The pool word stays the\n   block base address, so the field offset shows up in the instruction — which is\n   what the image holds; folding base+offset into one literal does not match. */\n\n#endif\n\nextern u8 native_data_020d940c[];\ns32 native_main_0204ad90(u32 index) {\n    return M2C_FIELD(native_data_020d940c, s8 *, index * 8);\n}',
         controlDiff=(4,), dir='r1_main_small'),
    dict(address=0x020bf504, bytes=20, source='native_main_020bf504.c',
         relocations=[(16, 2, 'native_data_020e2cb0', 0)],
         control='/* Halfword table read with a two-byte stride from 0x020e2cb0.\n   Unknowns: the table contents and the index domain. */\n#include "context.h"\n#ifndef R1_MAIN_SMALL_CONTEXT_H\n#define R1_MAIN_SMALL_CONTEXT_H\n\n\n/* Byte-offset field access on a measured global block. The pool word stays the\n   block base address, so the field offset shows up in the instruction — which is\n   what the image holds; folding base+offset into one literal does not match. */\n\n#endif\n\nextern u8 native_data_020e2cb0[];\nu32 native_main_020bf504(u32 index) {\n    return M2C_FIELD(native_data_020e2cb0, u16 *, index * 6);\n}',
         controlDiff=(0, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 16, 17, 18, 19), dir='r1_main_small'),
    dict(address=0x0204b818, bytes=20, source='native_main_0204b818.c',
         relocations=[(16, 2, 'native_fn_02063e04', 0)],
         control='/* Tail-call a helper with two byte-truncated arguments.\n   Unknowns: the callee role and why only the low bytes survive. */\n#include "context.h"\n#ifndef R1_MAIN_SMALL_CONTEXT_H\n#define R1_MAIN_SMALL_CONTEXT_H\n\n\n/* Byte-offset field access on a measured global block. The pool word stays the\n   block base address, so the field offset shows up in the instruction — which is\n   what the image holds; folding base+offset into one literal does not match. */\n\n#endif\n\nextern u32 native_fn_02063e04(u32, u32);\nu32 native_main_0204b818(u32 a, u32 b) {\n    return (native_fn_02063e04((u8)a, (u8)b)) + 1;\n}',
         controlDiff=(1, 2, 3, 12, 13, 14, 15, 16, 17, 18, 19), dir='r1_main_small'),
    dict(address=0x020d3fbc, bytes=20, source='native_main_020d3fbc.c',
         relocations=[(16, 2, 'native_fn_0203d0c0', 0)],
         control='/* Tail-call a helper with the constant 0x2a and a byte-truncated argument.\n   Unknowns: the callee role and the constant meaning. */\n#include "context.h"\n#ifndef R1_MAIN_SMALL_CONTEXT_H\n#define R1_MAIN_SMALL_CONTEXT_H\n\n\n/* Byte-offset field access on a measured global block. The pool word stays the\n   block base address, so the field offset shows up in the instruction — which is\n   what the image holds; folding base+offset into one literal does not match. */\n\n#endif\n\nextern u32 native_fn_0203d0c0(u32, u32);\nu32 native_main_020d3fbc(u32 value) {\n    return (native_fn_0203d0c0(0x2a, (u8)value)) + 1;\n}',
         controlDiff=(1, 2, 3, 12, 13, 14, 15, 16, 17, 18, 19), dir='r1_main_small'),
    dict(address=0x0202bba0, bytes=20, source='native_main_0202bba0.c',
         relocations=[],
         control='/* Read a word from a record, or an indexed word through the caller pointer.\n   Unknowns: the record layout and the null-pointer contract. */\n#include "context.h"\n#ifndef R1_MAIN_SMALL_CONTEXT_H\n#define R1_MAIN_SMALL_CONTEXT_H\n\n\n/* Byte-offset field access on a measured global block. The pool word stays the\n   block base address, so the field offset shows up in the instruction — which is\n   what the image holds; folding base+offset into one literal does not match. */\n\n#endif\n\nu32 native_main_0202bba0(u8 *p, u8 *q) {\n    if (q == 0)\n        return M2C_FIELD(p, u32 *, 8);\n    return *(u32 *)(q + M2C_FIELD(p, u16 *, 0xa));\n}',
         controlDiff=(4,), dir='r1_main_small'),
    dict(address=0x0202e35c, bytes=24, source='native_main_0202e35c.c',
         relocations=[(20, 2, 'native_data_020edf84', 0)],
         control='/* Spin until the word at 0x020edf84+4 becomes zero.\n   Unknowns: which producer clears the word and the timeout contract. */\n#include "context.h"\n#ifndef R1_MAIN_SMALL_CONTEXT_H\n#define R1_MAIN_SMALL_CONTEXT_H\n\n\n/* Byte-offset field access on a measured global block. The pool word stays the\n   block base address, so the field offset shows up in the instruction — which is\n   what the image holds; folding base+offset into one literal does not match. */\n\n#endif\n\nextern u8 native_data_020edf84[];\nvoid native_main_0202e35c(void) {\n    while (M2C_FIELD(native_data_020edf84, volatile u32 *, 8) != 0) {\n    }\n}',
         controlDiff=(4,), dir='r1_main_small'),
)



def decode_target(data, offset, address):
    """Decode the ARM BL target stored at ``data[offset]``."""
    word = int.from_bytes(data[offset:offset + 4], 'little')
    immediate = word & 0xFFFFFF
    if immediate & 0x800000:
        immediate -= 0x1000000
    return address + offset + 8 + (immediate << 2)


def resolve_rule(config, name):
    for lane in LANE_DIRS:
        if name.startswith(lane):
            return source_units.resolve(config, name)
    return source_units.resolve(config, name)


def compile_unit(root, config, rule, work, source, tag):
    compiler = root / config['compilers'][rule['compilerSha256']]
    flags = [flag for flag in rule['compilerFlags'] if flag not in ('-thumb', '-c')]
    flags.append('-c')
    if rule.get('mode') == 'thumb':
        flags.append('-thumb')
    obj = work / f'{source.stem}-{tag}.o'
    env = dict(os.environ, LM_LICENSE_FILE=str(root / 'tools/mwccarm/mwccarm/license.dat'))
    result = subprocess.run([str(compiler), *flags, str(source), '-o', str(obj)],
                            cwd=str(source.parent), env=env, capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit(f'{source.name}: compile failed\n{result.stdout[-900:]}')
    return form_search.read_object(obj)


def pin_relocations(relocations, defined, image, address):
    """Decode linker-resolved helper calls into address-bearing symbol names."""
    pinned = []
    for offset, kind, symbol, addend in relocations:
        if symbol in defined or re.search(r'[0-9a-f]{8}$', symbol):
            pinned.append((offset, kind, symbol, addend))
            continue
        if kind not in (1, 28, 29, 30, 31):
            raise SystemExit(f'unpinnable relocation {kind} {symbol} at {offset:#x}')
        target = decode_target(image, offset, address)
        pinned.append((offset, kind, f'native_fn_{target:08x}', addend))
    return tuple(pinned)


def patch(text, address, relocations, defined, modes):
    return form_search.relocate(text, address, relocations, defined, modes=modes)


def check_row(root, config, modes, work, row, failures):
    address = row['address']
    name = row['source']
    source = root / 'src/main' / row['dir'] / name
    if not source.is_file():
        failures.append(f'{name}: missing')
        return
    rule = resolve_rule(config, str(source.relative_to(root)).replace('\\', '/'))
    image, _, base = form_search.module_image(root, MODULE)
    offset = None
    extent = None
    for line in (root / 'ledger/functions.jsonl').open(encoding='utf-8'):
        if not line.strip():
            continue
        entry = json.loads(line)
        if entry['module'] == MODULE and int(entry['address'], 0) == address:
            offset = int(entry['binaryOffset'])
            extent = int(entry['bytes'])
            break
    if offset is None:
        failures.append(f'{name}: not in the main ledger')
        return
    want = image[offset:offset + row['bytes']]
    text, defined, relocations = compile_unit(root, config, rule, work, source, 'unit')
    pinned = pin_relocations(relocations, defined, want, address)
    if tuple(pinned) != tuple(tuple(x) for x in row['relocations']):
        failures.append(f'{name}: relocations {pinned} != pinned {row["relocations"]}')
    got = patch(text, address, pinned, defined, modes)
    diff = [i for i, (a, b) in enumerate(zip(got, want)) if a != b]
    if len(got) != len(want) or diff:
        failures.append(f'{name}: patched {len(got)} B, diff {diff[:12]}')

    # 2. every ABS32 slot: the image word must be exactly the object's target
    words = []
    for slot, kind, symbol, addend in pinned:
        if kind != 2:
            continue
        target = defined.get(symbol) or form_search.symbol_address(symbol)
        word = int.from_bytes(want[slot:slot + 4], 'little')
        words.append(word)
        if word != target:
            failures.append(f'{name}: +{slot:#x} image word {word:#010x} != target {target:#010x}')

    # 3. whole-C negative control
    control = work / f'{address:08x}-control.c'
    control.write_text(row['control'], encoding='utf-8')
    ctext, cdefined, crelocations = compile_unit(root, config, rule, work, control, 'control')
    cpinned = pin_relocations(crelocations, cdefined, want, address)
    cgot = patch(ctext, address, cpinned, cdefined, modes)
    cdiff = [i for i, (a, b) in enumerate(zip(cgot, want)) if a != b]
    if not cdiff:
        failures.append(f'{name}: negative control still matches the image')
    elif tuple(cdiff) != tuple(row['controlDiff']):
        failures.append(f'{name}: control diff {cdiff[:12]} != pinned {row["controlDiff"][:12]}')
    print(f'{address:#010x} {row["bytes"]:3d} B {name:26s} profile={rule["compilerFlags"][0]} '
          f'relocs={len(pinned)} bytes=EXACT control_diff={cdiff[:6]}')
    return tuple(words)


def main():
    failures = []
    config = source_units.load_config(ROOT)
    modes = form_search.TargetModes(ROOT, MODULE)
    work = Path(tempfile.mkdtemp(prefix='main-rows-2-'))
    (work / 'context.h').write_text(
        (ROOT / 'src/main/r1_main_small/context.h').read_text(encoding='utf-8'), encoding='utf-8')
    pinned = []
    for row in ROWS:
        pinned.append(check_row(ROOT, config, modes, work, row, failures))
    print()
    for row, words in zip(ROWS, pinned):
        if words is None:
            continue
        print(f'  {row["address"]:#010x} {row["bytes"]:3d} B  pool='
              + ', '.join('%#010x' % w for w in words))
    total = sum(row['bytes'] for row in ROWS)
    print(f'\n{len(ROWS)} rows, {total} bytes, {len(failures)} failure(s)')
    for failure in failures:
        print('  FAIL', failure)
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
