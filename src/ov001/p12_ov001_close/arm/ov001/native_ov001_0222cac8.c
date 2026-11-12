/* ov001 row 0x0222cac8: 84 bytes.
 *
 * What it does: 19 instructions; 5 call(s) to 0x02008d78, 0x020c5938, 0x0222cb1c, +2 more; loops (back edge at +0x18); 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 5 calls (19 instructions, 5 calls, 0 branches, 2 back edges, 2 literal slots).
 *
 *   pool +0x4c -> constant 0x000006f4 (image word 0x000006f4)
 *   pool +0x50 -> constant 0x02249828 (image word 0x02249828)
 *   2 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0222cac8; the literal pool and
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

extern void native_fn_02008d78(void);
extern void native_fn_020c5938(void);
extern void native_fn_0222cb1c(void);
extern void native_fn_0222cb48(void);
extern void native_fn_0222cc2c(void);


asm u32 native_ov001_0222cac8 (register u32 a0)
{
    stmdb sp!, {lr}
    sub sp, sp, #756
    sub sp, sp, #1024
    ldr r2, =0x000006f4
    add r0, sp, #0
    mov r1, #0
    bl native_fn_02008d78
    bl native_fn_020c5938
    bl native_fn_0222cb1c
    ldr r1, =0x02249828
    strb r0, [r1]
    add r0, sp, #0
    bl native_fn_0222cb48
    mov r1, r0
    add r0, sp, #0
    bl native_fn_0222cc2c
    add sp, sp, #756
    add sp, sp, #1024
    ldmia sp!, {pc}
}
