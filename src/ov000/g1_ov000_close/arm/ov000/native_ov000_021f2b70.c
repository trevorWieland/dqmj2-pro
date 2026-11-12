/* ov000 row 0x021f2b70: 184 bytes.
 *
 * What it does: 45 instructions and 5 call(s), then a 7-entry dispatch through an inline branch table at 0x021f2bb4 (dispatch word at 0x021f2bac)
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

extern void native_fn_021f2b14(void);
extern void native_fn_021f2ab8(void);
extern void native_fn_0205f9e4(void);


asm u32 native_ov000_021f2b70 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r4, r0
    ldrh r2, [r4, #12]
    ldr r3, [r4, #0x4]
    ldrh r1, [r4, #14]
    cmp r3, #0
    movne r0, #1
    add r2, r3, r2
    moveq r0, #0
    cmp r2, r1
    movlt r1, #1
    movge r1, #0
    bl native_fn_021f2b14
    ldrsb r0, [r4, #16]
    cmp r0, #6
    addls pc, pc, r0, lsl #2
    b L_021f2c14
    dcd 0xea000005
    dcd 0xea00000a
    dcd 0xea00000f
    dcd 0xea000002
    dcd 0xea00000d
    dcd 0xea000000
    dcd 0xea00000b
    mov r0, #240
    mov r2, r0
    mov r1, #40
    mov r3, #128
    bl native_fn_021f2ab8
    b L_021f2c14
    mov r0, #240
    mov r2, r0
    mov r1, #32
    mov r3, #120
    bl native_fn_021f2ab8
    b L_021f2c14
    mov r0, #240
    mov r2, r0
    mov r1, #64
    mov r3, #152
    bl native_fn_021f2ab8
L_021f2c14:
    ldr r0, [pc, #0x8]
    ldr r0, [r0, #0x14]
    bl native_fn_0205f9e4
    ldmia sp!, {r4, pc}
    dcd 0x02236da4
}
