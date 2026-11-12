/* ov006 row 0x021df17c: 96 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x54 -> native_data_0220d0c4 (image word 0x0220d0c4)
 *   pool +0x58 -> native_data_0220d0bc (image word 0x0220d0bc)
 *   pool +0x5c -> constant 0x0220f594 (image word 0x0220f594)
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021df17c; the literal pool and
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

extern u8 native_data_0220d0c4[];
extern void native_fn_02048404(void);
extern u8 native_data_0220d0bc[];
extern void native_fn_0204854c(void);
extern void native_fn_02048308(void);
extern void native_fn_0204b1a0(void);


asm u32 native_ov006_021df17c (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r1, =native_data_0220d0c4
    mov r0, #1
    mov r2, #4
    mov r3, #2
    bl native_fn_02048404
    mov r3, r0
    ldr r2, =native_data_0220d0bc
    and r1, r3, #255
    mov r0, #1
    strb r3, [r2]
    bl native_fn_0204854c
    ldr r1, =0x0220f594
    str r0, [r1, #0x24]
    ldr r0, [r0, #0x4]
    str r0, [r1, #0x5c]
    bl native_fn_02048308
    ldr r0, =0x0220f594
    ldr r0, [r0, #0x5c]
    bl native_fn_0204b1a0
    ldmia sp!, {r3, pc}
}
