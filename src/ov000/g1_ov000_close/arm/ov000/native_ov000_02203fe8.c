/* ov000 row 0x02203fe8: 96 bytes.
 *
 * What it does: 20 instructions; 3 call(s) to 0x02061944, 0x0205db90, 0x0205d9e8; loops (back edge at +0x08); 4 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x50 -> native_data_0222f56c (image word 0x0222f56c)
 *   pool +0x54 -> constant 0x020dae90 (image word 0x020dae90)
 *   pool +0x58 -> constant 0x020dae88 (image word 0x020dae88)
 *   pool +0x5c -> constant 0x02238190 (image word 0x02238190)
 *   2 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02203fe8; the literal pool and
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

extern void native_fn_02061944(void);
extern u8 native_data_0222f56c[];
extern void native_fn_0205db90(void);
extern void native_fn_0205d9e8(void);


asm u32 native_ov000_02203fe8 (register u32 a0)
{
    stmdb sp!, {lr}
    sub sp, sp, #36
    bl native_fn_02061944
    mov r2, #0
    strb r2, [r0, #0x26a]
    ldr r1, =native_data_0222f56c
    add r0, sp, #4
    sub r2, r2, #1
    bl native_fn_0205db90
    mov r12, #4
    ldr r2, =0x020dae90
    ldr r3, =0x020dae88
    add r1, sp, #4
    mov r0, #2
    str r12, [sp]
    bl native_fn_0205d9e8
    ldr r1, =0x02238190
    str r0, [r1, #0x10]
    add sp, sp, #36
    ldmia sp!, {pc}
}
