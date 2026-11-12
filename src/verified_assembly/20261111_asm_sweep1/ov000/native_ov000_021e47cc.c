/* ov000 row 0x021e47cc: 88 bytes.
 *
 * Decoded shape: loop with no calls.
 *
 *   pool +0x54 -> native_data_02234388 (image word 0x02234388)
 *   back edge +0x48 -> +0x10
 *   test +0x14 cmp r3, #0
 *   test +0x20 cmp r3, r0
 *   test +0x28 cmpeq r3, r1
 *   test +0x30 cmpeq r3, r2
 *   memory +0x10 ldrb r3, [r4, #0x1c]
 *   memory +0x1c ldrb r3, [r4, #0x1d]
 *   memory +0x24 ldrsbeq r3, [r4, #0x1e]
 *   memory +0x2c ldrsbeq r3, [r4, #0x20]
 *
 * Why transcribed rather than written as C: same compound identity scan (92 vs 88 B)
 * Recorded in docs/authoring/2026-11-11-ov000-pass2.md.
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e47cc; the literal pool and
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


asm u32 native_ov000_021e47cc (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov lr, #0
    ldr r4, =native_data_02234388
    mov ip, lr
ov000_021e47cc_L10:
    ldrb r3, [r4, #0x1c]
    cmp r3, #0
    beq ov000_021e47cc_L3c
    ldrb r3, [r4, #0x1d]
    cmp r3, r0
    ldreqsb r3, [r4, #0x1e]
    cmpeq r3, r1
    ldreqsb r3, [r4, #0x20]
    cmpeq r3, r2
    moveq lr, r4
    beq ov000_021e47cc_L4c
ov000_021e47cc_L3c:
    add ip, ip, #1
    cmp ip, #0x40
    add r4, r4, #0x34
    blt ov000_021e47cc_L10
ov000_021e47cc_L4c:
    mov r0, lr
    ldmia sp!, {r4, pc}
}
