/* ov000 row 0x021fa6b0: 1116 bytes.
 *
 * What it does: 277 instructions; 38 call(s) to 0x02215698, 0x02066c3c, 0x021f97ec, +35 more; loops (back edge at +0x10); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x454 -> constant 0x02236f28 (image word 0x02236f28)
 *   pool +0x458 -> constant 0x66666667 (image word 0x66666667)
 *   branch +0x1c -> +0x44
 *   branch +0x40 -> +0x448
 *   branch +0x48 -> +0x448
 *   branch +0x94 -> +0x3e0
 *   branch +0xa0 -> +0x3e0
 *   branch +0xa8 -> +0x3e0
 *   branch +0xdc -> +0x3e0
 *   branch +0x128 -> +0x29c
 *   branch +0x14c -> +0x244
 *   branch +0x170 -> +0x244
 *   branch +0x190 -> +0x244
 *   branch +0x1ac -> +0x1cc
 *   branch +0x1d8 -> +0x210
 *   branch +0x1e8 -> +0x200
 *   branch +0x1fc -> +0x210
 *   branch +0x254 -> +0x27c
 *   branch +0x264 -> +0x27c
 *   back edge +0x298 -> +0x134
 *   back edge +0x2d8 -> +0x2c0
 *   back edge +0x320 -> +0x2f0
 *   branch +0x368 -> +0x3a4
 *   branch +0x3a0 -> +0x3b8
 *   back edge +0x3b4 -> +0x35c
 *   back edge +0x3c4 -> +0x358
 *   branch +0x3dc -> +0x3fc
 *   test +0x18 cmp r0, #3
 *   test +0x44 cmp r0, #2
 *   test +0x90 cmp r1, r0
 *   test +0x9c cmp r0, #28
 *   test +0xa4 cmp r1, #36
 *   test +0xd8 cmp r1, r0
 *   test +0x124 cmp r0, #0
 *   test +0x144 cmp r6, r0
 *   test +0x148 cmpne r8, #0
 *   test +0x16c cmp r3, r1
 *   test +0x18c cmp r3, r1
 *   test +0x1a4 cmp r1, #168
 *   test +0x1d4 cmp r0, #1
 *   test +0x1e4 cmp r0, #0
 *   test +0x1f0 cmp r0, #128
 *   test +0x204 cmp r0, #48
 *   test +0x21c cmp r0, #1
 *   test +0x224 cmpeq r0, #48
 *   test +0x248 cmp r0, #0
 *   test +0x250 cmpne r6, r0
 *   test +0x260 cmp r1, r0
 *   test +0x294 cmp r1, r0, asr #24
 *   test +0x2d4 cmp r6, #3
 *   test +0x318 cmp r9, #3
 *   test +0x364 cmp r7, r0
 *   test +0x3b0 cmp r10, #3
 *   test +0x3c0 cmp r7, #168
 *   0 block transfer(s), 20 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021fa6b0; the literal pool and
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

extern void native_fn_02215698(void);
extern void native_fn_02066c3c(void);
extern void native_fn_021f97ec(void);
extern void native_fn_0206cf44(void);
extern void native_fn_02062a10(void);
extern void native_fn_0206cfe4(void);
extern void native_fn_02044cdc(void);
extern void native_fn_020628b0(void);
extern void native_fn_02008d78(void);
extern void native_fn_02062850(void);
extern void native_fn_02215bc8(void);
extern void native_fn_021f9148(void);
extern void native_fn_021e7b9c(void);
extern void native_fn_0206d250(void);
extern void native_fn_0204b2d0(void);
extern void native_fn_021f8f70(void);
extern void native_fn_0204b380(void);


asm u32 native_ov000_021fa6b0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #40
    bl native_fn_02215698
    mov r5, r0
    bl native_fn_02066c3c
    ldrb r0, [r0]
    cmp r0, #3
    bne ov000_021fa6b0_L44
    bl native_fn_021f97ec
    add r0, r5, #1024
    ldrsb r2, [r0, #151]
    ldr r0, =0x02236f28
    ldrb r1, [r5, #0x498]
    ldrsb r0, [r0, r2]
    ldrb r2, [r5, #0x499]
    bl native_fn_0206cf44
    b ov000_021fa6b0_L448
ov000_021fa6b0_L44:
    cmp r0, #2
    bne ov000_021fa6b0_L448
    add r0, r5, #1024
    ldrsb r1, [r0, #151]
    add r2, r5, #160
    ldr r0, [r2, r1, lsl #3]
    add r7, r2, r1, lsl #3
    bl native_fn_02062a10
    add r2, r5, #1024
    ldrsb r3, [r2, #151]
    ldr r1, =0x02236f28
    str r0, [sp, #0x4]
    ldrsb r0, [r1, r3]
    ldrsb r2, [r2, #145]
    mov r1, #8
    str r2, [sp]
    bl native_fn_0206cfe4
    ldrb r1, [r5, #0x498]
    mvn r0, #3
    cmp r1, r0
    blt ov000_021fa6b0_L3e0
    ldrb r0, [r5, #0x499]
    cmp r0, #28
    blo ov000_021fa6b0_L3e0
    cmp r1, #36
    bhs ov000_021fa6b0_L3e0
    ldr r0, [sp, #0x4]
    ldrsh r0, [r0, #24]
    bl native_fn_02044cdc
    mov r0, r0, lsl #1
    rsb r0, r0, #5
    mov r3, #40
    mul r1, r0, r3
    add r0, r1, r1, lsr #31
    mov r0, r0, asr #1
    ldrb r1, [r5, #0x499]
    add r0, r0, #48
    cmp r1, r0
    bge ov000_021fa6b0_L3e0
    ldrb r10, [r7, #0x5]
    mov r0, #0
    mov r1, #16
    str r0, [sp]
    strb r1, [r7, #0x4]
    ldrb r0, [r5, #0x499]
    ldr r2, =0x66666667
    add r4, r5, #1024
    sub r1, r0, #28
    mov r0, r1, lsr #31
    smull r1, r6, r2, r1
    add r6, r0, r6, asr #4
    mul r0, r6, r3
    add r0, r0, #48
    strb r0, [r7, #0x5]
    ldrsb r0, [r4, #149]
    ldr r6, [sp]
    cmp r0, #0
    ble ov000_021fa6b0_L29c
    ldr r11, =0x02236f28
    add r9, r5, #160
ov000_021fa6b0_L134:
    ldr r0, [r9]
    bl native_fn_02062a10
    mov r8, r0
    ldrsb r0, [r4, #151]
    cmp r6, r0
    cmpne r8, #0
    beq ov000_021fa6b0_L244
    ldr r0, [sp, #0x4]
    ldrsh r0, [r0, #24]
    bl native_fn_02044cdc
    ldrb r2, [r7, #0x5]
    mov r1, #40
    ldrb r3, [r9, #0x5]
    mla r1, r0, r1, r2
    cmp r3, r1
    bgt ov000_021fa6b0_L244
    ldrsh r0, [r8, #24]
    bl native_fn_02044cdc
    ldrb r2, [r9, #0x5]
    mov r1, #40
    ldrb r3, [r7, #0x5]
    mla r1, r0, r1, r2
    cmp r3, r1
    bgt ov000_021fa6b0_L244
    ldrsh r0, [r8, #24]
    bl native_fn_02044cdc
    mov r1, #40
    mla r1, r0, r1, r10
    cmp r1, #168
    strltb r10, [r9, #0x5]
    blt ov000_021fa6b0_L1cc
    ldrsh r0, [r8, #24]
    bl native_fn_02044cdc
    rsb r1, r0, #2
    mov r0, #40
    mul r0, r1, r0
    add r0, r0, #48
    strb r0, [r9, #0x5]
ov000_021fa6b0_L1cc:
    ldrsh r0, [r8, #24]
    bl native_fn_02044cdc
    cmp r0, #1
    bne ov000_021fa6b0_L210
    ldrb r1, [r7, #0x5]
    sub r0, r1, r10
    cmp r0, #0
    ble ov000_021fa6b0_L200
    add r0, r1, #40
    cmp r0, #128
    movgt r0, #128
    strb r0, [r7, #0x5]
    b ov000_021fa6b0_L210
ov000_021fa6b0_L200:
    sub r0, r1, #40
    cmp r0, #48
    movlt r0, #48
    strb r0, [r7, #0x5]
ov000_021fa6b0_L210:
    ldr r0, [sp, #0x4]
    ldrsh r0, [r0, #24]
    bl native_fn_02044cdc
    cmp r0, #1
    ldreqb r0, [r7, #0x5]
    cmpeq r0, #48
    ldreqb r0, [r9, #0x5]
    addeq r0, r0, #40
    streqb r0, [r9, #0x5]
    ldrsb r0, [r11]
    ldrb r1, [r9, #0x4]
    ldrb r2, [r9, #0x5]
    bl native_fn_0206cf44
ov000_021fa6b0_L244:
    ldr r0, [r9]
    cmp r0, #0
    ldrnesb r0, [r4, #151]
    cmpne r6, r0
    beq ov000_021fa6b0_L27c
    ldrb r1, [r7, #0x5]
    ldrb r0, [r9, #0x5]
    cmp r1, r0
    bls ov000_021fa6b0_L27c
    ldr r0, [sp]
    add r0, r0, #1
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    str r0, [sp]
ov000_021fa6b0_L27c:
    add r9, r9, #8
    add r11, r11, #1
    add r0, r6, #1
    mov r0, r0, lsl #24
    mov r6, r0, asr #24
    ldrsb r1, [r4, #149]
    cmp r1, r0, asr #24
    bgt ov000_021fa6b0_L134
ov000_021fa6b0_L29c:
    add r0, r5, #1024
    ldrsb r2, [r0, #151]
    ldr r0, =0x02236f28
    ldrb r1, [r7, #0x4]
    ldrsb r0, [r0, r2]
    ldrb r2, [r7, #0x5]
    bl native_fn_0206cf44
    mov r6, #0
    mov r4, r6
ov000_021fa6b0_L2c0:
    mov r0, r4
    bl native_fn_020628b0
    add r0, r6, #1
    mov r0, r0, lsl #24
    mov r6, r0, asr #24
    cmp r6, #3
    blt ov000_021fa6b0_L2c0
    mov r8, #0
    ldr r6, =0x02236f28
    add r7, sp, #8
    mov r9, r8
    add r4, sp, #16
ov000_021fa6b0_L2f0:
    add r1, r5, r9, lsl #3
    add r0, r9, #1
    ldr r2, [r1, #0xa0]
    ldr r3, [r1, #0xa4]
    ldrsb r1, [r6], #1
    mov r0, r0, lsl #24
    str r2, [r4, r9, lsl #3]
    add r2, r4, r9, lsl #3
    mov r9, r0, asr #24
    str r3, [r2, #0x4]
    cmp r9, #3
    strb r1, [r7], #1
    blt ov000_021fa6b0_L2f0
    add r0, r5, #160
    mov r1, #0
    mov r2, #24
    bl native_fn_02008d78
    ldr r0, =0x02236f28
    mov r1, #0
    mov r2, #3
    bl native_fn_02008d78
    ldr r9, =0x02236f28
    mov r7, #48
    add r6, sp, #16
    add r4, sp, #8
    mov r11, #0
ov000_021fa6b0_L358:
    mov r10, r11
ov000_021fa6b0_L35c:
    add r0, r6, r10, lsl #3
    ldrb r0, [r0, #0x5]
    cmp r7, r0
    bne ov000_021fa6b0_L3a4
    ldr r0, [r6, r10, lsl #3]
    bl native_fn_02062850
    add r0, r6, r10, lsl #3
    ldr r1, [r6, r10, lsl #3]
    ldr r0, [r0, #0x4]
    add r2, r5, r8, lsl #3
    str r1, [r2, #0xa0]
    str r0, [r2, #0xa4]
    ldrsb r1, [r4, r10]
    add r0, r8, #1
    mov r0, r0, lsl #24
    strb r1, [r9], #1
    mov r8, r0, asr #24
    b ov000_021fa6b0_L3b8
ov000_021fa6b0_L3a4:
    add r0, r10, #1
    mov r0, r0, lsl #24
    mov r10, r0, asr #24
    cmp r10, #3
    blt ov000_021fa6b0_L35c
ov000_021fa6b0_L3b8:
    add r0, r7, #40
    and r7, r0, #255
    cmp r7, #168
    blo ov000_021fa6b0_L358
    bl native_fn_02215bc8
    ldr r0, [sp]
    bl native_fn_021f9148
    mov r0, #104
    bl native_fn_021e7b9c
    b ov000_021fa6b0_L3fc
ov000_021fa6b0_L3e0:
    add r0, r5, #1024
    ldrsb r2, [r0, #151]
    ldr r0, =0x02236f28
    ldrb r1, [r7, #0x4]
    ldrsb r0, [r0, r2]
    ldrb r2, [r7, #0x5]
    bl native_fn_0206cf44
ov000_021fa6b0_L3fc:
    ldr r0, [sp]
    add r1, r5, #160
    add r1, r1, r0, lsl #3
    ldrb r0, [r1, #0x4]
    strh r0, [sp, #12]
    ldrb r0, [r1, #0x5]
    strh r0, [sp, #14]
    ldrsb r0, [r1, #6]
    bl native_fn_0206d250
    mov r1, r0
    add r2, sp, #12
    add r0, r5, #16
    bl native_fn_0204b2d0
    bl native_fn_021f8f70
    add r0, r5, #16
    mov r1, #1
    bl native_fn_0204b380
    mov r0, #4
    strb r0, [r5, #0x494]
ov000_021fa6b0_L448:
    mov r0, #0
    add sp, sp, #40
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
