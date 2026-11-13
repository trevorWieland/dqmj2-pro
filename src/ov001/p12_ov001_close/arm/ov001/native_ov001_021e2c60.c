/* ov001 row 0x021e2c60: 84 bytes.
 *
 * What it does: 21 instructions; 4 call(s) to 0x021db438, 0x021db8d0, 0x021e2cac, +1 more; loops (back edge at +0x08); returns through pop {r3, r4, r5, pc}
 *
 * Decoded shape: loop with 4 calls (21 instructions, 4 calls, 1 branch, 3 back edges, 0 literal slots).
 *
 *   branch +0x18 -> +0x4c
 *   branch +0x28 -> +0x4c
 *   back edge +0x48 -> +0x2c
 *   test +0x14 cmp r0, #0
 *   test +0x24 cmp r2, #0
 *   test +0x34 cmp r5, r0
 *   test +0x44 cmp r1, r2
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021e2c60; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity fixes the instruction stream, not the field, block and callee semantics behind the addresses and strides it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void ov001_side_slot_record_021db438(void);
extern void ov001_record_is_active_021db8d0(void);


asm u32 native_ov001_021e2c60 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r2
    bl ov001_side_slot_record_021db438
    mov r4, r0
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_021e2c60_L4c
    ldrb r2, [r4, #0x43c]
    mov r1, #0
    cmp r2, #0
    ble ov001_021e2c60_L4c
ov001_021e2c60_L2c:
    add r0, r4, r1
    ldrb r0, [r0, #0x432]
    cmp r5, r0
    moveq r0, #1
    ldmeqia sp!, {r3, r4, r5, pc}
    add r1, r1, #1
    cmp r1, r2
    blt ov001_021e2c60_L2c
ov001_021e2c60_L4c:
    mov r0, #0
    ldmia sp!, {r3, r4, r5, pc}
}
