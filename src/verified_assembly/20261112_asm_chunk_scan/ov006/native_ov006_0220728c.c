/* ov006 row 0x0220728c: 564 bytes.
 *
 * What it does: Copies a 5-register block to an optional destination under a condition in one predicated move.
 *
 * Decoded shape: predicated block copy.
 *
 *   pool +0x21c -> constant 0x00000ff7 (image word 0x00000ff7)
 *   pool +0x220 -> constant 0x0221c27c (image word 0x0221c27c)
 *   pool +0x224 -> constant 0x88888889 (image word 0x88888889)
 *   pool +0x228 -> constant 0x66666667 (image word 0x66666667)
 *   pool +0x22c -> constant 0x0221c290 (image word 0x0221c290)
 *   pool +0x230 -> constant 0x2aaaaaab (image word 0x2aaaaaab)
 *   branch +0x18 -> +0x210
 *   branch +0xa0 -> +0xd0
 *   branch +0xb4 -> +0xc0
 *   back edge +0xc8 -> +0xa8
 *   branch +0xcc -> +0x108
 *   branch +0xdc -> +0x108
 *   branch +0xf0 -> +0xfc
 *   back edge +0x104 -> +0xe4
 *   branch +0x13c -> +0x178
 *   branch +0x194 -> +0x1d8
 *   branch +0x1a4 -> +0x1b4
 *   back edge +0x1b0 -> +0x19c
 *   branch +0x1b8 -> +0x1d8
 *   test +0x14 tst r1, r0
 *   test +0x9c cmp r0, #0
 *   test +0xb0 cmp r9, r0
 *   test +0xc4 cmp r8, #3
 *   test +0xd8 cmp r0, #0
 *   test +0xec cmp r9, r0
 *   test +0x100 cmp r8, #3
 *   test +0x134 cmp r4, #0
 *   test +0x164 cmp r4, r12
 *   test +0x168 cmpeq lr, #0
 *   test +0x190 cmp r0, #0
 *   test +0x1a0 cmp r0, #0
 *   test +0x1ac cmp r2, #12
 *   test +0x1b4 cmp r2, #0
 *   3 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x0220728c; the literal pool and
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

extern void native_fn_0202a634(void);
extern void native_fn_021e7d78(void);
extern void native_fn_021e7e28(void);
extern void native_fn_0205e7a8(void);
extern void native_fn_02063fa0(void);
extern void native_fn_02062a68(void);
extern void native_fn_020628b0(void);
extern void native_fn_02063fac(void);
extern void native_fn_02062a78(void);
extern void native_fn_02062980(void);
extern void native_fn_020627a0(void);
extern void native_fn_0207cdb8(void);
extern void native_fn_0207ca14(void);
extern void native_fn_0207ca3c(void);
extern void native_fn_020629e0(void);
extern void native_fn_02206374(void);
extern void native_fn_022061e8(void);
extern void native_fn_0220692c(void);
extern void native_fn_022063e8(void);
extern void native_fn_02206328(void);
extern void native_fn_021e648c(void);


asm u32 native_ov006_0220728c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    mov r7, r0
    bl native_fn_0202a634
    ldrh r1, [r0, #2]
    ldr r0, =0x00000ff7
    tst r1, r0
    beq ov006_0220728c_L210
    ldr r0, =0x0221c27c
    ldr r5, =0x88888889
    ldr r6, [r0]
    mov r2, #15
    smull r1, r0, r5, r6
    mov r3, r6, lsr #31
    add r0, r6, r0
    add r0, r3, r0, asr #3
    smull r0, r1, r2, r0
    sub r0, r6, r0
    ldr r2, =0x66666667
    smull r1, r4, r5, r6
    add r4, r6, r4
    mov lr, r0, lsr #31
    smull r1, r5, r2, r0
    smull r1, r6, r2, r0
    add r5, lr, r5, asr #1
    mov r12, #5
    smull r1, r2, r12, r5
    add r4, r3, r4, asr #3
    sub r5, r0, r1
    add r6, lr, r6, asr #1
    bl native_fn_021e7d78
    bl native_fn_021e7e28
    mvn r0, #0
    mov r1, #82
    bl native_fn_0205e7a8
    add r1, r5, r6, lsl #2
    ldr r0, =0x0221c290
    ldr r9, [r0, r1, lsl #2]
    mov r0, r9
    bl native_fn_02063fa0
    cmp r0, #0
    beq ov006_0220728c_Ld0
    mov r8, #0
ov006_0220728c_La8:
    mov r0, r8
    bl native_fn_02062a68
    cmp r9, r0
    bne ov006_0220728c_Lc0
    mov r0, r8
    bl native_fn_020628b0
ov006_0220728c_Lc0:
    add r8, r8, #1
    cmp r8, #3
    blt ov006_0220728c_La8
    b ov006_0220728c_L108
ov006_0220728c_Ld0:
    mov r0, r9
    bl native_fn_02063fac
    cmp r0, #0
    beq ov006_0220728c_L108
    mov r8, #0
ov006_0220728c_Le4:
    mov r0, r8
    bl native_fn_02062a78
    cmp r9, r0
    bne ov006_0220728c_Lfc
    mov r0, r8
    bl native_fn_02062980
ov006_0220728c_Lfc:
    add r8, r8, #1
    cmp r8, #3
    blt ov006_0220728c_Le4
ov006_0220728c_L108:
    mov r0, r9
    bl native_fn_020627a0
    mov r0, #1
    bl native_fn_0207cdb8
    mov r0, #1
    bl native_fn_0207ca14
    ldr r0, =0x0221c27c
    ldr r0, [r0, #0x4]
    bl native_fn_0207ca3c
    bl native_fn_020629e0
    ldr r1, =0x0221c27c
    cmp r4, #0
    str r0, [r1, #0x10]
    ble ov006_0220728c_L178
    ldr r3, =0x2aaaaaab
    mov r2, r0, lsr #31
    smull r1, r14, r3, r0
    smull r1, r12, r3, r0
    add r12, r2, r12, asr #1
    add lr, r2, lr, asr #1
    mov r3, #12
    smull r1, r2, r3, r14
    sub lr, r0, r1
    cmp r4, r12
    cmpeq lr, #0
    subeq r4, r4, #1
    moveq r6, #2
    moveq r5, #3
ov006_0220728c_L178:
    bl native_fn_02206374
    mov r0, r4
    bl native_fn_022061e8
    ldr r1, =0x0221c290
    add r0, r5, r6, lsl #2
    ldr r0, [r1, r0, lsl #2]
    cmp r0, #0
    bne ov006_0220728c_L1d8
    mov r2, #0
ov006_0220728c_L19c:
    ldr r0, [r1, r2, lsl #2]
    cmp r0, #0
    beq ov006_0220728c_L1b4
    add r2, r2, #1
    cmp r2, #12
    blt ov006_0220728c_L19c
ov006_0220728c_L1b4:
    cmp r2, #0
    ble ov006_0220728c_L1d8
    sub r3, r2, #1
    mov r1, r3, lsr #31
    mov r2, r3, asr #1
    rsb r0, r1, r3, lsl #30
    add r2, r3, r2, lsr #30
    add r5, r1, r0, ror #30
    mov r6, r2, asr #2
ov006_0220728c_L1d8:
    add r0, r6, r6, lsl #2
    add r2, r5, r0
    rsb r1, r4, r4, lsl #4
    ldr r0, =0x0221c27c
    add r1, r2, r1
    str r1, [r0]
    bl native_fn_0220692c
    bl native_fn_022063e8
    mov r0, r5
    mov r1, r6
    bl native_fn_02206328
    ldr r0, =0x0221c27c
    mov r1, #1
    str r1, [r0, #0x8]
ov006_0220728c_L210:
    mov r0, r7
    bl native_fn_021e648c
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
