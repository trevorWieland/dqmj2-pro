/* ov000 row 0x02207848: 132 bytes.
 *
 * What it does: 32 instructions; 10 call(s) to 0x02004120, 0x02008d78, 0x0203cc2c, +7 more; loops (back edge at +0x10); returns through pop {r3, r4, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x80 -> native_data_0222f6f4 (image word 0x0222f6f4)
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02207848; the literal pool and
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

extern void native_fn_02004120(void);
extern void native_fn_02008d78(void);
extern u8 native_data_0222f6f4[];
extern void native_fn_0203cc2c(void);
extern void native_fn_0204518c(void);
extern void native_fn_0204820c(void);
extern void native_fn_0202a498(void);
extern void native_fn_02048308(void);
extern void native_fn_022078cc(void);
extern void native_fn_0220681c(void);


asm u32 native_ov000_02207848 (register u32 a0)
{
    stmdb sp!, {r3, r4, lr}
    sub sp, sp, #12
    mov r0, #0
    strh r0, [sp]
    bl native_fn_02004120
    mov r1, #0
    mov r2, #16384
    bl native_fn_02008d78
    ldr r0, =native_data_0222f6f4
    mov r1, #2
    bl native_fn_0203cc2c
    mov r4, r0
    add r0, sp, #4
    mov r1, r4
    mov r2, #0
    bl native_fn_0204518c
    ldr r0, [sp, #0x4]
    ldr r2, [sp, #0x8]
    mov r1, #0
    bl native_fn_0204820c
    add r0, sp, #0
    mov r1, #0
    mov r2, #2
    bl native_fn_0204820c
    mov r1, r4
    mov r0, #2
    bl native_fn_0202a498
    bl native_fn_02048308
    bl native_fn_022078cc
    bl native_fn_0220681c
    add sp, sp, #12
    ldmia sp!, {r3, r4, pc}
}
