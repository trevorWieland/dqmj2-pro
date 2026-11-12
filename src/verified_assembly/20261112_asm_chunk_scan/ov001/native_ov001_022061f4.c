/* ov001 row 0x022061f4: 668 bytes.
 *
 * What it does: Copies a 8-register block to an optional destination under a condition in one predicated move.
 *
 * Decoded shape: predicated block copy.
 *
 *   pool +0x294 -> constant 0x9999999a (image word 0x9999999a)
 *   pool +0x298 -> constant 0x3fb99999 (image word 0x3fb99999)
 *   branch +0x30 -> +0x44
 *   branch +0x58 -> +0x70
 *   branch +0x78 -> +0x180
 *   branch +0xc4 -> +0xe4
 *   branch +0xd0 -> +0xe4
 *   back edge +0xe0 -> +0xb0
 *   branch +0x100 -> +0x114
 *   branch +0x10c -> +0x114
 *   branch +0x15c -> +0x180
 *   branch +0x188 -> +0x1cc
 *   branch +0x1c8 -> +0x1ec
 *   branch +0x1d4 -> +0x1ec
 *   branch +0x1f8 -> +0x218
 *   branch +0x228 -> +0x27c
 *   branch +0x274 -> +0x27c
 *   test +0x1c cmp r1, r0
 *   test +0x2c cmp r1, #0
 *   test +0x54 cmp r7, r0
 *   test +0x74 tst r0, #1
 *   test +0xb4 cmp r0, r8
 *   test +0xcc cmp r0, r1
 *   test +0xfc cmp r7, r0
 *   test +0x108 cmp r0, #0
 *   test +0x11c cmp r0, #0
 *   test +0x158 cmp r0, r8
 *   test +0x184 cmp r0, #0
 *   test +0x1d0 cmp r0, #0
 *   test +0x1e0 cmp r1, r0
 *   test +0x1f4 cmp r0, r1
 *   test +0x210 cmp r0, r1
 *   test +0x21c cmp r0, #80
 *   test +0x224 cmphs r0, #80
 *   test +0x270 cmp r0, #0
 *   16 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022061f4; the literal pool and
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

extern void native_fn_021f1a44(void);
extern void native_fn_020630b0(void);
extern void native_fn_0220617c(void);
extern void native_fn_02213698(void);
extern void native_fn_02212828(void);
extern void native_fn_0220619c(void);
extern void native_fn_02206550(void);
extern void native_fn_0220720c(void);
extern void native_fn_022065f0(void);
extern void native_fn_020244c4(void);
extern void native_fn_02024540(void);
extern void native_fn_02024394(void);
extern void native_fn_022064c0(void);


asm u32 native_ov001_022061f4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    mov r9, r0
    ldrsb r0, [r9, #8]
    bl native_fn_021f1a44
    ldrsh r1, [r9, #38]
    mvn r0, #0
    ldr r4, [r9, #0x28]
    cmp r1, r0
    ldr r5, [r9, #0x40]
    moveq r0, #0
    ldmeqia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
    cmp r1, #0
    ble ov001_022061f4_L44
    sub r0, r1, #1
    strh r0, [r9, #38]
    mov r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
ov001_022061f4_L44:
    ldr r0, [r4, #0x1e8]
    ldr r7, [r9, #0x38]
    ldrb r0, [r0, #0xab]
    bl native_fn_020630b0
    cmp r7, r0
    blt ov001_022061f4_L70
    mov r1, #0
    mov r0, r9
    strb r1, [r9, #0x23]
    bl native_fn_0220617c
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
ov001_022061f4_L70:
    ldr r0, [r9, #0x44]
    tst r0, #1
    beq ov001_022061f4_L180
    mov r0, r4
    bl native_fn_02213698
    ldr r1, [r4, #0x1e8]
    mov r6, r0
    ldrb r0, [r1, #0xab]
    bl native_fn_020630b0
    ldr r3, [r9, #0x30]
    ldr r2, [r9, #0x34]
    mov r1, #0
    add r2, r3, r2
    str r2, [r9, #0x30]
    mov r8, r0
    str r1, [r9, #0x34]
ov001_022061f4_Lb0:
    ldr r0, [r9, #0x38]
    cmp r0, r8
    ldr r1, [r6, r0, lsl #2]
    ldrge r0, [r6, r8, lsl #2]
    strge r0, [r9, #0x30]
    bge ov001_022061f4_Le4
    ldr r0, [r9, #0x30]
    cmp r0, r1
    blt ov001_022061f4_Le4
    ldr r0, [r9, #0x38]
    add r0, r0, #1
    str r0, [r9, #0x38]
    b ov001_022061f4_Lb0
ov001_022061f4_Le4:
    ldr r0, [r9, #0x38]
    ldrsb r1, [r9, #36]
    sub r0, r0, r7
    add r0, r1, r0
    strb r0, [r9, #0x24]
    ldr r0, [r9, #0x38]
    cmp r7, r0
    bge ov001_022061f4_L114
    bl native_fn_02212828
    cmp r0, #0
    beq ov001_022061f4_L114
    bl native_fn_0220619c
ov001_022061f4_L114:
    ldr r0, [r9, #0x34]
    ldr r1, [r9, #0x30]
    cmp r0, #0
    moveq r3, #1
    ldr r2, [r9, #0x38]
    movne r3, #0
    mov r0, r9
    bl native_fn_02206550
    ldrb r0, [r4, #0x31f]
    ldrb r1, [r9, #0x24]
    bl native_fn_0220720c
    ldr r0, [r9, #0x44]
    bic r0, r0, #1
    str r0, [r9, #0x44]
    ldrb r0, [r5]
    strb r0, [r5, #0x1]
    ldr r0, [r9, #0x38]
    cmp r0, r8
    blt ov001_022061f4_L180
    mov r0, #0
    strb r0, [r9, #0x23]
    ldrb r1, [r5, #0x1]
    mov r0, r9
    bl native_fn_022065f0
    mov r0, r9
    bl native_fn_0220617c
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
ov001_022061f4_L180:
    ldr r0, [r9, #0x34]
    cmp r0, #0
    ble ov001_022061f4_L1cc
    mov r0, r4
    bl native_fn_02213698
    ldr r1, [r9, #0x38]
    ldr r0, [r0, r1, lsl #2]
    bl native_fn_020244c4
    mov r2, r0
    mov r3, r1
    ldr r0, =0x9999999a
    ldr r1, =0x3fb99999
    bl native_fn_02024540
    bl native_fn_02024394
    movs r1, r0
    moveq r1, #1
    mov r0, r9
    bl native_fn_022064c0
    b ov001_022061f4_L1ec
ov001_022061f4_L1cc:
    ldrb r0, [r9, #0x23]
    cmp r0, #0
    beq ov001_022061f4_L1ec
    ldrb r1, [r5]
    ldrb r0, [r5, #0x1]
    cmp r1, r0
    moveq r0, #0
    streqb r0, [r9, #0x23]
ov001_022061f4_L1ec:
    ldrb r0, [r5]
    ldrb r1, [r5, #0x1]
    cmp r0, r1
    bls ov001_022061f4_L218
    ldr r0, [r9, #0x3c]
    add r0, r1, r0
    strb r0, [r5, #0x1]
    ldrb r1, [r5]
    and r0, r0, #255
    cmp r0, r1
    strhib r1, [r5, #0x1]
ov001_022061f4_L218:
    ldrb r0, [r5]
    cmp r0, #80
    ldrhsb r0, [r5, #0x1]
    cmphs r0, #80
    blo ov001_022061f4_L27c
    ldr r0, [r9, #0x38]
    add r0, r0, #1
    str r0, [r9, #0x38]
    ldrsb r0, [r9, #36]
    add r1, r0, #1
    strb r1, [r9, #0x24]
    ldrb r0, [r4, #0x31f]
    and r1, r1, #255
    bl native_fn_0220720c
    ldr r1, [r9, #0x30]
    ldr r2, [r9, #0x38]
    mov r0, r9
    mov r3, #1
    bl native_fn_02206550
    mov r0, #0
    strb r0, [r5, #0x1]
    bl native_fn_02212828
    cmp r0, #0
    beq ov001_022061f4_L27c
    bl native_fn_0220619c
ov001_022061f4_L27c:
    ldrb r1, [r5, #0x1]
    mov r0, r9
    bl native_fn_022065f0
    mov r0, r9
    bl native_fn_0220617c
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
