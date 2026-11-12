/* ov000 row 0x021ed404: 348 bytes.
 *
 * What it does: 82 instructions and 11 call(s), then a 5-entry dispatch through an inline branch table at 0x021ed42c (dispatch word at 0x021ed424)
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

extern void native_fn_021f02f0(void);
extern void native_fn_021f0394(void);
extern void native_fn_021ef4d8(void);
extern void native_fn_021ef57c(void);
extern void native_fn_021ef11c(void);
extern u8 native_data_0222b8c4[];
extern u8 native_data_0222b8ec[];
extern u8 native_data_0222b8e0[];
extern u8 native_data_0222b8f8[];


asm u32 native_ov000_021ed404 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    sub sp, sp, #56
    ldr r0, [pc, #0x138]
    ldr r0, [r0, #0x4]
    ldrsb r1, [r0, #32]
    add r0, r0, #256
    ldrsb r4, [r0, #2]
    cmp r1, #4
    addls pc, pc, r1, lsl #2
    b L_021ed518
    dcd 0xea000003
    dcd 0xea000006
    dcd 0xea000003
    dcd 0xea000012
    dcd 0xea000024
    bl native_fn_021f02f0
    b L_021ed518
    bl native_fn_021f02f0
    b L_021ed518
    cmp r4, #0
    beq L_021ed480
    cmp r4, #3
    bne L_021ed480
    ldr r1, [pc, #0xe8]
    add r0, sp, #8
    ldr r2, [r1, #0x10]
    ldr r1, [r1, #0xc]
    str r2, [sp, #0xc]
    str r1, [sp, #0x8]
    bl native_fn_021f0394
    b L_021ed518
L_021ed480:
    bl native_fn_021f02f0
    b L_021ed518
    cmp r4, #1
    beq L_021ed4b8
    cmp r4, #4
    bne L_021ed4b8
    ldr r1, [pc, #0xb0]
    add r0, sp, #0
    ldr r2, [r1, #0x18]
    ldr r1, [r1, #0x14]
    str r2, [sp, #0x4]
    str r1, [sp]
    bl native_fn_021f0394
    b L_021ed518
L_021ed4b8:
    ldr r0, [pc, #0x94]
    add r3, sp, #44
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    mov r0, r3
    bl native_fn_021f0394
    b L_021ed518
    cmp r4, #1
    beq L_021ed500
    cmp r4, #3
    bne L_021ed518
    ldr r0, [pc, #0x6c]
    add r3, sp, #32
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    mov r0, r3
    bl native_fn_021f0394
    b L_021ed518
L_021ed500:
    ldr r0, [pc, #0x54]
    add r12, sp, #16
    ldmia r0, {r0, r1, r2, r3}
    stmia r12, {r0, r1, r2, r3}
    mov r0, r12
    bl native_fn_021f0394
L_021ed518:
    bl native_fn_021ef4d8
    bl native_fn_021ef57c
    mov r0, #0
    bl native_fn_021ef11c
    ldr r1, [pc, #0x1c]
    mov r2, #1
    ldr r3, [r1, #0x4]
    mov r0, #2
    strb r4, [r3, #0x20]
    ldr r1, [r1, #0x4]
    strb r2, [r1, #0x100]
    add sp, sp, #56
    ldmia sp!, {r4, pc}
    dcd 0x02236bc4
    dcd native_data_0222b8c4
    dcd native_data_0222b8ec
    dcd native_data_0222b8e0
    dcd native_data_0222b8f8
}
