/* ov000 row 0x021f56d0: 516 bytes.
 *
 * What it does: 128 instructions and 17 call(s), then a 12-entry dispatch through an inline branch table at 0x021f5720 (dispatch word at 0x021f5718)
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

extern void native_fn_02061dcc(void);
extern void native_fn_020624c0(void);
extern void native_fn_02223ec0(void);
extern void native_fn_02049f4c(void);
extern void native_fn_02223d40(void);
extern void native_fn_020602ec(void);
extern void native_fn_0204aaf0(void);
extern void native_fn_0204ab98(void);
extern void native_fn_02072f48(void);
extern void native_fn_020630b0(void);
extern void native_fn_0204a9d4(void);
extern void native_fn_021f5518(void);
extern void native_fn_0204ac20(void);
extern u8 native_data_0222f2ec[];


asm u32 native_ov000_021f56d0 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    sub sp, sp, #16
    mov r7, r0
    bl native_fn_02061dcc
    ldr r4, [r0]
    mov r0, #19
    ldr r5, [r4, #0x4]
    bl native_fn_020624c0
    bl native_fn_02223ec0
    add r2, sp, #12
    mov r1, #0
    mov r0, r7
    strh r1, [r2]
    strh r1, [r2, #2]
    mov r6, #1
    bl native_fn_02061dcc
    bl native_fn_02049f4c
    cmp r7, #11
    addls pc, pc, r7, lsl #2
    b L_021f58c8
    dcd 0xea000068
    dcd 0xea000067
    dcd 0xea000066
    dcd 0xea000065
    dcd 0xea000064
    dcd 0xea000063
    dcd 0xea000004
    dcd 0xea000003
    dcd 0xea000002
    dcd 0xea000014
    dcd 0xea000013
    dcd 0xea000012
    mov r0, #19
    bl native_fn_020624c0
    sub r1, r7, #6
    mov r1, r1, lsl #24
    mov r1, r1, asr #24
    bl native_fn_02223d40
    movs r2, r0
    ldrnesh r1, [r2, #24]
    cmpne r1, #0
    addeq sp, sp, #16
    ldmeqia sp!, {r4, r5, r6, r7, r8, pc}
    mov r3, #0
    mov r0, r4
    str r3, [sp]
    mov r4, r6
    str r4, [sp, #0x4]
    bl native_fn_020602ec
    add sp, sp, #16
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
    mov r0, #19
    bl native_fn_020624c0
    sub r1, r7, #9
    mov r1, r1, lsl #24
    mov r1, r1, asr #24
    bl native_fn_02223d40
    movs r4, r0
    ldrnesh r0, [r4, #24]
    cmpne r0, #0
    addeq sp, sp, #16
    ldmeqia sp!, {r4, r5, r6, r7, r8, pc}
    mov r3, r6
    str r3, [sp]
    str r3, [sp, #0x4]
    add r1, sp, #12
    mov r0, r7
    str r3, [sp, #0x8]
    mov r2, #5
    bl native_fn_0204aaf0
    ldrsh r0, [sp, #12]
    mov r2, #0
    ldr r3, [pc, #0xd8]
    add r0, r0, #16
    strh r0, [sp, #12]
    str r2, [sp]
    add r1, sp, #12
    mov r0, r7
    mov r2, r6
    bl native_fn_0204ab98
    ldrsh r0, [sp, #12]
    add r0, r0, #8
    strh r0, [sp, #12]
    ldrsh r0, [r4, #24]
    ldrb r8, [r4, #0x30]
    bl native_fn_02072f48
    cmp r0, #0
    bne L_021f58ac
    cmp r8, #100
    beq L_021f5874
    ldrb r0, [r4, #0x1c]
    bl native_fn_020630b0
    cmp r0, r8
    moveq r6, #5
    mov r4, #2
    str r4, [sp]
    mov r4, #0
    add r1, sp, #12
    mov r0, r7
    mov r2, r6
    mov r3, r8
    str r4, [sp, #0x4]
    bl native_fn_0204a9d4
    add sp, sp, #16
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
L_021f5874:
    ldrb r3, [r5, #0x1c]
    ldrsh r0, [sp, #12]
    ldrb r2, [r5, #0x1d]
    ldrsh r1, [sp, #14]
    add r0, r3, r0, asr #3
    mov r0, r0, lsl #24
    add r1, r2, r1, asr #3
    mov r2, r1, lsl #24
    mov r1, r0, asr #24
    mov r2, r2, asr #24
    mov r0, r6
    bl native_fn_021f5518
    add sp, sp, #16
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
L_021f58ac:
    mov r4, #0
    add r1, sp, #12
    mov r0, r7
    mov r2, r6
    mov r3, #2
    str r4, [sp]
    bl native_fn_0204ac20
L_021f58c8:
    add sp, sp, #16
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
    dcd native_data_0222f2ec
}
