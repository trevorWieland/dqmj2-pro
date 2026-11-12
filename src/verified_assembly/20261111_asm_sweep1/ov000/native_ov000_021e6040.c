/* ov000 row 0x021e6040: 104 bytes.
 *
 * What it does: Scans 0x20 16-byte entries for an id; on a match copies 12 bytes into an
 * optional output and returns the index, else -1.
 *
 * Decoded shape: loop with no calls.
 *
 *   pool +0x64 -> native_data_02232668 (image word 0x02232668)
 *   back edge +0x5c -> +0x20
 *   test +0x0c cmp lr, #0x20
 *   test +0x24 cmp r1, #0
 *   test +0x30 cmp r1, r2
 *   test +0x38 cmp ip, #0
 *   memory +0x20 ldrb r1, [r3]
 *   memory +0x2c ldrb r1, [r3, #1]
 *   1 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e6040; the literal pool and
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

extern u8 native_data_02232668[];


asm u32 native_ov000_021e6040 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    mov lr, r0
    mov ip, r1
    cmp lr, #0x20
    mvn r0, #0
    ldmgeia sp!, {r3, pc}
    ldr r1, =native_data_02232668
    add r3, r1, lr, lsl #4
ov000_021e6040_L20:
    ldrb r1, [r3]
    cmp r1, #0
    beq ov000_021e6040_L50
    ldrb r1, [r3, #1]
    cmp r1, r2
    bne ov000_021e6040_L50
    cmp ip, #0
    addne r0, r3, #4
    ldmneia r0, {r0, r1, r2}
    stmneia ip, {r0, r1, r2}
    mov r0, lr
    ldmia sp!, {r3, pc}
ov000_021e6040_L50:
    add lr, lr, #1
    cmp lr, #0x20
    add r3, r3, #0x10
    blt ov000_021e6040_L20
    ldmia sp!, {r3, pc}
}
