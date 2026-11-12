/* ov006 row 0x021ed6a8: 86 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   0 block transfer(s), 9 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ed6a8; the literal pool and
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

extern void native_fn_021edc78(void);
extern void native_fn_021edb9c(void);


asm u32 native_ov006_021ed6a8 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    add r5, r0, #0x0
    mov r0, #0x1
    add r4, r1, #0x0
    add r6, r2, #0x0
    add r7, r3, #0x0
    bl native_fn_021edc78
    strh r0, [r5, #0]
    mov r0, #0x0
    strh r0, [r5, #0x2]
    strh r0, [r5, #0x4]
    lsl r0, r4, #0x10
    lsr r0, r0, #0x10
    bl native_fn_021edc78
    strh r0, [r5, #0x6]
    mov r0, #0x0
    strh r0, [r5, #0x8]
    lsl r0, r6, #0x10
    lsr r0, r0, #0x10
    bl native_fn_021edc78
    strh r0, [r5, #0xa]
    lsl r0, r7, #0x10
    lsr r0, r0, #0x10
    bl native_fn_021edc78
    strh r0, [r5, #0xc]
    add r1, sp, #0x8
    mov r0, #0x10
    ldrsb r0, [r1, r0]
    mov r2, #0x8
    strb r0, [r5, #0xe]
    mov r0, #0x14
    ldrsb r0, [r1, r0]
    ldr r1, [sp, #0x20]
    strb r0, [r5, #0xf]
    add r5, #0x10
    add r0, r5, #0x0
    bl native_fn_021edb9c
    pop {r3, r4, r5, r6, r7, pc}
}
