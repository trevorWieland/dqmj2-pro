/* ov000 row 0x021f3b58: 80 bytes.
 *
 * Decoded shape: loop with no calls.
 *
 *   pool +0x4c -> native_data_02236ed8 (image word 0x02236ed8)
 *   back edge +0x44 -> +0x14
 *   test +0x18 cmp r1, #0
 *   test +0x3c cmp r3, #8
 *   memory +0x08 ldr ip, [r1, #4]
 *   memory +0x14 ldrb r1, [r2, #0x278]
 *   memory +0x30 strb r2, [r1, #0x278]
 *   1 store instruction(s)
 *
 * Why transcribed rather than written as C: slot pointer walk versus indexed `mla` store not reconciled (72
 * vs 80 B)
 * Recorded in docs/authoring/2026-11-11-ov000-pass2.md.
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f3b58; the literal pool and
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

extern u8 native_data_02236ed8[];


asm u32 native_ov000_021f3b58 (register u32 a0)
{
    ldr r1, =native_data_02236ed8
    mvn r0, #0
    ldr ip, [r1, #4]
    mov r3, #0
    mov r2, ip
ov000_021f3b58_L14:
    ldrb r1, [r2, #0x278]
    cmp r1, #0
    bne ov000_021f3b58_L38
    mov r0, #0x27c
    mla r1, r3, r0, ip
    mov r2, #1
    mov r0, r3
    strb r2, [r1, #0x278]
    bx lr
ov000_021f3b58_L38:
    add r3, r3, #1
    cmp r3, #8
    add r2, r2, #0x27c
    blt ov000_021f3b58_L14
    bx lr
}
