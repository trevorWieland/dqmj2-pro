/* ov000 row 0x0222ab60: 148 bytes.
 *
 * What it does: 33 instructions; 5 call(s) to 0x0222b4ec, 0x020c49e8, 0x0222b38c, +2 more; loops (back edge at +0x10); returns through pop {r4, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x84 -> constant 0x022475fc (image word 0x022475fc)
 *   pool +0x88 -> constant 0x022475ec (image word 0x022475ec)
 *   pool +0x8c -> constant 0x022475d4 (image word 0x022475d4)
 *   pool +0x90 -> constant 0x022475dc (image word 0x022475dc)
 *   test +0x1c cmp r0, #0
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0222ab60; the literal pool and
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

extern void native_fn_0222b4ec(void);
extern void native_fn_020c49e8(void);
extern void native_fn_0222b38c(void);
extern void native_fn_0222b3ec(void);
extern void native_fn_02063b18(void);


asm u32 native_ov000_0222ab60 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    sub sp, sp, #8
    ldr r4, =0x022475fc
    bl native_fn_0222b4ec
    bl native_fn_020c49e8
    ldr r0, =0x022475ec
    ldrsb r0, [r0, #32]
    cmp r0, #0
    addne sp, sp, #8
    ldmneia sp!, {r4, pc}
    mov r0, #11
    bl native_fn_0222b38c
    mov r0, #4
    str r0, [sp]
    mov r1, #23
    ldr r0, =0x022475d4
    str r1, [sp, #0x4]
    ldrb r1, [r0]
    ldr r2, =0x022475dc
    mov r0, r4
    mov r3, #1
    bl native_fn_0222b3ec
    mov r0, #46
    bl native_fn_02063b18
    ldr r1, =0x022475d4
    ldrb r1, [r1]
    sub r0, r1, r0
    subs r0, r0, #2
    str r0, [r4]
    movmi r0, #0
    strmi r0, [r4]
    add sp, sp, #8
    ldmia sp!, {r4, pc}
}
