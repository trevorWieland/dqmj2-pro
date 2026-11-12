/* ov006 row 0x021ed99c: 56 bytes.
 *
 * What it does: Writes one block of 1 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x34 -> constant 0xedb88320 (image word 0xedb88320)
 *   branch +0x14 -> +0x1e
 *   branch +0x1c -> +0x20
 *   back edge +0x24 -> +0x10
 *   back edge +0x2c -> +0x0c
 *   test +0x12 tst r6, r5
 *   test +0x22 cmp r2, #0x8
 *   test +0x2a cmp r0, r3
 *   1 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ed99c; the literal pool and
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



asm u32 native_ov006_021ed99c (register u32 a0)
{
    push {r4, r5, r6, r7}
    mov r5, #0x1
    add r3, r5, #0x0
    ldr r4, =0xedb88320
    mov r0, #0x0
    add r3, #0xff
ov006_021ed99c_Lc:
    add r7, r0, #0x0
    mov r2, #0x0
ov006_021ed99c_L10:
    add r6, r7, #0x0
    tst r6, r5
    beq ov006_021ed99c_L1e
    lsr r6, r7, #0x1
    add r7, r6, #0x0
    eor r7, r4
    b ov006_021ed99c_L20
ov006_021ed99c_L1e:
    lsr r7, r7, #0x1
ov006_021ed99c_L20:
    add r2, r2, #0x1
    cmp r2, #0x8
    blt ov006_021ed99c_L10
    add r0, r0, #0x1
    stmia r1!, {r7}
    cmp r0, r3
    blt ov006_021ed99c_Lc
    pop {r4, r5, r6, r7}
    bx lr
    mov r8, r8
}
