/* ov006 row 0x021fa7d0: 40 bytes.
 *
 * What it does: Writes one block of 5 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x24 -> constant 0x0221c0ec (image word 0x0221c0ec)
 *   branch +0x0e -> +0x22
 *   test +0x0c cmp r0, r4
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fa7d0; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 15 of 40 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_021fedc8(void);
extern void native_fn_021fedec(void);
extern void native_fn_021fabe4(void);


asm u32 native_ov006_021fa7d0 (register u32 a0)
{
    push {r4, lr}
    add r4, r0, #0x0
    bl native_fn_021fedc8
    add r0, #0xf6
    ldrb r0, [r0, #0]
    cmp r0, r4
    beq ov006_021fa7d0_L22
    ldr r0, =0x0221c0ec
    ldr r0, [r0, #0x8]
    add r0, #0x43
    strb r4, [r0, #0]
    add r0, r4, #0x0
    bl native_fn_021fedec
    bl native_fn_021fabe4
ov006_021fa7d0_L22:
    pop {r4, pc}
}
