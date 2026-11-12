/* ov006 row 0x021f8b3c: 52 bytes.
 *
 * What it does: Writes one block of 4 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x24 -> constant 0x0221c0d8 (image word 0x0221c0d8)
 *   pool +0x28 -> native_data_0220b62c (image word 0x0220b62c)
 *   pool +0x2c -> native_data_0220b630 (image word 0x0220b630)
 *   pool +0x30 -> native_data_0220b62e (image word 0x0220b62e)
 *   branch +0x08 -> +0x0e
 *   branch +0x0c -> +0x10
 *   test +0x06 cmp r1, #0x4
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f8b3c; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 14 of 52 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_0220b62c[];
extern u8 native_data_0220b630[];
extern u8 native_data_0220b62e[];
extern void native_fn_021f2948(void);


asm u32 native_ov006_021f8b3c (register u32 a0)
{
    push {r4, lr}
    ldr r0, =0x0221c0d8
    ldrb r1, [r0, #0]
    cmp r1, #0x4
    bhs ov006_021f8b3c_Le
    mov r0, #0x2
    b ov006_021f8b3c_L10
ov006_021f8b3c_Le:
    mov r0, #0x3
ov006_021f8b3c_L10:
    lsl r4, r1, #0x3
    ldr r1, =native_data_0220b62c
    ldr r2, =native_data_0220b630
    ldr r3, =native_data_0220b62e
    ldrh r1, [r1, r4]
    ldrh r2, [r2, r4]
    ldrh r3, [r3, r4]
    bl native_fn_021f2948
    pop {r4, pc}
}
