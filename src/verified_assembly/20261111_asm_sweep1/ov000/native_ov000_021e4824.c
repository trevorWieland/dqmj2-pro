/* ov000 row 0x021e4824: 120 bytes.
 *
 * What it does: Scans 0x40 0x34-byte entries for a three-field key; on a match copies 12
 * bytes into up to two optional outputs.
 *
 * Decoded shape: loop with no calls.
 *
 *   pool +0x74 -> native_data_02234388 (image word 0x02234388)
 *   back edge +0x68 -> +0x0c
 *   test +0x10 cmp ip, #0
 *   test +0x1c cmp ip, r0
 *   test +0x24 cmpeq ip, r1
 *   test +0x2c cmpeq ip, r2
 *   memory +0x0c ldrb ip, [r4, #0x1c]
 *   memory +0x18 ldrb ip, [r4, #0x1d]
 *   memory +0x20 ldrsbeq ip, [r4, #0x1e]
 *   memory +0x28 ldrsbeq ip, [r4, #0x20]
 *   memory +0x40 ldr r3, [sp, #8]
 *   2 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e4824; the literal pool and
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


asm u32 native_ov000_021e4824 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    ldr r4, =native_data_02234388
    mov lr, #0
ov000_021e4824_Lc:
    ldrb ip, [r4, #0x1c]
    cmp ip, #0
    beq ov000_021e4824_L5c
    ldrb ip, [r4, #0x1d]
    cmp ip, r0
    ldreqsb ip, [r4, #0x1e]
    cmpeq ip, r1
    ldreqsb ip, [r4, #0x20]
    cmpeq ip, r2
    bne ov000_021e4824_L5c
    cmp r3, #0
    ldmneia r4, {r0, r1, r2}
    stmneia r3, {r0, r1, r2}
    ldr r3, [sp, #8]
    cmp r3, #0
    addne r0, r4, #0xc
    ldmneia r0, {r0, r1, r2}
    stmneia r3, {r0, r1, r2}
    mov r0, #1
    ldmia sp!, {r4, pc}
ov000_021e4824_L5c:
    add lr, lr, #1
    cmp lr, #0x40
    add r4, r4, #0x34
    blt ov000_021e4824_Lc
    mov r0, #0
    ldmia sp!, {r4, pc}
}
