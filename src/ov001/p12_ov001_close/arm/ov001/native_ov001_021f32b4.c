/* ov001 row 0x021f32b4: 444 bytes.
 *
 * What it does: 109 instructions; 14 call(s) to 0x0207afec, 0x0205d790, 0x021f335c, +11 more; loops (back edge at +0x14); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 14 calls (109 instructions, 14 calls, 11 branches, 12 back edges, 2 literal slots).
 *
 *   pool +0x1b4 -> constant 0x0223989c (image word 0x0223989c)
 *   pool +0x1b8 -> constant 0x66666667 (image word 0x66666667)
 *   branch +0x38 -> +0x64
 *   branch +0x48 -> +0x64
 *   branch +0x54 -> +0xf0
 *   branch +0x60 -> +0xf0
 *   branch +0x68 -> +0xf0
 *   branch +0x80 -> +0xf0
 *   branch +0x88 -> +0xa8
 *   branch +0xa4 -> +0x1a8
 *   branch +0xec -> +0x1a8
 *   branch +0xf8 -> +0x15c
 *   branch +0x118 -> +0x130
 *   branch +0x12c -> +0x148
 *   back edge +0x154 -> +0x10c
 *   branch +0x158 -> +0x1a8
 *   test +0x44 cmp r1, #0
 *   test +0x50 cmp r1, #0
 *   test +0x5c cmp r0, #0
 *   test +0x64 cmp r9, #182
 *   test +0x78 cmp r0, #7
 *   test +0x7c cmpne r0, #9
 *   test +0x84 cmp r5, #0
 *   test +0xf0 cmp r5, #0
 *   test +0x114 cmp r0, #0
 *   test +0x128 cmp r0, #0
 *   test +0x14c cmp r7, #3
 *   test +0x15c cmp r0, #0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f32b4; the literal pool and
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

extern void native_fn_0207afec(void);
extern void native_fn_0205d790(void);
extern void native_fn_021eec7c(void);
extern void native_fn_02041f74(void);
extern void native_fn_021eedbc(void);
extern void native_fn_021db438(void);
extern void native_fn_021db8d0(void);
extern void native_fn_021f307c(void);
extern void native_fn_021d8b4c(void);


asm u32 native_ov001_021f32b4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    sub sp, sp, #16
    mov r9, r0
    mov r8, r1
    mvn r6, #0
    bl native_fn_0207afec
    mov r7, r0
    ldrsh r4, [r7, #12]
    mov r0, r4
    bl native_fn_0205d790
    ldrh r1, [r7, #8]
    mov r5, r0
    mov r0, r1, lsl #16
    movs r0, r0, lsr #28
    beq ov001_021f32b4_L64
    ldr r0, =0x0223989c
    ldrb r1, [r0, #0x8]
    cmp r1, #0
    bne ov001_021f32b4_L64
    ldrb r1, [r0, #0x10]
    cmp r1, #0
    beq ov001_021f32b4_Lf0
    ldrb r0, [r0, #0x30]
    cmp r0, #0
    bne ov001_021f32b4_Lf0
ov001_021f32b4_L64:
    cmp r9, #182
    beq ov001_021f32b4_Lf0
    ldrh r0, [r7, #8]
    mov r0, r0, lsl #20
    mov r0, r0, lsr #28
    cmp r0, #7
    cmpne r0, #9
    beq ov001_021f32b4_Lf0
    cmp r5, #0
    blt ov001_021f32b4_La8
    mov r0, r4
    mov r1, r8
    mov r2, r5
    bl native_fn_021eec7c
    mov r0, r0, lsl #24
    mov r6, r0, asr #24
    b ov001_021f32b4_L1a8
ov001_021f32b4_La8:
    add r1, sp, #4
    mov r0, r8
    bl native_fn_02041f74
    ldrb r1, [r8, #0x31e]
    ldr r5, =0x66666667
    mov r0, r4
    str r1, [sp]
    ldr r2, [sp, #0xc]
    ldr r1, [sp, #0x4]
    mov r4, r2, lsl #3
    smull r2, r3, r5, r4
    mov r4, r4, lsr #31
    ldr r2, [sp, #0x8]
    add r3, r4, r3, asr #2
    bl native_fn_021eedbc
    mov r0, r0, lsl #24
    mov r6, r0, asr #24
    b ov001_021f32b4_L1a8
ov001_021f32b4_Lf0:
    cmp r5, #0
    ldrb r0, [r8, #0x31e]
    blt ov001_021f32b4_L15c
    mov r1, #0
    bl native_fn_021db438
    mov r8, r0
    mov r7, #0
ov001_021f32b4_L10c:
    mov r0, r8
    bl native_fn_021db8d0
    cmp r0, #0
    bne ov001_021f32b4_L130
    mov r0, r8
    mov r1, r9
    bl native_fn_021f307c
    cmp r0, #0
    beq ov001_021f32b4_L148
ov001_021f32b4_L130:
    mov r0, r4
    mov r1, r8
    mov r2, r5
    bl native_fn_021eec7c
    mov r0, r0, lsl #24
    mov r6, r0, asr #24
ov001_021f32b4_L148:
    add r7, r7, #1
    cmp r7, #3
    add r8, r8, #1088
    blt ov001_021f32b4_L10c
    b ov001_021f32b4_L1a8
ov001_021f32b4_L15c:
    cmp r0, #0
    moveq r0, #3
    movne r0, #11
    add r1, sp, #4
    bl native_fn_021d8b4c
    ldrb r1, [r8, #0x31e]
    ldr r5, =0x66666667
    mov r0, r4
    str r1, [sp]
    ldr r2, [sp, #0xc]
    ldr r1, [sp, #0x4]
    mov r4, r2, lsl #3
    smull r2, r3, r5, r4
    mov r4, r4, lsr #31
    ldr r2, [sp, #0x8]
    add r3, r4, r3, asr #2
    bl native_fn_021eedbc
    mov r0, r0, lsl #24
    mov r6, r0, asr #24
ov001_021f32b4_L1a8:
    mov r0, r6
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
