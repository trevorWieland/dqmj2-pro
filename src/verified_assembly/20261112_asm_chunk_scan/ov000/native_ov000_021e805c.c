/* ov000 row 0x021e805c: 456 bytes.
 *
 * What it does: Copies a 5-register block to an optional destination under a condition in one predicated move.
 *
 * Decoded shape: predicated block copy.
 *
 *   pool +0x1c4 -> constant 0x88888889 (image word 0x88888889)
 *   branch +0x20 -> +0x5c
 *   branch +0x38 -> +0x1bc
 *   branch +0x58 -> +0x1bc
 *   branch +0xb8 -> +0x114
 *   branch +0x110 -> +0x1bc
 *   branch +0x120 -> +0x19c
 *   branch +0x148 -> +0x16c
 *   branch +0x168 -> +0x184
 *   branch +0x198 -> +0x1bc
 *   test +0x1c cmp r2, #0
 *   test +0x34 cmp r1, #0
 *   test +0x11c cmp r0, #2
 *   test +0x140 cmp r0, #0
 *   9 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e805c; the literal pool and
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

extern void native_fn_02042c2c(void);
extern void native_fn_02041f90(void);
extern void native_fn_0203d294(void);
extern void native_fn_021e7d18(void);
extern void native_fn_0202818c(void);
extern void native_fn_02028158(void);
extern void native_fn_02025a28(void);
extern void native_fn_02024e0c(void);
extern void native_fn_02025ca4(void);
extern void native_fn_020259b4(void);


asm u32 native_ov000_021e805c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r4, r0
    add r1, r4, #512
    ldrsh r2, [r1, #172]
    sub r2, r2, #1
    strh r2, [r1, #172]
    ldrsh r2, [r1, #172]
    cmp r2, #0
    ble ov000_021e805c_L5c
    ldrsh r2, [r1, #174]
    sub r2, r2, #1
    strh r2, [r1, #174]
    ldrsh r1, [r1, #174]
    cmp r1, #0
    ble ov000_021e805c_L1bc
    bl native_fn_02042c2c
    mov r2, r0
    ldr r1, [r4, #0x2b0]
    mov r0, r4
    add r1, r2, r1
    mov r2, #0
    bl native_fn_02041f90
    b ov000_021e805c_L1bc
ov000_021e805c_L5c:
    mov r0, #63
    bl native_fn_0203d294
    add r1, r0, #30
    add r0, r4, #512
    strh r1, [r0, #172]
    ldr r2, [r4, #0x284]
    ldr r1, [r4, #0x74]
    ldr r0, [r4, #0x2a4]
    sub r3, r2, r1
    smull r1, r2, r3, r3
    ldr r12, [r4, #0x280]
    ldr r3, [r4, #0x70]
    ldr r5, [r4, #0x288]
    sub r12, r12, r3
    ldr r3, [r4, #0x78]
    smlal r1, r2, r12, r12
    sub r3, r5, r3
    smlal r1, r2, r3, r3
    mov r3, r1, lsr #12
    orr r3, r3, r2, lsl #20
    mov r1, r0, asr #31
    subs r0, r0, r3
    sbcs r0, r1, r2, asr #12
    bge ov000_021e805c_L114
    mov r0, r4
    mov r1, #1
    mov r2, #0
    bl native_fn_021e7d18
    add r0, r4, #112
    add r1, r4, #640
    bl native_fn_0202818c
    mov r5, r0
    mov r0, r4
    bl native_fn_02042c2c
    sub r0, r5, r0
    bl native_fn_02028158
    ldr r3, =0x88888889
    mov r1, r0, lsr #31
    smull r2, r12, r3, r0
    add r12, r0, r12
    add r12, r1, r12, asr #4
    str r12, [r4, #0x2b0]
    add r0, r4, #512
    mov r1, #30
    strh r1, [r0, #174]
    b ov000_021e805c_L1bc
ov000_021e805c_L114:
    mov r0, #7
    bl native_fn_0203d294
    cmp r0, #2
    blt ov000_021e805c_L19c
    mov r0, r4
    mov r1, #1
    mov r2, #0
    bl native_fn_021e7d18
    mov r0, #7
    bl native_fn_0203d294
    sub r0, r0, #4
    cmp r0, #0
    mov r0, #7
    ble ov000_021e805c_L16c
    bl native_fn_0203d294
    sub r0, r0, #4
    mov r0, r0, lsl #12
    bl native_fn_02025a28
    mov r1, r0
    mov r0, #1056964608
    bl native_fn_02024e0c
    b ov000_021e805c_L184
ov000_021e805c_L16c:
    bl native_fn_0203d294
    sub r0, r0, #4
    mov r0, r0, lsl #12
    bl native_fn_02025a28
    mov r1, #1056964608
    bl native_fn_02025ca4
ov000_021e805c_L184:
    bl native_fn_020259b4
    str r0, [r4, #0x2b0]
    add r0, r4, #512
    mov r1, #32
    strh r1, [r0, #174]
    b ov000_021e805c_L1bc
ov000_021e805c_L19c:
    mov r1, #0
    mov r0, r4
    mov r2, r1
    bl native_fn_021e7d18
    mov r1, #0
    str r1, [r4, #0x2b0]
    add r0, r4, #512
    strh r1, [r0, #174]
ov000_021e805c_L1bc:
    mov r0, #0
    ldmia sp!, {r3, r4, r5, pc}
}
