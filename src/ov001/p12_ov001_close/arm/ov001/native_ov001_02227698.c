/* ov001 row 0x02227698: 84 bytes.
 *
 * What it does: 20 instructions; 4 call(s) to 0x02224020, 0x02226bdc, 0x02224050, +1 more; loops (back edge at +0x24); returns through pop {r3, r4, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block copy loop (20 instructions, 4 calls, 0 branches, 4 back edges, 1 literal slot).
 *
 *   pool +0x50 -> native_data_0222e854 (image word 0x0222e854)
 *   2 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02227698; the literal pool and
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

extern u8 native_data_0222e854[];
extern void native_fn_02224020(void);
extern void native_fn_02226bdc(void);
extern void native_fn_02224050(void);
extern void native_fn_02226cb0(void);


asm u32 native_ov001_02227698 (register u32 a0)
{
    stmdb sp!, {r3, r4, lr}
    sub sp, sp, #12
    ldr r1, =native_data_0222e854
    mov r4, r0
    add r3, sp, #0
    ldmia r1, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    ldr r1, [r4, #0x4]
    mov r0, r3
    bl native_fn_02224020
    add r0, sp, #0
    mov r1, r4
    mov r2, #26
    bl native_fn_02226bdc
    add r0, sp, #0
    bl native_fn_02224050
    add r0, sp, #0
    bl native_fn_02226cb0
    add sp, sp, #12
    ldmia sp!, {r3, r4, pc}
}
