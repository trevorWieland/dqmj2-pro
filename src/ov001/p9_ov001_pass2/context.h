/* Shared declarations for the ov001 pass-2 packet (p9).
 *
 * Every file in this directory is one measured function at its trailing address,
 * compiled under the module's real rule (src/ov001/** -> ov001, ARM, profile
 * p003).  The module base is 0x021d7240 and the compared image is
 * extract/arm9_overlays/ov001.bin, the decompressed overlay the ledger's
 * binaryOffset indexes.
 *
 * Mechanism notes measured while authoring this packet:
 *   - The 0x440-stride record scan at 0x0221a738..0x0221f0f4 is one shape: a
 *     do/while over three records, an exit test that `break`s to the shared
 *     return-0 epilogue, and `if (i == 2) return 1` before the advance.  The
 *     status block at record+0x200 must be written as a common subexpression
 *     (`((s8 *)(entry + 0x200))[0xNN]` twice); naming the pointer moves the add
 *     into r1 instead of r0 and never matches.
 *   - 0x022388ec is a signed-byte state block; 0x02242b50 is the battle-state
 *     block whose +0x10 word is the handle and +6/+7 are the mode bytes.
 *   - 0x02242aac is a signed-byte cursor whose +1 byte publishes the lookup
 *     result; 0x02242ab4 is the 12-byte-record table it indexes.
 *   - 0x0222ec84 is the session-open byte and 0x02238d7c+0x27 the released
 *     marker written by the teardown latch.
 */
typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;

/* 0x022388ec: state block whose +0xa/+0x11/+0x12/+0x1a bytes are live state. */
extern s8 native_data_ov001_022388ec[];
/* 0x02242aac: signed-byte cursor; +1 is the published lookup result. */
extern u8 native_data_ov001_02242aac[];
/* 0x02242ab4: 12-byte-record table indexed by the cursor. */
extern u8 native_data_ov001_02242ab4[];
/* 0x0222ec84: session-open byte. */
extern u8 native_data_ov001_0222ec84[];
/* 0x02238d7c: session record; +0x27 is the released marker. */
extern u8 native_data_ov001_02238d7c[];
/* 0x02242b50: battle state block (+6/+7 mode bytes, +0x10 handle). */
extern u8 native_data_ov001_02242b50[];

/* Overlay services. */
extern s32 native_fn_ov001_021db8d0(u8 *entry);
extern void native_fn_ov001_021f14a4(void);
extern s32 native_fn_ov001_02216ac4(u32 value, u8 arg1, s32 arg2);
