/* ov000 row 0x021fc7e8: 468 bytes.
 *
 * What it does: 114 instructions; 18 call(s) to 0x02215698, 0x02049ae4, 0x02049f24, +15 more; loops (back edge at +0x14); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x1c8 -> constant 0x021c9698 (image word 0x021c9698)
 *   pool +0x1cc -> constant 0x022372a8 (image word 0x022372a8)
 *   pool +0x1d0 -> constant 0x020dbc18 (image word 0x020dbc18)
 *   branch +0x38 -> +0x1a8
 *   branch +0x6c -> +0xbc
 *   branch +0xb8 -> +0x1a0
 *   branch +0xc8 -> +0x118
 *   branch +0x114 -> +0x1a0
 *   branch +0x1b0 -> +0x1bc
 *   test +0x34 cmp r0, #4
 *   test +0x68 cmp r1, #0
 *   test +0xc4 cmp r1, r0
 *   test +0x1ac cmp r1, #0
 *   0 block transfer(s), 13 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021fc7e8; the literal pool and
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

extern void native_fn_02215698(void);
extern void native_fn_02049ae4(void);
extern void native_fn_02049f24(void);
extern void native_fn_02049f30(void);
extern void native_fn_02049ad0(void);
extern void native_fn_02046af4(void);
extern void native_fn_02049f14(void);
extern void native_fn_02217bdc(void);
extern void native_fn_02065d88(void);
extern void native_fn_02066a6c(void);
extern void native_fn_02217cf0(void);
extern void native_fn_020853c8(void);


asm u32 native_ov000_021fc7e8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    sub sp, sp, #8
    bl native_fn_02215698
    mov r6, r0
    ldr r7, =0x021c9698
    bl native_fn_02049ae4
    mov r9, r0
    bl native_fn_02049f24
    mov r5, r0
    bl native_fn_02049f30
    ldr r0, =0x022372a8
    ldr r4, [r0, #0xc]
    ldr r0, [r4]
    cmp r0, #4
    bne ov000_021fc7e8_L1a8
    add r8, r4, #252
    ldr r1, [r4, #0xfc]
    ldr r0, [r8, #0x4]
    add r1, r1, #5
    sub r0, r1, r0
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02049ad0
    ldr r0, [r0]
    ldr r1, [r4, #0xfc]
    ldr r4, [r0, #0x4]
    cmp r1, #0
    bne ov000_021fc7e8_Lbc
    str r5, [sp]
    mov r0, #255
    str r0, [sp, #0x4]
    ldrb r2, [r4, #0x5e]
    ldr r1, [r4, #0x68]
    mov r0, r7
    mov r3, #0
    bl native_fn_02046af4
    mov r0, r5
    bl native_fn_02049f14
    mov r3, #1
    str r3, [sp]
    mov r2, #87
    mov r0, #5
    mov r1, #7
    str r2, [sp, #0x4]
    mov r2, #55
    bl native_fn_02217bdc
    b ov000_021fc7e8_L1a0
ov000_021fc7e8_Lbc:
    ldrh r0, [r8, #14]
    sub r0, r0, #1
    cmp r1, r0
    bne ov000_021fc7e8_L118
    str r5, [sp]
    mov r0, #255
    str r0, [sp, #0x4]
    ldrb r2, [r4, #0x5e]
    ldr r1, [r4, #0x68]
    mov r0, r7
    mov r3, #0
    bl native_fn_02046af4
    mov r0, r5
    bl native_fn_02049f14
    mov r3, #1
    str r3, [sp]
    mov r2, #87
    mov r0, #5
    mov r1, #7
    str r2, [sp, #0x4]
    mov r2, #56
    bl native_fn_02217bdc
    b ov000_021fc7e8_L1a0
ov000_021fc7e8_L118:
    ldr r0, =0x022372a8
    ldr r0, [r0, #0xc]
    add r0, r0, r1, lsl #2
    ldr r8, [r0, #0x1ec]
    mov r0, r8
    bl native_fn_02065d88
    ldrb r0, [r0, #0x24]
    bl native_fn_02066a6c
    add r0, r0, #123
    add r0, r0, #256
    mov r3, r0, lsl #1
    mov r0, r7
    ldr r1, =0x020dbc18
    add r2, r5, #2
    ldrh r7, [r1, r3]
    mov r1, #255
    mov r3, #0
    strh r7, [r5]
    str r2, [sp]
    str r1, [sp, #0x4]
    ldr r1, [r4, #0x68]
    ldrb r2, [r4, #0x5e]
    bl native_fn_02046af4
    mov r0, r5
    bl native_fn_02049f14
    mov r0, r8, lsl #16
    mov r2, r0, lsr #16
    mov r3, #1
    str r3, [sp]
    mov r0, #87
    str r0, [sp, #0x4]
    mov r0, #14
    mov r1, #0
    bl native_fn_02217bdc
ov000_021fc7e8_L1a0:
    add r0, r6, #16
    bl native_fn_02217cf0
ov000_021fc7e8_L1a8:
    ldr r1, [r9]
    cmp r1, #0
    beq ov000_021fc7e8_L1bc
    ldr r0, [r9, #0x4]
    bl native_fn_020853c8
ov000_021fc7e8_L1bc:
    mov r0, #0
    add sp, sp, #8
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
