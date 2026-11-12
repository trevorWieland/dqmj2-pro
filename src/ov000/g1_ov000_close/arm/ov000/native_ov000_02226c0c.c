/* ov000 row 0x02226c0c: 428 bytes.
 *
 * What it does: 105 instructions and 12 call(s), then a 5-entry dispatch through an inline branch table at 0x02226d48 (dispatch word at 0x02226d40)
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

extern void native_fn_0202a634(void);
extern void native_fn_02226af8(void);
extern void native_fn_02224e38(void);
extern void native_fn_02226984(void);
extern void native_fn_01ffb4c4(void);
extern void native_fn_02224b84(void);
extern void native_fn_022260ec(void);
extern void native_fn_02227408(void);
extern void native_fn_02227870(void);
extern void native_fn_022260a8(void);
extern void native_fn_02226614(void);
extern u8 native_data_0222feb4[];


asm u32 native_ov000_02226c0c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    mov r6, #0
    bl native_fn_0202a634
    ldr r1, [pc, #0x190]
    mov r7, r0
    ldrsb r0, [r1, #24]
    ldr r5, [pc, #0x188]
    mov r8, r6
    add r4, r0, r0, lsl #2
    bl native_fn_02226af8
    ldr r0, [pc, #0x174]
    ldrsb r1, [r0, #24]
    cmp r1, #11
    bgt L_02226c68
    bge L_02226ccc
    cmp r1, #3
    bgt L_02226d10
    cmp r1, #2
    blt L_02226d10
    beq L_02226c84
    cmp r1, #3
    beq L_02226ca8
    b L_02226d10
L_02226c68:
    cmp r1, #15
    bgt L_02226c78
    beq L_02226ca8
    b L_02226d10
L_02226c78:
    cmp r1, #23
    beq L_02226cf0
    b L_02226d10
L_02226c84:
    ldrsb r1, [r0, #28]
    cmp r1, #0
    beq L_02226d10
    mov r1, #6
    strb r1, [r0, #0x1a]
    mov r1, #5
    str r1, [r0, #0x14]
    mov r8, #1
    b L_02226d10
L_02226ca8:
    ldr r0, [pc, #0x100]
    ldrsb r0, [r0, #28]
    cmp r0, #0
    beq L_02226d10
    bl native_fn_02224e38
    ldr r1, [pc, #0xec]
    mov r8, #1
    str r0, [r1, #0x14]
    b L_02226d10
L_02226ccc:
    ldrsb r1, [r0, #28]
    cmp r1, #0
    beq L_02226d10
    mov r1, #14
    strb r1, [r0, #0x1a]
    mov r1, #5
    str r1, [r0, #0x14]
    mov r8, #1
    b L_02226d10
L_02226cf0:
    ldrsb r1, [r0, #28]
    cmp r1, #0
    beq L_02226d10
    mov r1, #26
    strb r1, [r0, #0x1a]
    mov r1, #5
    str r1, [r0, #0x14]
    mov r8, #1
L_02226d10:
    cmp r8, #0
    movne r0, #0
    ldmneia sp!, {r4, r5, r6, r7, r8, pc}
    bl native_fn_02226984
    cmp r0, #0
    beq L_02226d38
    ldr r0, [pc, #0x80]
    mov r1, #4
    str r1, [r0, #0x14]
    b L_02226da4
L_02226d38:
    ldrsb r0, [r5, r4]
    cmp r0, #4
    addls pc, pc, r0, lsl #2
    b L_02226da4
    dcd 0xea000013
    dcd 0xea000002
    dcd 0xea00000a
    dcd 0xea00000c
    dcd 0xea00000d
    bl native_fn_01ffb4c4
    ldrh r0, [r7, #2]
    tst r0, #1
    beq L_02226da4
    mov r0, #1
    bl native_fn_02224b84
    ldr r1, [pc, #0x34]
    str r0, [r1, #0x14]
    b L_02226da4
    bl native_fn_022260ec
    mov r6, r0
    b L_02226da4
    bl native_fn_02227408
    b L_02226da4
    bl native_fn_02227870
    b L_02226da4
    bl native_fn_022260a8
    mov r6, r0
L_02226da4:
    bl native_fn_02226614
    mov r0, r6
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
    dcd 0x022468b8
    dcd native_data_0222feb4
}
