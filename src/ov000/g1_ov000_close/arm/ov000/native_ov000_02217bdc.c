/* ov000 row 0x02217bdc: 140 bytes.
 *
 * What it does: 33 instructions; 4 call(s) to 0x02048f7c, 0x02049af0, 0x02048f7c, +1 more; loops (back edge at +0x1c); returns through pop {r4, r5, r6, r7, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x84 -> constant 0x0224535c (image word 0x0224535c)
 *   pool +0x88 -> constant 0x0224532c (image word 0x0224532c)
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02217bdc; the literal pool and
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

extern void native_fn_02048f7c(void);
extern void native_fn_02049af0(void);
extern void native_fn_02049ae4(void);


asm u32 native_ov000_02217bdc (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, lr}
    sub sp, sp, #12
    mov r7, r0
    mov r0, #1
    mov r6, r1
    mov r5, r2
    mov r4, r3
    bl native_fn_02048f7c
    ldr r2, =0x0224535c
    ldr r1, [sp, #0x20]
    ldr r3, [r2, r0, lsl #2]
    mov r0, r7
    str r4, [sp]
    ldr r4, [sp, #0x24]
    str r1, [sp, #0x4]
    mov r1, r6
    mov r2, r5
    mov r3, r3, asr #5
    str r4, [sp, #0x8]
    bl native_fn_02049af0
    mov r4, r0
    mov r0, #1
    bl native_fn_02048f7c
    ldr r3, =0x0224535c
    mov r12, r4, lsl #5
    ldr r1, =0x0224532c
    mov r2, #0
    str r12, [r3, r0, lsl #2]
    str r2, [r1, #0x2c]
    bl native_fn_02049ae4
    ldr r0, [r0, #0x4]
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, pc}
}
