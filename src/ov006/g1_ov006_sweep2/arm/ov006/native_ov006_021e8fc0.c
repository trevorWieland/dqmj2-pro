/* ov006 row 0x021e8fc0: 72 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x3c -> constant 0x02218e18 (image word 0x02218e18)
 *   pool +0x40 -> constant 0x02218d90 (image word 0x02218d90)
 *   pool +0x44 -> native_data_02207e04 (image word 0x02207e04)
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e8fc0; the literal pool and
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

extern void native_fn_0205f9e4(void);
extern u8 native_data_02207e04[];


asm u32 native_ov006_021e8fc0 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r6, r0
    ldr r0, =0x02218e18
    mov r5, r1
    mov r4, r2
    bl native_fn_0205f9e4
    ldr r0, =0x02218d90
    ldr r1, =native_data_02207e04
    ldr r2, [r0, #0x64]
    mov r0, r6
    ldr r3, [r1, r2, lsl #2]
    mov r1, r5
    mov r2, r4
    blx r3
    ldmia sp!, {r4, r5, r6, pc}
}
