/* ov000 row 0x0220819c: 92 bytes.
 *
 * What it does: 22 instructions; 7 call(s) to 0x0203cc2c, 0x0204518c, 0x0204820c, +4 more; loops (back edge at +0x10); returns through pop {r4, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x58 -> native_data_0222f728 (image word 0x0222f728)
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0220819c; the literal pool and
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

extern u8 native_data_0222f728[];
extern void native_fn_0203cc2c(void);
extern void native_fn_0204518c(void);
extern void native_fn_0204820c(void);
extern void native_fn_0202a498(void);
extern void native_fn_02048308(void);
extern void native_fn_022081f8(void);
extern void native_fn_0220681c(void);


asm u32 native_ov000_0220819c (register u32 a0)
{
    stmdb sp!, {r4, lr}
    sub sp, sp, #8
    ldr r0, =native_data_0222f728
    mov r1, #2
    bl native_fn_0203cc2c
    mov r4, r0
    add r0, sp, #0
    mov r1, r4
    mov r2, #0
    bl native_fn_0204518c
    ldr r0, [sp]
    ldr r2, [sp, #0x4]
    mov r1, #0
    bl native_fn_0204820c
    mov r1, r4
    mov r0, #2
    bl native_fn_0202a498
    bl native_fn_02048308
    bl native_fn_022081f8
    bl native_fn_0220681c
    add sp, sp, #8
    ldmia sp!, {r4, pc}
}
