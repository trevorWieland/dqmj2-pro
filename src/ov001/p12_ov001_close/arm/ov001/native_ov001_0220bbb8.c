/* ov001 row 0x0220bbb8: 376 bytes.
 *
 * What it does: 93 instructions; 17 call(s) to 0x0220b770, 0x0220b74c, 0x0220b794, +14 more; loops (back edge at +0x10); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 17 calls (93 instructions, 17 calls, 6 branches, 15 back edges, 1 literal slot).
 *
 *   pool +0x174 -> constant 0x66666667 (image word 0x66666667)
 *   branch +0x38 -> +0xb4
 *   branch +0x50 -> +0x70
 *   branch +0x6c -> +0x168
 *   branch +0xb0 -> +0x168
 *   branch +0xb8 -> +0x120
 *   branch +0xdc -> +0xf4
 *   branch +0xf0 -> +0x10c
 *   back edge +0x118 -> +0xd0
 *   branch +0x11c -> +0x168
 *   test +0x34 cmp r6, #4
 *   test +0x4c cmp r4, #0
 *   test +0xb4 cmp r4, #0
 *   test +0xd8 cmp r0, #0
 *   test +0xec cmp r0, #0
 *   test +0x110 cmp r6, #3
 *   test +0x120 cmp r8, #0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0220bbb8; the literal pool and
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

extern void native_fn_0220b770(void);
extern void native_fn_0220b74c(void);
extern void native_fn_0220b794(void);
extern void native_fn_0205d790(void);
extern void native_fn_021db438(void);
extern void native_fn_021eec7c(void);
extern void native_fn_02041f74(void);
extern void native_fn_021eedbc(void);
extern void native_fn_021db8d0(void);
extern void native_fn_0220bb7c(void);
extern void native_fn_021d8b4c(void);


asm u32 native_ov001_0220bbb8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    sub sp, sp, #16
    mov r5, r0
    mvn r9, #0
    bl native_fn_0220b770
    mov r7, r0
    bl native_fn_0220b74c
    mov r8, r0
    bl native_fn_0220b794
    mov r6, r0
    mov r0, r5
    bl native_fn_0205d790
    mov r4, r0
    cmp r6, #4
    beq ov001_0220bbb8_Lb4
    mov r0, r8
    mov r1, r6
    bl native_fn_021db438
    mov r6, r0
    cmp r4, #0
    blt ov001_0220bbb8_L70
    mov r0, r5
    mov r1, r6
    mov r2, r4
    bl native_fn_021eec7c
    mov r0, r0, lsl #24
    mov r9, r0, asr #24
    b ov001_0220bbb8_L168
ov001_0220bbb8_L70:
    add r1, sp, #4
    bl native_fn_02041f74
    ldrb r1, [r6, #0x31e]
    ldr r4, =0x66666667
    mov r0, r5
    str r1, [sp]
    ldr r2, [sp, #0xc]
    ldr r1, [sp, #0x4]
    mov r5, r2, lsl #3
    smull r2, r3, r4, r5
    mov r4, r5, lsr #31
    ldr r2, [sp, #0x8]
    add r3, r4, r3, asr #2
    bl native_fn_021eedbc
    mov r0, r0, lsl #24
    mov r9, r0, asr #24
    b ov001_0220bbb8_L168
ov001_0220bbb8_Lb4:
    cmp r4, #0
    blt ov001_0220bbb8_L120
    mov r0, r8
    mov r1, #0
    bl native_fn_021db438
    mov r8, r0
    mov r6, #0
ov001_0220bbb8_Ld0:
    mov r0, r8
    bl native_fn_021db8d0
    cmp r0, #0
    bne ov001_0220bbb8_Lf4
    mov r0, r8
    mov r1, r7
    bl native_fn_0220bb7c
    cmp r0, #0
    beq ov001_0220bbb8_L10c
ov001_0220bbb8_Lf4:
    mov r0, r5
    mov r1, r8
    mov r2, r4
    bl native_fn_021eec7c
    mov r0, r0, lsl #24
    mov r9, r0, asr #24
ov001_0220bbb8_L10c:
    add r6, r6, #1
    cmp r6, #3
    add r8, r8, #1088
    blt ov001_0220bbb8_Ld0
    b ov001_0220bbb8_L168
ov001_0220bbb8_L120:
    cmp r8, #0
    moveq r0, #3
    movne r0, #11
    add r1, sp, #4
    bl native_fn_021d8b4c
    str r8, [sp]
    ldr r0, [sp, #0xc]
    ldr r1, =0x66666667
    mov r2, r0, lsl #3
    smull r0, r3, r1, r2
    mov r4, r2, lsr #31
    ldr r1, [sp, #0x4]
    ldr r2, [sp, #0x8]
    mov r0, r5
    add r3, r4, r3, asr #2
    bl native_fn_021eedbc
    mov r0, r0, lsl #24
    mov r9, r0, asr #24
ov001_0220bbb8_L168:
    mov r0, r9
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
