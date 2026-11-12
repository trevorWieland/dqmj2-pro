/* ov000 row 0x0220b94c: 220 bytes.
 *
 * What it does: Copies a 3-register block to an optional destination under a condition in 2 predicated moves.
 *
 * Decoded shape: predicated block copy.
 *
 *   branch +0x2c -> +0x84
 *   branch +0x68 -> +0x7c
 *   branch +0x78 -> +0x84
 *   back edge +0x80 -> +0x1c
 *   test +0x28 cmp r0, #0
 *   test +0x70 cmp r5, #16
 *   test +0x84 cmp r5, #0
 *   1 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0220b94c; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_021e6040(void);
extern void native_fn_0203d294(void);
extern void native_fn_021e60a8(void);


asm u32 native_ov000_0220b94c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, lr}
    sub sp, sp, #28
    mov r5, #0
    mov r7, r0
    add r6, sp, #12
    mov r0, r5
    add r4, sp, #0
ov000_0220b94c_L1c:
    ldrb r2, [r7, #0x2c0]
    mov r1, r4
    bl native_fn_021e6040
    cmp r0, #0
    blt ov000_0220b94c_L84
    ldr r3, [r7, #0x2a8]
    ldr r2, [sp]
    ldr r1, [r7, #0x2b8]
    sub r2, r3, r2
    smull r12, r3, r2, r2
    ldr r8, [r7, #0x2b0]
    ldr lr, [sp, #0x8]
    mov r2, r1, asr #31
    sub r8, r8, lr
    smlal r12, r3, r8, r8
    mov r12, r12, lsr #12
    orr r12, r12, r3, lsl #20
    subs r1, r12, r1
    rscs r1, r2, r3, asr #12
    bge ov000_0220b94c_L7c
    add r5, r5, #1
    cmp r5, #16
    strb r0, [r6], #1
    bge ov000_0220b94c_L84
ov000_0220b94c_L7c:
    add r0, r0, #1
    b ov000_0220b94c_L1c
ov000_0220b94c_L84:
    cmp r5, #0
    addle r0, r7, #680
    addle r3, r7, #112
    ldmleia r0, {r0, r1, r2}
    addle sp, sp, #28
    stmleia r3, {r0, r1, r2}
    ldmleia sp!, {r3, r4, r5, r6, r7, r8, pc}
    mov r0, r5
    bl native_fn_0203d294
    add r2, sp, #12
    ldrb r0, [r2, r0]
    add r1, sp, #0
    bl native_fn_021e60a8
    add r4, sp, #0
    add r3, r7, #112
    ldmia r4, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    ldmia r4, {r0, r1, r2}
    add r3, r7, #272
    stmia r3, {r0, r1, r2}
    add sp, sp, #28
    ldmia sp!, {r3, r4, r5, r6, r7, r8, pc}
}
