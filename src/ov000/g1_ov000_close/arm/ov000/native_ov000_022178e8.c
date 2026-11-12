/* ov000 row 0x022178e8: 100 bytes.
 *
 * What it does: 24 instructions; 4 call(s) to 0x0203cc2c, 0x0204518c, 0x0204820c, +1 more; loops (back edge at +0x18); returns through pop {r4, r5, r6, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x60 -> native_data_0222f9f4 (image word 0x0222f9f4)
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022178e8; the literal pool and
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

extern u8 native_data_0222f9f4[];
extern void native_fn_0203cc2c(void);
extern void native_fn_0204518c(void);
extern void native_fn_0204820c(void);
extern void native_fn_0202a498(void);


asm u32 native_ov000_022178e8 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    sub sp, sp, #8
    mov r6, r0
    mov r5, r1
    ldr r0, =native_data_0222f9f4
    mov r1, #2
    bl native_fn_0203cc2c
    mov r4, r0
    add r0, sp, #0
    mov r1, r4
    mov r2, #17
    bl native_fn_0204518c
    ldr r0, [sp]
    add r1, r6, #2
    add r0, r0, r5, lsl #5
    mov r1, r1, lsl #5
    mov r2, #32
    bl native_fn_0204820c
    mov r1, r4
    mov r0, #2
    bl native_fn_0202a498
    mov r0, #0
    add sp, sp, #8
    ldmia sp!, {r4, r5, r6, pc}
}
