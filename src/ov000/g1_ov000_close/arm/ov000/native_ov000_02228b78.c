/* ov000 row 0x02228b78: 184 bytes.
 *
 * What it does: 40 instructions and 2 call(s), then a 7-entry dispatch through an inline branch table at 0x02228bb4 (dispatch word at 0x02228bac)
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

extern void native_fn_02044dc4(void);
extern void native_fn_020449d4(void);


asm u32 native_ov000_02228b78 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r5, r2
    mov r6, r0
    mov r0, r5
    mov r1, r3
    bl native_fn_02044dc4
    mov r4, r0
    mov r0, r5
    bl native_fn_020449d4
    ldrh r0, [r0, #4]
    mov r0, r0, lsl #24
    mov r0, r0, lsr #28
    cmp r0, #6
    addls pc, pc, r0, lsl #2
    b L_02228c10
    dcd 0xea000015
    dcd 0xea000014
    dcd 0xea000013
    dcd 0xea000002
    dcd 0xea00000d
    dcd 0xea000008
    dcd 0xea000003
    cmp r4, #7
    movhs r0, #340
    movlo r0, #336
    ldmia sp!, {r4, r5, r6, pc}
    cmp r4, #7
    ldrhs r0, [pc, #0x2c]
    ldrlo r0, [pc, #0x2c]
    ldmia sp!, {r4, r5, r6, pc}
    cmp r4, #7
    ldrhs r0, [pc, #0x24]
    ldrlo r0, [pc, #0x24]
    ldmia sp!, {r4, r5, r6, pc}
    cmp r4, #7
    ldrhs r0, [pc, #0x1c]
    ldrlo r0, [pc, #0x1c]
    ldmia sp!, {r4, r5, r6, pc}
L_02228c10:
    mov r0, r6
    ldmia sp!, {r4, r5, r6, pc}
    dcd 0x00000155
    dcd 0x00000151
    dcd 0x00000156
    dcd 0x00000152
    dcd 0x00000157
    dcd 0x00000153
}
