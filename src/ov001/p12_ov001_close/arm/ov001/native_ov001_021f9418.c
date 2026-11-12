/* ov001 row 0x021f9418: 88 bytes.
 *
 * What it does: 21 instructions; 1 call(s) to 0x0205e5d8; loops (back edge at +0x44); 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 1 call (21 instructions, 1 call, 0 branches, 1 back edge, 1 literal slot).
 *
 *   pool +0x54 -> native_data_0222e004 (image word 0x0222e004)
 *   2 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f9418; the literal pool and
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

extern u8 native_data_0222e004[];
extern void native_fn_0205e5d8(void);


asm u32 native_ov001_021f9418 (register u32 a0)
{
    stmdb sp!, {lr}
    sub sp, sp, #12
    ldr r2, =native_data_0222e004
    add r0, sp, #0
    ldrh r1, [r2, #16]
    ldrh r3, [r2, #14]
    ldrh r12, [r2, #18]
    strh r1, [sp, #2]
    strh r3, [sp]
    ldrh r3, [r2, #20]
    mov r1, #12
    strh r12, [sp, #4]
    strh r3, [sp, #6]
    ldrh r3, [r2, #22]
    ldrh r2, [r2, #24]
    strh r3, [sp, #8]
    strh r2, [sp, #10]
    bl native_fn_0205e5d8
    mov r0, #1
    add sp, sp, #12
    ldmia sp!, {pc}
}
