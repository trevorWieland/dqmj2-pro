/* ov006 row 0x021f3628: 56 bytes.
 *
 * What it does: 22 instructions; 2 call(s) to 0x021f39e8, 0x021f39e8; no back edge; returns through pop {r4, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x30 -> constant 0x0221c05c (image word 0x0221c05c)
 *   pool +0x34 -> constant 0x0000011f (image word 0x0000011f)
 *   branch +0x0e -> +0x2c
 *   test +0x0c cmp r4, r1
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f3628; the literal pool and
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

extern void native_fn_021f39e8(void);


asm u32 native_ov006_021f3628 (register u32 a0)
{
    push {r4, lr}
    ldr r1, =0x0221c05c
    add r4, r0, #0x0
    ldr r2, [r1, #0]
    ldr r1, =0x0000011f
    ldrsb r1, [r2, r1]
    cmp r4, r1
    beq ov006_021f3628_L2c
    mov r1, #0x1
    bl native_fn_021f39e8
    ldr r0, =0x0221c05c
    ldr r1, [r0, #0]
    ldr r0, =0x0000011f
    ldrsb r0, [r1, r0]
    mov r1, #0x0
    bl native_fn_021f39e8
    ldr r0, =0x0221c05c
    ldr r1, [r0, #0]
    ldr r0, =0x0000011f
    strb r4, [r1, r0]
ov006_021f3628_L2c:
    pop {r4, pc}
    mov r8, r8
}
