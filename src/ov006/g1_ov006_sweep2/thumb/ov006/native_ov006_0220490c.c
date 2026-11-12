/* ov006 row 0x0220490c: 16 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x0220490c; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity proves the instruction stream, not the meaning of the fields, blocks and callee contracts it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_0220491c(void);


asm u32 native_ov006_0220490c (register u32 a0)
{
    push {r3, r4, lr}
    sub sp, #0x4
    mov r4, #0x0
    str r4, [sp]
    bl native_fn_0220491c
    add sp, #0x4
    pop {r3, r4, pc}
}
