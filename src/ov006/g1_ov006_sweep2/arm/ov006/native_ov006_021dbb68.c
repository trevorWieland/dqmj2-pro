/* ov006 row 0x021dbb68: 32 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x1c -> constant 0x0220f3b8 (image word 0x0220f3b8)
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021dbb68; the literal pool and
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

extern void native_fn_021d8328(void);
extern void native_fn_021d7de4(void);


asm u32 native_ov006_021dbb68 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r1, =0x0220f3b8
    mov r0, #0
    str r0, [r1, #0x1c]
    bl native_fn_021d8328
    bl native_fn_021d7de4
    ldmia sp!, {r3, pc}
}
