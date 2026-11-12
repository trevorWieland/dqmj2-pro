/* ov000 row 0x02221a40: 100 bytes.
 *
 * What it does: 21 instructions; 2 call(s) to 0x0205db90, 0x0205d9e8; loops (back edge at +0x20); 4 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x54 -> constant 0x02246438 (image word 0x02246438)
 *   pool +0x58 -> native_data_0222fbb0 (image word 0x0222fbb0)
 *   pool +0x5c -> constant 0x020daf0c (image word 0x020daf0c)
 *   pool +0x60 -> constant 0x020daef8 (image word 0x020daef8)
 *   2 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02221a40; the literal pool and
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

extern u8 native_data_0222fbb0[];
extern void native_fn_0205db90(void);
extern void native_fn_0205d9e8(void);


asm u32 native_ov000_02221a40 (register u32 a0)
{
    stmdb sp!, {lr}
    sub sp, sp, #36
    mov r12, #1
    ldr r3, =0x02246438
    ldr r1, =native_data_0222fbb0
    add r0, sp, #4
    sub r2, r12, #2
    str r12, [r3, #0x18]
    bl native_fn_0205db90
    mov r12, #9
    ldr r2, =0x020daf0c
    ldr r3, =0x020daef8
    add r1, sp, #4
    mov r0, #2
    str r12, [sp]
    bl native_fn_0205d9e8
    ldr r1, =0x02246438
    str r0, [r1, #0x8]
    mov r0, #1
    add sp, sp, #36
    ldmia sp!, {pc}
}
