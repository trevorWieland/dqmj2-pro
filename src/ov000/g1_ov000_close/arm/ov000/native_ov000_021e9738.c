/* ov000 row 0x021e9738: 92 bytes.
 *
 * What it does: 23 instructions; 3 call(s) to 0x021e78e0, 0x021e7914, 0x021e970c; loops (back edge at +0x20); returns through pop {r4, r5, r6, r7, pc}
 *
 * Decoded shape: block fill.
 *
 *   branch +0x28 -> +0x50
 *   test +0x24 cmp r0, #0
 *   1 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e9738; the literal pool and
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

extern void native_fn_021e78e0(void);
extern void native_fn_021e7914(void);
extern void native_fn_021e970c(void);


asm u32 native_ov000_021e9738 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, lr}
    sub sp, sp, #20
    mov r6, r1
    mov r7, r0
    add r1, sp, #8
    mov r0, r6
    mov r5, r2
    mvn r4, #0
    bl native_fn_021e78e0
    cmp r0, #0
    beq ov000_021e9738_L50
    mov r0, r6
    bl native_fn_021e7914
    stmia sp, {r0, r5}
    ldr r1, [sp, #0x8]
    ldr r2, [sp, #0xc]
    ldr r3, [sp, #0x10]
    mov r0, r7
    bl native_fn_021e970c
    mov r4, r0
ov000_021e9738_L50:
    mov r0, r4
    add sp, sp, #20
    ldmia sp!, {r4, r5, r6, r7, pc}
}
