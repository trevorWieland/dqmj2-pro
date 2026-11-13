/* ov001 row 0x021dca60: 92 bytes.
 *
 * What it does: 23 instructions; 3 call(s) to 0x021db438, 0x021db8d0, 0x021dca80; loops (back edge at +0x10); returns through pop {r3, r4, r5, r6, r7, pc}
 *
 * Decoded shape: loop with 3 calls (23 instructions, 3 calls, 2 branches, 3 back edges, 0 literal slots).
 *
 *   branch +0x2c -> +0x44
 *   branch +0x3c -> +0x54
 *   back edge +0x50 -> +0x20
 *   test +0x28 cmp r0, #0
 *   test +0x38 cmp r1, r0
 *   test +0x48 cmp r4, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021dca60; the literal pool and
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


asm u32 native_ov001_021dca60 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    mov r7, r0
    ldrb r0, [r7, #0x31e]
    mov r1, #0
    bl ov001_side_slot_record_021db438
    mov r5, #0
    mov r6, r0
    mov r4, r5
ov001_021dca60_L20:
    mov r0, r6
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_021dca60_L44
    ldrb r1, [r6, #0x31f]
    ldrb r0, [r7, #0x31f]
    cmp r1, r0
    beq ov001_021dca60_L54
    add r5, r5, #1
ov001_021dca60_L44:
    add r4, r4, #1
    cmp r4, #3
    add r6, r6, #1088
    blt ov001_021dca60_L20
ov001_021dca60_L54:
    mov r0, r5
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
