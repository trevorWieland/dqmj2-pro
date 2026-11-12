/* ov006 row 0x021e6954: 80 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x4c -> constant 0x02218d90 (image word 0x02218d90)
 *   branch +0x2c -> +0x44
 *   test +0x08 cmp r0, #0
 *   test +0x18 cmp r0, #1
 *   test +0x24 cmp r4, #0
 *   test +0x28 cmpne r0, #0
 *   test +0x38 cmp r0, #1
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e6954; the literal pool and
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

extern void native_fn_021eba8c(void);
extern void native_fn_02041814(void);


asm u32 native_ov006_021e6954 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    bl native_fn_021eba8c
    cmp r0, #0
    movne r4, #1
    moveq r4, #0
    bl native_fn_02041814
    cmp r0, #1
    movne r0, #1
    moveq r0, #0
    cmp r4, #0
    cmpne r0, #0
    beq ov006_021e6954_L44
    ldr r0, =0x02218d90
    ldr r0, [r0, #0x40]
    cmp r0, #1
    moveq r0, #1
    ldmeqia sp!, {r4, pc}
ov006_021e6954_L44:
    mov r0, #0
    ldmia sp!, {r4, pc}
}
