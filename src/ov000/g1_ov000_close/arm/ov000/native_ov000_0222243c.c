/* ov000 row 0x0222243c: 192 bytes.
 *
 * What it does: 47 instructions; 10 call(s) to 0x0203cc2c, 0x0204518c, 0x02045490, +7 more; loops (back edge at +0x1c); returns through pop {r4, r5, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xbc -> native_data_0222fc14 (image word 0x0222fc14)
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0222243c; the literal pool and
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

extern u8 native_data_0222fc14[];
extern void native_fn_0203cc2c(void);
extern void native_fn_0204518c(void);
extern void native_fn_02045490(void);
extern void native_fn_02045994(void);
extern void native_fn_0204820c(void);
extern void native_fn_02048308(void);
extern void native_fn_0202a498(void);


asm u32 native_ov000_0222243c (register u32 a0)
{
    stmdb sp!, {r4, r5, lr}
    sub sp, sp, #12
    mov r5, r0
    mov r2, #0
    ldr r0, =native_data_0222fc14
    mov r1, #2
    strh r2, [sp]
    bl native_fn_0203cc2c
    mov r4, r0
    add r0, sp, #4
    mov r1, r4
    mov r2, #1
    bl native_fn_0204518c
    ldr r1, [sp, #0x4]
    ldr r3, [sp, #0x8]
    mov r0, #1
    mov r2, #0
    bl native_fn_02045490
    ldr r1, [sp, #0x8]
    add r0, sp, #4
    str r1, [r5, #0x4]
    mov r1, r4
    mov r2, #8
    bl native_fn_0204518c
    ldr r1, [sp, #0x4]
    mov r0, #1
    mov r2, #0
    mov r3, #2048
    bl native_fn_02045994
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
    bl native_fn_02048308
    mov r1, r4
    mov r0, #2
    bl native_fn_0202a498
    add sp, sp, #12
    ldmia sp!, {r4, r5, pc}
}
