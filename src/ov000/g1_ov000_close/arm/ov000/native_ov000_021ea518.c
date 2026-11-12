/* ov000 row 0x021ea518: 112 bytes.
 *
 * What it does: 25 instructions and 1 call(s), then a 9-entry dispatch through an inline branch table at 0x021ea538 (dispatch word at 0x021ea530)
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

extern void native_fn_020449d4(void);


asm u32 native_ov000_021ea518 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    bl native_fn_020449d4
    ldrh r0, [r0, #4]
    mov r0, r0, lsl #20
    mov r0, r0, lsr #28
    cmp r0, #8
    addls pc, pc, r0, lsl #2
    b L_021ea574
    dcd 0xea000007
    dcd 0xea000006
    dcd 0xea000005
    dcd 0xea000006
    dcd 0xea000005
    dcd 0xea000004
    dcd 0xea000005
    dcd 0xea000004
    dcd 0xea000003
    ldr r0, [pc, #0x18]
    ldmia sp!, {r3, pc}
    ldr r0, [pc, #0x14]
    ldmia sp!, {r3, pc}
    ldr r0, [pc, #0x8]
    ldmia sp!, {r3, pc}
L_021ea574:
    ldr r0, [pc, #0x8]
    ldmia sp!, {r3, pc}
    dcd 0x00000133
    dcd 0x0000017e
    dcd 0x0000019a
}
