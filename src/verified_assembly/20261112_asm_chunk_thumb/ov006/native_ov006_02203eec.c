/* ov006 row 0x02203eec: 48 bytes.
 *
 * What it does: Writes one block of 3 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x28 -> constant 0x027fffa8 (image word 0x027fffa8)
 *   pool +0x2c -> constant 0x0221c18c (image word 0x0221c18c)
 *   branch +0x0c -> +0x12
 *   branch +0x1c -> +0x22
 *   test +0x1a cmp r0, r1
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02203eec; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 14 of 48 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;



asm u32 native_ov006_02203eec (register u32 a0)
{
    ldr r1, =0x027fffa8
    ldrh r2, [r1, #0]
    mov r1, #0x2
    lsl r1, r1, #0xe
    and r1, r2
    asr r1, r1, #0xf
    beq ov006_02203eec_L12
    mov r0, #0x0
    bx lr
ov006_02203eec_L12:
    ldr r1, =0x0221c18c
    ldr r1, [r1, #0x4]
    ldrh r1, [r1, #0x34]
    and r1, r0
    cmp r0, r1
    bne ov006_02203eec_L22
    mov r0, #0x1
    bx lr
ov006_02203eec_L22:
    mov r0, #0x0
    bx lr
    mov r8, r8
}
