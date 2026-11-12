/* ov006 row 0x021dea9c: 512 bytes.
 *
 * What it does: Writes one block of 2 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x1ec -> native_data2_0220f738 (image word 0x0220f738)
 *   pool +0x1f0 -> native_data2_0220f614 (image word 0x0220f614)
 *   pool +0x1f4 -> constant 0x0220f72c (image word 0x0220f72c)
 *   pool +0x1f8 -> native_data6_0220f594 (image word 0x0220f594)
 *   pool +0x1fc -> constant 0x0220f644 (image word 0x0220f644)
 *   back edge +0x3c -> +0x24
 *   branch +0x8c -> +0xc8
 *   back edge +0xdc -> +0x84
 *   branch +0x120 -> +0x170
 *   branch +0x1b0 -> +0x1d8
 *   test +0x2c cmp r0, #1
 *   test +0x38 cmp r7, #3
 *   test +0x44 cmp r10, r0
 *   test +0x88 cmp r0, #1
 *   test +0xd4 cmp r7, #2
 *   test +0x11c cmp r0, #1
 *   test +0x1ac cmp r0, #1
 *   1 block transfer(s), 16 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021dea9c; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity proves the instruction stream, not the meaning of the fields, blocks and callee contracts it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data2_0220f738[];
extern u8 native_data2_0220f614[];
extern u8 native_data6_0220f594[];
extern void native_fn_021dec9c(void);
extern void native_fn_021dfd80(void);
extern void native_fn_021de980(void);
extern void native_fn_02067748(void);
extern void native_fn_0205dc70(void);
extern void native_fn_02048034(void);
extern void native_fn_021df140(void);
extern void native_fn_0204b5b0(void);
extern void native_fn_02049604(void);
extern void native_fn_021df310(void);
extern void native_fn_021df4b0(void);
extern void native_fn_020414c8(void);
extern void native_fn_02041538(void);
extern void native_fn_02041908(void);


asm u32 native_ov006_021dea9c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, lr}
    sub sp, sp, #20
    mov r10, r0
    mov r4, #0
    mov r9, r1
    ldr r5, =native_data2_0220f738
    ldr r1, =native_data2_0220f614
    mov r6, r10
    mov r7, r4
ov006_021dea9c_L24:
    ldr r0, [r1, r7, lsl #4]
    add r7, r7, #1
    cmp r0, #1
    addeq r0, r4, #1
    andeq r4, r0, #255
    cmp r7, #3
    blt ov006_021dea9c_L24
    rsb r0, r4, #8
    cmp r10, r0
    andgt r10, r0, #255
    ldr r0, =0x0220f72c
    ldrsh r1, [sp, #60]
    strh r3, [r0, #2]
    ldrsh r3, [sp, #56]
    strh r1, [r0, #6]
    strb r2, [r0]
    ldr r1, =native_data6_0220f594
    mov r2, #4
    strb r2, [r1, #0x2]
    strh r3, [r0, #4]
    bl native_fn_021dec9c
    ldr r8, =native_data2_0220f614
    ldr r4, =native_data6_0220f594
    mov r7, #0
ov006_021dea9c_L84:
    ldr r0, [r8]
    cmp r0, #1
    bne ov006_021dea9c_Lc8
    ldrb r0, [r8, #0x8]
    add r1, r7, #1
    rsb r3, r7, #26
    str r0, [sp]
    ldrh r2, [r8, #10]
    mov r0, r7
    and r1, r1, #255
    str r2, [sp, #0x4]
    ldrb r2, [r4, #0x2]
    and r3, r3, #255
    bl native_fn_021dfd80
    ldrb r0, [r4, #0x2]
    add r0, r0, #2
    strb r0, [r4, #0x2]
ov006_021dea9c_Lc8:
    add r0, r7, #1
    mov r0, r0, lsl #24
    mov r7, r0, asr #24
    cmp r7, #2
    add r8, r8, #16
    ble ov006_021dea9c_L84
    mov r0, r10, lsl #1
    and r0, r0, #255
    stmia sp, {r0, r10}
    str r6, [sp, #0x8]
    mov r0, #0
    str r0, [sp, #0xc]
    ldr r0, =native_data6_0220f594
    str r9, [sp, #0x10]
    ldrb r2, [r0, #0x2]
    ldr r0, =native_data2_0220f738
    mov r1, #1
    mov r3, #24
    bl native_fn_021de980
    ldr r4, =0x0220f644
    ldr r0, [r4]
    cmp r0, #1
    bne ov006_021dea9c_L170
    bl native_fn_02067748
    ldr r1, [r0, #0x4]
    mov r0, #15
    add r1, r1, #59
    mov r1, r1, lsl #16
    mov r2, r1, lsr #16
    mov r1, #2
    bl native_fn_0205dc70
    mov r1, #0
    bl native_fn_02048034
    ldrb r2, [r4, #0x8]
    mov r0, #3
    mov r1, #2
    str r2, [sp]
    ldrh r4, [r4, #10]
    mov r2, #22
    mov r3, #28
    str r4, [sp, #0x4]
    bl native_fn_021dfd80
ov006_021dea9c_L170:
    bl native_fn_021df140
    mov r1, #192
    bl native_fn_0204b5b0
    ldr r2, =native_data6_0220f594
    mov r3, #0
    mov r0, r5
    mov r1, #1
    str r9, [r5]
    strb r3, [r2, #0x3]
    bl native_fn_02049604
    bl native_fn_021df310
    mov r0, #1
    bl native_fn_021df4b0
    ldr r0, =native_data6_0220f594
    ldr r0, [r0, #0x40]
    cmp r0, #1
    bne ov006_021dea9c_L1d8
    mov r0, #63
    bl native_fn_020414c8
    mov r0, #0
    mov r1, #2
    mov r2, #8
    bl native_fn_02041538
    mov r0, #8
    mov r1, #10
    bl native_fn_02041908
ov006_021dea9c_L1d8:
    ldr r0, =native_data6_0220f594
    mov r1, #0
    str r1, [r0, #0x40]
    add sp, sp, #20
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, pc}
}
