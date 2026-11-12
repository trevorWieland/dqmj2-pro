/* ov006 row 0x021f9ba8: 72 bytes.
 *
 * What it does: 33 instructions; 3 call(s) to 0x021f9bbc, 0x021f9bb4, 0x021f9a44; loops (back edge at +0x32); returns through pop {r3, r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x44 -> constant 0x0221c0e4 (image word 0x0221c0e4)
 *   branch +0x18 -> +0x22
 *   branch +0x1c -> +0x22
 *   branch +0x20 -> +0x34
 *   branch +0x24 -> +0x2a
 *   branch +0x28 -> +0x2c
 *   back edge +0x32 -> +0x14
 *   back edge +0x3a -> +0x0c
 *   test +0x16 cmp r2, #0x30
 *   test +0x1a cmp r2, #0x20
 *   test +0x1e cmp r2, #0x0
 *   test +0x22 cmp r5, #0x2
 *   test +0x30 cmp r5, #0x3
 *   test +0x38 cmp r4, #0x4
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f9ba8; the literal pool and
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

extern void native_fn_021f9a44(void);


asm u32 native_ov006_021f9ba8 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    mov r4, #0x0
    ldr r7, =0x0221c0e4
    add r6, r4, #0x0
    mov r0, #0x20
    mov r1, #0x30
ov006_021f9ba8_Lc:
    ldr r2, [r7, #0]
    mov r5, #0x0
    add r2, #0x8
    add r3, r2, r6
ov006_021f9ba8_L14:
    ldrb r2, [r3, r5]
    cmp r2, #0x30
    beq ov006_021f9ba8_L22
    cmp r2, #0x20
    beq ov006_021f9ba8_L22
    cmp r2, #0x0
    bne ov006_021f9ba8_L34
ov006_021f9ba8_L22:
    cmp r5, #0x2
    bne ov006_021f9ba8_L2a
    add r2, r1, #0x0
    b ov006_021f9ba8_L2c
ov006_021f9ba8_L2a:
    add r2, r0, #0x0
ov006_021f9ba8_L2c:
    strb r2, [r3, r5]
    add r5, r5, #0x1
    cmp r5, #0x3
    blt ov006_021f9ba8_L14
ov006_021f9ba8_L34:
    add r4, r4, #0x1
    add r6, r6, #0x3
    cmp r4, #0x4
    blt ov006_021f9ba8_Lc
    bl native_fn_021f9a44
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
}
