/* ov000 row 0x0220a6e8: 160 bytes.
 *
 * What it does: 40 instructions; 7 call(s) to 0x020c56b4, 0x02209c68, 0x02042c0c, +4 more; loops (back edge at +0x14); returns through pop {r3, r4, r5, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x24 -> +0x3c
 *   branch +0x38 -> +0x98
 *   branch +0x68 -> +0x98
 *   test +0x1c cmp r0, #3
 *   test +0x20 cmpne r0, #6
 *   test +0x64 cmp r0, #31
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0220a6e8; the literal pool and
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


asm u32 native_ov000_0220a6e8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    add r0, r5, #512
    ldrsh r0, [r0, #118]
    mov r4, #0
    bl native_fn_020c56b4
    ldrb r0, [r0, #0x7]
    cmp r0, #3
    cmpne r0, #6
    bne ov000_0220a6e8_L3c
    mov r0, r5
    mov r1, #3
    bl native_fn_02209c68
    mov r4, #1
    b ov000_0220a6e8_L98
ov000_0220a6e8_L3c:
    add r1, r5, #512
    ldrsh r2, [r1, #122]
    mov r0, r5
    add r2, r2, #1
    strh r2, [r1, #122]
    ldrsh r1, [r1, #122]
    and r1, r1, #255
    bl native_fn_02042c0c
    add r2, r5, #512
    ldrsh r0, [r2, #122]
    cmp r0, #31
    blt ov000_0220a6e8_L98
    mov r1, #31
    mov r0, r5
    strh r1, [r2, #122]
    bl native_fn_02042c0c
    mov r0, r5
    mov r1, #1
    bl native_fn_0221089c
    mov r0, r5
    mov r1, #3
    bl native_fn_02209c68
    mov r4, #1
ov000_0220a6e8_L98:
    mov r0, r4
    ldmia sp!, {r3, r4, r5, pc}
}
