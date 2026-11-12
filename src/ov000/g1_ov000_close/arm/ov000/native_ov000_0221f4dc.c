/* ov000 row 0x0221f4dc: 288 bytes.
 *
 * What it does: 66 instructions; 8 call(s) to 0x0205dc70, 0x02046af4, 0x0205dc70, +5 more; loops (back edge at +0x14); returns through pop {r3, pc}; 6 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x108 -> constant 0x022463f6 (image word 0x022463f6)
 *   pool +0x10c -> constant 0x021c9698 (image word 0x021c9698)
 *   pool +0x110 -> constant 0x0224640a (image word 0x0224640a)
 *   pool +0x114 -> constant 0x022463b0 (image word 0x022463b0)
 *   pool +0x118 -> constant 0x02246420 (image word 0x02246420)
 *   pool +0x11c -> constant 0x022463dc (image word 0x022463dc)
 *   back edge +0xd4 -> +0xc0
 *   test +0xcc cmp r0, #3
 *   0 block transfer(s), 15 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0221f4dc; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity fixes the instruction stream, not the field, block and callee semantics behind the addresses and strides it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_0205dc70(void);
extern void native_fn_02046af4(void);
extern void native_fn_0222137c(void);
extern void native_fn_02062b00(void);
extern void native_fn_020629e0(void);


asm u32 native_ov000_0221f4dc (register u32 a0)
{
    stmdb sp!, {r3, lr}
    sub sp, sp, #8
    mov r0, #9
    mov r1, #0
    mov r2, #2
    bl native_fn_0205dc70
    ldr r2, =0x022463f6
    mov r1, r0
    str r2, [sp]
    mov r12, #255
    ldr r0, =0x021c9698
    mov r2, #24
    mov r3, #0
    str r12, [sp, #0x4]
    bl native_fn_02046af4
    mov r0, #9
    mov r1, #0
    mov r2, #3
    bl native_fn_0205dc70
    ldr r2, =0x0224640a
    mov r1, r0
    str r2, [sp]
    mov r0, #255
    str r0, [sp, #0x4]
    ldr r0, =0x021c9698
    mov r2, #24
    mov r3, #0
    bl native_fn_02046af4
    ldr r2, =0x022463b0
    mov r0, #0
    ldr r3, [r2, #0x1c]
    ldr r1, =0x02246420
    strh r0, [r3, #156]
    ldr r12, [r2, #0x1c]
    ldrsh r3, [r12, #156]
    strh r3, [r12, #24]
    ldr r3, [r2, #0x1c]
    str r0, [r3, #0x98]
    ldr r12, [r2, #0x1c]
    ldr r3, [r12, #0x98]
    str r3, [r12, #0x14]
    ldr r3, [r2, #0x1c]
    mov r12, r0
    strb r0, [r3, #0x9f]
    ldr r3, [r2, #0x1c]
    ldrb r2, [r3, #0x9f]
    strb r2, [r3, #0x1b]
    ldr r2, =0x022463dc
ov000_0221f4dc_Lc0:
    mov r3, r0, lsl #1
    add r0, r0, #1
    strh r12, [r2, r3]
    cmp r0, #3
    strb r12, [r1], #1
    blt ov000_0221f4dc_Lc0
    bl native_fn_0222137c
    bl native_fn_02062b00
    ldr r1, =0x022463b0
    str r0, [r1, #0x14]
    bl native_fn_020629e0
    ldr r1, =0x022463b0
    mov r2, #0
    str r0, [r1, #0x10]
    ldr r0, [r1, #0x24]
    str r2, [r0, #0x14]
    add sp, sp, #8
    ldmia sp!, {r3, pc}
}
