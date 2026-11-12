/* ov001 row 0x0220375c: 88 bytes.
 *
 * What it does: 21 instructions; 2 call(s) to 0x0204a574, 0x021fe2b8; loops (back edge at +0x3c); returns through pop {r3, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 2 calls (21 instructions, 2 calls, 0 branches, 2 back edges, 1 literal slot).
 *
 *   pool +0x54 -> native_data_0222e058 (image word 0x0222e058)
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0220375c; the literal pool and
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

extern u8 native_data_0222e058[];
extern void native_fn_0204a574(void);
extern void native_fn_021fe2b8(void);


asm u32 native_ov001_0220375c (register u32 a0)
{
    stmdb sp!, {r3, lr}
    sub sp, sp, #16
    ldr r1, =native_data_0222e058
    mov r0, #1
    ldrh r2, [r1, #6]
    ldrh r3, [r1, #4]
    mov r1, #8
    strh r2, [sp, #14]
    strh r3, [sp, #12]
    str r1, [sp]
    str r0, [sp, #0x4]
    add r1, sp, #12
    mov r2, r0
    mov r3, r0
    str r0, [sp, #0x8]
    bl native_fn_0204a574
    mov r0, #1
    mov r1, #0
    bl native_fn_021fe2b8
    add sp, sp, #16
    ldmia sp!, {r3, pc}
}
