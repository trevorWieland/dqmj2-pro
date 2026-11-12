/* ov006 row 0x021ed5c8: 140 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x84 -> constant 0x02219b6c (image word 0x02219b6c)
 *   pool +0x88 -> constant 0x02219b4c (image word 0x02219b4c)
 *   0 block transfer(s), 9 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ed5c8; the literal pool and
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

extern void native_fn_021edb9c(void);
extern void native_fn_021edc78(void);
extern void native_fn_021edc50(void);


asm u32 native_ov006_021ed5c8 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    ldr r1, =0x02219b6c
    add r5, r0, #0x0
    mov r0, #0x1d
    ldrsb r0, [r1, r0]
    ldr r1, =0x02219b4c
    mov r6, #0x0
    strb r0, [r5, #0]
    mov r0, #0x1
    strb r0, [r5, #0x1]
    ldr r0, [r1, #0x28]
    ldr r1, [r1, #0x24]
    lsl r0, r0, #0x10
    asr r4, r0, #0x10
    add r0, r5, #0x6
    add r2, r4, #0x0
    bl native_fn_021edb9c
    lsl r0, r4, #0x10
    lsr r0, r0, #0x10
    bl native_fn_021edc78
    strh r0, [r5, #0x2]
    add r0, r4, #0x6
    lsl r0, r0, #0x10
    asr r0, r0, #0x10
    add r1, r0, #0x1
    lsr r0, r1, #0x1f
    add r0, r1, r0
    asr r0, r0, #0x1
    lsl r0, r0, #0x11
    asr r7, r0, #0x10
    lsl r0, r7, #0x10
    lsr r0, r0, #0x10
    bl native_fn_021edc78
    strh r0, [r5, #0x4]
    add r0, r6, r7
    lsl r0, r0, #0x10
    asr r6, r0, #0x10
    mov r0, #0x60
    strb r0, [r5, r7]
    add r4, r5, r7
    mov r0, #0x0
    strb r0, [r4, #0x1]
    bl native_fn_021edc78
    strh r0, [r4, #0x4]
    mov r0, #0xe
    bl native_fn_021edc50
    str r0, [sp]
    add r0, r4, #0x6
    add r1, sp, #0x0
    mov r2, #0x4
    bl native_fn_021edb9c
    mov r0, #0x4
    bl native_fn_021edc78
    add r6, #0xa
    strh r0, [r4, #0x2]
    lsl r0, r6, #0x10
    asr r0, r0, #0x10
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
}
