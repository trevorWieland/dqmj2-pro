/* ov000 row 0x02204fbc: 1392 bytes.
 *
 * What it does: 345 instructions and 36 call(s), then a 11-entry dispatch through an inline branch table at 0x02205030 (dispatch word at 0x02205028)
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
extern void native_fn_020636e0(void);
extern void native_fn_0204ab44(void);
extern void native_fn_0207aa98(void);
extern void native_fn_0207ad3c(void);
extern void native_fn_0204a9d4(void);
extern void native_fn_0204ab98(void);
extern void native_fn_02060600(void);
extern void native_fn_02060738(void);
extern void native_fn_0204aaf0(void);
extern void native_fn_021f360c(void);
extern void native_fn_021f359c(void);
extern void native_fn_0205dc70(void);
extern void native_fn_020602ec(void);
extern u8 native_data_0222f574[];


asm u32 native_ov000_02204fbc (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, lr}
    sub sp, sp, #84
    mov r4, r0
    bl native_fn_02061944
    mov r0, r4
    bl native_fn_02061dcc
    add r2, sp, #16
    mov r1, #0
    strh r1, [r2]
    strh r1, [r2, #2]
    ldr r5, [r0]
    cmp r5, #0
    ldrne r0, [r5, #0x4]
    cmpne r0, #0
    addeq sp, sp, #84
    ldmeqia sp!, {r4, r5, r6, r7, r8, r9, pc}
    bl native_fn_02049ffc
    ldr r0, [pc, #0x518]
    ldrb r0, [r0, #0x9]
    cmp r0, #0
    addeq sp, sp, #84
    ldmeqia sp!, {r4, r5, r6, r7, r8, r9, pc}
    add r1, sp, #20
    mov r0, #0
    mov r2, #64
    bl native_fn_02008be0
    cmp r4, #10
    addls pc, pc, r4, lsl #2
    b L_02205518
    dcd 0xea00008e
    dcd 0xea000099
    dcd 0xea000107
    dcd 0xea000006
    dcd 0xea000134
    dcd 0xea000133
    dcd 0xea00001e
    dcd 0xea00001d
    dcd 0xea00001c
    dcd 0xea00001b
    dcd 0xea00001a
    ldr r0, [pc, #0x4bc]
    ldrb r0, [r0, #0x9]
    bl native_fn_020636e0
    cmp r0, #0
    mov r5, #1
    add r1, sp, #16
    beq L_022050a0
    ldr r0, [pc, #0x4a0]
    mov r3, #0
    ldrb r2, [r0, #0x9]
    mov r0, r4
    stmia sp, {r2, r5}
    mov r2, #8
    str r5, [sp, #0x8]
    bl native_fn_0204ab44
    add sp, sp, #84
    ldmia sp!, {r4, r5, r6, r7, r8, r9, pc}
L_022050a0:
    mov r0, #42
    str r0, [sp]
    str r5, [sp, #0x4]
    mov r0, r4
    mov r2, #5
    mov r3, #7
    str r5, [sp, #0x8]
    bl native_fn_0204ab44
    add sp, sp, #84
    ldmia sp!, {r4, r5, r6, r7, r8, r9, pc}
    ldr r0, [pc, #0x450]
    mov r6, #1
    ldrb r1, [r0, #0x7]
    add r3, sp, #12
    mov r2, #0
    strh r2, [r3]
    strh r2, [r3, #2]
    ldrb r0, [r0, #0x9]
    sub r2, r4, #6
    add r1, r1, r1, lsl #2
    add r1, r2, r1
    mov r9, r6
    and r8, r1, #255
    bl native_fn_0207aa98
    ldr r1, [pc, #0x418]
    mov r7, r0
    ldrb r0, [r1, #0x9]
    bl native_fn_020636e0
    cmp r0, #0
    moveq r6, #0
    beq L_0220512c
    ldr r0, [pc, #0x3fc]
    ldrb r0, [r0, #0x8]
    cmp r8, r0
    movhs r9, #3
L_0220512c:
    mov r0, r7
    bl native_fn_0207ad3c
    cmp r8, r0
    addgt sp, sp, #84
    ldmgtia sp!, {r4, r5, r6, r7, r8, r9, pc}
    mov r3, #1
    str r3, [sp]
    str r3, [sp, #0x4]
    add r1, sp, #12
    mov r0, r4
    mov r2, r9
    add r3, r8, #1
    bl native_fn_0204a9d4
    ldrsh r2, [sp, #12]
    ldr r3, [pc, #0x3b8]
    add r1, sp, #12
    add r2, r2, r0
    strh r2, [sp, #12]
    mov r2, #0
    str r2, [sp]
    mov r0, r4
    mov r2, r9
    bl native_fn_0204ab98
    mov r0, #24
    strh r0, [sp, #12]
    cmp r6, #0
    beq L_022051d4
    add r0, r7, r8, lsl #2
    ldrb r1, [r0, #0xa]
    add r2, sp, #12
    cmp r1, #0
    beq L_022051bc
    mov r0, r5
    mov r3, r9
    bl native_fn_02060600
    b L_02205200
L_022051bc:
    add r0, r7, r8
    ldrb r1, [r0, #0x32]
    mov r0, r5
    mov r3, r9
    bl native_fn_02060738
    b L_02205200
L_022051d4:
    mov r0, #42
    str r0, [sp]
    mov r2, #1
    str r2, [sp, #0x4]
    mov r5, #0
    add r1, sp, #12
    mov r0, r4
    mov r2, #5
    mov r3, #7
    str r5, [sp, #0x8]
    bl native_fn_0204aaf0
L_02205200:
    mov r0, #200
    strh r0, [sp, #12]
    cmp r6, #0
    add r1, sp, #12
    beq L_0220523c
    mov r0, #3
    str r0, [sp]
    mov r0, #0
    str r0, [sp, #0x4]
    ldrb r3, [r7, r8]
    mov r0, r4
    mov r2, r9
    bl native_fn_0204a9d4
    add sp, sp, #84
    ldmia sp!, {r4, r5, r6, r7, r8, r9, pc}
L_0220523c:
    mov r0, #43
    stmia sp, {r0, r9}
    mov r2, #0
    str r2, [sp, #0x8]
    mov r0, r4
    mov r2, #5
    mov r3, #7
    bl native_fn_0204aaf0
    ldrsh r1, [sp, #12]
    add r0, r1, r0
    strh r0, [sp, #12]
    add sp, sp, #84
    ldmia sp!, {r4, r5, r6, r7, r8, r9, pc}
    mov r0, #70
    str r0, [sp]
    mov r5, #1
    str r5, [sp, #0x4]
    add r1, sp, #16
    mov r0, r4
    mov r2, #5
    mov r3, #2
    str r5, [sp, #0x8]
    bl native_fn_0204aaf0
    add sp, sp, #84
    ldmia sp!, {r4, r5, r6, r7, r8, r9, pc}
    bl native_fn_021f360c
    cmp r0, #0
    addeq sp, sp, #84
    ldmeqia sp!, {r4, r5, r6, r7, r8, r9, pc}
    ldr r0, [pc, #0x268]
    ldrb r0, [r0, #0x9]
    bl native_fn_021f359c
    ldr r1, [pc, #0x25c]
    ldrb r6, [r0, #0x3]
    ldrb r0, [r1, #0x9]
    bl native_fn_020636e0
    cmp r0, #0
    beq L_0220542c
    ldr r0, [pc, #0x244]
    ldrb r0, [r0, #0x9]
    bl native_fn_021f359c
    ldrh r8, [r0, #4]
    cmp r8, #0
    bne L_0220534c
    cmp r6, #0
    mov r5, #1
    add r1, sp, #16
    bne L_02205324
    mov r0, #73
    str r0, [sp]
    str r5, [sp, #0x4]
    mov r0, r4
    mov r2, #5
    mov r3, #2
    str r5, [sp, #0x8]
    bl native_fn_0204aaf0
    add sp, sp, #84
    ldmia sp!, {r4, r5, r6, r7, r8, r9, pc}
L_02205324:
    mov r0, #69
    str r0, [sp]
    str r5, [sp, #0x4]
    mov r0, r4
    mov r2, #5
    mov r3, #2
    str r5, [sp, #0x8]
    bl native_fn_0204aaf0
    add sp, sp, #84
    ldmia sp!, {r4, r5, r6, r7, r8, r9, pc}
L_0220534c:
    ldr r0, [pc, #0x1d4]
    cmp r8, r0
    bne L_02205388
    mov r0, #75
    str r0, [sp]
    mov r5, #1
    str r5, [sp, #0x4]
    add r1, sp, #16
    mov r0, r4
    mov r2, #5
    mov r3, #2
    str r5, [sp, #0x8]
    bl native_fn_0204aaf0
    add sp, sp, #84
    ldmia sp!, {r4, r5, r6, r7, r8, r9, pc}
L_02205388:
    mov r2, r8
    mov r0, #2
    mov r1, #0
    bl native_fn_0205dc70
    mov r3, #0
    mov r2, r0
    str r3, [sp]
    mov r7, #1
    mov r0, r5
    mov r1, r8
    str r7, [sp, #0x4]
    bl native_fn_020602ec
    ldrsh r1, [sp, #16]
    cmp r6, #2
    add r0, r1, r0
    strh r0, [sp, #16]
    addlt sp, sp, #84
    ldmltia sp!, {r4, r5, r6, r7, r8, r9, pc}
    ldr r0, [pc, #0x148]
    ldrb r0, [r0, #0x9]
    bl native_fn_021f359c
    ldrh r0, [r0, #6]
    cmp r0, #0
    addne sp, sp, #84
    ldmneia sp!, {r4, r5, r6, r7, r8, r9, pc}
    ldrsh r1, [sp, #16]
    mov r0, #68
    mov r2, r7
    add r1, r1, #16
    strh r1, [sp, #16]
    str r0, [sp]
    mov r0, r4
    str r2, [sp, #0x4]
    mov r4, #0
    add r1, sp, #16
    mov r2, #5
    mov r3, #2
    str r4, [sp, #0x8]
    bl native_fn_0204aaf0
    add sp, sp, #84
    ldmia sp!, {r4, r5, r6, r7, r8, r9, pc}
L_0220542c:
    mov r0, #42
    str r0, [sp]
    mov r5, #1
    str r5, [sp, #0x4]
    add r1, sp, #16
    mov r0, r4
    mov r2, #5
    mov r3, #7
    str r5, [sp, #0x8]
    bl native_fn_0204aaf0
    add sp, sp, #84
    ldmia sp!, {r4, r5, r6, r7, r8, r9, pc}
    ldr r0, [pc, #0xbc]
    ldrb r0, [r0, #0x9]
    bl native_fn_021f359c
    ldr r1, [pc, #0xb0]
    ldrh r7, [r0, #6]
    ldrb r0, [r1, #0x9]
    bl native_fn_021f359c
    ldr r1, [pc, #0xa0]
    ldrb r8, [r0, #0x3]
    ldrb r0, [r1, #0x9]
    bl native_fn_020636e0
    cmp r0, #0
    cmpne r7, #0
    addeq sp, sp, #84
    ldmeqia sp!, {r4, r5, r6, r7, r8, r9, pc}
    mov r2, r7
    mov r0, #2
    mov r1, #0
    bl native_fn_0205dc70
    mov r3, #0
    mov r2, r0
    str r3, [sp]
    mov r6, #1
    mov r0, r5
    mov r1, r7
    str r6, [sp, #0x4]
    bl native_fn_020602ec
    ldrsh r1, [sp, #16]
    cmp r8, #2
    add r0, r1, r0
    strh r0, [sp, #16]
    addle sp, sp, #84
    ldmleia sp!, {r4, r5, r6, r7, r8, r9, pc}
    ldrsh r1, [sp, #16]
    mov r0, #68
    mov r2, r6
    add r1, r1, #16
    strh r1, [sp, #16]
    str r0, [sp]
    mov r0, r4
    str r2, [sp, #0x4]
    mov r4, #0
    add r1, sp, #16
    mov r2, #5
    mov r3, #2
    str r4, [sp, #0x8]
    bl native_fn_0204aaf0
L_02205518:
    add sp, sp, #84
    ldmia sp!, {r4, r5, r6, r7, r8, r9, pc}
    dcd 0x02238190
    dcd native_data_0222f574
    dcd 0x0000ffff
}
