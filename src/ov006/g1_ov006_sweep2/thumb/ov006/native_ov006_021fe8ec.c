/* ov006 row 0x021fe8ec: 68 bytes.
 *
 * What it does: Writes one block of 1 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x3c -> constant 0x0221c140 (image word 0x0221c140)
 *   pool +0x40 -> native_data_0220b99c (image word 0x0220b99c)
 *   branch +0x1e -> +0x24
 *   branch +0x22 -> +0x2e
 *   branch +0x2a -> +0x2e
 *   test +0x28 cmp r0, r1
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fe8ec; the literal pool and
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

extern void native_fn_0220410c(void);
extern u8 native_data_0220b99c[];
extern void native_fn_021fea34(void);


asm u32 native_ov006_021fe8ec (register u32 a0)
{
    push {r3, lr}
    add r0, sp, #0x0
    bl native_fn_0220410c
    ldr r0, =0x0221c140
    ldr r2, [r0, #0]
    ldr r0, =native_data_0220b99c
    ldrb r1, [r2, #0x1b]
    ldrb r1, [r0, r1]
    add r0, sp, #0x0
    ldrh r3, [r0, #0x2]
    ldrh r0, [r2, #0x12]
    sub r3, r3, r0
    lsr r0, r1, #0x1
    sub r0, r3, r0
    bpl ov006_021fe8ec_L24
    mov r0, #0x0
    b ov006_021fe8ec_L2e
ov006_021fe8ec_L24:
    ldrb r2, [r2, #0x19]
    sub r1, r2, r1
    cmp r0, r1
    blt ov006_021fe8ec_L2e
    add r0, r1, #0x0
ov006_021fe8ec_L2e:
    bl native_fn_021fea34
    ldr r0, =0x0221c140
    mov r1, #0x3
    ldr r0, [r0, #0]
    strb r1, [r0, #0x1d]
    pop {r3, pc}
}
