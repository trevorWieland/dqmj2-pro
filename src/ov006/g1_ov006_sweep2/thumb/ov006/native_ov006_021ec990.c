/* ov006 row 0x021ec990: 68 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x3c -> native_data_0220d43c (image word 0x0220d43c)
 *   pool +0x40 -> native_data_0220d448 (image word 0x0220d448)
 *   branch +0x26 -> +0x2e
 *   test +0x24 cmp r2, #0xd
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ec990; the literal pool and
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

extern u8 native_data_0220d43c[];
extern void native_fn_021edcd0(void);
extern void native_fn_021edb9c(void);
extern u8 native_data_0220d448[];


asm u32 native_ov006_021ec990 (register u32 a0)
{
    push {r4, lr}
    add r4, r0, #0x0
    ldr r0, =native_data_0220d43c
    bl native_fn_021edcd0
    str r0, [r4, #0]
    ldr r1, =native_data_0220d43c
    ldr r2, [r4, #0]
    add r0, r4, #0x4
    bl native_fn_021edb9c
    mov r0, #0x1
    str r0, [r4, #0x24]
    ldr r0, =native_data_0220d448
    bl native_fn_021edcd0
    add r2, r0, #0x0
    str r0, [r4, #0x28]
    cmp r2, #0xd
    bls ov006_021ec990_L2e
    mov r0, #0x0
    mvn r0, r0
    pop {r4, pc}
ov006_021ec990_L2e:
    add r4, #0x2c
    ldr r1, =native_data_0220d448
    add r0, r4, #0x0
    bl native_fn_021edb9c
    mov r0, #0x0
    pop {r4, pc}
}
