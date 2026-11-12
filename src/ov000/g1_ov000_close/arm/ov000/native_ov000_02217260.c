/* ov000 row 0x02217260: 124 bytes.
 *
 * What it does: 30 instructions and 4 call(s), then a 15-entry dispatch through an inline branch table at 0x02217278 (dispatch word at 0x02217270)
 *
 * Carrier: mwccarm asm with dcd data runs.
 * The measured extent is code plus data inside the function. The data
 * runs are emitted as data, not decoded as instructions; every
 * instruction, branch target, pool word and table entry is read from
 * the image.
 *
 * Unknowns: the field roles, the meaning of the table entries and every callee contract are not established by byte identity; the dispatch range and the table bounds are measured.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_021fab58(void);
extern void native_fn_02074764(void);
extern void native_fn_02201fcc(void);
extern void native_fn_021fe3ec(void);


asm u32 native_ov000_02217260 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r0, [pc, #0x6c]
    ldrsb r0, [r0, #16]
    cmp r0, #14
    addls pc, pc, r0, lsl #2
    b L_022172d0
    dcd 0xea00000d
    dcd 0xea000013
    dcd 0xea00000d
    dcd 0xea000011
    dcd 0xea000010
    dcd 0xea00000f
    dcd 0xea00000e
    dcd 0xea00000d
    dcd 0xea00000c
    dcd 0xea000008
    dcd 0xea000009
    dcd 0xea000009
    dcd 0xea000008
    dcd 0xea000007
    dcd 0xea000006
    bl native_fn_021fab58
    b L_022172d0
    bl native_fn_02074764
    b L_022172d0
    bl native_fn_02201fcc
    b L_022172d0
    bl native_fn_021fe3ec
L_022172d0:
    mov r0, #0
    ldmia sp!, {r3, pc}
    dcd 0x0224536c
}
