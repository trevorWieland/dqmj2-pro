/* ov001 row 0x021dc190: 48 bytes.
 *
 * What it does: 12 instructions; 2 call(s) to 0x021db8d0, 0x021dc064; loops (back edge at +0x08); returns through pop {r4, pc}
 *
 * Decoded shape: loop with 2 calls (12 instructions, 2 calls, 0 branches, 2 back edges, 0 literal slots).
 *
 *   test +0x0c cmp r0, #0
 *   test +0x20 cmp r0, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021dc190; the literal pool and
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

extern void native_fn_021db8d0(void);
extern void native_fn_021dc064(void);


asm u32 native_ov001_021dc190 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r4, r0
    bl native_fn_021db8d0
    cmp r0, #0
    moveq r0, #0
    ldmeqia sp!, {r4, pc}
    add r0, r4, #676
    bl native_fn_021dc064
    cmp r0, #0
    moveq r0, #0
    movne r0, #1
    ldmia sp!, {r4, pc}
}
