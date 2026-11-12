/* ov006 row 0x021f24a4: 48 bytes.
 *
 * What it does: Writes one block of 1 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x28 -> constant 0x0221c008 (image word 0x0221c008)
 *   pool +0x2c -> native_fn_021f24d4+1 (image word 0x021f24d5)
 *   branch +0x1a -> +0x26
 *   test +0x18 cmp r1, #0x4
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f24a4; the literal pool and
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

extern void native_fn_021f24d4(void);
extern void native_fn_02204970(void);


asm u32 native_ov006_021f24a4 (register u32 a0)
{
    push {r3, lr}
    ldr r1, =0x0221c008
    mov r3, #0x0
    ldr r2, [r1, #0]
    mvn r3, r3
    strb r3, [r2, #0x16]
    ldr r3, [r1, #0]
    ldrh r2, [r3, #0x14]
    add r2, r2, #0x1
    strh r2, [r3, #0x14]
    ldr r2, [r1, #0]
    ldrh r1, [r2, #0x14]
    cmp r1, #0x4
    blo ov006_021f24a4_L26
    mov r1, #0x0
    strh r1, [r2, #0x14]
    ldr r1, =native_fn_021f24d4+1
    bl native_fn_02204970
ov006_021f24a4_L26:
    pop {r3, pc}
}
