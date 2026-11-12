/* ov006 row 0x021e4bd8: 68 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x3c -> constant 0x020b9f64 (image word 0x020b9f64)
 *   pool +0x40 -> constant 0x02218d30 (image word 0x02218d30)
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e4bd8; the literal pool and
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

extern void native_fn_021e3cd4(void);
extern void native_fn_021e7e78(void);


asm u32 native_ov006_021e4bd8 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    bl native_fn_021e3cd4
    ldr r2, =0x020b9f64
    ldr r1, =0x02218d30
    mov r0, #74
    str r2, [r1, #0xc]
    str r0, [r1, #0x1c]
    mov r0, #1
    str r0, [r1, #0x18]
    mov r2, #3
    str r2, [r1, #0x14]
    mov r2, #0
    str r2, [r1, #0x10]
    bl native_fn_021e7e78
    ldmia sp!, {r3, pc}
}
