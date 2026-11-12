/* ov006 row 0x021e2ab8: 236 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xd8 -> constant 0x01fffba0 (image word 0x01fffba0)
 *   pool +0xdc -> native_data2_02216a58 (image word 0x02216a58)
 *   pool +0xe0 -> native_data2_022169d0 (image word 0x022169d0)
 *   pool +0xe4 -> constant 0x02216a54 (image word 0x02216a54)
 *   pool +0xe8 -> constant 0x0221696c (image word 0x0221696c)
 *   branch +0x54 -> +0x88
 *   branch +0x68 -> +0xac
 *   branch +0x84 -> +0xac
 *   back edge +0xb8 -> +0x4c
 *   test +0x50 cmp r9, #3
 *   test +0xb0 cmp r9, #4
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e2ab8; the literal pool and
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

extern void native_fn_020633b0(void);
extern void native_fn_02008d78(void);
extern u8 native_data2_02216a58[];
extern u8 native_data2_022169d0[];
extern void native_fn_02062a10(void);
extern void native_fn_02046af4(void);
extern void native_fn_02067748(void);
extern void native_fn_020bb1b4(void);


asm u32 native_ov006_021e2ab8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #8
    bl native_fn_020633b0
    mov r8, r0
    ldr r0, =0x01fffba0
    mov r1, #0
    mov r2, #6
    bl native_fn_02008d78
    ldr r0, =native_data2_02216a58
    mov r1, #0
    mov r2, #128
    bl native_fn_02008d78
    mov r9, #0
    mov r5, #255
    ldr r10, =native_data2_02216a58
    ldr r7, =native_data2_022169d0
    mov r4, r9
    mov r6, r5
    mov r11, r9
ov006_021e2ab8_L4c:
    str r10, [r7, r9, lsl #2]
    cmp r9, #3
    bge ov006_021e2ab8_L88
    add r0, r8, r9, lsl #2
    ldr r0, [r0, #0x1c]
    bl native_fn_02062a10
    movs r1, r0
    beq ov006_021e2ab8_Lac
    str r10, [sp]
    mov r0, r11
    mov r2, r11
    mov r3, r11
    str r6, [sp, #0x4]
    bl native_fn_02046af4
    b ov006_021e2ab8_Lac
ov006_021e2ab8_L88:
    bl native_fn_02067748
    mov r1, r0
    str r10, [sp]
    mov r0, r4
    add r1, r1, #16
    str r5, [sp, #0x4]
    mov r2, r4
    mov r3, r4
    bl native_fn_02046af4
ov006_021e2ab8_Lac:
    add r9, r9, #1
    cmp r9, #4
    add r10, r10, #32
    blt ov006_021e2ab8_L4c
    ldr r1, =native_data2_022169d0
    ldr r2, =0x02216a54
    ldr r3, =0x0221696c
    mov r0, #4
    bl native_fn_020bb1b4
    add sp, sp, #8
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
