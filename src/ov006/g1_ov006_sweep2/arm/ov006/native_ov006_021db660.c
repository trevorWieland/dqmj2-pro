/* ov006 row 0x021db660: 72 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x44 -> constant 0x0220f3b8 (image word 0x0220f3b8)
 *   branch +0x20 -> +0x34
 *   test +0x18 cmp r0, #0
 *   test +0x24 cmp r0, #0
 *   test +0x34 cmp r0, #1
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021db660; the literal pool and
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

extern void native_fn_021db5b4(void);


asm u32 native_ov006_021db660 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    bl native_fn_021db5b4
    ldr r1, =0x0220f3b8
    mov r2, #1
    str r2, [r1, #0x1c]
    ldr r0, [r0]
    cmp r0, #0
    ldrsb r0, [r1]
    bne ov006_021db660_L34
    cmp r0, #0
    moveq r0, #2
    streq r0, [r1, #0x1c]
    ldmia sp!, {r3, pc}
ov006_021db660_L34:
    cmp r0, #1
    moveq r0, #2
    streq r0, [r1, #0x1c]
    ldmia sp!, {r3, pc}
}
