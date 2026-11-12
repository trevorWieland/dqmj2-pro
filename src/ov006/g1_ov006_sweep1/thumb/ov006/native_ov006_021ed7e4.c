/* ov006 row 0x021ed7e4: 136 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x80 -> native_data2_0221a8b4 (image word 0x0221a8b4)
 *   pool +0x84 -> constant 0x0221a8b6 (image word 0x0221a8b6)
 *   branch +0x16 -> +0x26
 *   branch +0x5e -> +0x74
 *   test +0x14 cmp r0, #0x0
 *   test +0x5c cmp r0, r6
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ed7e4; the literal pool and
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

extern void native_fn_021ebb1c(void);
extern void native_fn_021ec6e0(void);
extern u8 native_data2_0221a8b4[];
extern void native_fn_021edb9c(void);
extern void native_fn_021ed86c(void);
extern void native_fn_021ed8d0(void);
extern void native_fn_021ed93c(void);
extern void native_fn_021ebb2c(void);


asm u32 native_ov006_021ed7e4 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x10
    add r4, r2, #0x0
    add r7, r0, #0x0
    add r0, r4, #0x0
    add r5, r1, #0x0
    add r6, r3, #0x0
    bl native_fn_021ebb1c
    str r0, [sp, #0x8]
    cmp r0, #0x0
    bne ov006_021ed7e4_L26
    mov r0, #0x2
    bl native_fn_021ec6e0
    mov r0, #0x0
    add sp, #0x10
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
ov006_021ed7e4_L26:
    ldr r0, =native_data2_0221a8b4
    ldr r1, [sp, #0x28]
    mov r2, #0x2
    bl native_fn_021edb9c
    ldr r0, =0x0221a8b6
    ldr r1, [sp, #0x2c]
    ldr r2, [sp, #0x30]
    bl native_fn_021edb9c
    ldr r2, [sp, #0x30]
    ldr r1, =native_data2_0221a8b4
    add r0, sp, #0x0
    add r2, r2, #0x2
    add r3, r4, #0x0
    bl native_fn_021ed86c
    add r0, sp, #0x0
    add r1, r5, #0x0
    add r2, r7, #0x0
    add r3, r4, #0x0
    bl native_fn_021ed8d0
    add r0, r5, #0x0
    add r1, r4, #0x0
    bl native_fn_021ed93c
    cmp r0, r6
    beq ov006_021ed7e4_L74
    mov r0, #0x12
    bl native_fn_021ec6e0
    ldr r0, [sp, #0x8]
    bl native_fn_021ebb2c
    mov r0, #0x0
    add sp, #0x10
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
ov006_021ed7e4_L74:
    ldr r0, [sp, #0x8]
    bl native_fn_021ebb2c
    mov r0, #0x0
    add sp, #0x10
    pop {r3, r4, r5, r6, r7, pc}
}
