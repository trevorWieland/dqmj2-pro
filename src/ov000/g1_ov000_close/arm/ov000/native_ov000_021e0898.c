/* ov000 row 0x021e0898: 172 bytes.
 *
 * What it does: 41 instructions; 3 call(s) to 0x02028044, 0x0200103c, 0x02029870; loops (back edge at +0x3c); returns through pop {r3, r4, r5, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xa4 -> constant 0x66666667 (image word 0x66666667)
 *   pool +0xa8 -> constant 0x022322d4 (image word 0x022322d4)
 *   0 block transfer(s), 9 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e0898; the literal pool and
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

extern void native_fn_02028044(void);
extern void native_fn_0200103c(void);
extern void native_fn_02029870(void);


asm u32 native_ov000_021e0898 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    sub sp, sp, #48
    ldr r4, =0x66666667
    mov r3, r2, lsl #4
    mov r2, r3, lsr #31
    smull r3, r12, r4, r3
    mov lr, #0
    add r12, r2, r12, asr #2
    mov r5, r0
    mov r4, r1
    str lr, [sp, #0x24]
    str lr, [sp, #0x28]
    str r12, [sp, #0x2c]
    ldr r1, [r4, #0x4]
    add r0, sp, #0
    bl native_fn_02028044
    add r0, sp, #36
    add r1, sp, #0
    mov r2, r0
    bl native_fn_0200103c
    ldr r2, [sp, #0x24]
    ldr r0, [r5]
    ldr r1, [sp, #0x28]
    add r12, r2, r0
    str r12, [sp, #0x24]
    ldr r0, [r5, #0x4]
    ldr r2, [sp, #0x2c]
    add r3, r1, r0
    str r3, [sp, #0x28]
    ldr r1, [r5, #0x8]
    ldr r0, =0x022322d4
    add r2, r2, r1
    str r12, [r0, #0x70]
    str r3, [r0, #0x74]
    mov r1, r4
    str r2, [sp, #0x2c]
    str r2, [r0, #0x78]
    bl native_fn_02029870
    ldr r0, [r4, #0x4]
    add sp, sp, #48
    ldmia sp!, {r3, r4, r5, pc}
}
