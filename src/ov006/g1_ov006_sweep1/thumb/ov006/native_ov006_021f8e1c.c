/* ov006 row 0x021f8e1c: 128 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x58 -> native_data_0220dd78 (image word 0x0220dd78)
 *   pool +0x5c -> constant 0x0200494c (image word 0x0200494c)
 *   pool +0x60 -> native_data_0220dd8c (image word 0x0220dd8c)
 *   pool +0x64 -> constant 0x02004fd8 (image word 0x02004fd8)
 *   pool +0x68 -> native_data_0220dda4 (image word 0x0220dda4)
 *   pool +0x6c -> constant 0x020048a0 (image word 0x020048a0)
 *   pool +0x70 -> native_data_0220ddbc (image word 0x0220ddbc)
 *   pool +0x74 -> constant 0x02004cd8 (image word 0x02004cd8)
 *   pool +0x78 -> constant 0x04001008 (image word 0x04001008)
 *   pool +0x7c -> constant 0x04000008 (image word 0x04000008)
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f8e1c; the literal pool and
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

extern u8 native_data_0220dd78[];
extern void native_fn_021f27d4(void);
extern u8 native_data_0220dd8c[];
extern u8 native_data_0220dda4[];
extern u8 native_data_0220ddbc[];


asm u32 native_ov006_021f8e1c (register u32 a0)
{
    push {r4, lr}
    ldr r0, =native_data_0220dd78
    ldr r1, =0x0200494c
    bl native_fn_021f27d4
    ldr r0, =native_data_0220dd8c
    ldr r1, =0x02004fd8
    bl native_fn_021f27d4
    ldr r0, =native_data_0220dda4
    ldr r1, =0x020048a0
    bl native_fn_021f27d4
    ldr r0, =native_data_0220ddbc
    ldr r1, =0x02004cd8
    bl native_fn_021f27d4
    ldr r3, =0x04001008
    mov r1, #0x3
    ldrh r0, [r3, #0]
    mov r2, #0x3
    bic r0, r1
    orr r0, r2
    strh r0, [r3, #0]
    ldrh r0, [r3, #0x2]
    bic r0, r1
    orr r0, r2
    strh r0, [r3, #0x2]
    ldr r3, =0x04000008
    mov r0, #0x2
    ldrh r4, [r3, #0]
    bic r4, r1
    orr r0, r4
    strh r0, [r3, #0]
    ldrh r0, [r3, #0x2]
    bic r0, r1
    orr r0, r2
    strh r0, [r3, #0x2]
    ldrh r0, [r3, #0x4]
    bic r0, r1
    orr r0, r2
    strh r0, [r3, #0x4]
    pop {r4, pc}
    mov r8, r8
}
