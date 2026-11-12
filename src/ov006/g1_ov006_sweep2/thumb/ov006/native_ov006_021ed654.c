/* ov006 row 0x021ed654: 84 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x50 -> constant 0x0221a8ac (image word 0x0221a8ac)
 *   branch +0x0a -> +0x40
 *   test +0x08 cmp r0, #0x1
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ed654; the literal pool and
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

extern void native_fn_021ed768(void);
extern void native_fn_021edc78(void);
extern void native_fn_021edb9c(void);


asm u32 native_ov006_021ed654 (register u32 a0)
{
    push {r4, r5, lr}
    sub sp, #0xc
    add r5, r1, #0x0
    add r4, r3, #0x0
    cmp r0, #0x1
    bne ov006_021ed654_L40
    ldr r0, [sp, #0x18]
    mov r1, #0x1
    strh r1, [r0, #0]
    add r0, r5, #0x2
    str r0, [sp]
    ldr r0, =0x0221a8ac
    ldr r3, [sp, #0x1c]
    str r0, [sp, #0x4]
    mov r0, #0x8
    str r0, [sp, #0x8]
    add r0, r2, #0x0
    mov r2, #0x0
    ldrsh r2, [r4, r2]
    add r1, r5, #0x4
    bl native_fn_021ed768
    ldrh r0, [r4, #0]
    bl native_fn_021edc78
    strh r0, [r5, #0]
    mov r0, #0x0
    ldrsh r0, [r4, r0]
    add sp, #0xc
    add r0, r0, #0x4
    strh r0, [r4, #0]
    pop {r4, r5, pc}
ov006_021ed654_L40:
    add r1, r2, #0x0
    mov r2, #0x0
    ldrsh r2, [r4, r2]
    add r0, r5, #0x0
    bl native_fn_021edb9c
    add sp, #0xc
    pop {r4, r5, pc}
}
