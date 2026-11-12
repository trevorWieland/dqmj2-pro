/* ov000 row 0x0220f018: 216 bytes.
 *
 * What it does: 54 instructions; 9 call(s) to 0x02041f74, 0x02042c2c, 0x02212d54, +6 more; loops (back edge at +0x14); returns through pop {r3, r4, r5, r6, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x20 -> +0x64
 *   branch +0x60 -> +0xcc
 *   branch +0x68 -> +0xcc
 *   branch +0x80 -> +0xcc
 *   test +0x1c cmp r0, #5
 *   test +0x64 cmp r0, #4
 *   test +0x7c cmp r4, #0
 *   0 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0220f018; the literal pool and
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

extern void native_fn_02041f74(void);
extern void native_fn_02042c2c(void);
extern void native_fn_02212d54(void);
extern void native_fn_021e7b9c(void);
extern void native_fn_0220ef3c(void);


asm u32 native_ov000_0220f018 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, lr}
    sub sp, sp, #28
    add r1, sp, #16
    mov r6, r0
    mov r5, #0
    bl native_fn_02041f74
    ldrb r0, [r6, #0x2c3]
    cmp r0, #5
    bne ov000_0220f018_L64
    mov r0, r6
    bl native_fn_02042c2c
    str r0, [sp]
    mov r0, #5
    str r0, [sp, #0x4]
    mov r1, r5
    str r1, [sp, #0x8]
    str r1, [sp, #0xc]
    ldr r1, [sp, #0x10]
    ldr r2, [sp, #0x14]
    ldr r3, [sp, #0x18]
    bl native_fn_02212d54
    mov r5, r0
    mov r0, #195
    bl native_fn_021e7b9c
    b ov000_0220f018_Lcc
ov000_0220f018_L64:
    cmp r0, #4
    bne ov000_0220f018_Lcc
    add r0, r6, #512
    ldrsh r0, [r0, #118]
    bl native_fn_0220ef3c
    mov r4, r0
    cmp r4, #0
    ble ov000_0220f018_Lcc
    mov r0, r6
    bl native_fn_02042c2c
    str r0, [sp]
    mov r1, #5
    mov r0, r4, lsl #16
    str r1, [sp, #0x4]
    mov r1, r5
    str r1, [sp, #0x8]
    mov r0, r0, asr #16
    str r0, [sp, #0xc]
    ldr r1, [sp, #0x10]
    ldr r2, [sp, #0x14]
    ldr r3, [sp, #0x18]
    mov r0, #4
    bl native_fn_02212d54
    mov r5, r0
    mov r0, #194
    bl native_fn_021e7b9c
ov000_0220f018_Lcc:
    mov r0, r5
    add sp, sp, #28
    ldmia sp!, {r3, r4, r5, r6, pc}
}
