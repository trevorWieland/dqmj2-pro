/* ov001 row 0x021fec1c: 96 bytes.
 *
 * What it does: 23 instructions; 1 call(s) to 0x0204aeb4; loops (back edge at +0x50); returns through pop {r3, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 1 call (23 instructions, 1 call, 0 branches, 1 back edge, 1 literal slot).
 *
 *   pool +0x5c -> constant 0x02239c10 (image word 0x02239c10)
 *   test +0x10 cmp r1, #12
 *   test +0x24 cmp r0, #0
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021fec1c; the literal pool and
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

extern void native_fn_0204aeb4(void);


asm u32 native_ov001_021fec1c (register u32 a0)
{
    stmdb sp!, {r3, lr}
    sub sp, sp, #16
    ldr r1, =0x02239c10
    ldrb r1, [r1, #0xa]
    cmp r1, #12
    addhs sp, sp, #16
    ldmhsia sp!, {r3, pc}
    mov r1, #0
    str r1, [sp]
    cmp r0, #0
    str r1, [sp, #0x4]
    mov r0, #21
    str r0, [sp, #0x8]
    str r1, [sp, #0xc]
    ldr r0, =0x02239c10
    moveq r3, #1
    ldr r0, [r0, #0x48]
    movne r3, #0
    mov r1, #1
    mov r2, #3
    bl native_fn_0204aeb4
    add sp, sp, #16
    ldmia sp!, {r3, pc}
}
