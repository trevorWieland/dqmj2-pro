/* ov006 row 0x021e94e4: 72 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x40 -> native_data_0220d114 (image word 0x0220d114)
 *   pool +0x44 -> constant 0x02218d90 (image word 0x02218d90)
 *   branch +0x1c -> +0x38
 *   test +0x0c cmp r1, r0
 *   test +0x18 cmpne r0, #0
 *   test +0x2c cmp r1, r0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e94e4; the literal pool and
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

extern u8 native_data_0220d114[];


asm u32 native_ov006_021e94e4 (register u32 a0)
{
    ldr r1, =native_data_0220d114
    mvn r0, #0
    ldr r1, [r1, #0x8]
    cmp r1, r0
    ldrne r0, =0x02218d90
    ldrne r0, [r0, #0x60]
    cmpne r0, #0
    bne ov006_021e94e4_L38
    ldr r1, =native_data_0220d114
    mvn r0, #0
    ldr r1, [r1, #0x20]
    cmp r1, r0
    moveq r0, #1
    bxeq lr
ov006_021e94e4_L38:
    mov r0, #0
    bx lr
}
