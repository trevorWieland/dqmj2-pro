/* ov000 row 0x021fbf44: 1300 bytes.
 *
 * What it does: Copies a 2-register block to an optional destination under a condition in one predicated move.
 *
 * Decoded shape: predicated block copy.
 *
 *   pool +0x50c -> native_data_022372a8 (image word 0x022372a8)
 *   pool +0x510 -> constant 0x00000ff7 (image word 0x00000ff7)
 *   branch +0x58 -> +0x458
 *   branch +0x5c -> +0x74
 *   branch +0x60 -> +0x98
 *   branch +0x64 -> +0xec
 *   branch +0x68 -> +0x13c
 *   branch +0x6c -> +0x224
 *   branch +0x70 -> +0x3c8
 *   branch +0x94 -> +0x458
 *   branch +0xe8 -> +0x458
 *   branch +0xf8 -> +0x10c
 *   branch +0x108 -> +0x130
 *   branch +0x110 -> +0x11c
 *   branch +0x118 -> +0x130
 *   branch +0x138 -> +0x458
 *   branch +0x144 -> +0x458
 *   branch +0x1e8 -> +0x1f8
 *   branch +0x1fc -> +0x214
 *   branch +0x210 -> +0x458
 *   branch +0x220 -> +0x458
 *   branch +0x258 -> +0x2ac
 *   branch +0x270 -> +0x284
 *   branch +0x288 -> +0x2a0
 *   branch +0x29c -> +0x2ac
 *   branch +0x2b4 -> +0x2d4
 *   branch +0x2c0 -> +0x3bc
 *   branch +0x2d0 -> +0x3bc
 *   branch +0x2d8 -> +0x2ec
 *   branch +0x2e8 -> +0x3bc
 *   branch +0x2f0 -> +0x3bc
 *   branch +0x37c -> +0x390
 *   branch +0x38c -> +0x39c
 *   branch +0x3c4 -> +0x458
 *   branch +0x3d4 -> +0x458
 *   branch +0x3f8 -> +0x450
 *   back edge +0x45c -> +0x44
 *   branch +0x46c -> +0x498
 *   branch +0x49c -> +0x4c8
 *   branch +0x4bc -> +0x4c8
 *   branch +0x4d8 -> +0x500
 *   test +0x30 cmp r0, #0
 *   test +0x50 cmp r0, #5
 *   test +0xf4 tst r0, #1
 *   test +0x10c tst r0, #2
 *   test +0x140 cmp r0, #0
 *   test +0x1e0 cmp r2, r0
 *   test +0x1ec cmp r2, #0
 *   test +0x1f8 cmp r2, #0
 *   test +0x244 cmp r0, r6
 *   test +0x254 cmp r0, #0
 *   test +0x268 cmp r1, r0
 *   test +0x274 cmp r1, #0
 *   test +0x284 cmp r1, #0
 *   test +0x2b0 tst r0, #1
 *   test +0x2bc cmp r0, #0
 *   test +0x2d4 tst r0, #2
 *   test +0x2ec tst r0, #4
 *   test +0x304 cmp r0, #2
 *   test +0x320 cmp r0, #0
 *   test +0x370 cmp r0, #0
 *   test +0x3d0 tst r1, r0
 *   test +0x3f4 cmp r0, #0
 *   test +0x458 cmp r11, #1
 *   test +0x468 cmp r1, #0
 *   test +0x498 cmp r9, #0
 *   test +0x4b8 cmp r0, #0
 *   test +0x4d4 cmp r0, #6
 *   35 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021fbf44; the literal pool and
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

extern void native_fn_022156c4(void);
extern void native_fn_02215698(void);
extern void native_fn_0202a634(void);
extern u8 native_data8_022372a8[];
extern void native_fn_021fca9c(void);
extern void native_fn_0204b61c(void);
extern void native_fn_0204b138(void);
extern void native_fn_021fc458(void);
extern void native_fn_021fc73c(void);
extern void native_fn_0221794c(void);
extern void native_fn_021fdf44(void);
extern void native_fn_02062520(void);
extern void native_fn_021fdd60(void);
extern void native_fn_021fdad8(void);
extern void native_fn_020620e8(void);
extern void native_fn_020c4c58(void);
extern void native_fn_021e7b9c(void);
extern void native_fn_02217bdc(void);
extern void native_fn_02217cf0(void);
extern void native_fn_021fcd4c(void);
extern void native_fn_02217c9c(void);
extern void native_fn_02026144(void);
extern void native_fn_021fdd6c(void);
extern void native_fn_021fded0(void);
extern void native_fn_020496b0(void);
extern void native_fn_021fcce4(void);


asm u32 native_ov000_021fbf44 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #12
    bl native_fn_022156c4
    str r0, [sp, #0x8]
    bl native_fn_02215698
    mov r10, r0
    mov r9, #0
    bl native_fn_0202a634
    ldr r1, =native_data8_022372a8
    mov r7, r0
    ldr r0, [r1, #0x8]
    mov r8, r9
    cmp r0, #0
    movne r0, #1
    stmneib r1, {r0, r8}
    ldr r4, =native_data8_022372a8
    mvn r5, #0
ov000_021fbf44_L44:
    ldr r6, [r4, #0xc]
    mov r11, #0
    ldr r0, [r6]
    cmp r0, #5
    addls pc, pc, r0, lsl #2
    b ov000_021fbf44_L458
    b ov000_021fbf44_L74
    b ov000_021fbf44_L98
    b ov000_021fbf44_Lec
    b ov000_021fbf44_L13c
    b ov000_021fbf44_L224
    b ov000_021fbf44_L3c8
ov000_021fbf44_L74:
    mov r0, r11
    bl native_fn_021fca9c
    mov r11, #1
    ldr r1, [r4, #0xc]
    mov r0, r11
    str r0, [r1]
    mov r0, #0
    str r0, [r4, #0x4]
    b ov000_021fbf44_L458
ov000_021fbf44_L98:
    mov r0, #2
    bl native_fn_021fca9c
    add r0, r10, #16
    mov r1, #1
    bl native_fn_0204b61c
    add r0, r6, #420
    mov r1, r11
    mov r2, r11
    bl native_fn_0204b138
    add r0, r6, #420
    mov r1, #1
    mov r2, r11
    bl native_fn_0204b138
    ldr r1, [r4, #0xc]
    mov r0, #2
    str r0, [r1]
    mov r0, #1
    str r0, [r4, #0x4]
    ldr r0, [r4, #0xc]
    add r9, r0, #12
    b ov000_021fbf44_L458
ov000_021fbf44_Lec:
    add r9, r6, #12
    ldrh r0, [r7, #2]
    tst r0, #1
    beq ov000_021fbf44_L10c
    bl native_fn_021fc458
    mov r0, #1
    str r0, [r4, #0x4]
    b ov000_021fbf44_L130
ov000_021fbf44_L10c:
    tst r0, #2
    beq ov000_021fbf44_L11c
    bl native_fn_021fc73c
    b ov000_021fbf44_L130
ov000_021fbf44_L11c:
    mov r0, r9
    bl native_fn_0221794c
    ldr r1, [r4, #0x4]
    orr r0, r1, r0
    str r0, [r4, #0x4]
ov000_021fbf44_L130:
    mov r0, r9
    bl native_fn_021fdf44
    b ov000_021fbf44_L458
ov000_021fbf44_L13c:
    bl native_fn_02062520
    cmp r0, #0
    beq ov000_021fbf44_L458
    bl native_fn_021fdd60
    ldr r0, [r4, #0xc]
    ldr r0, [r0, #0x5f4]
    bl native_fn_021fdad8
    ldr r1, [r4, #0xc]
    str r0, [r1, #0x5f8]
    ldr r2, [r4, #0xc]
    mov r1, r11
    mov r0, #4
    str r1, [r2, #0x5fc]
    bl native_fn_021fca9c
    add r0, r10, #16
    mov r1, #1
    bl native_fn_0204b61c
    ldr r6, [r4, #0xc]
    mov r1, r11
    add r0, r6, #180
    mov r2, r11
    bl native_fn_0204b138
    add r0, r6, #180
    mov r1, #1
    mov r2, r11
    bl native_fn_0204b138
    ldr r2, [r4, #0xc]
    mov r1, #4
    str r1, [r2]
    mov r1, #1
    str r1, [r4, #0x4]
    str r1, [r4, #0x8]
    strb r1, [r4, #0x2]
    mov r0, #9
    strb r1, [r4]
    bl native_fn_020620e8
    ldr r1, [r4, #0xc]
    add r9, r1, #252
    ldrh r0, [r9, #14]
    ldr r2, [r1, #0xfc]
    sub r0, r0, #1
    cmp r2, r0
    moveq r8, r11
    beq ov000_021fbf44_L1f8
    cmp r2, #0
    addne r0, r1, r2, lsl #2
    ldrne r8, [r0, #0x1ec]
ov000_021fbf44_L1f8:
    cmp r2, #0
    bne ov000_021fbf44_L214
    ldr r1, [r4, #0xc]
    ldr r0, [r1, #0x5f8]
    ldr r1, [r1, #0xc]
    bl native_fn_020c4c58
    b ov000_021fbf44_L458
ov000_021fbf44_L214:
    mov r0, r8
    mov r1, r5
    bl native_fn_020c4c58
    b ov000_021fbf44_L458
ov000_021fbf44_L224:
    add r9, r6, #252
    mov r0, r9
    ldr r6, [r9, #0x4]
    bl native_fn_0221794c
    ldr r1, [r4, #0x4]
    orr r0, r1, r0
    str r0, [r4, #0x4]
    ldr r0, [r9, #0x4]
    cmp r0, r6
    movne r0, #1
    strneb r0, [r4]
    ldr r0, [r4, #0x4]
    cmp r0, #0
    beq ov000_021fbf44_L2ac
    ldrh r0, [r9, #14]
    ldr r1, [r9]
    sub r0, r0, #1
    cmp r1, r0
    moveq r8, #0
    beq ov000_021fbf44_L284
    cmp r1, #0
    ldrne r0, [r4, #0xc]
    addne r0, r0, r1, lsl #2
    ldrne r8, [r0, #0x1ec]
ov000_021fbf44_L284:
    cmp r1, #0
    bne ov000_021fbf44_L2a0
    ldr r1, [r4, #0xc]
    ldr r0, [r1, #0x5f8]
    ldr r1, [r1, #0xc]
    bl native_fn_020c4c58
    b ov000_021fbf44_L2ac
ov000_021fbf44_L2a0:
    mov r0, r8
    mov r1, r5
    bl native_fn_020c4c58
ov000_021fbf44_L2ac:
    ldrh r0, [r7, #2]
    tst r0, #1
    beq ov000_021fbf44_L2d4
    bl native_fn_021fc458
    cmp r0, #0
    beq ov000_021fbf44_L3bc
    mov r0, #1
    str r0, [r4, #0x4]
    strb r0, [r4]
    b ov000_021fbf44_L3bc
ov000_021fbf44_L2d4:
    tst r0, #2
    beq ov000_021fbf44_L2ec
    bl native_fn_021fc73c
    mov r0, #83
    bl native_fn_021e7b9c
    b ov000_021fbf44_L3bc
ov000_021fbf44_L2ec:
    tst r0, #4
    beq ov000_021fbf44_L3bc
    ldrb r0, [r4, #0x1]
    add r0, r0, #1
    strb r0, [r4, #0x1]
    and r0, r0, #255
    cmp r0, #2
    movhs r0, #0
    strhsb r0, [r4, #0x1]
    bl native_fn_021fdd60
    ldrb r0, [r4, #0x1]
    mov r1, #8
    mov r3, #1
    cmp r0, #0
    moveq r0, #34
    movne r0, #33
    mov r0, r0, lsl #16
    mov r2, r0, lsr #16
    mov r0, #1
    str r0, [sp]
    mov r0, #87
    str r0, [sp, #0x4]
    mov r0, #5
    bl native_fn_02217bdc
    add r0, r10, #16
    bl native_fn_02217cf0
    mov r0, #1
    strb r0, [r4]
    ldr r0, [r4, #0xc]
    ldr r0, [r0]
    bl native_fn_021fcd4c
    ldr r0, [r9]
    ldr r1, [r4, #0xc]
    cmp r0, #0
    add r0, r1, r0, lsl #2
    ldr r8, [r0, #0x1ec]
    bne ov000_021fbf44_L390
    ldr r0, [r1, #0x5f8]
    ldr r1, [r1, #0xc]
    bl native_fn_020c4c58
    b ov000_021fbf44_L39c
ov000_021fbf44_L390:
    mov r0, r8
    mov r1, r5
    bl native_fn_020c4c58
ov000_021fbf44_L39c:
    ldr r1, [r4, #0xc]
    mov r0, #4
    str r0, [r1, #0x8]
    ldr r1, [r4, #0xc]
    mov r0, #5
    str r0, [r1]
    mov r0, #1
    str r0, [r4, #0x4]
ov000_021fbf44_L3bc:
    mov r0, r9
    bl native_fn_021fdf44
    b ov000_021fbf44_L458
ov000_021fbf44_L3c8:
    ldrh r1, [r7, #2]
    ldr r0, =0x00000ff7
    tst r1, r0
    beq ov000_021fbf44_L458
    mov r0, #1
    bl native_fn_02217c9c
    ldr r1, [r4, #0xc]
    ldr r0, [r1, #0x8]
    str r0, [r1]
    ldr r1, [r4, #0xc]
    ldr r0, [r1, #0x5fc]
    cmp r0, #0
    beq ov000_021fbf44_L450
    add r9, r1, #252
    ldrh r0, [r9, #14]
    sub r0, r0, #1
    str r0, [r1, #0xfc]
    ldrh r6, [r9, #12]
    ldrh r0, [r9, #14]
    mov r1, r6
    sub r0, r0, #1
    bl native_fn_02026144
    mul r0, r6, r0
    str r0, [r9, #0x4]
    ldr r2, [r4, #0xc]
    mov r1, r11
    mov r0, #85
    str r1, [r2, #0x5fc]
    bl native_fn_021e7b9c
    mov r0, r8
    mov r1, r5
    bl native_fn_020c4c58
    mov r0, #1
    strb r0, [r4]
ov000_021fbf44_L450:
    mov r0, #1
    str r0, [r4, #0x4]
ov000_021fbf44_L458:
    cmp r11, #1
    beq ov000_021fbf44_L44
    ldr r0, =native_data8_022372a8
    ldr r1, [r0, #0x4]
    cmp r1, #0
    beq ov000_021fbf44_L498
    ldr r0, [r0, #0xc]
    ldr r0, [r0]
    bl native_fn_021fcd4c
    ldr r0, =native_data8_022372a8
    ldr r0, [r0, #0xc]
    ldr r0, [r0]
    bl native_fn_021fdd6c
    ldr r0, =native_data8_022372a8
    mov r1, #0
    str r1, [r0, #0x4]
ov000_021fbf44_L498:
    cmp r9, #0
    beq ov000_021fbf44_L4c8
    ldr r1, =native_data8_022372a8
    mov r0, r9
    ldr r1, [r1, #0xc]
    ldr r1, [r1]
    bl native_fn_021fded0
    ldr r0, [r9, #0xc4]
    cmp r0, #0
    beq ov000_021fbf44_L4c8
    add r0, r9, #168
    bl native_fn_020496b0
ov000_021fbf44_L4c8:
    ldr r0, =native_data8_022372a8
    ldr r1, [r0, #0xc]
    ldr r0, [r1, #0x4]
    cmp r0, #6
    beq ov000_021fbf44_L500
    ldr r0, [r1]
    bl native_fn_021fcce4
    ldr r0, =native_data8_022372a8
    mov r1, #6
    ldr r3, [r0, #0xc]
    ldr r2, [r3, #0x4]
    str r2, [r3]
    ldr r0, [r0, #0xc]
    str r1, [r0, #0x4]
ov000_021fbf44_L500:
    ldr r0, [sp, #0x8]
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
