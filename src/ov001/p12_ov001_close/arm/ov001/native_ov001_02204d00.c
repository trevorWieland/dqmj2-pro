/* ov001 row 0x02204d00: 36 bytes.
 *
 * What it does: 9 instructions; 2 call(s) to 0x02204250, 0x022042c4; loops (back edge at +0x04); returns through pop {r3, pc}
 *
 * Decoded shape: loop with 2 calls (9 instructions, 2 calls, 0 branches, 2 back edges, 0 literal slots).
 *
 *   test +0x0c cmp r1, #127
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02204d00; the literal pool and
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

extern void native_fn_02204250(void);
extern void native_fn_022042c4(void);


asm u32 native_ov001_02204d00 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    bl native_fn_02204250
    ldr r1, [r0]
    cmp r1, #127
    moveq r0, #127
    ldmeqia sp!, {r3, pc}
    bl native_fn_022042c4
    mov r0, #127
    ldmia sp!, {r3, pc}
}
