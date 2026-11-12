/* ov006 row 0x021f2a4c: 40 bytes.
 *
 * What it does: Writes one block of 2 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x24 -> constant 0x0221c050 (image word 0x0221c050)
 *   branch +0x10 -> +0x1a
 *   back edge +0x20 -> +0x0a
 *   test +0x0e cmp r0, #0x0
 *   test +0x1e cmp r4, #0x4
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f2a4c; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 10 of 40 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02202d64(void);


asm u32 native_ov006_021f2a4c (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    mov r4, #0x0
    ldr r6, =0x0221c050
    add r5, r4, #0x0
    add r7, r4, #0x0
ov006_021f2a4c_La:
    ldr r0, [r6, #0]
    ldr r0, [r0, r5]
    cmp r0, #0x0
    beq ov006_021f2a4c_L1a
    bl native_fn_02202d64
    ldr r0, [r6, #0]
    str r7, [r0, r5]
ov006_021f2a4c_L1a:
    add r4, r4, #0x1
    add r5, r5, #0x4
    cmp r4, #0x4
    blt ov006_021f2a4c_La
    pop {r3, r4, r5, r6, r7, pc}
}
