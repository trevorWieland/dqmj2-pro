/* ov006 row 0x021def28: 92 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x54 -> constant 0x0220f594 (image word 0x0220f594)
 *   pool +0x58 -> constant 0x0220f654 (image word 0x0220f654)
 *   test +0x08 cmp r1, #1
 *   test +0x28 cmp r2, #0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021def28; the literal pool and
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

extern void native_fn_0205fa4c(void);
extern void native_fn_0205f98c(void);


asm u32 native_ov006_021def28 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    mov r1, r0
    cmp r1, #1
    ldreq r0, =0x0220f594
    moveq r2, #2
    ldrne r0, =0x0220f594
    movne r2, #0
    strb r2, [r0]
    ldr r0, =0x0220f654
    ldr r2, [r0, #0x1c]
    cmp r2, #0
    ldmeqia sp!, {r3, pc}
    bl native_fn_0205fa4c
    ldr r0, =0x0220f654
    mov r1, #0
    ldr r0, [r0, #0x1c]
    bl native_fn_0205f98c
    ldr r1, [r0, #0x7c]
    bic r1, r1, #2
    str r1, [r0, #0x7c]
    ldmia sp!, {r3, pc}
}
