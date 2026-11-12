/* ov006 row 0x0220692c: 504 bytes.
 *
 * What it does: Copies a 5-register block to an optional destination under a condition in one predicated move.
 *
 * Decoded shape: predicated block copy.
 *
 *   pool +0x1d0 -> constant 0x0221c27c (image word 0x0221c27c)
 *   pool +0x1d4 -> native_data_0220bbf0 (image word 0x0220bbf0)
 *   pool +0x1d8 -> constant 0x88888889 (image word 0x88888889)
 *   pool +0x1dc -> constant 0x66666667 (image word 0x66666667)
 *   pool +0x1e0 -> constant 0x2aaaaaab (image word 0x2aaaaaab)
 *   pool +0x1e4 -> constant 0x0221c49c (image word 0x0221c49c)
 *   pool +0x1e8 -> constant 0x0221c64c (image word 0x0221c64c)
 *   pool +0x1ec -> constant 0x0221c308 (image word 0x0221c308)
 *   pool +0x1f0 -> constant 0x0221c2c0 (image word 0x0221c2c0)
 *   pool +0x1f4 -> constant 0x0221c350 (image word 0x0221c350)
 *   branch +0xac -> +0xec
 *   branch +0xe8 -> +0x124
 *   branch +0x128 -> +0x198
 *   branch +0x194 -> +0x1bc
 *   test +0x9c cmp r4, #1
 *   test +0x124 cmp r6, #4
 *   11 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x0220692c; the literal pool and
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

extern u8 native_data2_0220bbf0[];
extern void native_fn_020c18d8(void);
extern void native_fn_02048a60(void);
extern void native_fn_0204b74c(void);
extern void native_fn_0204b2d0(void);
extern void native_fn_0204b380(void);
extern void native_fn_0204b770(void);
extern void native_fn_0204b6dc(void);
extern void native_fn_0204b61c(void);


asm u32 native_ov006_0220692c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    sub sp, sp, #8
    ldr r3, =0x0221c27c
    ldr r8, =native_data2_0220bbf0
    ldr r6, [r3]
    ldr r5, =0x88888889
    mov r7, r6, lsr #31
    smull r1, r0, r5, r6
    add r0, r6, r0
    add r0, r7, r0, asr #3
    mov r2, #15
    smull r0, r1, r2, r0
    sub r0, r6, r0
    ldr r4, =0x66666667
    ldr r1, [r3, #0x10]
    ldrh r12, [r8, #2]
    add r2, r1, #11
    ldr r3, =0x2aaaaaab
    ldrh r8, [r8]
    smull r14, r1, r5, r6
    add r1, r6, r1
    mov lr, r0, lsr #31
    smull r5, r6, r4, r0
    strh r8, [sp, #4]
    smull r8, r5, r4, r0
    add r6, lr, r6, asr #1
    strh r12, [sp, #6]
    mov r12, #5
    smull r8, r4, r3, r2
    mov r2, r2, lsr #31
    add r4, r2, r4, asr #1
    add r5, lr, r5, asr #1
    smull r2, r3, r12, r6
    sub r6, r0, r2
    mov r2, r4
    add r1, r7, r1, asr #3
    mov r0, #0
    bl native_fn_020c18d8
    ldrsh r1, [sp, #6]
    cmp r4, #1
    mov r0, r0, lsl #16
    add r0, r1, r0, asr #16
    strh r0, [sp, #6]
    bne ov006_0220692c_Lec
    ldr r0, =0x0221c49c
    ldr r1, =0x0221c64c
    ldr r2, [r0, #0x7c]
    orr r2, r2, #2
    str r2, [r0, #0x7c]
    ldr r2, [r1, #0x7c]
    bic r2, r2, #2
    str r2, [r1, #0x7c]
    ldrsh r1, [sp, #4]
    ldrsh r2, [sp, #6]
    bl native_fn_02048a60
    ldr r0, =0x0221c308
    mov r1, #120
    bl native_fn_0204b74c
    b ov006_0220692c_L124
ov006_0220692c_Lec:
    ldr r0, =0x0221c64c
    ldr r1, =0x0221c49c
    ldr r2, [r0, #0x7c]
    orr r2, r2, #2
    str r2, [r0, #0x7c]
    ldr r2, [r1, #0x7c]
    bic r2, r2, #2
    str r2, [r1, #0x7c]
    ldrsh r1, [sp, #4]
    ldrsh r2, [sp, #6]
    bl native_fn_02048a60
    ldr r0, =0x0221c308
    mov r1, #48
    bl native_fn_0204b74c
ov006_0220692c_L124:
    cmp r6, #4
    bge ov006_0220692c_L198
    mov r0, #40
    ldr r1, =native_data2_0220bbf0
    mul r3, r6, r0
    ldrh r4, [r1, #38]
    ldrh r1, [r1, #36]
    mul r2, r5, r0
    strh r1, [sp]
    strh r4, [sp, #2]
    mov r0, r3, lsl #16
    ldrsh r4, [sp]
    mov r1, r2, lsl #16
    ldrsh r3, [sp, #2]
    add r4, r4, r0, asr #16
    ldr r0, =0x0221c2c0
    add r3, r3, r1, asr #16
    add r2, sp, #0
    mov r1, #0
    strh r4, [sp]
    strh r3, [sp, #2]
    bl native_fn_0204b2d0
    ldr r0, =0x0221c2c0
    mov r1, #1
    bl native_fn_0204b380
    ldr r0, =0x0221c308
    mov r1, #0
    bl native_fn_0204b770
    b ov006_0220692c_L1bc
ov006_0220692c_L198:
    ldr r0, =0x0221c308
    add r1, sp, #4
    bl native_fn_0204b6dc
    ldr r0, =0x0221c2c0
    mov r1, #0
    bl native_fn_0204b380
    ldr r0, =0x0221c308
    mov r1, #1
    bl native_fn_0204b770
ov006_0220692c_L1bc:
    ldr r0, =0x0221c350
    mov r1, #0
    bl native_fn_0204b61c
    add sp, sp, #8
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
