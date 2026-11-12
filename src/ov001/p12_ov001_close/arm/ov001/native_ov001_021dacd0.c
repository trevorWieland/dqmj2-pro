/* ov001 row 0x021dacd0: 504 bytes.
 *
 * What it does: 126 instructions; 20 call(s) to 0x021d8dec, 0x022094bc, 0x021dad74, +17 more; loops (back edge at +0x48); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: loop with 20 calls (126 instructions, 20 calls, 14 branches, 7 back edges, 0 literal slots).
 *
 *   branch +0x40 -> +0x1cc
 *   branch +0x54 -> +0x1c0
 *   branch +0x58 -> +0x68
 *   branch +0x64 -> +0x6c
 *   branch +0x84 -> +0x128
 *   branch +0x8c -> +0xa4
 *   branch +0xa0 -> +0x128
 *   branch +0xc8 -> +0x120
 *   branch +0xd0 -> +0x128
 *   branch +0xe0 -> +0xf4
 *   branch +0x10c -> +0x128
 *   branch +0x11c -> +0x128
 *   branch +0x12c -> +0x150
 *   branch +0x13c -> +0x150
 *   branch +0x154 -> +0x160
 *   branch +0x15c -> +0x170
 *   branch +0x164 -> +0x188
 *   branch +0x16c -> +0x188
 *   branch +0x178 -> +0x188
 *   branch +0x198 -> +0x1b0
 *   branch +0x1bc -> +0x1cc
 *   back edge +0x1e8 -> +0x1c
 *   test +0x3c cmp r5, r6
 *   test +0x50 cmp r5, #0
 *   test +0x60 cmp r9, #0
 *   test +0x80 cmp r9, #0
 *   test +0x88 cmp r7, #0
 *   test +0x9c cmp r0, #0
 *   test +0xc4 cmp r0, #0
 *   test +0xcc cmp r7, #0
 *   test +0xdc cmp r0, #0
 *   test +0xfc tst r0, #1
 *   test +0x108 cmp r0, #0
 *   test +0x128 cmp r7, #0
 *   test +0x138 cmp r0, #0
 *   test +0x150 cmp r6, #0
 *   test +0x158 cmp r5, #0
 *   test +0x160 cmp r6, #0
 *   test +0x168 cmp r5, #0
 *   test +0x174 cmp r0, #0
 *   test +0x194 tst r0, #64
 *   test +0x1d4 cmp r0, #0
 *   test +0x1e4 cmp r4, #60
 *   0 block transfer(s), 9 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021dacd0; the literal pool and
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

extern void native_fn_021d8dec(void);
extern void native_fn_022094bc(void);
extern void native_fn_0205d790(void);
extern void native_fn_021eec7c(void);
extern void native_fn_021db8d0(void);
extern void native_fn_022047ec(void);
extern void native_fn_0205d7cc(void);
extern void native_fn_021dab28(void);


asm u32 native_ov001_021dacd0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #16
    mov r10, r0
    mov r4, #0
    add r0, r10, #93
    str r4, [sp, #0x4]
    str r0, [sp, #0xc]
ov001_021dacd0_L1c:
    add r11, r10, r4
    add r1, r11, #512
    add r0, r11, #768
    ldrsb r6, [r0, #158]
    ldrsb r5, [r1, #44]
    mov r0, #1
    str r0, [sp]
    ldrsb r7, [r1, #104]
    cmp r5, r6
    beq ov001_021dacd0_L1cc
    mov r0, r4
    bl native_fn_021d8dec
    mov r8, r0
    cmp r5, #0
    beq ov001_021dacd0_L1c0
    bgt ov001_021dacd0_L68
    ldrsh r9, [r8, #10]
    cmp r9, #0
    bne ov001_021dacd0_L6c
ov001_021dacd0_L68:
    ldrsh r9, [r8, #4]
ov001_021dacd0_L6c:
    mov r2, r7
    mov r0, r4
    mov r1, r5
    bl native_fn_022094bc
    mov r7, r0
    cmp r9, #0
    beq ov001_021dacd0_L128
    cmp r7, #0
    blt ov001_021dacd0_La4
    add r0, r10, r7
    add r0, r0, #768
    ldrsb r0, [r0, #218]
    cmp r0, #0
    bne ov001_021dacd0_L128
ov001_021dacd0_La4:
    mov r0, r9
    bl native_fn_0205d790
    mov r2, r0
    mov r0, r9
    mov r1, r10
    bl native_fn_021eec7c
    add r0, r0, #1
    str r0, [sp, #0x8]
    cmp r0, #0
    ble ov001_021dacd0_L120
    cmp r7, #0
    blt ov001_021dacd0_L128
    mov r0, r10
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_021dacd0_Lf4
    ldrb r0, [r10, #0x31e]
    ldrb r1, [r10, #0x31f]
    mov r2, r7
    bl native_fn_022047ec
ov001_021dacd0_Lf4:
    mov r0, r9
    bl native_fn_0205d7cc
    tst r0, #1
    movne r0, #1
    moveq r0, #0
    cmp r0, #0
    beq ov001_021dacd0_L128
    ldr r0, [sp, #0x8]
    add r1, r10, r7
    strb r0, [r1, #0x3da]
    b ov001_021dacd0_L128
ov001_021dacd0_L120:
    mov r0, #0
    str r0, [sp]
ov001_021dacd0_L128:
    cmp r7, #0
    blt ov001_021dacd0_L150
    mov r0, r10
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_021dacd0_L150
    mov r2, r7
    ldrb r0, [r10, #0x31e]
    ldrb r1, [r10, #0x31f]
    bl native_fn_022047ec
ov001_021dacd0_L150:
    cmp r6, #0
    ble ov001_021dacd0_L160
    cmp r5, #0
    blt ov001_021dacd0_L170
ov001_021dacd0_L160:
    cmp r6, #0
    bge ov001_021dacd0_L188
    cmp r5, #0
    ble ov001_021dacd0_L188
ov001_021dacd0_L170:
    ldrsh r0, [r8, #10]
    cmp r0, #0
    beq ov001_021dacd0_L188
    mov r0, r10
    mov r1, r4
    bl native_fn_021dab28
ov001_021dacd0_L188:
    mov r0, r4
    bl native_fn_021d8dec
    ldrb r0, [r0, #0x3]
    tst r0, #64
    beq ov001_021dacd0_L1b0
    ldr r0, [sp, #0xc]
    ldrb r0, [r0, #0x300]
    orr r1, r0, #2
    ldr r0, [sp, #0xc]
    strb r1, [r0, #0x300]
ov001_021dacd0_L1b0:
    ldr r0, [sp, #0x4]
    add r0, r0, #1
    str r0, [sp, #0x4]
    b ov001_021dacd0_L1cc
ov001_021dacd0_L1c0:
    mov r0, r10
    mov r1, r4
    bl native_fn_021dab28
ov001_021dacd0_L1cc:
    ldr r0, [sp]
    add r4, r4, #1
    cmp r0, #0
    addne r0, r11, #512
    ldrnesb r0, [r0, #44]
    strneb r0, [r11, #0x39e]
    cmp r4, #60
    blt ov001_021dacd0_L1c
    ldr r0, [sp, #0x4]
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
