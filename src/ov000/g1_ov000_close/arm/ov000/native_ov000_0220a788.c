/* ov000 row 0x0220a788: 108 bytes.
 *
 * What it does: 27 instructions; 5 call(s) to 0x020c56b4, 0x02209c68, 0x02042c0c, +2 more; loops (back edge at +0x10); returns through pop {r4, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x20 -> +0x38
 *   test +0x18 cmp r0, #3
 *   test +0x1c cmpne r0, #6
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0220a788; the literal pool and
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
extern void native_fn_02209c68(void);
extern void native_fn_02042c0c(void);
extern void native_fn_0221089c(void);


asm u32 native_ov000_0220a788 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r4, r0
    add r0, r4, #512
    ldrsh r0, [r0, #118]
    bl native_fn_020c56b4
    ldrb r0, [r0, #0x7]
    cmp r0, #3
    cmpne r0, #6
    bne ov000_0220a788_L38
    mov r0, r4
    mov r1, #3
    bl native_fn_02209c68
    mov r0, #1
    ldmia sp!, {r4, pc}
ov000_0220a788_L38:
    mov r1, #31
    add r2, r4, #512
    mov r0, r4
    strh r1, [r2, #122]
    bl native_fn_02042c0c
    mov r0, r4
    mov r1, #1
    bl native_fn_0221089c
    mov r0, r4
    mov r1, #3
    bl native_fn_02209c68
    mov r0, #1
    ldmia sp!, {r4, pc}
}
