/* ov000 row 0x0220ba28: 584 bytes.
 *
 * What it does: 146 instructions; 17 call(s) to 0x0203d294, 0x0203d294, 0x0220a2a4, +14 more; loops (back edge at +0x18); returns through pop {r3, r4, r5, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x10 -> +0xc4
 *   branch +0x34 -> +0x64
 *   branch +0x44 -> +0x64
 *   branch +0x60 -> +0xa0
 *   branch +0xc8 -> +0x124
 *   branch +0x128 -> +0x150
 *   branch +0x154 -> +0x1b4
 *   branch +0x170 -> +0x18c
 *   branch +0x1b8 -> +0x1d8
 *   branch +0x1dc -> +0x238
 *   branch +0x1fc -> +0x210
 *   test +0x0c cmp r1, #0
 *   test +0x30 tst r0, #3
 *   test +0x40 cmp r0, #60
 *   test +0x84 cmp r0, #40
 *   test +0xc4 cmp r1, #10
 *   test +0x100 cmp r0, #0
 *   test +0x110 tst r0, #7
 *   test +0x124 cmp r1, #20
 *   test +0x150 cmp r1, #22
 *   test +0x164 cmp r5, #0
 *   test +0x18c cmp r5, #20
 *   test +0x1b4 cmp r1, #24
 *   test +0x1d8 cmp r1, #26
 *   test +0x1f0 cmp r5, #31
 *   test +0x210 cmp r5, #20
 *   test +0x238 cmp r1, #28
 *   0 block transfer(s), 17 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0220ba28; the literal pool and
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

extern void native_fn_0203d294(void);
extern void native_fn_0220a2a4(void);
extern void native_fn_02026144(void);
extern void native_fn_020c56b4(void);
extern void native_fn_02042bfc(void);
extern void native_fn_02042c2c(void);
extern void native_fn_02028158(void);
extern void native_fn_02041f90(void);
extern void native_fn_02042c0c(void);
extern void native_fn_0220b94c(void);


asm u32 native_ov000_0220ba28 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r4, r0
    ldrb r1, [r4, #0x279]
    cmp r1, #0
    bne ov000_0220ba28_Lc4
    mov r0, #60
    bl native_fn_0203d294
    add r2, r0, #30
    add r1, r4, #512
    mvn r0, #-2147483648
    strh r2, [r1, #122]
    bl native_fn_0203d294
    tst r0, #3
    bne ov000_0220ba28_L64
    add r0, r4, #512
    ldrsh r0, [r0, #122]
    cmp r0, #60
    bge ov000_0220ba28_L64
    mov r1, #0
    mov r0, r4
    mov r2, r1
    bl native_fn_0220a2a4
    mov r0, #0
    str r0, [r4, #0x27c]
    b ov000_0220ba28_La0
ov000_0220ba28_L64:
    mov r0, r4
    mov r1, #1
    mov r2, #0
    bl native_fn_0220a2a4
    mov r0, #360
    bl native_fn_0203d294
    sub r2, r0, #180
    add r0, r2, #20
    cmp r0, #40
    add r0, r4, #512
    ldrsh r1, [r0, #122]
    movlo r2, #0
    mov r0, r2, lsl #12
    bl native_fn_02026144
    str r0, [r4, #0x27c]
ov000_0220ba28_La0:
    add r0, r4, #512
    ldrsh r0, [r0, #118]
    bl native_fn_020c56b4
    ldr r1, [r0, #0x14]
    mov r0, r4
    bl native_fn_02042bfc
    mov r0, #10
    strb r0, [r4, #0x279]
    ldmia sp!, {r3, r4, r5, pc}
ov000_0220ba28_Lc4:
    cmp r1, #10
    bne ov000_0220ba28_L124
    bl native_fn_02042c2c
    ldr r1, [r4, #0x27c]
    add r0, r0, r1
    bl native_fn_02028158
    mov r1, r0
    mov r0, r4
    mov r2, #0
    bl native_fn_02041f90
    add r0, r4, #512
    ldrsh r1, [r0, #122]
    sub r1, r1, #1
    strh r1, [r0, #122]
    ldrsh r0, [r0, #122]
    cmp r0, #0
    ldmgtia sp!, {r3, r4, r5, pc}
    mvn r0, #-2147483648
    bl native_fn_0203d294
    tst r0, #7
    moveq r0, #0
    movne r0, #20
    strb r0, [r4, #0x279]
    ldmia sp!, {r3, r4, r5, pc}
ov000_0220ba28_L124:
    cmp r1, #20
    bne ov000_0220ba28_L150
    mov r1, #0
    mov r2, r1
    bl native_fn_0220a2a4
    add r0, r4, #512
    mov r1, #0
    strh r1, [r0, #122]
    mov r0, #22
    strb r0, [r4, #0x279]
    ldmia sp!, {r3, r4, r5, pc}
ov000_0220ba28_L150:
    cmp r1, #22
    bne ov000_0220ba28_L1b4
    add r1, r4, #512
    ldrsh r1, [r1, #122]
    rsb r5, r1, #31
    cmp r5, #0
    movle r0, #24
    strleb r0, [r4, #0x279]
    ble ov000_0220ba28_L18c
    and r1, r5, #255
    bl native_fn_02042c0c
    add r0, r4, #512
    ldrsh r1, [r0, #122]
    add r1, r1, #1
    strh r1, [r0, #122]
ov000_0220ba28_L18c:
    cmp r5, #20
    movlt r0, #1
    ldrb r1, [r4, #0x2c2]
    movge r0, #0
    and r0, r0, #255
    and r0, r0, #15
    bic r1, r1, #15
    orr r0, r1, r0
    strb r0, [r4, #0x2c2]
    ldmia sp!, {r3, r4, r5, pc}
ov000_0220ba28_L1b4:
    cmp r1, #24
    bne ov000_0220ba28_L1d8
    bl native_fn_0220b94c
    add r0, r4, #512
    mov r1, #0
    strh r1, [r0, #122]
    mov r0, #26
    strb r0, [r4, #0x279]
    ldmia sp!, {r3, r4, r5, pc}
ov000_0220ba28_L1d8:
    cmp r1, #26
    bne ov000_0220ba28_L238
    add r1, r4, #512
    ldrsh r5, [r1, #122]
    and r1, r5, #255
    bl native_fn_02042c0c
    cmp r5, #31
    movge r0, #28
    strgeb r0, [r4, #0x279]
    bge ov000_0220ba28_L210
    add r0, r4, #512
    ldrsh r1, [r0, #122]
    add r1, r1, #1
    strh r1, [r0, #122]
ov000_0220ba28_L210:
    cmp r5, #20
    movlt r0, #1
    ldrb r1, [r4, #0x2c2]
    movge r0, #0
    and r0, r0, #255
    and r0, r0, #15
    bic r1, r1, #15
    orr r0, r1, r0
    strb r0, [r4, #0x2c2]
    ldmia sp!, {r3, r4, r5, pc}
ov000_0220ba28_L238:
    cmp r1, #28
    moveq r0, #0
    streqb r0, [r4, #0x279]
    ldmia sp!, {r3, r4, r5, pc}
}
