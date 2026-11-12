/* ov000 row 0x021e46ec: 88 bytes.
 *
 * Decoded shape: loop with no calls.
 *
 *   pool +0x54 -> native_data_02234388 (image word 0x02234388)
 *   back edge +0x48 -> +0x10
 *   test +0x14 cmp r3, #0
 *   test +0x20 cmp r3, r2
 *   test +0x28 cmpeq r3, r0
 *   test +0x30 cmpeq r3, r1
 *   memory +0x10 ldrb r3, [lr, #0x1c]
 *   memory +0x1c ldrb r3, [lr, #0x1d]
 *   memory +0x24 ldrbeq r3, [lr, #0x1f]
 *   memory +0x2c ldrsbeq r3, [lr, #0x1e]
 *
 * Why transcribed rather than written as C: compound identity scan allocates two registers differently (92
 * vs 88 B)
 * Recorded in docs/authoring/2026-11-11-ov000-pass2.md.
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e46ec; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the meaning of the fields, blocks and callee contracts
 * the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_02234388[];


asm u32 native_ov000_021e46ec (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r4, #0
    ldr lr, =native_data_02234388
    mov ip, r4
ov000_021e46ec_L10:
    ldrb r3, [lr, #0x1c]
    cmp r3, #0
    beq ov000_021e46ec_L3c
    ldrb r3, [lr, #0x1d]
    cmp r3, r2
    ldreqb r3, [lr, #0x1f]
    cmpeq r3, r0
    ldreqsb r3, [lr, #0x1e]
    cmpeq r3, r1
    moveq r4, lr
    beq ov000_021e46ec_L4c
ov000_021e46ec_L3c:
    add ip, ip, #1
    cmp ip, #0x40
    add lr, lr, #0x34
    blt ov000_021e46ec_L10
ov000_021e46ec_L4c:
    mov r0, r4
    ldmia sp!, {r4, pc}
}
