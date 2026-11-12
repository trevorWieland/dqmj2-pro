/* ov000 row 0x0220fc60: 88 bytes.
 *
 * What it does: 22 instructions; 3 call(s) to 0x020c56b4, 0x02042c0c, 0x02209c68; loops (back edge at +0x14); returns through pop {r3, r4, r5, pc}
 *
 * Decoded shape: chunk loop.
 *
 *   branch +0x20 -> +0x50
 *   test +0x1c cmp r0, #4
 *   2 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0220fc60; the literal pool and
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

extern void native_fn_020c56b4(void);
extern void native_fn_02042c0c(void);
extern void native_fn_02209c68(void);


asm u32 native_ov000_0220fc60 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    add r0, r5, #512
    ldrsh r0, [r0, #118]
    mov r4, #0
    bl native_fn_020c56b4
    ldrb r0, [r0, #0x8]
    cmp r0, #4
    bne ov000_0220fc60_L50
    add r0, r5, #680
    add r3, r5, #112
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    mov r0, r5
    mov r1, r4
    bl native_fn_02042c0c
    mov r0, r5
    mov r1, #3
    bl native_fn_02209c68
    mov r4, #1
ov000_0220fc60_L50:
    mov r0, r4
    ldmia sp!, {r3, r4, r5, pc}
}
