/* ov006 row 0x021e5870: 132 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x10 -> +0x74
 *   branch +0x24 -> +0x74
 *   branch +0x34 -> +0x58
 *   branch +0x44 -> +0x58
 *   back edge +0x70 -> +0x1c
 *   test +0x0c cmp r2, #0
 *   test +0x20 cmp r4, #0
 *   test +0x60 cmp r0, r2
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e5870; the literal pool and
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



asm u32 native_ov006_021e5870 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r12, #0
    mov r0, r12
    cmp r2, #0
    ble ov006_021e5870_L74
    mov r6, #225
    mov r5, #67
ov006_021e5870_L1c:
    ldrsb r4, [r3, r0]
    cmp r4, #0
    beq ov006_021e5870_L74
    mov r4, r0, asr #1
    add r4, r0, r4, lsr #30
    movs r4, r4, asr #2
    beq ov006_021e5870_L58
    mov r4, r0, lsr #31
    rsb lr, r4, r0, lsl #30
    adds r4, r4, lr, ror #30
    bne ov006_021e5870_L58
    strb r6, [r1, r12]
    add r4, r12, #1
    strb r5, [r1, r4]
    add r12, r12, #2
ov006_021e5870_L58:
    ldrsb r4, [r3, r0]
    add r0, r0, #1
    cmp r0, r2
    sub r4, r4, #47
    strb r4, [r1, r12]
    add r12, r12, #1
    blt ov006_021e5870_L1c
ov006_021e5870_L74:
    mov r2, #0
    mov r0, r1
    strb r2, [r1, r12]
    ldmia sp!, {r4, r5, r6, pc}
}
