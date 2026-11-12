/* ov000 row 0x02208b8c: 96 bytes.
 *
 * What it does: 22 instructions; 6 call(s) to 0x0205be34, 0x0205bf7c, 0x0205bfac, +3 more; loops (back edge at +0x0c); 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x58 -> constant 0xfffeb266 (image word 0xfffeb266)
 *   pool +0x5c -> constant 0xfffff4a4 (image word 0xfffff4a4)
 *   2 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02208b8c; the literal pool and
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

extern void native_fn_0205be34(void);
extern void native_fn_0205bf7c(void);
extern void native_fn_0205bfac(void);
extern void native_fn_0205be74(void);
extern void native_fn_0205bea4(void);
extern void native_fn_0205bf2c(void);


asm u32 native_ov000_02208b8c (register u32 a0)
{
    stmdb sp!, {lr}
    sub sp, sp, #12
    mov r0, #89
    bl native_fn_0205be34
    mov r0, #0
    bl native_fn_0205bf7c
    mov r0, #0
    bl native_fn_0205bfac
    ldr r3, =0xfffeb266
    ldr r1, =0xfffff4a4
    mov r2, #0
    add r0, sp, #0
    str r3, [sp]
    str r2, [sp, #0x4]
    str r1, [sp, #0x8]
    bl native_fn_0205be74
    mov r0, #368640
    bl native_fn_0205bea4
    mov r0, #1
    bl native_fn_0205bf2c
    add sp, sp, #12
    ldmia sp!, {pc}
}
