/* ov000 row 0x021f8c20: 100 bytes.
 *
 * What it does: 24 instructions; 3 call(s) to 0x0204b85c, 0x0205f98c, 0x0204b178; loops (back edge at +0x38); returns through pop {r4, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x60 -> constant 0x02236f74 (image word 0x02236f74)
 *   0 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f8c20; the literal pool and
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

extern void native_fn_0204b85c(void);
extern void native_fn_0205f98c(void);
extern void native_fn_0204b178(void);


asm u32 native_ov000_021f8c20 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    sub sp, sp, #16
    add r1, sp, #12
    mov r0, #0
    strh r0, [r1]
    strh r0, [r1, #2]
    mov r3, #1
    ldr r4, =0x02236f74
    str r3, [sp]
    mov r0, #29
    str r0, [sp, #0x4]
    mov r2, #5
    mov r0, r4
    str r2, [sp, #0x8]
    bl native_fn_0204b85c
    mov r1, #0
    ldr r0, [r4, #0x1c]
    str r1, [r4, #0x10]
    str r1, [r4, #0x2c]
    bl native_fn_0205f98c
    mov r1, #29
    bl native_fn_0204b178
    add sp, sp, #16
    ldmia sp!, {r4, pc}
}
