/* ov006 row 0x021ef810: 60 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x38 -> constant 0x000001e6 (image word 0x000001e6)
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ef810; the literal pool and
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

extern void native_fn_020900f4(void);
extern void native_fn_020907e4(void);
extern void native_fn_021ef7f8(void);


asm u32 native_ov006_021ef810 (register u32 a0)
{
    push {r4, r5, r6, lr}
    sub sp, #0x10
    add r5, r0, #0x0
    add r6, r1, #0x0
    mov r1, #0x8
    add r0, sp, #0x4
    strb r1, [r0, #0x4]
    mov r1, #0x2
    strb r1, [r0, #0x5]
    sub r1, r1, #0x3
    str r1, [sp, #0xc]
    ldr r1, =0x000001e6
    add r4, r2, #0x0
    strh r1, [r0, #0x6]
    bl native_fn_020900f4
    add r1, sp, #0x4
    bl native_fn_020907e4
    add r0, r5, #0x0
    add r1, sp, #0x8
    add r2, sp, #0x4
    add r3, r6, #0x0
    str r4, [sp]
    bl native_fn_021ef7f8
    add sp, #0x10
    pop {r4, r5, r6, pc}
}
