/* ov006 row 0x021f2124: 56 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x30 -> constant 0x0221aad0 (image word 0x0221aad0)
 *   pool +0x34 -> native_data_0220d480 (image word 0x0220d480)
 *   branch +0x14 -> +0x18
 *   branch +0x16 -> +0x22
 *   test +0x12 cmp r1, r0
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f2124; the literal pool and
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

extern u8 native_data_0220d480[];
extern void native_fn_021f1ef0(void);


asm u32 native_ov006_021f2124 (register u32 a0)
{
    push {r4, lr}
    add r4, r0, #0x0
    ldr r0, =0x0221aad0
    ldr r0, [r0, #0x38]
    str r0, [r4, #0]
    ldr r0, =native_data_0220d480
    ldr r1, [r0, #0xc]
    mov r0, #0x0
    mvn r0, r0
    cmp r1, r0
    bne ov006_021f2124_L18
    b ov006_021f2124_L22
ov006_021f2124_L18:
    bl native_fn_021f1ef0
    ldr r1, =native_data_0220d480
    ldr r1, [r1, #0xc]
    sub r0, r1, r0
ov006_021f2124_L22:
    str r0, [r4, #0x4]
    ldr r0, =0x0221aad0
    ldr r0, [r0, #0x78]
    str r0, [r4, #0x8]
    mov r0, #0x1
    pop {r4, pc}
    mov r8, r8
}
