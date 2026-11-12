/* ov001 row 0x021dfcec: 68 bytes.
 *
 * What it does: 16 instructions; 3 call(s) to 0x021db438, 0x021db8d0, 0x021dfd0c; loops (back edge at +0x04); returns through pop {r4, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 3 calls (16 instructions, 3 calls, 0 branches, 3 back edges, 1 literal slot).
 *
 *   pool +0x40 -> constant 0x0223896c (image word 0x0223896c)
 *   back edge +0x38 -> +0x20
 *   test +0x10 cmp r0, #0
 *   test +0x24 cmp r0, #0
 *   test +0x34 cmp r2, #6
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021dfcec; the literal pool and
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

extern void native_fn_021db438(void);
extern void native_fn_021db8d0(void);


asm u32 native_ov001_021dfcec (register u32 a0)
{
    stmdb sp!, {r4, lr}
    bl native_fn_021db438
    mov r4, r0
    bl native_fn_021db8d0
    cmp r0, #0
    ldmeqia sp!, {r4, pc}
    ldr r1, =0x0223896c
    mov r2, #0
ov001_021dfcec_L20:
    ldr r0, [r1, r2, lsl #2]
    cmp r0, #0
    streq r4, [r1, r2, lsl #2]
    ldmeqia sp!, {r4, pc}
    add r2, r2, #1
    cmp r2, #6
    blt ov001_021dfcec_L20
    ldmia sp!, {r4, pc}
}
