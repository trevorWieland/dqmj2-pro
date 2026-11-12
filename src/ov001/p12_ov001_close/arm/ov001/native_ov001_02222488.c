/* ov001 row 0x02222488: 60 bytes.
 *
 * What it does: 14 instructions; 2 call(s) to 0x021dbe5c, 0x022224b8; loops (back edge at +0x18); returns through pop {r3, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 2 calls (14 instructions, 2 calls, 1 branch, 1 back edge, 1 literal slot).
 *
 *   pool +0x38 -> constant 0x000005dc (image word 0x000005dc)
 *   branch +0x14 -> +0x28
 *   branch +0x24 -> +0x30
 *   test +0x10 cmp r1, #2
 *   test +0x20 cmp r0, r1
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02222488; the literal pool and
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

extern void native_fn_021dbe5c(void);


asm u32 native_ov001_02222488 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r0, [r0]
    add r1, r0, #512
    ldrsb r1, [r1, #47]
    cmp r1, #2
    bge ov001_02222488_L28
    bl native_fn_021dbe5c
    ldr r1, =0x000005dc
    cmp r0, r1
    blt ov001_02222488_L30
ov001_02222488_L28:
    mov r0, #1
    ldmia sp!, {r3, pc}
ov001_02222488_L30:
    mov r0, #0
    ldmia sp!, {r3, pc}
}
