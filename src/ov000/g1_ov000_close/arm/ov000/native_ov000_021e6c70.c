/* ov000 row 0x021e6c70: 96 bytes.
 *
 * What it does: 24 instructions; 4 call(s) to 0x021e63a4, 0x021e63c8, 0x0202859c, +1 more; loops (back edge at +0x18); returns through pop {r3, r4, r5, r6, r7, r8, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e6c70; the literal pool and
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

extern void native_fn_021e63a4(void);
extern void native_fn_021e63c8(void);
extern void native_fn_0202859c(void);
extern void native_fn_021e6c3c(void);


asm u32 native_ov000_021e6c70 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, lr}
    sub sp, sp, #12
    mov r4, r0
    mov r8, r1
    mov r7, r2
    mov r6, r3
    bl native_fn_021e63a4
    mov r5, r0
    mov r0, r4
    bl native_fn_021e63c8
    mov r4, r0
    mov r0, r5
    mov r1, #0
    bl native_fn_0202859c
    mov r1, r0
    ldr r3, [sp, #0x28]
    add r0, r4, #76
    add r2, sp, #0
    str r8, [sp]
    str r7, [sp, #0x4]
    str r6, [sp, #0x8]
    bl native_fn_021e6c3c
    add sp, sp, #12
    ldmia sp!, {r3, r4, r5, r6, r7, r8, pc}
}
