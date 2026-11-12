/* ov006 row 0x021e7210: 88 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x50 -> native_data_0220d114 (image word 0x0220d114)
 *   pool +0x54 -> constant 0x02218d90 (image word 0x02218d90)
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e7210; the literal pool and
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

extern void native_fn_021e7268(void);
extern void native_fn_02048404(void);
extern u8 native_data_0220d114[];
extern void native_fn_0204854c(void);
extern void native_fn_0204b1a0(void);


asm u32 native_ov006_021e7210 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    mov r4, r1
    bl native_fn_021e7268
    mov r0, #1
    mov r1, r5
    mov r2, r4
    mov r3, r0
    bl native_fn_02048404
    mov r3, r0
    ldr r2, =native_data_0220d114
    and r1, r3, #255
    mov r0, #1
    strb r3, [r2]
    bl native_fn_0204854c
    ldr r1, =0x02218d90
    str r0, [r1, #0x34]
    ldr r0, [r0, #0x4]
    bl native_fn_0204b1a0
    ldmia sp!, {r3, r4, r5, pc}
}
