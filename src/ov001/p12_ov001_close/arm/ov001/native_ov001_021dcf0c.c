/* ov001 row 0x021dcf0c: 72 bytes.
 *
 * What it does: 18 instructions; 1 call(s) to 0x021db8d0; loops (back edge at +0x0c); returns through pop {r3, r4, r5, pc}
 *
 * Decoded shape: loop with 1 call (18 instructions, 1 call, 1 branch, 1 back edge, 0 literal slots).
 *
 *   branch +0x14 -> +0x40
 *   test +0x10 cmp r0, #0
 *   test +0x38 tst r2, r0, lsl r1
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021dcf0c; the literal pool and
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

extern void ov001_record_is_active_021db8d0(void);


asm u32 native_ov001_021dcf0c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    mov r4, r1
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_021dcf0c_L40
    mov r0, r4, asr #2
    add r0, r4, r0, lsr #29
    add r2, r5, r0, asr #3
    mov r1, r4, lsr #31
    rsb r0, r1, r4, lsl #29
    add r1, r1, r0, ror #29
    ldrb r2, [r2, #0x3ed]
    mov r0, #1
    tst r2, r0, lsl r1
    ldmneia sp!, {r3, r4, r5, pc}
ov001_021dcf0c_L40:
    mov r0, #0
    ldmia sp!, {r3, r4, r5, pc}
}
