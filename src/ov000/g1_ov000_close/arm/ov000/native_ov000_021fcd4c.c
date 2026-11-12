/* ov000 row 0x021fcd4c: 3468 bytes.
 *
 * What it does: 864 instructions; 103 call(s) to 0x02215698, 0x02062aa0, 0x02062ad0, +100 more; loops (back edge at +0x14); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0xd80 -> constant 0x022372a8 (image word 0x022372a8)
 *   pool +0xd84 -> native_data_0222f430 (image word 0x0222f430)
 *   pool +0xd88 -> constant 0x021c9698 (image word 0x021c9698)
 *   branch +0x54 -> +0x68
 *   branch +0x60 -> +0x27c
 *   branch +0x64 -> +0xd3c
 *   branch +0xb4 -> +0x214
 *   branch +0x110 -> +0x1b8
 *   branch +0x11c -> +0x138
 *   branch +0x134 -> +0x150
 *   branch +0x1b4 -> +0x200
 *   back edge +0x210 -> +0xc8
 *   branch +0x278 -> +0xd3c
 *   branch +0x2e0 -> +0x2f4
 *   branch +0x2f0 -> +0x318
 *   branch +0x304 -> +0x318
 *   branch +0x324 -> +0x330
 *   branch +0x32c -> +0x354
 *   branch +0x3d0 -> +0x3f0
 *   branch +0x3ec -> +0x420
 *   branch +0x41c -> +0x474
 *   branch +0x44c -> +0x454
 *   branch +0x490 -> +0x4a0
 *   branch +0x49c -> +0x4a8
 *   branch +0x4b8 -> +0x4d8
 *   branch +0x4e4 -> +0xa38
 *   branch +0x4f4 -> +0x9bc
 *   branch +0x55c -> +0x9bc
 *   branch +0x578 -> +0x9ac
 *   branch +0x580 -> +0x754
 *   branch +0x58c -> +0x5c0
 *   branch +0x5a4 -> +0x5c0
 *   branch +0x5bc -> +0x5f8
 *   branch +0x5f4 -> +0x9ac
 *   branch +0x65c -> +0x6a0
 *   branch +0x69c -> +0x724
 *   branch +0x6a4 -> +0x6ec
 *   branch +0x6e8 -> +0x724
 *   branch +0x720 -> +0x9ac
 *   branch +0x750 -> +0x9ac
 *   branch +0x764 -> +0x7dc
 *   branch +0x7d8 -> +0x9ac
 *   branch +0x7e0 -> +0x800
 *   branch +0x7fc -> +0x870
 *   branch +0x86c -> +0x9ac
 *   branch +0x8e4 -> +0x930
 *   branch +0x92c -> +0x980
 *   branch +0x930 -> +0x9ac
 *   back edge +0x9b8 -> +0x508
 *   branch +0x9c8 -> +0xa38
 *   branch +0xa4c -> +0xb34
 *   branch +0xa74 -> +0xb00
 *   branch +0xa84 -> +0xac4
 *   branch +0xa8c -> +0xac0
 *   branch +0xaac -> +0xac0
 *   branch +0xabc -> +0xac4
 *   branch +0xafc -> +0xbbc
 *   branch +0xb30 -> +0xbbc
 *   branch +0xb54 -> +0xba0
 *   branch +0xb68 -> +0xb9c
 *   branch +0xb80 -> +0xb9c
 *   branch +0xb98 -> +0xba0
 *   branch +0xc14 -> +0xcf0
 *   back edge +0xc3c -> +0xc24
 *   test +0x50 cmp r1, #2
 *   test +0x5c cmp r0, #4
 *   test +0xb0 cmp r0, #0
 *   test +0x10c cmp r1, r0
 *   test +0x118 cmp r8, r0
 *   test +0x20c cmp r8, r0
 *   test +0x2a8 cmp r1, #0
 *   test +0x2dc cmp r2, #0
 *   test +0x2fc cmp r2, r1
 *   test +0x320 cmp r1, #0
 *   test +0x3c8 cmp r1, r0
 *   test +0x3cc cmpne r5, #0
 *   test +0x3e8 cmp r0, #0
 *   test +0x444 cmp r3, r7
 *   test +0x48c cmp r1, r0
 *   test +0x4b4 cmp r0, #0
 *   test +0x4e0 cmp r0, #0
 *   test +0x4f0 cmp r0, #0
 *   test +0x558 cmp r7, r0
 *   test +0x574 cmp r7, r0
 *   test +0x57c cmp r7, #0
 *   test +0x588 cmp r0, #0
 *   test +0x5a0 cmp r0, #0
 *   test +0x5b8 cmp r0, r1
 *   test +0x650 cmp r8, #0
 *   test +0x6a0 cmp r8, #0
 *   test +0x760 cmp r8, r0
 *   test +0x7dc cmp r8, #0
 *   test +0x7f8 cmp r0, #0
 *   test +0x898 cmp r0, #0
 *   test +0x8e0 cmp r8, #0
 *   test +0x9b4 cmp r9, r0
 *   test +0x9c4 cmp r1, r0
 *   test +0xa3c cmp r1, #0
 *   test +0xa48 cmpne r1, r0
 *   test +0xa80 cmp r4, r0
 *   test +0xa88 cmp r4, #0
 *   test +0xaa8 cmp r0, #0
 *   test +0xab8 cmp r0, #0
 *   test +0xb50 cmp r0, #0
 *   test +0xb64 cmp r0, #0
 *   test +0xb7c cmp r0, #0
 *   test +0xb94 cmp r1, r0
 *   test +0xc10 cmp r1, r0
 *   test +0xcfc cmp r1, r0
 *   test +0xd20 cmp r1, r0
 *   test +0xd40 cmp r0, #2
 *   2 block transfer(s), 124 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021fcd4c; the literal pool and
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

extern void ov000_display_context_02215698(void);
extern void native_fn_02062aa0(void);
extern void native_fn_02062ad0(void);
extern void native_fn_02216434(void);
extern void native_fn_0204a644(void);
extern void native_fn_02049ad0(void);
extern void native_fn_02049ffc(void);
extern void native_fn_02062a50(void);
extern void native_fn_0221742c(void);
extern void native_fn_02062a88(void);
extern void native_fn_02215430(void);
extern void native_fn_0204a1d0(void);
extern void native_fn_0204a4ac(void);
extern void native_fn_02045dc4(void);
extern void native_fn_02217f14(void);
extern void native_fn_02049008(void);
extern void native_fn_02217dbc(void);
extern void native_fn_02026144(void);
extern void native_fn_0204a010(void);
extern void native_fn_0204a724(void);
extern void native_fn_02065d88(void);
extern void native_fn_02211064(void);
extern void native_fn_0204a574(void);
extern void native_fn_0204a448(void);
extern void native_fn_02062d04(void);
extern void native_fn_02087e44(void);
extern void native_fn_02063144(void);
extern void native_fn_02048094(void);
extern u8 native_data_0222f430[];
extern void native_fn_0204a104(void);
extern void native_fn_02085284(void);
extern void native_fn_02046af4(void);
extern void native_fn_02087d0c(void);
extern void native_fn_02217e4c(void);
extern void native_fn_021fdf28(void);
extern void native_fn_0205fb3c(void);
extern void native_fn_02217f78(void);


asm u32 native_ov000_021fcd4c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #120
    str r0, [sp, #0x10]
    bl ov000_display_context_02215698
    str r0, [sp, #0x28]
    bl native_fn_02062aa0
    bl native_fn_02062ad0
    add r1, sp, #52
    mov r0, #0
    strh r0, [r1]
    strh r0, [r1, #2]
    mov r4, #1
    bl native_fn_02216434
    mov r1, #0
    add r2, sp, #48
    str r1, [sp, #0x20]
    str r1, [sp, #0x24]
    strh r1, [r2]
    strh r1, [r2, #2]
    ldr r1, [sp, #0x10]
    cmp r1, #2
    beq ov000_021fcd4c_L68
    mov r0, r1
    cmp r0, #4
    beq ov000_021fcd4c_L27c
    b ov000_021fcd4c_Ld3c
ov000_021fcd4c_L68:
    ldr r1, [sp, #0x24]
    strh r1, [sp, #52]
    ldr r1, =0x022372a8
    ldrh r2, [r0, #2]
    ldr r4, [r1, #0xc]
    mov r1, #1
    str r2, [sp]
    str r1, [sp, #0x4]
    str r1, [sp, #0x8]
    ldrb r2, [r0]
    ldrb r3, [r0, #0x1]
    add r1, sp, #52
    add r6, r4, #12
    mov r0, #23
    bl native_fn_0204a644
    ldrh r1, [r6, #12]
    mov r8, #0
    sub r0, r1, #1
    cmp r0, #0
    ble ov000_021fcd4c_L214
    mvn r7, #15
    mov r5, #4
    mov r11, r8
    add r4, sp, #52
ov000_021fcd4c_Lc8:
    add r0, r8, #5
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02049ad0
    ldr r0, [r0]
    ldr r0, [r0, #0x4]
    bl native_fn_02049ffc
    add r0, r8, #12
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02049ad0
    ldr r0, [r0]
    ldr r0, [r0, #0x4]
    bl native_fn_02049ffc
    ldr r1, [r6, #0x4]
    ldrh r0, [r6, #14]
    add r1, r8, r1
    cmp r1, r0
    bge ov000_021fcd4c_L1b8
    bl native_fn_02062aa0
    cmp r8, r0
    bge ov000_021fcd4c_L138
    mov r0, r8
    bl native_fn_02062a50
    mov r9, r0
    mov r0, #7
    bl native_fn_0221742c
    b ov000_021fcd4c_L150
ov000_021fcd4c_L138:
    bl native_fn_02062aa0
    sub r0, r8, r0
    bl native_fn_02062a88
    mov r9, r0
    mov r0, #8
    bl native_fn_0221742c
ov000_021fcd4c_L150:
    mov r10, r0
    mov r0, r9
    strh r7, [sp, #52]
    bl native_fn_02215430
    mov r3, r0
    add r0, r8, #12
    mov r0, r0, lsl #24
    stmia sp, {r5, r11}
    mov r0, r0, asr #24
    mov r1, r4
    mov r2, #1
    bl native_fn_0204a1d0
    mov r0, #24
    strh r0, [sp, #52]
    mov r0, #1
    str r0, [sp]
    mov r0, #0
    str r0, [sp, #0x4]
    add r0, r8, #5
    mov r0, r0, lsl #24
    mov r1, r9
    mov r2, r10
    mov r0, r0, asr #24
    mov r3, r4
    bl native_fn_0204a4ac
    b ov000_021fcd4c_L200
ov000_021fcd4c_L1b8:
    add r0, r8, #5
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02049ad0
    ldr r1, [r0]
    mov r0, #7
    ldr r9, [r1, #0x4]
    bl native_fn_0221742c
    mov r1, r0
    ldrb r0, [r9, #0x1e]
    str r0, [sp]
    ldrb r0, [r9, #0x1f]
    str r0, [sp, #0x4]
    ldrb r0, [r1, #0xa]
    ldrb r1, [r1, #0xb]
    ldrb r2, [r9, #0x1c]
    ldrb r3, [r9, #0x1d]
    bl native_fn_02045dc4
ov000_021fcd4c_L200:
    add r8, r8, #1
    ldrh r1, [r6, #12]
    sub r0, r1, #1
    cmp r8, r0
    blt ov000_021fcd4c_Lc8
ov000_021fcd4c_L214:
    add r0, r1, #4
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    mov r1, #5
    mov r2, #2
    mov r3, #34
    bl native_fn_02217f14
    mov r1, #5
    str r0, [sp, #0x24]
    mov r4, #0
    mov r0, r6
    mov r2, r1
    mov r3, #7
    str r4, [sp]
    bl native_fn_02049008
    mov r2, #1
    str r2, [sp]
    mov r0, r6
    mov r1, #12
    mov r2, #6
    mov r3, #8
    bl native_fn_02049008
    bl native_fn_02217dbc
    mov r0, #28
    str r0, [sp, #0x20]
    b ov000_021fcd4c_Ld3c
ov000_021fcd4c_L27c:
    ldr r0, [sp, #0x24]
    ldr r1, =0x022372a8
    str r0, [sp, #0x1c]
    ldr r0, [r1, #0xc]
    add r6, r0, #252
    ldrh r5, [r6, #12]
    ldrh r7, [r6, #14]
    ldr r10, [r0, #0x5f4]
    mov r1, r5
    mov r0, r7
    bl native_fn_02026144
    cmp r1, #0
    subne r0, r7, r1
    strne r0, [sp, #0x14]
    subeq r0, r7, r5
    streq r0, [sp, #0x14]
    mov r0, r10
    bl native_fn_02215430
    mov r7, r0
    mov r0, #2
    bl native_fn_02049ad0
    ldr r0, [r0]
    ldr r2, [r6]
    ldr r0, [r0, #0x4]
    cmp r2, #0
    bne ov000_021fcd4c_L2f4
    ldr r1, =0x022372a8
    ldr r1, [r1, #0xc]
    ldr r5, [r1, #0x5f8]
    b ov000_021fcd4c_L318
ov000_021fcd4c_L2f4:
    ldrh r1, [r6, #14]
    sub r1, r1, #1
    cmp r2, r1
    moveq r5, #0
    beq ov000_021fcd4c_L318
    ldr r1, =0x022372a8
    ldr r1, [r1, #0xc]
    add r1, r1, r2, lsl #2
    ldr r5, [r1, #0x1ec]
ov000_021fcd4c_L318:
    ldr r1, =0x022372a8
    ldrb r1, [r1, #0x2]
    cmp r1, #0
    beq ov000_021fcd4c_L330
    bl native_fn_02049ffc
    b ov000_021fcd4c_L354
ov000_021fcd4c_L330:
    ldrb r1, [r0, #0x5f]
    mov r2, #0
    mov r3, #104
    mov r1, r1, lsl #3
    str r1, [sp]
    ldrb r1, [r0, #0x5e]
    mov r1, r1, lsl #3
    sub r1, r1, #104
    bl native_fn_0204a010
ov000_021fcd4c_L354:
    mvn r0, #63
    strh r0, [sp, #52]
    mov r0, #4
    str r0, [sp]
    mov r0, #0
    str r0, [sp, #0x4]
    add r1, sp, #52
    mov r3, r7
    mov r0, #2
    mov r2, #1
    bl native_fn_0204a1d0
    mvn r0, #55
    strh r0, [sp, #52]
    mov r0, #2
    str r0, [sp]
    mov r1, #40
    str r1, [sp, #0x4]
    mov r1, #1
    str r1, [sp, #0x8]
    mov r2, #0
    add r1, sp, #52
    mov r3, #5
    str r2, [sp, #0xc]
    bl native_fn_0204a724
    mvn r0, #23
    strh r0, [sp, #52]
    ldrh r0, [r6, #14]
    ldr r1, [r6]
    sub r0, r0, #1
    cmp r1, r0
    cmpne r5, #0
    beq ov000_021fcd4c_L3f0
    mov r0, r5
    bl native_fn_02065d88
    ldrb r1, [r0, #0x2d]
    mov r0, r10
    bl native_fn_02211064
    cmp r0, #0
    bne ov000_021fcd4c_L420
ov000_021fcd4c_L3f0:
    mov r0, #2
    str r0, [sp]
    mov r1, #41
    str r1, [sp, #0x4]
    mov r2, #1
    str r2, [sp, #0x8]
    mov r2, #0
    add r1, sp, #52
    mov r3, #5
    str r2, [sp, #0xc]
    bl native_fn_0204a724
    b ov000_021fcd4c_L474
ov000_021fcd4c_L420:
    ldrb r0, [r10, #0x31]
    bl native_fn_02065d88
    mov r8, r0
    mov r0, r5
    bl native_fn_02065d88
    ldrh r1, [r8, #28]
    ldrh r0, [r0, #28]
    sub r1, r7, r1
    add r3, r1, r0
    cmp r3, r7
    movgt r4, #9
    bgt ov000_021fcd4c_L454
    movlt r4, #7
ov000_021fcd4c_L454:
    mov r0, #4
    mov r2, r4
    str r0, [sp]
    mov r4, #0
    add r1, sp, #52
    mov r0, #2
    str r4, [sp, #0x4]
    bl native_fn_0204a1d0
ov000_021fcd4c_L474:
    mov r0, #24
    strh r0, [sp, #52]
    bl native_fn_02062aa0
    ldr r1, =0x022372a8
    ldr r1, [r1, #0xc]
    ldr r1, [r1, #0xc]
    cmp r1, r0
    bge ov000_021fcd4c_L4a0
    mov r0, #7
    bl native_fn_0221742c
    b ov000_021fcd4c_L4a8
ov000_021fcd4c_L4a0:
    mov r0, #8
    bl native_fn_0221742c
ov000_021fcd4c_L4a8:
    mov r2, r0
    ldr r0, =0x022372a8
    ldrb r0, [r0, #0x2]
    cmp r0, #0
    beq ov000_021fcd4c_L4d8
    mov r0, #1
    add r3, sp, #52
    mov r1, r10
    str r0, [sp]
    mov r4, #0
    str r4, [sp, #0x4]
    bl native_fn_0204a4ac
ov000_021fcd4c_L4d8:
    ldr r0, =0x022372a8
    ldrb r0, [r0]
    cmp r0, #0
    beq ov000_021fcd4c_La38
    ldrh r0, [r6, #12]
    mov r9, #0
    cmp r0, #0
    ble ov000_021fcd4c_L9bc
    mvn r0, #39
    str r0, [sp, #0x2c]
    add r4, r0, #24
    add r5, sp, #52
ov000_021fcd4c_L508:
    ldr r0, [r6, #0x4]
    add r1, r9, #5
    add r0, r0, r9
    mov r0, r0, lsl #16
    mov r7, r0, asr #16
    mov r0, r1, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02049ad0
    ldr r0, [r0]
    ldr r0, [r0, #0x4]
    bl native_fn_02049ffc
    add r0, r9, #12
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02049ad0
    ldr r0, [r0]
    ldr r0, [r0, #0x4]
    bl native_fn_02049ffc
    ldrh r0, [r6, #14]
    sub r0, r0, #1
    cmp r7, r0
    beq ov000_021fcd4c_L9bc
    mov r0, #16
    strh r0, [sp, #52]
    ldr r0, =0x022372a8
    ldr r1, [r0, #0xc]
    ldr r0, [r1, #0x5f0]
    cmp r7, r0
    bgt ov000_021fcd4c_L9ac
    cmp r7, #0
    bne ov000_021fcd4c_L754
    ldr r0, [r1, #0x5f8]
    cmp r0, #0
    beq ov000_021fcd4c_L5c0
    bl native_fn_02065d88
    ldrb r1, [r0, #0x2d]
    mov r0, r10
    bl native_fn_02211064
    cmp r0, #0
    beq ov000_021fcd4c_L5c0
    ldr r1, =0x022372a8
    ldrb r0, [r10, #0x31]
    ldr r1, [r1, #0xc]
    ldr r1, [r1, #0x5f8]
    cmp r0, r1
    bne ov000_021fcd4c_L5f8
ov000_021fcd4c_L5c0:
    mov r0, #20
    str r0, [sp]
    mov r0, #3
    str r0, [sp, #0x4]
    mov r0, #1
    str r0, [sp, #0x8]
    add r0, r9, #5
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    mov r1, r5
    mov r2, #5
    mov r3, #2
    bl native_fn_0204a574
    b ov000_021fcd4c_L9ac
ov000_021fcd4c_L5f8:
    bl native_fn_02065d88
    ldrh r11, [r0, #28]
    ldr r0, =0x022372a8
    ldr r0, [r0, #0xc]
    ldr r0, [r0, #0x5f8]
    bl native_fn_02065d88
    ldrh r7, [r0, #28]
    mov r1, #20
    add r0, r9, #5
    str r1, [sp]
    mov r1, #1
    mov r0, r0, lsl #24
    str r1, [sp, #0x4]
    str r1, [sp, #0x8]
    mov r0, r0, asr #24
    mov r1, r5
    mov r2, #5
    mov r3, #2
    bl native_fn_0204a574
    ldr r0, [sp, #0x2c]
    sub r8, r7, r11
    strh r0, [sp, #52]
    cmp r8, #0
    mov r2, #0
    mov r3, #5
    ble ov000_021fcd4c_L6a0
    mov r0, #1
    str r0, [sp]
    mov r0, #13
    str r0, [sp, #0x4]
    mov r0, #1
    str r0, [sp, #0x8]
    mov r0, #0
    str r0, [sp, #0xc]
    add r0, r9, #12
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    mov r1, r5
    bl native_fn_0204a724
    mov r0, r8, lsl #16
    mov r3, r0, asr #16
    b ov000_021fcd4c_L724
ov000_021fcd4c_L6a0:
    cmp r8, #0
    bge ov000_021fcd4c_L6ec
    mov r0, #1
    str r0, [sp]
    mov r0, #14
    str r0, [sp, #0x4]
    mov r0, #1
    str r0, [sp, #0x8]
    mov r0, #0
    str r0, [sp, #0xc]
    add r0, r9, #12
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    mov r1, r5
    bl native_fn_0204a724
    sub r0, r11, r7
    mov r0, r0, lsl #16
    mov r3, r0, asr #16
    b ov000_021fcd4c_L724
ov000_021fcd4c_L6ec:
    mov r0, #2
    str r0, [sp]
    mov r0, #24
    str r0, [sp, #0x4]
    mov r0, #1
    str r0, [sp, #0x8]
    mov r0, #0
    str r0, [sp, #0xc]
    add r0, r9, #12
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    mov r1, r5
    bl native_fn_0204a724
    b ov000_021fcd4c_L9ac
ov000_021fcd4c_L724:
    strh r4, [sp, #52]
    mov r0, #3
    str r0, [sp]
    mov r0, #0
    str r0, [sp, #0x4]
    add r0, r9, #12
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    mov r1, r5
    mov r2, #1
    bl native_fn_0204a1d0
    b ov000_021fcd4c_L9ac
ov000_021fcd4c_L754:
    add r0, r1, r7, lsl #2
    ldr r8, [r0, #0x1ec]
    ldrb r0, [r10, #0x31]
    cmp r8, r0
    bne ov000_021fcd4c_L7dc
    mov r0, #8
    strh r0, [sp, #52]
    mov r0, #19
    str r0, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    str r0, [sp, #0x8]
    add r0, r9, #5
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    mov r1, r5
    mov r2, #5
    mov r3, #1
    bl native_fn_0204a574
    ldrsh r1, [sp, #52]
    mov r0, r8, lsl #16
    mov r3, r0, asr #16
    add r1, r1, #8
    add r0, r9, #5
    strh r1, [sp, #52]
    mov r1, #0
    mov r0, r0, lsl #24
    str r1, [sp]
    str r1, [sp, #0x4]
    mov r0, r0, asr #24
    mov r1, r5
    mov r2, #1
    bl native_fn_0204a448
    b ov000_021fcd4c_L9ac
ov000_021fcd4c_L7dc:
    cmp r8, #0
    beq ov000_021fcd4c_L800
    mov r0, r8
    bl native_fn_02065d88
    ldrb r1, [r0, #0x2d]
    mov r0, r10
    bl native_fn_02211064
    cmp r0, #0
    bne ov000_021fcd4c_L870
ov000_021fcd4c_L800:
    mov r0, r8, lsl #16
    mov r3, r0, asr #16
    mov r0, #0
    str r0, [sp]
    str r0, [sp, #0x4]
    add r0, r9, #5
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    mov r1, r5
    mov r2, #3
    bl native_fn_0204a448
    strh r4, [sp, #52]
    mov r0, #2
    str r0, [sp]
    mov r0, #24
    str r0, [sp, #0x4]
    mov r0, #3
    str r0, [sp, #0x8]
    mov r0, #0
    str r0, [sp, #0xc]
    add r0, r9, #12
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    mov r1, r5
    mov r2, #0
    mov r3, #5
    bl native_fn_0204a724
    b ov000_021fcd4c_L9ac
ov000_021fcd4c_L870:
    ldrb r0, [r10, #0x31]
    mov r7, #1
    bl native_fn_02065d88
    ldrh r0, [r0, #28]
    str r0, [sp, #0x18]
    mov r0, r8
    bl native_fn_02065d88
    ldrh r11, [r0, #28]
    mov r0, r8
    bl native_fn_02062d04
    cmp r0, #0
    mov r0, r8, lsl #16
    mov r3, r0, asr #16
    mov r0, #0
    str r0, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    add r0, r9, #5
    movle r7, #3
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    mov r1, r5
    mov r2, r7
    bl native_fn_0204a448
    ldr r0, [sp, #0x2c]
    strh r0, [sp, #52]
    ldr r0, [sp, #0x18]
    sub r8, r11, r0
    cmp r8, #0
    ble ov000_021fcd4c_L930
    mov r0, #1
    str r0, [sp]
    mov r0, #13
    str r0, [sp, #0x4]
    mov r0, #1
    str r0, [sp, #0x8]
    mov r0, #0
    str r0, [sp, #0xc]
    add r0, r9, #12
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    mov r1, r5
    mov r2, #0
    mov r3, #5
    bl native_fn_0204a724
    mov r0, r8, lsl #16
    mov r3, r0, asr #16
    b ov000_021fcd4c_L980
ov000_021fcd4c_L930:
    bge ov000_021fcd4c_L9ac
    mov r0, #1
    str r0, [sp]
    mov r0, #14
    str r0, [sp, #0x4]
    mov r0, #1
    str r0, [sp, #0x8]
    mov r0, #0
    str r0, [sp, #0xc]
    add r0, r9, #12
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    mov r1, r5
    mov r2, #0
    mov r3, #5
    bl native_fn_0204a724
    ldr r0, [sp, #0x18]
    sub r0, r0, r11
    mov r0, r0, lsl #16
    mov r3, r0, asr #16
ov000_021fcd4c_L980:
    strh r4, [sp, #52]
    mov r0, #3
    str r0, [sp]
    mov r0, #0
    str r0, [sp, #0x4]
    add r0, r9, #12
    mov r0, r0, lsl #24
    mov r2, r7
    mov r0, r0, asr #24
    mov r1, r5
    bl native_fn_0204a1d0
ov000_021fcd4c_L9ac:
    add r9, r9, #1
    ldrh r0, [r6, #12]
    cmp r9, r0
    blt ov000_021fcd4c_L508
ov000_021fcd4c_L9bc:
    ldr r1, [r6]
    ldr r0, [sp, #0x14]
    cmp r1, r0
    blt ov000_021fcd4c_La38
    ldrh r2, [r6, #14]
    ldr r0, [r6, #0x4]
    mov r1, #16
    sub r0, r2, r0
    sub r4, r0, #1
    strh r1, [sp, #48]
    mov r1, #34
    add r0, r4, #5
    str r1, [sp]
    mov r3, #1
    mov r0, r0, lsl #24
    str r3, [sp, #0x4]
    str r3, [sp, #0x8]
    add r1, sp, #48
    mov r0, r0, asr #24
    mov r2, #5
    mov r3, #2
    bl native_fn_0204a574
    add r0, r4, #12
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02049ad0
    ldr r0, [r0]
    mov r1, #0
    ldr r0, [r0, #0x4]
    ldr r0, [r0, #0x44]
    bl native_fn_02087e44
ov000_021fcd4c_La38:
    ldr r1, [r6]
    cmp r1, #0
    ldrneh r0, [r6, #14]
    subne r0, r0, #1
    cmpne r1, r0
    beq ov000_021fcd4c_Lb34
    ldr r0, =0x022372a8
    ldr r0, [r0, #0xc]
    add r0, r0, r1, lsl #2
    ldr r4, [r0, #0x1ec]
    mov r0, r4
    bl native_fn_02063144
    mov r1, #0
    strh r1, [sp, #52]
    ands r7, r0, #255
    beq ov000_021fcd4c_Lb00
    ldrb r0, [r10, #0x31]
    mov r5, #1
    cmp r4, r0
    beq ov000_021fcd4c_Lac4
    cmp r4, #0
    beq ov000_021fcd4c_Lac0
    mov r0, r4
    bl native_fn_02065d88
    mov r1, r0
    mov r0, r10
    ldrb r1, [r1, #0x2d]
    bl native_fn_02211064
    cmp r0, #0
    beq ov000_021fcd4c_Lac0
    mov r0, r4
    bl native_fn_02062d04
    cmp r0, #0
    bne ov000_021fcd4c_Lac4
ov000_021fcd4c_Lac0:
    mov r5, #3
ov000_021fcd4c_Lac4:
    mov r0, r7
    mov r1, #0
    bl native_fn_02048094
    mov r0, #2
    str r0, [sp]
    mov r0, #67
    stmib sp, {r0, r5}
    mov r0, #1
    str r0, [sp, #0xc]
    add r1, sp, #52
    mov r0, #24
    mov r2, #128
    mov r3, #5
    bl native_fn_0204a724
    b ov000_021fcd4c_Lbbc
ov000_021fcd4c_Lb00:
    mov r0, #16
    strh r0, [sp, #52]
    mov r0, #76
    str r0, [sp]
    mov r4, #1
    str r4, [sp, #0x4]
    add r1, sp, #52
    mov r0, #24
    mov r2, #5
    mov r3, #2
    str r4, [sp, #0x8]
    bl native_fn_0204a574
    b ov000_021fcd4c_Lbbc
ov000_021fcd4c_Lb34:
    mov r0, #24
    mov r4, #1
    bl native_fn_02049ad0
    ldr r0, [r0]
    ldr r0, [r0, #0x4]
    bl native_fn_02049ffc
    ldr r0, [r6]
    cmp r0, #0
    bne ov000_021fcd4c_Lba0
    ldr r0, =0x022372a8
    ldr r0, [r0, #0xc]
    ldr r0, [r0, #0x5f8]
    cmp r0, #0
    beq ov000_021fcd4c_Lb9c
    bl native_fn_02065d88
    ldrb r1, [r0, #0x2d]
    mov r0, r10
    bl native_fn_02211064
    cmp r0, #0
    beq ov000_021fcd4c_Lb9c
    ldr r0, =0x022372a8
    ldrb r1, [r10, #0x31]
    ldr r0, [r0, #0xc]
    ldr r0, [r0, #0x5f8]
    cmp r1, r0
    bne ov000_021fcd4c_Lba0
ov000_021fcd4c_Lb9c:
    mov r4, #3
ov000_021fcd4c_Lba0:
    ldr r3, =native_data_0222f430
    mov r5, #16
    add r1, sp, #52
    mov r2, r4
    mov r0, #24
    strh r5, [sp, #52]
    bl native_fn_0204a104
ov000_021fcd4c_Lbbc:
    mov r1, #5
    mov r4, #0
    mov r0, r6
    mov r2, r1
    mov r3, #7
    str r4, [sp]
    bl native_fn_02049008
    mov r1, #1
    str r1, [sp]
    mov r0, r6
    mov r1, #12
    mov r2, #6
    mov r3, #8
    bl native_fn_02049008
    ldr r0, =0x022372a8
    mov r1, r4
    strb r1, [r0, #0x2]
    strb r1, [r0]
    bl native_fn_02217dbc
    ldr r1, [r6]
    ldr r0, [sp, #0x14]
    cmp r1, r0
    blt ov000_021fcd4c_Lcf0
    add r2, sp, #56
    mov r1, #8
    mov r0, r4
ov000_021fcd4c_Lc24:
    strh r0, [r2]
    strh r0, [r2, #2]
    strh r0, [r2, #4]
    strh r0, [r2, #6]
    add r2, r2, #8
    subs r1, r1, #1
    bne ov000_021fcd4c_Lc24
    ldrh r1, [r6, #14]
    ldr r0, [r6, #0x4]
    sub r0, r1, r0
    sub r4, r0, #1
    add r0, r4, #5
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02049ad0
    ldr r1, [r0]
    mov r0, #0
    ldr r5, [r1, #0x4]
    mov r1, #5
    strh r0, [sp, #48]
    add r0, r5, #60
    mov r2, #2
    mov r3, #34
    bl native_fn_02085284
    add r1, sp, #56
    mov r0, #255
    str r1, [sp]
    str r0, [sp, #0x4]
    ldrb r2, [r5, #0x5e]
    ldrsh r3, [sp, #48]
    ldr r0, =0x021c9698
    ldr r1, [r5, #0x68]
    bl native_fn_02046af4
    ldrh r2, [r5, #108]
    ldr r0, =0x021c9698
    add r1, sp, #56
    bl native_fn_02087d0c
    add r2, r4, #5
    add r3, r4, #12
    str r0, [sp]
    mov r0, #28
    mov r1, r4, lsl #24
    mov r2, r2, lsl #24
    mov r3, r3, lsl #24
    str r0, [sp, #0x4]
    mov r0, r6
    mov r1, r1, asr #24
    mov r2, r2, asr #24
    mov r3, r3, asr #24
    bl native_fn_02217e4c
    str r0, [sp, #0x1c]
ov000_021fcd4c_Lcf0:
    ldrh r0, [r6, #14]
    ldr r1, [r6]
    sub r0, r0, #1
    cmp r1, r0
    movne r0, #224
    ldreq r0, [sp, #0x1c]
    moveq r0, r0, lsl #3
    and r0, r0, #255
    bl native_fn_021fdf28
    ldrh r0, [r6, #14]
    ldr r1, [r6]
    sub r0, r0, #1
    cmp r1, r0
    movne r1, #3
    ldr r0, [sp, #0x28]
    moveq r1, #2
    add r0, r0, #16
    and r1, r1, #255
    bl native_fn_0205fb3c
ov000_021fcd4c_Ld3c:
    ldr r0, [sp, #0x10]
    cmp r0, #2
    addne sp, sp, #120
    ldmneia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    ldrh r0, [r6, #12]
    ldr r2, [sp, #0x24]
    ldr r3, [sp, #0x20]
    sub r0, r0, #1
    mov r0, r0, lsl #24
    mov r1, r6
    mov r0, r0, asr #24
    bl native_fn_02217f78
    ldr r1, =0x022372a8
    ldr r1, [r1, #0xc]
    strb r0, [r1, #0x600]
    add sp, sp, #120
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
