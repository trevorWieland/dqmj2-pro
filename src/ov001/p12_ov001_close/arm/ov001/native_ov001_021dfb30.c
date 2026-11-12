/* ov001 row 0x021dfb30: 100 bytes.
 *
 * What it does: 25 instructions; 4 call(s) to 0x021db438, 0x021dc048, 0x021dc940, +1 more; loops (back edge at +0x24); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}
 *
 * Decoded shape: loop with 4 calls (25 instructions, 4 calls, 3 branches, 4 back edges, 0 literal slots).
 *
 *   branch +0x30 -> +0x54
 *   branch +0x3c -> +0x50
 *   branch +0x4c -> +0x54
 *   back edge +0x5c -> +0x1c
 *   test +0x2c cmp r1, #0
 *   test +0x34 cmp r6, #0
 *   test +0x58 cmp r5, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021dfb30; the literal pool and
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
extern void native_fn_021dc048(void);
extern void native_fn_021dc940(void);


asm u32 native_ov001_021dfb30 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    mov r5, #0
    mov r9, r0
    mov r8, r1
    mov r7, r2
    mov r6, r3
    mov r4, r5
ov001_021dfb30_L1c:
    mov r0, r9
    mov r1, r5
    bl ov001_side_slot_record_021db438
    ldrb r1, [r0, #0x31c]
    cmp r1, #0
    beq ov001_021dfb30_L54
    cmp r6, #0
    mov r1, r8
    beq ov001_021dfb30_L50
    mov r2, r7
    mov r3, r4
    bl native_fn_021dc048
    b ov001_021dfb30_L54
ov001_021dfb30_L50:
    bl native_fn_021dc940
ov001_021dfb30_L54:
    add r5, r5, #1
    cmp r5, #3
    blt ov001_021dfb30_L1c
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
