/* ov000 row 0x022033e0: 680 bytes.
 *
 * What it does: 166 instructions; 17 call(s) to 0x02061944, 0x02061dcc, 0x02049ffc, +14 more; loops (back edge at +0x0c); returns through pop {r4, r5, r6, r7, r8, r9, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x298 -> constant 0x021c9698 (image word 0x021c9698)
 *   pool +0x29c -> constant 0x02238190 (image word 0x02238190)
 *   pool +0x2a0 -> native_data_0222f560 (image word 0x0222f560)
 *   pool +0x2a4 -> native_data_0222b9f4 (image word 0x0222b9f4)
 *   branch +0x70 -> +0x80
 *   branch +0x84 -> +0xa0
 *   branch +0x8c -> +0x128
 *   branch +0x94 -> +0x24c
 *   branch +0xc0 -> +0xf4
 *   branch +0x1b0 -> +0x20c
 *   test +0x38 cmp r6, #0
 *   test +0x40 cmpne r7, #0
 *   test +0x6c cmp r0, #0
 *   test +0x78 cmp r0, #0
 *   test +0x80 cmp r9, #0
 *   test +0x88 cmp r9, #2
 *   test +0x90 cmp r9, #3
 *   test +0xa8 cmp r0, #0
 *   test +0xbc cmp r0, #0
 *   test +0x130 cmp r0, #0
 *   test +0x1a8 cmp r0, #0
 *   test +0x1ac cmpne r8, #0
 *   1 block transfer(s), 25 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022033e0; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity fixes the instruction stream, not the field, block and callee semantics behind the addresses and strides it touches.
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
extern void native_fn_02072f48(void);
extern void native_fn_020635d4(void);
extern void native_fn_02060434(void);
extern void native_fn_0205dc70(void);
extern void native_fn_0204abd4(void);
extern void native_fn_0204aaf0(void);
extern u8 native_data_0222f560[];
extern void native_fn_02087a48(void);
extern void native_fn_02044dc4(void);
extern u8 native_data_0222b9f4[];
extern void native_fn_0204ab44(void);


asm u32 native_ov000_022033e0 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, lr}
    sub sp, sp, #84
    mov r9, r0
    bl native_fn_02061944
    mov r4, r0
    mov r0, r9
    ldr r5, =0x021c9698
    bl native_fn_02061dcc
    add r2, sp, #16
    mov r1, #0
    strh r1, [r2]
    strh r1, [r2, #2]
    ldr r6, [r0]
    mov r8, #1
    cmp r6, #0
    ldrne r7, [r6, #0x4]
    cmpne r7, #0
    addeq sp, sp, #84
    ldmeqia sp!, {r4, r5, r6, r7, r8, r9, pc}
    mov r0, r7
    bl native_fn_02049ffc
    add r1, sp, #20
    mov r0, #0
    mov r2, #64
    bl native_fn_02008be0
    ldr r0, =0x02238190
    ldrsh r0, [r0, #12]
    cmp r0, #0
    ble ov000_022033e0_L80
    bl native_fn_02072f48
    cmp r0, #0
    movne r8, #0
ov000_022033e0_L80:
    cmp r9, #0
    beq ov000_022033e0_La0
    cmp r9, #2
    beq ov000_022033e0_L128
    cmp r9, #3
    beq ov000_022033e0_L24c
    add sp, sp, #84
    ldmia sp!, {r4, r5, r6, r7, r8, r9, pc}
ov000_022033e0_La0:
    ldr r1, =0x02238190
    ldrsh r0, [r1, #12]
    cmp r0, #0
    addeq sp, sp, #84
    ldmeqia sp!, {r4, r5, r6, r7, r8, r9, pc}
    ldrb r1, [r1, #0xe]
    bl native_fn_020635d4
    cmp r0, #0
    beq ov000_022033e0_Lf4
    mov r3, #0
    str r3, [sp]
    mov r1, #1
    str r1, [sp, #0x4]
    ldr r0, =0x02238190
    str r1, [sp, #0x8]
    ldrsh r1, [r0, #12]
    ldrb r2, [r0, #0xe]
    mov r0, r6
    bl native_fn_02060434
    add sp, sp, #84
    ldmia sp!, {r4, r5, r6, r7, r8, r9, pc}
ov000_022033e0_Lf4:
    mov r0, #5
    mov r1, #7
    mov r2, #42
    bl native_fn_0205dc70
    str r0, [sp]
    mov r3, #1
    add r2, sp, #16
    mov r0, r9
    mov r1, r5
    str r3, [sp, #0x4]
    bl native_fn_0204abd4
    add sp, sp, #84
    ldmia sp!, {r4, r5, r6, r7, r8, r9, pc}
ov000_022033e0_L128:
    ldr r0, =0x02238190
    ldrsh r0, [r0, #12]
    cmp r0, #0
    addeq sp, sp, #84
    ldmeqia sp!, {r4, r5, r6, r7, r8, r9, pc}
    mov r0, #8
    str r0, [sp]
    mov r3, #1
    str r3, [sp, #0x4]
    add r1, sp, #16
    mov r0, r9
    str r3, [sp, #0x8]
    mov r2, #5
    bl native_fn_0204aaf0
    strh r0, [sp, #16]
    mov r2, #1
    mov r1, #0
    ldr r0, =native_data_0222f560
    str r2, [sp]
    str r0, [sp, #0x4]
    ldrsh r2, [sp, #16]
    mov r0, r7
    mov r3, r1
    bl native_fn_02087a48
    ldrsh r2, [sp, #16]
    mov r0, r0, lsl #16
    ldr r1, =0x02238190
    add r0, r2, r0, asr #16
    strh r0, [sp, #16]
    ldrsh r0, [r1, #12]
    ldrb r1, [r1, #0xe]
    bl native_fn_020635d4
    cmp r0, #0
    cmpne r8, #0
    beq ov000_022033e0_L20c
    ldr r1, =0x02238190
    ldrsh r0, [r1, #12]
    ldrb r1, [r1, #0xe]
    bl native_fn_02044dc4
    sub r0, r0, #1
    mov r0, r0, lsl #16
    mov r0, r0, lsr #16
    str r0, [sp]
    mov r0, #1
    mov r2, #5
    str r0, [sp, #0x4]
    mov r4, #0
    add r1, sp, #16
    mov r0, r9
    mov r3, r2
    str r4, [sp, #0x8]
    bl native_fn_0204aaf0
    ldrsh r1, [sp, #16]
    add r0, r1, r0
    strh r0, [sp, #16]
    add sp, sp, #84
    ldmia sp!, {r4, r5, r6, r7, r8, r9, pc}
ov000_022033e0_L20c:
    mov r0, #43
    str r0, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    mov r2, #0
    str r2, [sp, #0x8]
    add r1, sp, #16
    mov r0, r9
    mov r2, #5
    mov r3, #7
    bl native_fn_0204aaf0
    ldrsh r1, [sp, #16]
    add r0, r1, r0
    strh r0, [sp, #16]
    add sp, sp, #84
    ldmia sp!, {r4, r5, r6, r7, r8, r9, pc}
ov000_022033e0_L24c:
    add r1, sp, #12
    mov r0, #0
    strh r0, [r1]
    strh r0, [r1, #2]
    add r0, r4, #512
    ldrsb r2, [r0, #105]
    ldr r0, =native_data_0222b9f4
    mov r4, #1
    sub r2, r2, #12
    mov r2, r2, lsl #1
    ldrh r3, [r0, r2]
    mov r0, r9
    mov r2, #5
    stmia sp, {r3, r4}
    mov r3, #2
    str r4, [sp, #0x8]
    bl native_fn_0204ab44
    add sp, sp, #84
    ldmia sp!, {r4, r5, r6, r7, r8, r9, pc}
}
