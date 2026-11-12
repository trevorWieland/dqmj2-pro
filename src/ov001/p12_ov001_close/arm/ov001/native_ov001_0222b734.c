/* ov001 row 0x0222b734: 124 bytes.
 *
 * What it does: 30 instructions; 6 call(s) to 0x02223fe8, 0x02226bdc, 0x02226640, +3 more; loops (back edge at +0x2c); returns through pop {r3, r4, r5, r6, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block copy loop (30 instructions, 6 calls, 0 branches, 6 back edges, 1 literal slot).
 *
 *   pool +0x78 -> native_data_0222e1d0 (image word 0x0222e1d0)
 *   2 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0222b734; the literal pool and
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

extern u8 native_data_0222e1d0[];
extern void native_fn_02223fe8(void);
extern void native_fn_02226bdc(void);
extern void native_fn_02226640(void);
extern void native_fn_02224570(void);
extern void native_fn_02224050(void);
extern void native_fn_02226cb0(void);


asm u32 native_ov001_0222b734 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, lr}
    sub sp, sp, #12
    ldr r1, =native_data_0222e1d0
    add r3, sp, #0
    mov r6, r0
    ldmia r1, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    ldr r4, [r6, #0x4]
    mov r0, r3
    mov r1, r4
    ldr r5, [r6]
    bl native_fn_02223fe8
    add r0, sp, #0
    mov r1, r6
    mov r2, #169
    bl native_fn_02226bdc
    add r0, sp, #0
    mov r1, r5
    mov r2, r4
    bl native_fn_02226640
    mov r1, r4
    add r0, sp, #0
    mov r2, #0
    bl native_fn_02224570
    add r0, sp, #0
    bl native_fn_02224050
    add r0, sp, #0
    bl native_fn_02226cb0
    add sp, sp, #12
    ldmia sp!, {r3, r4, r5, r6, pc}
}
