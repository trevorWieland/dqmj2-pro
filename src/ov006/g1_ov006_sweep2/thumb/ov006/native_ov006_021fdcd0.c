/* ov006 row 0x021fdcd0: 80 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x40 -> native_data_0220e120 (image word 0x0220e120)
 *   pool +0x44 -> constant 0x02004cd8 (image word 0x02004cd8)
 *   pool +0x48 -> constant 0x04001008 (image word 0x04001008)
 *   pool +0x4c -> constant 0x04000008 (image word 0x04000008)
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fdcd0; the literal pool and
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

extern u8 native_data_0220e120[];
extern void native_fn_021f27d4(void);


asm u32 native_ov006_021fdcd0 (register u32 a0)
{
    push {r3, lr}
    ldr r0, =native_data_0220e120
    ldr r1, =0x02004cd8
    bl native_fn_021f27d4
    ldr r3, =0x04001008
    mov r0, #0x3
    ldrh r2, [r3, #0]
    mov r1, #0x3
    bic r2, r0
    orr r2, r1
    strh r2, [r3, #0]
    ldrh r2, [r3, #0x2]
    bic r2, r0
    orr r2, r1
    strh r2, [r3, #0x2]
    ldr r3, =0x04000008
    ldrh r2, [r3, #0]
    bic r2, r0
    orr r2, r1
    strh r2, [r3, #0]
    ldrh r2, [r3, #0x2]
    bic r2, r0
    orr r2, r1
    strh r2, [r3, #0x2]
    ldrh r2, [r3, #0x4]
    bic r2, r0
    add r0, r2, #0x0
    orr r0, r1
    strh r0, [r3, #0x4]
    pop {r3, pc}
    mov r8, r8
}
