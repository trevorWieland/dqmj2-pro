/* ov006 row 0x021fc1c8: 32 bytes.
 *
 * What it does: Writes one block of 4 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x18 -> constant 0x0221c100 (image word 0x0221c100)
 *   pool +0x1c -> native_fn_021fc154+1 (image word 0x021fc155)
 *   branch +0x0e -> +0x16
 *   test +0x0c cmp r0, #0x78
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fc1c8; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 14 of 32 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_021fc154(void);
extern void native_fn_021f52cc(void);


asm u32 native_ov006_021fc1c8 (register u32 a0)
{
    push {r3, lr}
    ldr r0, =0x0221c100
    ldrb r1, [r0, #0]
    add r1, r1, #0x1
    strb r1, [r0, #0]
    ldrb r0, [r0, #0]
    cmp r0, #0x78
    blo ov006_021fc1c8_L16
    ldr r0, =native_fn_021fc154+1
    bl native_fn_021f52cc
ov006_021fc1c8_L16:
    pop {r3, pc}
}
