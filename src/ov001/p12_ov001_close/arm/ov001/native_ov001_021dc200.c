/* ov001 row 0x021dc200: 48 bytes.
 *
 * What it does: 12 instructions; 1 call(s) to 0x021dc108; loops (back edge at +0x08); returns through pop {r4, pc}
 *
 * Decoded shape: loop with 1 call (12 instructions, 1 call, 0 branches, 1 back edge, 0 literal slots).
 *
 *   test +0x0c cmp r0, #0
 *   test +0x20 cmp r0, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021dc200; the literal pool and
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

extern void native_fn_021dc108(void);


asm u32 native_ov001_021dc200 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r4, r0
    bl native_fn_021dc108
    cmp r0, #0
    moveq r0, #0
    ldmeqia sp!, {r4, pc}
    add r0, r4, #512
    ldrsb r0, [r0, #55]
    cmp r0, #0
    movne r0, #0
    moveq r0, #1
    ldmia sp!, {r4, pc}
}
