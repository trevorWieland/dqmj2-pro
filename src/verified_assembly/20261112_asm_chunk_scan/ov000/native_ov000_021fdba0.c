/* ov000 row 0x021fdba0: 448 bytes.
 *
 * What it does: Writes 2 blocks of 4 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x1b8 -> native_data_0222b9e8 (image word 0x0222b9e8)
 *   pool +0x1bc -> constant 0x022372a8 (image word 0x022372a8)
 *   back edge +0x30 -> +0x24
 *   branch +0x68 -> +0x9c
 *   branch +0x78 -> +0x9c
 *   back edge +0xa4 -> +0x58
 *   branch +0xc0 -> +0x11c
 *   branch +0xd4 -> +0xf8
 *   branch +0xe8 -> +0xf8
 *   back edge +0xf4 -> +0xd8
 *   branch +0xfc -> +0x11c
 *   branch +0x130 -> +0x174
 *   branch +0x148 -> +0x174
 *   back edge +0x170 -> +0x13c
 *   branch +0x18c -> +0x1a0
 *   back edge +0x1a8 -> +0x184
 *   test +0x64 cmp r0, #7
 *   test +0x74 cmp r0, #0
 *   test +0xa0 cmp r4, #255
 *   test +0xb4 cmp r0, #0
 *   test +0xbc cmpne r3, #0
 *   test +0xd0 cmp r5, #0
 *   test +0xe0 cmp r3, r0
 *   test +0xf0 cmp r1, r5
 *   test +0xf8 cmp r2, #0
 *   test +0x12c cmp r0, #0
 *   test +0x144 cmp r4, #0
 *   test +0x16c cmp r5, r0
 *   test +0x188 cmp r2, #0
 *   test +0x1a4 cmp r5, #255
 *   9 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021fdba0; the literal pool and
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

extern u8 native_data_0222b9e8[];
extern void native_fn_02065d88(void);
extern void native_fn_02063144(void);


asm u32 native_ov000_021fdba0 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    sub sp, sp, #8
    sub sp, sp, #1024
    mov r0, #0
    add r5, sp, #8
    mov r1, r0
    mov r2, r0
    mov r3, r0
    mov r4, #32
ov000_021fdba0_L24:
    stmia r5!, {r0, r1, r2, r3}
    stmia r5!, {r0, r1, r2, r3}
    subs r4, r4, #1
    bne ov000_021fdba0_L24
    ldr r0, =native_data_0222b9e8
    ldr r5, =0x022372a8
    ldr r2, [r0]
    ldr r1, [r0, #0x4]
    ldr r0, [r5, #0xc]
    mov r4, #0
    str r2, [sp]
    str r1, [sp, #0x4]
    str r4, [r0, #0x5f0]
ov000_021fdba0_L58:
    mov r0, r4
    bl native_fn_02065d88
    ldrb r0, [r0, #0x2c]
    cmp r0, #7
    bne ov000_021fdba0_L9c
    mov r0, r4
    bl native_fn_02063144
    cmp r0, #0
    ble ov000_021fdba0_L9c
    ldr r1, [r5, #0xc]
    ldr r0, [r1, #0x5f0]
    add r0, r1, r0, lsl #2
    str r4, [r0, #0x1f0]
    ldr r1, [r5, #0xc]
    ldr r0, [r1, #0x5f0]
    add r0, r0, #1
    str r0, [r1, #0x5f0]
ov000_021fdba0_L9c:
    add r4, r4, #1
    cmp r4, #255
    blt ov000_021fdba0_L58
    ldr r0, =0x022372a8
    ldr r4, [r0, #0xc]
    ldr r0, [r4, #0x5f4]
    cmp r0, #0
    ldrneb r3, [r0, #0x31]
    cmpne r3, #0
    beq ov000_021fdba0_L11c
    ldr r5, [r4, #0x5f0]
    mov r2, #0
    mov r1, r2
    cmp r5, #0
    ble ov000_021fdba0_Lf8
ov000_021fdba0_Ld8:
    add r0, r4, r1, lsl #2
    ldr r0, [r0, #0x1f0]
    cmp r3, r0
    moveq r2, #1
    beq ov000_021fdba0_Lf8
    add r1, r1, #1
    cmp r1, r5
    blt ov000_021fdba0_Ld8
ov000_021fdba0_Lf8:
    cmp r2, #0
    bne ov000_021fdba0_L11c
    add r1, r4, r5, lsl #2
    ldr r0, =0x022372a8
    str r3, [r1, #0x1f0]
    ldr r1, [r0, #0xc]
    ldr r0, [r1, #0x5f0]
    add r0, r0, #1
    str r0, [r1, #0x5f0]
ov000_021fdba0_L11c:
    ldr r6, =0x022372a8
    mov r5, #0
    ldr r1, [r6, #0xc]
    ldr r0, [r1, #0x5f0]
    cmp r0, #0
    ble ov000_021fdba0_L174
    add r8, sp, #0
    add r7, sp, #8
ov000_021fdba0_L13c:
    add r0, r1, r5, lsl #2
    ldr r4, [r0, #0x1f0]
    cmp r4, #0
    beq ov000_021fdba0_L174
    ldrb r1, [r6, #0x1]
    mov r0, r4
    ldr r1, [r8, r1, lsl #2]
    blx r1
    ldr r1, [r6, #0xc]
    str r4, [r7, r0, lsl #2]
    ldr r0, [r1, #0x5f0]
    add r5, r5, #1
    cmp r5, r0
    blt ov000_021fdba0_L13c
ov000_021fdba0_L174:
    mov r4, #0
    ldr r0, =0x022372a8
    mov r5, r4
    add r3, sp, #8
ov000_021fdba0_L184:
    ldr r2, [r3, r5, lsl #2]
    cmp r2, #0
    beq ov000_021fdba0_L1a0
    ldr r1, [r0, #0xc]
    add r1, r1, r4, lsl #2
    str r2, [r1, #0x1f0]
    add r4, r4, #1
ov000_021fdba0_L1a0:
    add r5, r5, #1
    cmp r5, #255
    blt ov000_021fdba0_L184
    add sp, sp, #8
    add sp, sp, #1024
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
