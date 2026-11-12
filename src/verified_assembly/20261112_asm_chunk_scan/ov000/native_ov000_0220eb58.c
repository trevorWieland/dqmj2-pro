/* ov000 row 0x0220eb58: 580 bytes.
 *
 * What it does: Copies a 5-register block to an optional destination under a condition in one predicated move.
 *
 * Decoded shape: predicated block copy.
 *
 *   pool +0x240 -> constant 0x88888889 (image word 0x88888889)
 *   branch +0x14 -> +0x38
 *   branch +0x40 -> +0x64
 *   branch +0x6c -> +0xd4
 *   branch +0xdc -> +0x11c
 *   branch +0x108 -> +0x11c
 *   branch +0x124 -> +0x1a0
 *   branch +0x134 -> +0x154
 *   branch +0x164 -> +0x180
 *   branch +0x1e4 -> +0x1fc
 *   branch +0x1f8 -> +0x238
 *   branch +0x200 -> +0x238
 *   branch +0x21c -> +0x22c
 *   branch +0x228 -> +0x234
 *   test +0x10 cmp r1, #0
 *   test +0x3c cmp r0, #10
 *   test +0x58 cmp r0, #150
 *   test +0x68 cmp r0, #20
 *   test +0xd8 cmp r0, #30
 *   test +0x104 cmp r1, #30
 *   test +0x120 cmp r0, #40
 *   test +0x130 tst r0, #3
 *   test +0x160 cmp r0, #1
 *   test +0x174 cmp r0, #0
 *   test +0x194 cmp r0, #300
 *   test +0x1e0 cmp r0, #100
 *   test +0x1fc cmp r0, #200
 *   test +0x214 cmp r0, #6
 *   16 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0220eb58; the literal pool and
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
extern void native_fn_0202818c(void);
extern void native_fn_02042c2c(void);
extern void native_fn_02028158(void);
extern void native_fn_02042104(void);
extern void native_fn_02041f90(void);
extern void native_fn_0220aac4(void);
extern void native_fn_02209c68(void);
extern void native_fn_020c56b4(void);


asm u32 native_ov000_0220eb58 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    ldrb r1, [r5, #0x279]
    mov r4, #0
    cmp r1, #0
    bne ov000_0220eb58_L38
    mov r1, r4
    mov r2, r4
    bl native_fn_0220a2a4
    add r0, r5, #512
    mov r1, r4
    strh r1, [r0, #122]
    mov r0, #10
    strb r0, [r5, #0x279]
ov000_0220eb58_L38:
    ldrb r0, [r5, #0x279]
    cmp r0, #10
    bne ov000_0220eb58_L64
    add r0, r5, #512
    ldrsh r1, [r0, #122]
    add r1, r1, #1
    strh r1, [r0, #122]
    ldrsh r0, [r0, #122]
    cmp r0, #150
    movgt r0, #20
    strgtb r0, [r5, #0x279]
ov000_0220eb58_L64:
    ldrb r0, [r5, #0x279]
    cmp r0, #20
    bne ov000_0220eb58_Ld4
    mov r0, r5
    mov r1, #1
    mov r2, #0
    bl native_fn_0220a2a4
    add r0, r5, #112
    add r1, r5, #680
    bl native_fn_0202818c
    str r0, [r5, #0x27c]
    mov r0, r5
    bl native_fn_02042c2c
    ldr r1, [r5, #0x27c]
    sub r0, r1, r0
    str r0, [r5, #0x27c]
    bl native_fn_02028158
    ldr r3, =0x88888889
    mov r1, r0, lsr #31
    smull r2, r12, r3, r0
    add r12, r0, r12
    add r12, r1, r12, asr #4
    str r12, [r5, #0x27c]
    add r0, r5, #512
    mov r1, #0
    strh r1, [r0, #122]
    mov r0, #30
    strb r0, [r5, #0x279]
ov000_0220eb58_Ld4:
    ldrb r0, [r5, #0x279]
    cmp r0, #30
    bne ov000_0220eb58_L11c
    ldr r1, [r5, #0x27c]
    mov r0, r5
    mov r2, #0
    bl native_fn_02042104
    add r0, r5, #512
    ldrsh r1, [r0, #122]
    add r1, r1, #1
    strh r1, [r0, #122]
    ldrsh r1, [r0, #122]
    cmp r1, #30
    ble ov000_0220eb58_L11c
    mov r1, #0
    strh r1, [r0, #122]
    mov r0, #40
    strb r0, [r5, #0x279]
ov000_0220eb58_L11c:
    ldrb r0, [r5, #0x279]
    cmp r0, #40
    bne ov000_0220eb58_L1a0
    add r0, r5, #512
    ldrsh r0, [r0, #122]
    tst r0, #3
    bne ov000_0220eb58_L154
    add r0, r5, #112
    add r1, r5, #680
    bl native_fn_0202818c
    mov r1, r0
    mov r0, r5
    mov r2, #0
    bl native_fn_02041f90
ov000_0220eb58_L154:
    add r0, r5, #512
    ldrsh r0, [r0, #122]
    and r0, r0, #3
    cmp r0, #1
    bne ov000_0220eb58_L180
    mov r0, r5
    mov r1, #1
    bl native_fn_0220aac4
    cmp r0, #0
    movne r0, #200
    strneb r0, [r5, #0x279]
ov000_0220eb58_L180:
    add r0, r5, #512
    ldrsh r1, [r0, #122]
    add r1, r1, #1
    strh r1, [r0, #122]
    ldrsh r0, [r0, #122]
    cmp r0, #300
    movgt r0, #100
    strgtb r0, [r5, #0x279]
ov000_0220eb58_L1a0:
    ldr r1, [r5, #0x70]
    ldr r0, [r5, #0x2a8]
    ldr r12, [r5, #0x78]
    sub r1, r1, r0
    smull r0, r2, r1, r1
    ldr r3, [r5, #0x2b0]
    mov r1, #0
    sub r3, r12, r3
    smlal r0, r2, r3, r3
    mov r0, r0, lsr #12
    orr r0, r0, r2, lsl #20
    subs r0, r0, #4096
    rscs r0, r1, r2, asr #12
    movlt r0, #100
    strltb r0, [r5, #0x279]
    ldrb r0, [r5, #0x279]
    cmp r0, #100
    bne ov000_0220eb58_L1fc
    mov r0, r5
    mov r1, #3
    bl native_fn_02209c68
    mov r4, #1
    b ov000_0220eb58_L238
ov000_0220eb58_L1fc:
    cmp r0, #200
    bne ov000_0220eb58_L238
    add r0, r5, #512
    ldrsh r0, [r0, #118]
    bl native_fn_020c56b4
    ldrb r0, [r0, #0x7]
    cmp r0, #6
    mov r0, r5
    bne ov000_0220eb58_L22c
    mov r1, #5
    bl native_fn_02209c68
    b ov000_0220eb58_L234
ov000_0220eb58_L22c:
    mov r1, #4
    bl native_fn_02209c68
ov000_0220eb58_L234:
    mov r4, #1
ov000_0220eb58_L238:
    mov r0, r4
    ldmia sp!, {r3, r4, r5, pc}
}
