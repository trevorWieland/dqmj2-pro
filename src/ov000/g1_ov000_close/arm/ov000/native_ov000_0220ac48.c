/* ov000 row 0x0220ac48: 296 bytes.
 *
 * What it does: 74 instructions; 12 call(s) to 0x0203d294, 0x0203d294, 0x0220a2a4, +9 more; loops (back edge at +0x1c); returns through pop {r3, r4, r5, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x14 -> +0xdc
 *   branch +0x38 -> +0x68
 *   branch +0x48 -> +0x68
 *   branch +0x64 -> +0x98
 *   branch +0xa4 -> +0xb4
 *   branch +0xb0 -> +0xc8
 *   test +0x10 cmp r2, #0
 *   test +0x34 tst r0, #3
 *   test +0x44 cmp r0, #60
 *   test +0x9c cmp r4, #0
 *   test +0xdc cmp r2, #10
 *   test +0x118 cmp r0, #0
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0220ac48; the literal pool and
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

extern void native_fn_0203d294(void);
extern void native_fn_0220a2a4(void);
extern void native_fn_02026144(void);
extern void native_fn_020c56b4(void);
extern void native_fn_02042bfc(void);
extern void native_fn_02042c2c(void);
extern void native_fn_02028158(void);
extern void native_fn_02041f90(void);


asm u32 native_ov000_0220ac48 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    ldrb r2, [r5, #0x279]
    mov r4, r1
    cmp r2, #0
    bne ov000_0220ac48_Ldc
    mov r0, #60
    bl native_fn_0203d294
    add r2, r0, #30
    add r1, r5, #512
    mvn r0, #-2147483648
    strh r2, [r1, #122]
    bl native_fn_0203d294
    tst r0, #3
    bne ov000_0220ac48_L68
    add r0, r5, #512
    ldrsh r0, [r0, #122]
    cmp r0, #60
    bge ov000_0220ac48_L68
    mov r1, #0
    mov r0, r5
    mov r2, r1
    bl native_fn_0220a2a4
    mov r0, #0
    str r0, [r5, #0x27c]
    b ov000_0220ac48_L98
ov000_0220ac48_L68:
    mov r0, r5
    mov r1, #1
    mov r2, #0
    bl native_fn_0220a2a4
    mov r0, #360
    bl native_fn_0203d294
    add r1, r5, #512
    sub r0, r0, #180
    ldrsh r1, [r1, #122]
    mov r0, r0, lsl #12
    bl native_fn_02026144
    str r0, [r5, #0x27c]
ov000_0220ac48_L98:
    add r0, r5, #512
    cmp r4, #0
    ldrsh r0, [r0, #118]
    bne ov000_0220ac48_Lb4
    bl native_fn_020c56b4
    ldr r1, [r0, #0x14]
    b ov000_0220ac48_Lc8
ov000_0220ac48_Lb4:
    bl native_fn_020c56b4
    ldr r0, [r0, #0x14]
    add r0, r0, r0, lsl #1
    add r0, r0, r0, lsr #31
    mov r1, r0, asr #1
ov000_0220ac48_Lc8:
    mov r0, r5
    bl native_fn_02042bfc
    mov r0, #10
    strb r0, [r5, #0x279]
    ldmia sp!, {r3, r4, r5, pc}
ov000_0220ac48_Ldc:
    cmp r2, #10
    ldmneia sp!, {r3, r4, r5, pc}
    bl native_fn_02042c2c
    ldr r1, [r5, #0x27c]
    add r0, r0, r1
    bl native_fn_02028158
    mov r1, r0
    mov r0, r5
    mov r2, #0
    bl native_fn_02041f90
    add r0, r5, #512
    ldrsh r1, [r0, #122]
    sub r1, r1, #1
    strh r1, [r0, #122]
    ldrsh r0, [r0, #122]
    cmp r0, #0
    movle r0, #0
    strleb r0, [r5, #0x279]
    ldmia sp!, {r3, r4, r5, pc}
}
