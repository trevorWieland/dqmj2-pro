/* ov006 row 0x021e9dc8: 60 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x38 -> native_data_0220d3b8 (image word 0x0220d3b8)
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e9dc8; the literal pool and
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

extern void native_fn_021e6530(void);
extern u8 native_data_0220d3b8[];
extern void native_fn_02072568(void);


asm u32 native_ov006_021e9dc8 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r4, r1
    bl native_fn_021e6530
    mov r1, r0
    ldr r2, =native_data_0220d3b8
    mov r0, #0
    str r1, [r2, #0x10]
    str r4, [r2]
    bl native_fn_02072568
    ldr r1, =native_data_0220d3b8
    mov r0, #1
    ldr r1, [r1]
    bl native_fn_02072568
    ldmia sp!, {r4, pc}
}
