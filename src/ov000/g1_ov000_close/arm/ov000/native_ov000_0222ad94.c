/* ov000 row 0x0222ad94: 284 bytes.
 *
 * What it does: 68 instructions; 4 call(s) to 0x0204a574, 0x02063b18, 0x0204a724, +1 more; loops (back edge at +0x90); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x110 -> constant 0x022475fc (image word 0x022475fc)
 *   pool +0x114 -> constant 0x022475dc (image word 0x022475dc)
 *   pool +0x118 -> constant 0x022475d4 (image word 0x022475d4)
 *   branch +0x5c -> +0xf8
 *   branch +0xa0 -> +0xf8
 *   branch +0xb8 -> +0xf8
 *   back edge +0x104 -> +0x48
 *   test +0x1c cmp r0, #0
 *   test +0x30 cmp r0, #0
 *   test +0x58 cmp r9, r0
 *   test +0x9c cmp r0, #0
 *   test +0xb4 cmp r1, r0
 *   test +0x100 cmp r8, r0
 *   1 block transfer(s), 9 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0222ad94; the literal pool and
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

extern void native_fn_0204a574(void);
extern void native_fn_02063b18(void);
extern void native_fn_0204a724(void);


asm u32 native_ov000_0222ad94 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #20
    ldr r7, =0x022475fc
    add r6, sp, #16
    ldrsb r0, [r7, #16]
    mov r8, #0
    strh r8, [r6]
    cmp r0, #0
    addne sp, sp, #20
    strh r8, [r6, #2]
    ldmneia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    ldrh r0, [r7, #12]
    cmp r0, #0
    addle sp, sp, #20
    ldmleia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    ldr r4, =0x022475dc
    mov r5, #16
    mov r11, #1
ov000_0222ad94_L48:
    ldr r0, =0x022475d4
    ldr r1, [r7, #0x4]
    ldrb r0, [r0]
    add r9, r1, r8
    cmp r9, r0
    bge ov000_0222ad94_Lf8
    add r0, r8, #3
    mov r0, r0, lsl #24
    mov r10, r0, asr #24
    mov r0, r9, lsl #1
    ldrh r2, [r4, r0]
    strh r5, [sp, #16]
    mov r0, r10
    stmia sp, {r2, r11}
    mov r1, r6
    mov r2, #0
    mov r3, #3
    str r11, [sp, #0x8]
    bl native_fn_0204a574
    mov r0, r9, lsl #1
    ldrh r0, [r4, r0]
    cmp r0, #0
    beq ov000_0222ad94_Lf8
    mov r0, #46
    bl native_fn_02063b18
    mov r1, r9, lsl #1
    ldrh r1, [r4, r1]
    cmp r1, r0
    bgt ov000_0222ad94_Lf8
    mov r1, #0
    strh r1, [sp, #16]
    mov r1, #3
    str r1, [sp]
    mov r1, #10
    str r1, [sp, #0x4]
    mov r1, #5
    str r1, [sp, #0x8]
    mov r1, #0
    str r1, [sp, #0xc]
    mov r0, r10
    mov r1, r6
    mov r2, #16
    mov r3, #9
    bl native_fn_0204a724
ov000_0222ad94_Lf8:
    add r8, r8, #1
    ldrh r0, [r7, #12]
    cmp r8, r0
    blt ov000_0222ad94_L48
    add sp, sp, #20
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
