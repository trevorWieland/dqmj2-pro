/* ov006 row 0x021e9e04: 116 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x70 -> constant 0x04000048 (image word 0x04000048)
 *   0 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e9e04; the literal pool and
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



asm u32 native_ov006_021e9e04 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    ldr r4, =0x04000048
    mov r1, #255
    ldrh r0, [r4]
    mov lr, #67108864
    mov r3, #239
    bic r0, r0, #63
    orr r0, r0, #63
    strh r0, [r4]
    ldrh r12, [r4]
    mov r2, #16
    add r0, r1, #4032
    bic r12, r12, #16128
    orr r12, r12, #16128
    strh r12, [r4]
    ldrh r12, [r4, #2]
    bic r12, r12, #63
    orr r12, r12, #31
    strh r12, [r4, #2]
    ldr r12, [lr]
    bic r12, r12, #57344
    orr r12, r12, #24576
    str r12, [lr]
    strh r3, [lr, #64]
    strh r2, [lr, #68]
    strh r1, [lr, #66]
    strh r0, [lr, #70]
    ldmia sp!, {r4, pc}
}
