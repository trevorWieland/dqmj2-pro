/* ov006 row 0x021ed768: 124 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x74 -> constant 0x0221a8b4 (image word 0x0221a8b4)
 *   pool +0x78 -> constant 0x0221a8b6 (image word 0x0221a8b6)
 *   branch +0x1e -> +0x28
 *   test +0x1c cmp r0, #0x0
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ed768; the literal pool and
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

extern void native_fn_021ed93c(void);
extern void native_fn_021ebb1c(void);
extern void native_fn_021edce4(void);
extern void native_fn_021edb9c(void);
extern void native_fn_021ed86c(void);
extern void native_fn_021ed8d0(void);
extern void native_fn_021ebb2c(void);


asm u32 native_ov006_021ed768 (register u32 a0)
{
    push {r4, r5, r6, r7, lr}
    sub sp, #0x14
    add r5, r2, #0x0
    add r7, r1, #0x0
    add r4, r3, #0x0
    add r1, r5, #0x0
    add r6, r0, #0x0
    bl native_fn_021ed93c
    strb r0, [r4, #0]
    add r0, r5, #0x0
    bl native_fn_021ebb1c
    str r0, [sp, #0xc]
    cmp r0, #0x0
    bne ov006_021ed768_L28
    mov r0, #0x0
    add sp, #0x14
    mvn r0, r0
    pop {r4, r5, r6, r7, pc}
ov006_021ed768_L28:
    bl native_fn_021edce4
    add r1, sp, #0x0
    strh r0, [r1, #0]
    ldr r0, [sp, #0x28]
    add r1, sp, #0x0
    mov r2, #0x2
    bl native_fn_021edb9c
    ldr r0, =0x0221a8b4
    ldr r1, [sp, #0x28]
    mov r2, #0x2
    bl native_fn_021edb9c
    ldr r0, =0x0221a8b6
    ldr r1, [sp, #0x2c]
    ldr r2, [sp, #0x30]
    bl native_fn_021edb9c
    ldr r2, [sp, #0x30]
    ldr r1, =0x0221a8b4
    add r0, sp, #0x4
    add r2, r2, #0x2
    add r3, r5, #0x0
    bl native_fn_021ed86c
    add r0, sp, #0x4
    add r1, r7, #0x0
    add r2, r6, #0x0
    add r3, r5, #0x0
    bl native_fn_021ed8d0
    ldr r0, [sp, #0xc]
    bl native_fn_021ebb2c
    mov r0, #0x0
    add sp, #0x14
    pop {r4, r5, r6, r7, pc}
}
