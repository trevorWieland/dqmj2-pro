/* ov006 row 0x021ef0a0: 56 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x30 -> constant 0x0221aad0 (image word 0x0221aad0)
 *   pool +0x34 -> constant 0x0221ab54 (image word 0x0221ab54)
 *   branch +0x0e -> +0x14
 *   branch +0x12 -> +0x26
 *   branch +0x20 -> +0x26
 *   test +0x0c cmp r2, r5
 *   test +0x1e cmp r2, #0x4
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ef0a0; the literal pool and
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

extern void native_fn_02007ff4(void);
extern void native_fn_02008008(void);


asm u32 native_ov006_021ef0a0 (register u32 a0)
{
    push {r3, r4, r5, lr}
    blx native_fn_02007ff4
    ldr r1, =0x0221aad0
    ldr r5, [r1, #0x6c]
    ldr r2, [r1, #0x68]
    cmp r2, r5
    bne ov006_021ef0a0_L14
    mov r4, #0x0
    b ov006_021ef0a0_L26
ov006_021ef0a0_L14:
    ldr r2, =0x0221ab54
    lsl r3, r5, #0x2
    ldr r4, [r2, r3]
    add r2, r5, #0x1
    str r2, [r1, #0x6c]
    cmp r2, #0x4
    blt ov006_021ef0a0_L26
    mov r2, #0x0
    str r2, [r1, #0x6c]
ov006_021ef0a0_L26:
    blx native_fn_02008008
    add r0, r4, #0x0
    pop {r3, r4, r5, pc}
    mov r8, r8
}
