/* ov001 row 0x021e8dd0: 56 bytes.
 *
 * What it does: 13 instructions; 1 call(s) to 0x0203cf9c; loops (back edge at +0x1c); returns through pop {r3, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 1 call (13 instructions, 1 call, 0 branches, 1 back edge, 1 literal slot).
 *
 *   pool +0x34 -> constant 0x02238d58 (image word 0x02238d58)
 *   test +0x0c cmp r1, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021e8dd0; the literal pool and
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

extern void native_fn_0203cf9c(void);


asm u32 native_ov001_021e8dd0 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r0, =0x02238d58
    ldr r1, [r0]
    cmp r1, #0
    moveq r0, #0
    ldmeqia sp!, {r3, pc}
    mov r0, #1
    bl native_fn_0203cf9c
    ldr r0, =0x02238d58
    mov r1, #0
    str r1, [r0]
    mov r0, #1
    ldmia sp!, {r3, pc}
}
