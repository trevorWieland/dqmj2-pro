/* ov001 row 0x021e7f3c: 108 bytes.
 *
 * What it does: 27 instructions; 7 call(s) to 0x021e7d88, 0x021db438, 0x021db438, +4 more; loops (back edge at +0x04); returns through pop {r4, r5, r6, r7, r8, pc}
 *
 * Decoded shape: loop with 7 calls (27 instructions, 7 calls, 0 branches, 6 back edges, 0 literal slots).
 *
 *   branch +0x3c -> +0x64
 *   back edge +0x60 -> +0x44
 *   test +0x34 cmp r6, #0
 *   test +0x5c cmp r5, r6
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021e7f3c; the literal pool and
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

extern void native_fn_021e7d88(void);
extern void ov001_side_slot_record_021db438(void);
extern void ov001_mode_byte_021db530(void);
extern void native_fn_021e7538(void);


asm u32 native_ov001_021e7f3c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    bl native_fn_021e7d88
    mov r0, #0
    mov r1, r0
    bl ov001_side_slot_record_021db438
    mov r7, r0
    mov r0, #1
    mov r1, #0
    bl ov001_side_slot_record_021db438
    mov r8, r0
    mov r0, #0
    bl ov001_mode_byte_021db530
    mov r6, r0
    cmp r6, #0
    mov r5, #0
    ble ov001_021e7f3c_L64
    mov r4, r5
ov001_021e7f3c_L44:
    mov r0, r5
    mov r1, r7
    mov r2, r8
    mov r3, r4
    bl native_fn_021e7538
    add r5, r5, #1
    cmp r5, r6
    blt ov001_021e7f3c_L44
ov001_021e7f3c_L64:
    mov r0, r6
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
