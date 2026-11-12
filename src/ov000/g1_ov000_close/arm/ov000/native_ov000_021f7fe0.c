/* ov000 row 0x021f7fe0: 100 bytes.
 *
 * What it does: 24 instructions; 4 call(s) to 0x02062aa0, 0x02062a50, 0x0206c88c, +1 more; loops (back edge at +0x04); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x60 -> constant 0x02236f28 (image word 0x02236f28)
 *   back edge +0x58 -> +0x28
 *   test +0x10 cmp r7, #0
 *   test +0x50 cmp r8, r7
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f7fe0; the literal pool and
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

extern void native_fn_02062aa0(void);
extern void native_fn_02062a50(void);
extern void native_fn_0206c88c(void);


asm u32 native_ov000_021f7fe0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    bl native_fn_02062aa0
    mov r7, r0
    mov r8, #0
    cmp r7, #0
    ldmleia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
    ldr r9, =0x02236f28
    mov r6, #2
    mov r5, #1
    mov r4, #32
ov000_021f7fe0_L28:
    mov r0, r8
    bl native_fn_02062a50
    mov r1, r0
    str r6, [sp]
    ldrsh r0, [r1, #24]
    ldrb r1, [r1, #0x1a]
    mov r2, r5
    mov r3, r4
    bl native_fn_0206c88c
    add r8, r8, #1
    cmp r8, r7
    strb r0, [r9], #1
    blt ov000_021f7fe0_L28
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
