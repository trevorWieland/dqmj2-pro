/* ov000 row 0x021fdfac: 128 bytes.
 *
 * What it does: 28 instructions; 2 call(s) to 0x0205db90, 0x0205d9e8; loops (back edge at +0x2c); 4 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x70 -> native_data_0222f44c (image word 0x0222f44c)
 *   pool +0x74 -> constant 0x020dc880 (image word 0x020dc880)
 *   pool +0x78 -> constant 0x020dc878 (image word 0x020dc878)
 *   pool +0x7c -> constant 0x022372b8 (image word 0x022372b8)
 *   back edge +0x2c -> +0x14
 *   2 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021fdfac; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity fixes the instruction stream, not the field, block and callee semantics behind the addresses and strides it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_0222f44c[];
extern void native_fn_0205db90(void);
extern void native_fn_0205d9e8(void);


asm u32 native_ov000_021fdfac (register u32 a0)
{
    stmdb sp!, {lr}
    sub sp, sp, #36
    add r2, sp, #4
    mov r1, #8
    mov r0, #0
ov000_021fdfac_L14:
    strb r0, [r2]
    strb r0, [r2, #0x1]
    strb r0, [r2, #0x2]
    strb r0, [r2, #0x3]
    add r2, r2, #4
    subs r1, r1, #1
    bne ov000_021fdfac_L14
    ldr r1, =native_data_0222f44c
    add r0, sp, #4
    mvn r2, #0
    bl native_fn_0205db90
    mov r12, #3
    ldr r2, =0x020dc880
    ldr r3, =0x020dc878
    add r1, sp, #4
    mov r0, #1
    str r12, [sp]
    bl native_fn_0205d9e8
    ldr r1, =0x022372b8
    str r0, [r1]
    mov r0, #1
    add sp, sp, #36
    ldmia sp!, {pc}
}
