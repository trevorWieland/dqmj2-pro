/* ov000 row 0x0220f858: 860 bytes.
 *
 * What it does: Copies a 5-register block to an optional destination under a condition in one predicated move.
 *
 * Decoded shape: predicated block copy.
 *
 *   pool +0x350 -> constant 0x88888889 (image word 0x88888889)
 *   pool +0x354 -> constant 0x41a00000 (image word 0x41a00000)
 *   pool +0x358 -> constant 0x45800000 (image word 0x45800000)
 *   branch +0x34 -> +0x84
 *   branch +0x8c -> +0x164
 *   branch +0xa8 -> +0xdc
 *   branch +0x104 -> +0x140
 *   branch +0x16c -> +0x21c
 *   branch +0x194 -> +0x1c0
 *   branch +0x1bc -> +0x1e0
 *   branch +0x208 -> +0x21c
 *   branch +0x224 -> +0x314
 *   branch +0x240 -> +0x270
 *   branch +0x298 -> +0x2c4
 *   branch +0x2c0 -> +0x2e4
 *   branch +0x32c -> +0x348
 *   test +0x10 cmp r0, #0
 *   test +0x20 cmp r0, #0
 *   test +0x30 cmp r0, #0
 *   test +0x88 cmp r0, #10
 *   test +0xa4 cmp r0, #0
 *   test +0x168 cmp r0, #20
 *   test +0x204 cmp r0, #0
 *   test +0x220 cmp r0, #30
 *   test +0x23c cmp r1, #0
 *   test +0x318 cmp r0, #40
 *   test +0x328 cmp r0, #50
 *   23 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0220f858; the literal pool and
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

extern void native_fn_0220a2a4(void);
extern void native_fn_020c56b4(void);
extern void native_fn_02042bfc(void);
extern void native_fn_0220f018(void);
extern void native_fn_0203d294(void);
extern void native_fn_02028158(void);
extern void native_fn_02042c2c(void);
extern void native_fn_02041f90(void);
extern void native_fn_02025a28(void);
extern void native_fn_02025578(void);
extern void native_fn_0202537c(void);
extern void native_fn_02025ab8(void);
extern void native_fn_02024e0c(void);
extern void native_fn_02025ca4(void);
extern void native_fn_020259b4(void);
extern void native_fn_02042c0c(void);
extern void native_fn_0221089c(void);


asm u32 native_ov000_0220f858 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r5, r0
    ldrb r0, [r5, #0x160]
    mov r4, #0
    cmp r0, #0
    moveq r0, #50
    streqb r0, [r5, #0x279]
    ldrb r0, [r5, #0x1e2]
    cmp r0, #0
    moveq r0, #0
    ldmeqia sp!, {r4, r5, r6, pc}
    ldrb r0, [r5, #0x279]
    cmp r0, #0
    bne ov000_0220f858_L84
    mov r0, r5
    mov r1, #2
    mov r2, #0
    bl native_fn_0220a2a4
    add r0, r5, #512
    ldrsh r0, [r0, #118]
    bl native_fn_020c56b4
    ldr r1, [r0, #0x18]
    mov r0, r5
    bl native_fn_02042bfc
    add r0, r5, #512
    mov r1, #120
    strh r1, [r0, #122]
    mov r0, #10
    strb r0, [r5, #0x279]
    ldrb r0, [r5, #0x2c2]
    bic r0, r0, #15
    orr r0, r0, #1
    strb r0, [r5, #0x2c2]
ov000_0220f858_L84:
    ldrb r0, [r5, #0x279]
    cmp r0, #10
    bne ov000_0220f858_L164
    add r3, r5, #512
    ldrsh r0, [r3, #122]
    sub r0, r0, #1
    strh r0, [r3, #122]
    ldrsh r0, [r3, #122]
    cmp r0, #0
    bgt ov000_0220f858_Ldc
    mov r0, #1
    mov r1, #0
    strb r0, [r5, #0x2c1]
    mov r12, #10
    mov r0, r5
    mov r2, r1
    strh r12, [r3, #122]
    mov r3, #20
    strb r3, [r5, #0x279]
    bl native_fn_0220a2a4
    mov r0, r5
    bl native_fn_0220f018
ov000_0220f858_Ldc:
    add r0, r5, #512
    ldrsh r3, [r0, #122]
    ldr r1, =0x88888889
    mov r2, #30
    smull r0, r12, r1, r3
    add r12, r3, r12
    mov r0, r3, lsr #31
    add r12, r0, r12, asr #4
    smull r0, r1, r2, r12
    subs r12, r3, r0
    bne ov000_0220f858_L140
    mov r0, #2
    bl native_fn_0203d294
    add r1, r0, #1
    mov r0, #180
    mul r0, r1, r0
    add r0, r0, #90
    mov r0, r0, lsl #12
    bl native_fn_02028158
    ldr r3, =0x88888889
    mov r1, r0, lsr #31
    smull r2, r12, r3, r0
    add r12, r0, r12
    add r12, r1, r12, asr #4
    str r12, [r5, #0x27c]
ov000_0220f858_L140:
    mov r0, r5
    bl native_fn_02042c2c
    ldr r1, [r5, #0x27c]
    add r0, r0, r1
    bl native_fn_02028158
    mov r1, r0
    mov r0, r5
    mov r2, #0
    bl native_fn_02041f90
ov000_0220f858_L164:
    ldrb r0, [r5, #0x279]
    cmp r0, #20
    bne ov000_0220f858_L21c
    add r0, r5, #512
    ldrsh r6, [r0, #122]
    mov r0, r6
    bl native_fn_02025a28
    ldr r1, =0x41a00000
    bl native_fn_02025578
    mov r1, #0
    bl native_fn_0202537c
    mov r0, r6
    bls ov000_0220f858_L1c0
    bl native_fn_02025a28
    ldr r1, =0x41a00000
    bl native_fn_02025578
    mov r1, r0
    ldr r0, =0x45800000
    bl native_fn_02025ab8
    mov r1, r0
    mov r0, #1056964608
    bl native_fn_02024e0c
    b ov000_0220f858_L1e0
ov000_0220f858_L1c0:
    bl native_fn_02025a28
    ldr r1, =0x41a00000
    bl native_fn_02025578
    mov r1, r0
    ldr r0, =0x45800000
    bl native_fn_02025ab8
    mov r1, #1056964608
    bl native_fn_02025ca4
ov000_0220f858_L1e0:
    bl native_fn_020259b4
    ldr r2, [r5, #0x74]
    add r1, r5, #512
    add r0, r2, r0
    str r0, [r5, #0x74]
    ldrsh r0, [r1, #122]
    sub r0, r0, #1
    strh r0, [r1, #122]
    ldrsh r0, [r1, #122]
    cmp r0, #0
    bgt ov000_0220f858_L21c
    mov r0, #31
    strh r0, [r1, #122]
    mov r0, #30
    strb r0, [r5, #0x279]
ov000_0220f858_L21c:
    ldrb r0, [r5, #0x279]
    cmp r0, #30
    bne ov000_0220f858_L314
    add r0, r5, #512
    ldrsh r1, [r0, #122]
    sub r1, r1, #1
    strh r1, [r0, #122]
    ldrsh r1, [r0, #122]
    cmp r1, #0
    bgt ov000_0220f858_L270
    mov r1, #0
    strb r1, [r5, #0x1e2]
    strh r1, [r0, #122]
    mov r0, #40
    strb r0, [r5, #0x279]
    strb r1, [r5, #0x2c1]
    ldr r0, [r5, #0x74]
    mov r4, #1
    add r0, r0, #205
    add r0, r0, #91136
    str r0, [r5, #0x74]
ov000_0220f858_L270:
    add r0, r5, #512
    ldrsh r0, [r0, #122]
    rsb r6, r0, #31
    mov r0, r6
    bl native_fn_02025a28
    ldr r1, =0x41a00000
    bl native_fn_02025578
    mov r1, #0
    bl native_fn_0202537c
    mov r0, r6
    bls ov000_0220f858_L2c4
    bl native_fn_02025a28
    ldr r1, =0x41a00000
    bl native_fn_02025578
    mov r1, r0
    ldr r0, =0x45800000
    bl native_fn_02025ab8
    mov r1, r0
    mov r0, #1056964608
    bl native_fn_02024e0c
    b ov000_0220f858_L2e4
ov000_0220f858_L2c4:
    bl native_fn_02025a28
    ldr r1, =0x41a00000
    bl native_fn_02025578
    mov r1, r0
    ldr r0, =0x45800000
    bl native_fn_02025ab8
    mov r1, #1056964608
    bl native_fn_02025ca4
ov000_0220f858_L2e4:
    bl native_fn_020259b4
    ldr r2, [r5, #0x74]
    add r1, r5, #512
    sub r0, r2, r0
    str r0, [r5, #0x74]
    ldrsh r1, [r1, #122]
    mov r0, r5
    and r1, r1, #255
    bl native_fn_02042c0c
    mov r0, r5
    mov r1, #0
    bl native_fn_0221089c
ov000_0220f858_L314:
    ldrb r0, [r5, #0x279]
    cmp r0, #40
    moveq r0, #50
    streqb r0, [r5, #0x279]
    ldrb r0, [r5, #0x279]
    cmp r0, #50
    bne ov000_0220f858_L348
    mov r0, #0
    strb r0, [r5, #0x1e2]
    ldrb r0, [r5, #0x2c2]
    mov r4, #1
    bic r0, r0, #15
    strb r0, [r5, #0x2c2]
ov000_0220f858_L348:
    mov r0, r4
    ldmia sp!, {r4, r5, r6, pc}
}
