/* ov000 row 0x021ee01c: 92 bytes.
 *
 * What it does: 22 instructions and 2 call(s), then a 1-entry dispatch through an inline branch table at 0x021ee038 (dispatch word at 0x021ee030)
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

extern void native_fn_021f02b4(void);


asm u32 native_ov000_021ee01c (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r0, [pc, #0x4c]
    ldr r1, [r0, #0x4]
    ldrsb r0, [r1, #32]
    cmp r0, #4
    addls pc, pc, r0, lsl #2
    ldmia sp!, {r3, pc}
    dcd 0xea000003
    ldmia sp!, {r3, pc}
    ldmia sp!, {r3, pc}
    ldmia sp!, {r3, pc}
    ldmia sp!, {r3, pc}
    ldrb r0, [r1, #0x504]
    cmp r0, #0
    mov r0, #3
    bne L_021ee068
    mov r1, r0
    bl native_fn_021f02b4
    ldmia sp!, {r3, pc}
L_021ee068:
    mov r1, #1
    bl native_fn_021f02b4
    ldmia sp!, {r3, pc}
    dcd 0x02236bc4
}
