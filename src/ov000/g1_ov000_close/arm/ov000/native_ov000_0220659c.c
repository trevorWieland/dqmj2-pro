/* ov000 row 0x0220659c: 240 bytes.
 *
 * What it does: 58 instructions; 11 call(s) to 0x0203cc2c, 0x0204518c, 0x0204820c, +8 more; loops (back edge at +0x30); returns through pop {r3, r4, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xe8 -> native_data_0222f610 (image word 0x0222f610)
 *   pool +0xec -> constant 0x02238248 (image word 0x02238248)
 *   back edge +0x30 -> +0x18
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0220659c; the literal pool and
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

extern u8 native_data_0222f610[];
extern void native_fn_0203cc2c(void);
extern void native_fn_0204518c(void);
extern void native_fn_0204820c(void);
extern void native_fn_02048308(void);
extern void native_fn_02045490(void);
extern void native_fn_0202a37c(void);
extern void native_fn_02008e0c(void);
extern void native_fn_0202a498(void);


asm u32 native_ov000_0220659c (register u32 a0)
{
    stmdb sp!, {r3, r4, lr}
    sub sp, sp, #44
    mov r2, #0
    add r1, sp, #12
    strh r2, [sp]
    mov r0, #8
ov000_0220659c_L18:
    strb r2, [r1]
    strb r2, [r1, #0x1]
    strb r2, [r1, #0x2]
    strb r2, [r1, #0x3]
    add r1, r1, #4
    subs r0, r0, #1
    bne ov000_0220659c_L18
    ldr r0, =native_data_0222f610
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
    bl native_fn_02048308
    add r0, sp, #4
    mov r1, r4
    mov r2, #1
    bl native_fn_0204518c
    ldr r1, [sp, #0x4]
    ldr r3, [sp, #0x8]
    mov r0, #1
    mov r2, #0
    bl native_fn_02045490
    add r0, sp, #4
    mov r1, r4
    mov r2, #2
    bl native_fn_0204518c
    mov r0, #2
    mov r1, #2048
    mov r2, #4
    bl native_fn_0202a37c
    mov r1, r0
    ldr r2, =0x02238248
    ldr r0, [sp, #0x4]
    str r1, [r2, #0x8]
    ldr r2, [sp, #0x8]
    bl native_fn_02008e0c
    mov r1, r4
    mov r0, #2
    bl native_fn_0202a498
    add sp, sp, #44
    ldmia sp!, {r3, r4, pc}
}
