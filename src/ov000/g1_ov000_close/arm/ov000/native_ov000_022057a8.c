/* ov000 row 0x022057a8: 1092 bytes.
 *
 * What it does: 272 instructions and 31 call(s), then a 11-entry dispatch through an inline branch table at 0x02205808 (dispatch word at 0x02205800)
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

extern void native_fn_02061944(void);
extern void native_fn_02061dcc(void);
extern void native_fn_02049ffc(void);
extern void native_fn_02008be0(void);
extern void native_fn_02063798(void);
extern void native_fn_0204aaf0(void);
extern void native_fn_021f3628(void);
extern void native_fn_021f35b0(void);
extern void native_fn_02044ff4(void);
extern void native_fn_020602ec(void);


asm u32 native_ov000_022057a8 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    sub sp, sp, #144
    mov r7, r0
    bl native_fn_02061944
    mov r0, r7
    bl native_fn_02061dcc
    add r2, sp, #12
    mov r1, #0
    strh r1, [r2]
    strh r1, [r2, #2]
    ldr r4, [r0]
    cmp r4, #0
    ldrne r0, [r4, #0x4]
    cmpne r0, #0
    addeq sp, sp, #144
    ldmeqia sp!, {r4, r5, r6, r7, r8, pc}
    bl native_fn_02049ffc
    add r1, sp, #80
    mov r0, #0
    mov r2, #64
    bl native_fn_02008be0
    cmp r7, #10
    addls pc, pc, r7, lsl #2
    b L_02205be0
    dcd 0xea0000f4
    dcd 0xea0000f3
    dcd 0xea0000f2
    dcd 0xea0000f1
    dcd 0xea0000f0
    dcd 0xea0000ef
    dcd 0xea000003
    dcd 0xea000024
    dcd 0xea000044
    dcd 0xea00004f
    dcd 0xea0000b7
    ldr r0, [pc, #0x3ac]
    ldrb r0, [r0]
    bl native_fn_02063798
    cmp r0, #0
    mov r2, #1
    add r1, sp, #12
    beq L_02205888
    ldr r0, [pc, #0x390]
    ldrb r3, [r0]
    mov r0, r7
    str r3, [sp]
    str r2, [sp, #0x4]
    str r2, [sp, #0x8]
    mov r2, #11
    mov r3, #0
    bl native_fn_0204aaf0
    ldrsh r1, [sp, #12]
    add r0, r1, r0
    strh r0, [sp, #12]
    add sp, sp, #144
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
L_02205888:
    mov r0, #42
    str r0, [sp]
    str r2, [sp, #0x4]
    str r2, [sp, #0x8]
    mov r0, r7
    mov r2, #5
    mov r3, #7
    bl native_fn_0204aaf0
    ldrsh r1, [sp, #12]
    add r0, r1, r0
    strh r0, [sp, #12]
    add sp, sp, #144
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
    ldr r0, [pc, #0x324]
    ldrb r0, [r0]
    bl native_fn_02063798
    cmp r0, #0
    add r1, sp, #12
    beq L_02205908
    ldr r0, [pc, #0x30c]
    mov r3, #1
    ldrb r2, [r0]
    mov r0, r7
    stmia sp, {r2, r3}
    str r3, [sp, #0x8]
    mov r2, #17
    bl native_fn_0204aaf0
    ldrsh r1, [sp, #12]
    add r0, r1, r0
    strh r0, [sp, #12]
    add sp, sp, #144
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
L_02205908:
    mov r0, #42
    str r0, [sp]
    mov r2, #1
    str r2, [sp, #0x4]
    str r2, [sp, #0x8]
    mov r0, r7
    mov r2, #5
    mov r3, #7
    bl native_fn_0204aaf0
    ldrsh r1, [sp, #12]
    add r0, r1, r0
    strh r0, [sp, #12]
    add sp, sp, #144
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
    mov r0, #38
    str r0, [sp]
    mov r4, #1
    str r4, [sp, #0x4]
    add r1, sp, #12
    mov r0, r7
    mov r2, #9
    mov r3, #5
    str r4, [sp, #0x8]
    bl native_fn_0204aaf0
    add sp, sp, #144
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
    bl native_fn_021f3628
    cmp r0, #0
    addeq sp, sp, #144
    ldmeqia sp!, {r4, r5, r6, r7, r8, pc}
    ldr r0, [pc, #0x260]
    ldrb r0, [r0]
    bl native_fn_02063798
    cmp r0, #0
    beq L_022059a4
    ldr r0, [pc, #0x24c]
    ldrb r0, [r0]
    bl native_fn_021f35b0
    ldrb r5, [r0, #0x3]
L_022059a4:
    ldr r0, [pc, #0x23c]
    ldrb r0, [r0]
    bl native_fn_02063798
    cmp r0, #0
    beq L_02205ae4
    ldr r0, [pc, #0x228]
    ldrb r0, [r0]
    bl native_fn_021f35b0
    ldr r1, [pc, #0x21c]
    ldrh r8, [r0, #4]
    ldrb r0, [r1]
    bl native_fn_021f35b0
    cmp r8, #0
    ldrb r2, [r0, #0x8]
    bne L_02205a40
    cmp r5, #0
    mov r4, #1
    add r1, sp, #12
    bne L_02205a18
    mov r0, #73
    str r0, [sp]
    str r4, [sp, #0x4]
    mov r0, r7
    mov r2, #5
    mov r3, #2
    str r4, [sp, #0x8]
    bl native_fn_0204aaf0
    add sp, sp, #144
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
L_02205a18:
    mov r0, #69
    str r0, [sp]
    str r4, [sp, #0x4]
    mov r0, r7
    mov r2, #5
    mov r3, #2
    str r4, [sp, #0x8]
    bl native_fn_0204aaf0
    add sp, sp, #144
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
L_02205a40:
    add r0, sp, #48
    mov r1, r8
    bl native_fn_02044ff4
    mov r3, #0
    str r3, [sp]
    mov r6, #1
    add r2, sp, #48
    mov r0, r4
    mov r1, r8
    str r6, [sp, #0x4]
    bl native_fn_020602ec
    ldrsh r1, [sp, #12]
    mov r0, r0, lsl #16
    cmp r5, #2
    add r0, r1, r0, asr #16
    strh r0, [sp, #12]
    addlt sp, sp, #144
    ldmltia sp!, {r4, r5, r6, r7, r8, pc}
    ldr r0, [pc, #0x158]
    ldrb r0, [r0]
    bl native_fn_021f35b0
    ldrh r0, [r0, #6]
    cmp r0, #0
    addne sp, sp, #144
    ldmneia sp!, {r4, r5, r6, r7, r8, pc}
    ldrsh r1, [sp, #12]
    mov r0, #68
    mov r2, r6
    add r1, r1, #16
    strh r1, [sp, #12]
    str r0, [sp]
    str r2, [sp, #0x4]
    mov r4, #0
    add r1, sp, #12
    mov r0, r7
    mov r2, #5
    mov r3, #2
    str r4, [sp, #0x8]
    bl native_fn_0204aaf0
    add sp, sp, #144
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
L_02205ae4:
    mov r0, #42
    str r0, [sp]
    mov r4, #1
    str r4, [sp, #0x4]
    add r1, sp, #12
    mov r0, r7
    mov r2, #5
    mov r3, #7
    str r4, [sp, #0x8]
    bl native_fn_0204aaf0
    add sp, sp, #144
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
    ldr r0, [pc, #0xcc]
    ldrb r0, [r0]
    bl native_fn_021f35b0
    ldr r1, [pc, #0xc0]
    ldrh r6, [r0, #6]
    ldrb r0, [r1]
    bl native_fn_021f35b0
    ldr r1, [pc, #0xb0]
    ldrb r8, [r0, #0x9]
    ldrb r0, [r1]
    bl native_fn_021f35b0
    ldr r1, [pc, #0xa0]
    ldrb r5, [r0, #0x3]
    ldrb r0, [r1]
    bl native_fn_02063798
    cmp r0, #0
    cmpne r6, #0
    addeq sp, sp, #144
    ldmeqia sp!, {r4, r5, r6, r7, r8, pc}
    add r0, sp, #16
    mov r1, r6
    mov r2, r8
    bl native_fn_02044ff4
    mov r3, #0
    str r3, [sp]
    mov r12, #1
    add r2, sp, #16
    mov r0, r4
    mov r1, r6
    str r12, [sp, #0x4]
    bl native_fn_020602ec
    ldrsh r1, [sp, #12]
    cmp r5, #2
    add r0, r1, r0
    strh r0, [sp, #12]
    addle sp, sp, #144
    ldmleia sp!, {r4, r5, r6, r7, r8, pc}
    ldrsh r1, [sp, #12]
    mov r0, #68
    mov r2, #1
    add r1, r1, #16
    strh r1, [sp, #12]
    str r0, [sp]
    str r2, [sp, #0x4]
    mov r4, #0
    add r1, sp, #12
    mov r0, r7
    mov r2, #5
    mov r3, #2
    str r4, [sp, #0x8]
    bl native_fn_0204aaf0
L_02205be0:
    add sp, sp, #144
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
    dcd 0x02238190
}
