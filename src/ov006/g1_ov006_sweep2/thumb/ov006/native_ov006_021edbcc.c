/* ov006 row 0x021edbcc: 84 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x50 -> constant 0x01ff6210 (image word 0x01ff6210)
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021edbcc; the literal pool and
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

extern void native_fn_02026124(void);
extern void native_fn_020907f4(void);


asm u32 native_ov006_021edbcc (register u32 a0)
{
    push {r4, r5, r6, lr}
    sub sp, #0x8
    ldr r2, [r1, #0]
    ldr r0, [r1, #0x4]
    ldr r5, [sp, #0x18]
    str r2, [sp]
    str r0, [sp, #0x4]
    ldr r0, [r5, #0]
    mov r4, #0x0
    ldr r2, =0x01ff6210
    asr r1, r0, #0x1f
    add r3, r4, #0x0
    blx native_fn_02026124
    lsr r3, r0, #0x6
    lsl r2, r1, #0x1a
    orr r3, r2
    lsr r0, r1, #0x6
    add r6, r4, r3
    adc r4, r0
    ldr r0, [r5, #0x4]
    ldr r2, =0x01ff6210
    asr r1, r0, #0x1f
    mov r3, #0x0
    blx native_fn_02026124
    lsr r3, r0, #0x6
    lsl r2, r1, #0x1a
    orr r3, r2
    lsr r0, r1, #0x6
    add r2, r6, r3
    adc r4, r0
    add r0, sp, #0x0
    mov r1, #0x1
    add r3, r4, #0x0
    bl native_fn_020907f4
    add sp, #0x8
    pop {r4, r5, r6, pc}
    mov r8, r8
}
