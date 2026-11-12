/* ov006 row 0x021dff30: 72 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021dff30; the literal pool and
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

extern void native_fn_02067b58(void);
extern void native_fn_02068ac4(void);


asm u32 native_ov006_021dff30 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    sub sp, sp, #16
    bl native_fn_02067b58
    ldrh r0, [r0, #4]
    str r0, [sp]
    bl native_fn_02067b58
    ldrb r0, [r0, #0x6]
    str r0, [sp, #0x4]
    bl native_fn_02067b58
    ldrb r0, [r0, #0x7]
    str r0, [sp, #0x8]
    bl native_fn_02067b58
    ldr r1, [r0]
    add r0, sp, #0
    str r1, [sp, #0xc]
    bl native_fn_02068ac4
    add sp, sp, #16
    ldmia sp!, {r3, pc}
}
