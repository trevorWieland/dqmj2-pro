/* ov001 row 0x021d95b0: 292 bytes.
 *
 * What it does: 73 instructions; 5 call(s) to 0x021d96b0, 0x02028fac, 0x02000ce8, +2 more; loops (back edge at +0x28); returns through pop {r3, r4, r5, pc}
 *
 * Decoded shape: block copy loop (73 instructions, 5 calls, 2 branches, 4 back edges, 0 literal slots).
 *
 *   branch +0x18 -> +0x100
 *   branch +0x30 -> +0x100
 *   branch +0x104 -> +0x118
 *   test +0x14 cmp r1, #0
 *   test +0x2c cmp r0, #0
 *   test +0x100 cmp r4, #0
 *   2 block transfer(s), 9 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021d95b0; the literal pool and
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

extern void native_fn_02028fac(void);
extern void native_fn_02000ce8(void);
extern void native_fn_02028044(void);
extern void native_fn_0200103c(void);


asm u32 native_ov001_021d95b0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    sub sp, sp, #48
    mov r5, r0
    ldr r1, [r5, #0x1e0]
    mov r4, #0
    cmp r1, #0
    blt ov001_021d95b0_L100
    ldr r2, [r5, #0x60]
    add r3, sp, #36
    ldr r2, [r2]
    bl native_fn_02028fac
    cmp r0, #0
    beq ov001_021d95b0_L100
    ldr r2, [r5, #0x7c]
    ldr r1, [sp, #0x24]
    ldr r0, [sp, #0x28]
    smull r3, r1, r2, r1
    adds r2, r3, #2048
    adc r1, r1, #0
    mov r2, r2, lsr #12
    orr r2, r2, r1, lsl #20
    str r2, [sp, #0x24]
    ldr r2, [r5, #0x7c]
    ldr r1, [sp, #0x2c]
    smull r3, r0, r2, r0
    adds r2, r3, #2048
    adc r0, r0, #0
    mov r2, r2, lsr #12
    orr r2, r2, r0, lsl #20
    str r2, [sp, #0x28]
    ldr r2, [r5, #0x7c]
    add r0, sp, #0
    smull r3, r1, r2, r1
    adds r2, r3, #2048
    adc r1, r1, #0
    mov r2, r2, lsr #12
    orr r2, r2, r1, lsl #20
    str r2, [sp, #0x2c]
    bl native_fn_02000ce8
    ldr r1, [r5, #0x8c]
    add r0, sp, #0
    bl native_fn_02028044
    add r0, sp, #36
    add r1, sp, #0
    mov r2, r0
    bl native_fn_0200103c
    ldr r1, [sp, #0x24]
    ldr r0, [r5, #0x70]
    ldr r2, [sp, #0x28]
    add r3, r1, r0
    str r3, [sp, #0x24]
    ldr r0, [r5, #0x74]
    ldr r1, [sp, #0x2c]
    add r0, r2, r0
    str r0, [sp, #0x28]
    ldr r0, [r5, #0x78]
    mov r4, #1
    add r0, r1, r0
    str r0, [sp, #0x2c]
    str r3, [r5, #0x110]
    ldr r0, [r5, #0x74]
    str r0, [r5, #0x114]
    ldr r0, [sp, #0x2c]
    str r0, [r5, #0x118]
ov001_021d95b0_L100:
    cmp r4, #0
    bne ov001_021d95b0_L118
    add r0, r5, #112
    add r3, r5, #272
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
ov001_021d95b0_L118:
    mov r0, r4
    add sp, sp, #48
    ldmia sp!, {r3, r4, r5, pc}
}
