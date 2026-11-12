/* ov000 row 0x02205594: 92 bytes.
 *
 * What it does: 19 instructions; 3 call(s) to 0x02061944, 0x0205db90, 0x0205d9e8; loops (back edge at +0x08); 4 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x4c -> native_data_0222f578 (image word 0x0222f578)
 *   pool +0x50 -> constant 0x020dc3c0 (image word 0x020dc3c0)
 *   pool +0x54 -> constant 0x020dc3bc (image word 0x020dc3bc)
 *   pool +0x58 -> constant 0x02238190 (image word 0x02238190)
 *   2 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02205594; the literal pool and
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
extern u8 native_data_0222f578[];
extern void native_fn_0205db90(void);
extern void native_fn_0205d9e8(void);


asm u32 native_ov000_02205594 (register u32 a0)
{
    stmdb sp!, {lr}
    sub sp, sp, #36
    bl native_fn_02061944
    mov r2, #0
    strb r2, [r0, #0x26a]
    ldr r1, =native_data_0222f578
    add r0, sp, #4
    sub r2, r2, #1
    bl native_fn_0205db90
    mov r0, #2
    ldr r2, =0x020dc3c0
    ldr r3, =0x020dc3bc
    add r1, sp, #4
    str r0, [sp]
    bl native_fn_0205d9e8
    ldr r1, =0x02238190
    str r0, [r1, #0x14]
    add sp, sp, #36
    ldmia sp!, {pc}
}
