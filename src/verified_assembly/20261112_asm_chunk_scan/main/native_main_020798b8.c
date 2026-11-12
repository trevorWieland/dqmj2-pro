/* main row 0x020798b8: 1204 bytes.
 *
 * What it does: Copies a 5-register block to an optional destination under a condition in one predicated move.
 *
 * Decoded shape: predicated block copy.
 *
 *   pool +0x490 -> native_data_021c65d0 (image word 0x021c65d0)
 *   pool +0x494 -> native_data_021c6544 (image word 0x021c6544)
 *   pool +0x498 -> native_data_021c9698 (image word 0x021c9698)
 *   pool +0x49c -> native_data_020de46c (image word 0x020de46c)
 *   pool +0x4a0 -> constant 0x88888889 (image word 0x88888889)
 *   pool +0x4a4 -> native_data_022550ff (image word 0x022550ff)
 *   pool +0x4a8 -> constant 0x91a2b3c5 (image word 0x91a2b3c5)
 *   pool +0x4ac -> native_data_020de470 (image word 0x020de470)
 *   pool +0x4b0 -> native_data_020de474 (image word 0x020de474)
 *   back edge +0x3c -> +0x24
 *   branch +0x80 -> +0x444
 *   branch +0xf0 -> +0x1d8
 *   branch +0x190 -> +0x1bc
 *   back edge +0x1d4 -> +0x100
 *   branch +0x404 -> +0x430
 *   back edge +0x438 -> +0x3f4
 *   test +0x7c cmp r1, #0
 *   test +0xe0 cmp r6, #0
 *   test +0x18c cmp r3, #100
 *   test +0x198 tst r1, #128
 *   test +0x1d0 cmp r5, r6
 *   test +0x26c cmp r0, r4
 *   test +0x400 cmp r0, #100
 *   test +0x434 cmp r8, #3
 *   46 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020798b8; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02217440(void);
extern u8 native_data_021c65d0[];
extern void native_fn_02049ad0(void);
extern void native_fn_02049ffc(void);
extern u8 native_data_021c6544[];
extern u8 native_data_021c9698[];
extern void native_fn_02046af4(void);
extern void native_fn_0204a104(void);
extern void native_fn_020602ec(void);
extern void native_fn_0204a574(void);
extern u8 native_data_020de46c[];
extern void native_fn_0204a154(void);
extern void native_fn_021df3bc(void);
extern u8 native_data_022550ff[];
extern u8 native_data_020de470[];
extern void native_fn_0208791c(void);
extern u8 native_data_020de474[];
extern void native_fn_0221742c(void);
extern void native_fn_02065818(void);
extern void native_fn_0204a644(void);


asm u32 native_main_020798b8 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #76
    bl native_fn_02217440
    add r0, sp, #12
    mov r2, #0
    add r1, sp, #16
    strh r2, [r0]
    strh r2, [r0, #2]
    mov r0, #7
main_020798b8_L24:
    strh r2, [r1]
    strh r2, [r1, #2]
    strh r2, [r1, #4]
    strh r2, [r1, #6]
    add r1, r1, #8
    subs r0, r0, #1
    bne main_020798b8_L24
    strh r2, [r1]
    mov r0, #12
    strh r2, [r1, #2]
    ldr r7, =native_data_021c65d0
    bl native_fn_02049ad0
    mov r8, r0
    mov r0, #12
    mov r9, #0
    bl native_fn_02049ad0
    ldr r0, [r0]
    ldr r4, [r0, #0x4]
    mov r0, r4
    bl native_fn_02049ffc
    ldr r0, =native_data_021c6544
    ldr r1, [r0, #0x18]
    cmp r1, #0
    beq main_020798b8_L444
    mov r1, #16
    strh r1, [sp, #12]
    ldrsh r1, [r0, #18]
    ldrb r0, [r4, #0x1d]
    mov r2, r9
    ldrb r6, [r7, #0x5d]
    sub r0, r1, r0
    mov r0, r0, lsl #3
    strh r0, [sp, #14]
    add r1, sp, #16
    str r1, [sp]
    mov r4, #255
    ldr r0, =native_data_021c9698
    mov r3, r2
    add r1, r7, #4
    str r4, [sp, #0x4]
    bl native_fn_02046af4
    add r1, sp, #12
    add r3, sp, #16
    mov r0, #12
    mov r2, #1
    bl native_fn_0204a104
    ldrsh r0, [sp, #14]
    cmp r6, #0
    mov r5, r9
    add r0, r0, #16
    strh r0, [sp, #14]
    ble main_020798b8_L1d8
    add r10, r7, #24
    add r4, sp, #12
    mov r11, #1
main_020798b8_L100:
    ldrsh r1, [sp, #14]
    add r0, r7, r5, lsl #1
    mov r2, r10
    stmia sp, {r1, r11}
    ldrh r1, [r0, #84]
    ldr r0, [r8]
    mov r3, #24
    bl native_fn_020602ec
    mov r0, #120
    strh r0, [sp, #12]
    mov r0, #1
    str r0, [sp]
    str r0, [sp, #0x4]
    mov r0, #0
    str r0, [sp, #0x8]
    mov r0, #12
    mov r1, r4
    mov r2, #5
    mov r3, #1
    bl native_fn_0204a574
    ldrsh r3, [sp, #12]
    mov r1, r4
    mov r2, #1
    add r0, r3, r0
    strh r0, [sp, #12]
    ldr r3, =native_data_020de46c
    mov r0, #12
    bl native_fn_0204a104
    ldrsh r2, [sp, #12]
    add r1, r7, r5
    ldrb r1, [r1, #0x5a]
    add r0, r2, r0
    strh r0, [sp, #12]
    bic r3, r1, #128
    ldrsh r9, [sp, #12]
    cmp r3, #100
    bge main_020798b8_L1bc
    mov r0, #2
    tst r1, #128
    movne r2, #5
    str r0, [sp]
    mov r0, #0
    str r0, [sp, #0x4]
    moveq r2, #1
    mov r0, #12
    mov r1, r4
    bl native_fn_0204a154
main_020798b8_L1bc:
    ldrsh r0, [sp, #14]
    add r10, r10, #20
    add r5, r5, #1
    add r0, r0, #16
    strh r0, [sp, #14]
    cmp r5, r6
    blt main_020798b8_L100
main_020798b8_L1d8:
    mov r0, #16
    strh r0, [sp, #12]
    mov r0, #58
    str r0, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    mov r0, #0
    str r0, [sp, #0x8]
    add r1, sp, #12
    mov r0, #12
    mov r2, #5
    mov r3, #2
    bl native_fn_0204a574
    ldrsh r1, [sp, #12]
    add r1, r1, r0
    ldrb r0, [r7, #0x5e]
    strh r1, [sp, #12]
    bl native_fn_021df3bc
    ldrb r1, [r0, #0x2]
    mov r0, #1
    mov r3, #0
    str r1, [sp]
    stmib sp, {r0, r3}
    add r1, sp, #12
    mov r0, #12
    mov r2, #6
    bl native_fn_0204a574
    ldrsh r3, [sp, #12]
    ldrsh r2, [sp, #14]
    ldr r1, [r7]
    add r0, r3, r0
    strh r0, [sp, #12]
    ldr r0, =0x88888889
    add r2, r2, #16
    umull r0, r4, r1, r0
    ldr r0, =native_data_022550ff
    mov r4, r4, lsr #4
    cmp r0, r4
    strh r2, [sp, #14]
    movlo r4, r0
    mov r0, #16
    strh r0, [sp, #12]
    mov r0, #10
    str r0, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    mov r0, #0
    str r0, [sp, #0x8]
    add r1, sp, #12
    mov r0, #12
    mov r2, #5
    mov r3, #2
    bl native_fn_0204a574
    ldrsh r3, [sp, #12]
    ldr r1, =0x91a2b3c5
    mov r2, #4
    add r0, r3, r0
    strh r0, [sp, #12]
    umull r0, r3, r4, r1
    ldrsh r5, [sp, #12]
    add r1, sp, #12
    mov r3, r3, lsr #11
    add r0, r5, #8
    strh r0, [sp, #12]
    str r2, [sp]
    mov r0, #0
    str r0, [sp, #0x4]
    mov r0, #12
    mov r2, #1
    bl native_fn_0204a154
    ldrsh r3, [sp, #12]
    add r1, sp, #12
    mov r2, #1
    add r0, r3, r0
    strh r0, [sp, #12]
    ldr r3, =native_data_020de470
    mov r0, #12
    bl native_fn_0204a104
    ldrsh r2, [sp, #12]
    ldr r1, =0x91a2b3c5
    mov r3, r4
    add r0, r2, r0
    strh r0, [sp, #12]
    umull r0, r4, r3, r1
    mov r4, r4, lsr #11
    mov r2, #3600
    umull r0, r1, r2, r4
    sub r4, r3, r0
    ldr r0, =0x88888889
    add r1, sp, #16
    umull r2, r0, r4, r0
    mov r0, r0, lsr #5
    mov r2, #60
    mov r3, #2
    bl native_fn_0208791c
    mov r0, #12
    add r1, sp, #12
    mov r2, #1
    add r3, sp, #16
    bl native_fn_0204a104
    ldrsh r3, [sp, #12]
    add r1, sp, #12
    mov r2, #1
    add r0, r3, r0
    strh r0, [sp, #12]
    ldr r3, =native_data_020de474
    mov r0, #12
    bl native_fn_0204a104
    ldrsh r1, [sp, #12]
    mov r2, #60
    mov r3, #2
    add r0, r1, r0
    strh r0, [sp, #12]
    ldr r0, =0x88888889
    umull r1, r0, r4, r0
    mov r0, r0, lsr #5
    umull r0, r1, r2, r0
    add r1, sp, #16
    sub r0, r4, r0
    bl native_fn_0208791c
    add r1, sp, #12
    add r3, sp, #16
    mov r0, #12
    mov r2, #1
    bl native_fn_0204a104
    ldrsh r2, [sp, #12]
    add r1, r9, #7
    mov r8, #0
    add r0, r2, r0
    mov r1, r1, asr #3
    strh r0, [sp, #12]
    add r0, r1, #2
    mov r0, r0, lsl #24
    mov r4, r0, asr #24
    mov r5, r8
main_020798b8_L3f4:
    add r0, r7, r8
    ldrb r0, [r0, #0x5a]
    bic r0, r0, #128
    cmp r0, #100
    blt main_020798b8_L430
    mov r0, r5
    bl native_fn_0221742c
    add r1, r8, #4
    sub r1, r1, r6
    mov r1, r1, lsl #1
    add r1, r1, #11
    mov r2, r1, lsl #24
    mov r1, r4
    mov r2, r2, asr #24
    bl native_fn_02065818
main_020798b8_L430:
    add r8, r8, #1
    cmp r8, #3
    blt main_020798b8_L3f4
    add sp, sp, #76
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
main_020798b8_L444:
    mov r1, r9
    strh r1, [sp, #12]
    ldrsh r2, [r0, #18]
    ldrb r1, [r4, #0x1d]
    mov r0, #66
    mov r4, #1
    sub r1, r2, r1
    add r1, r1, #2
    mov r1, r1, lsl #3
    strh r1, [sp, #14]
    stmia sp, {r0, r4}
    add r1, sp, #12
    mov r0, #12
    mov r2, #5
    mov r3, #2
    str r4, [sp, #0x8]
    bl native_fn_0204a644
    add sp, sp, #76
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
