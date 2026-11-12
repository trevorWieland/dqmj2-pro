/* ov006 row 0x022040cc: 64 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x3c -> constant 0x027fffa8 (image word 0x027fffa8)
 *   branch +0x10 -> +0x18
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x022040cc; the literal pool and
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

extern void native_fn_02203fac(void);


asm u32 native_ov006_022040cc (register u32 a0)
{
    push {r3, lr}
    sub sp, #0x8
    ldr r1, =0x027fffa8
    ldrh r2, [r1, #0]
    mov r1, #0x2
    lsl r1, r1, #0xe
    and r1, r2
    asr r1, r1, #0xf
    beq ov006_022040cc_L18
    add sp, #0x8
    mov r0, #0x0
    pop {r3, pc}
ov006_022040cc_L18:
    ldrh r2, [r0, #0]
    add r1, sp, #0x0
    strh r2, [r1, #0]
    ldrh r2, [r0, #0x2]
    strh r2, [r1, #0x2]
    ldrh r3, [r0, #0]
    ldrh r2, [r0, #0x4]
    add r2, r3, r2
    strh r2, [r1, #0x4]
    ldrh r2, [r0, #0x2]
    ldrh r0, [r0, #0x6]
    add r0, r2, r0
    strh r0, [r1, #0x6]
    add r0, sp, #0x0
    bl native_fn_02203fac
    add sp, #0x8
    pop {r3, pc}
}
