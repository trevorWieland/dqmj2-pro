/* ov006 row 0x021fee28: 280 bytes.
 *
 * What it does: Writes one block of 2 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x110 -> constant 0x0221c148 (image word 0x0221c148)
 *   pool +0x114 -> constant 0x000004e6 (image word 0x000004e6)
 *   branch +0x24 -> +0x2e
 *   branch +0x26 -> +0x3a
 *   branch +0x2a -> +0x3a
 *   branch +0x2c -> +0x78
 *   branch +0x30 -> +0x36
 *   branch +0x32 -> +0x3a
 *   branch +0x34 -> +0x78
 *   branch +0x38 -> +0x78
 *   branch +0x52 -> +0x98
 *   back edge +0x74 -> +0x54
 *   branch +0x76 -> +0x98
 *   branch +0x9a -> +0xa4
 *   branch +0x9c -> +0xcc
 *   branch +0xa0 -> +0xba
 *   branch +0xa2 -> +0xf8
 *   branch +0xa6 -> +0xb4
 *   branch +0xaa -> +0xf8
 *   branch +0xac -> +0xcc
 *   branch +0xb0 -> +0xe2
 *   branch +0xb2 -> +0xf8
 *   branch +0xb6 -> +0xe2
 *   branch +0xb8 -> +0xf8
 *   test +0x22 cmp r5, #0xa
 *   test +0x28 cmp r5, #0x0
 *   test +0x2e cmp r5, #0x1a
 *   test +0x36 cmp r5, #0x20
 *   test +0x50 cmp r5, #0x0
 *   test +0x72 cmp r4, r5
 *   test +0x98 cmp r5, #0x5
 *   test +0x9e cmp r5, #0x0
 *   test +0xa4 cmp r5, #0xd
 *   test +0xa8 cmp r5, #0xa
 *   test +0xae cmp r5, #0xd
 *   test +0xb4 cmp r5, #0x1a
 *   0 block transfer(s), 9 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fee28; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity proves the instruction stream, not the meaning of the fields, blocks and callee contracts it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02008d78(void);
extern void native_fn_022045c8(void);
extern void native_fn_021ff614(void);
extern void native_fn_02008e0c(void);


asm u32 native_ov006_021fee28 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x8
    str r0, [sp]
    ldr r0, =0x0221c148
    mov r2, #0x10
    ldr r1, [r0, #0]
    mov r0, #0x12
    lsl r0, r0, #0x6
    add r0, r1, r0
    mov r1, #0x0
    blx native_fn_02008d78
    ldr r0, [sp]
    mov r1, #0x20
    bl native_fn_022045c8
    add r5, r0, #0x0
    cmp r5, #0xa
    bgt ov006_021fee28_L2e
    bge ov006_021fee28_L3a
    cmp r5, #0x0
    beq ov006_021fee28_L3a
    b ov006_021fee28_L78
ov006_021fee28_L2e:
    cmp r5, #0x1a
    bgt ov006_021fee28_L36
    beq ov006_021fee28_L3a
    b ov006_021fee28_L78
ov006_021fee28_L36:
    cmp r5, #0x20
    bne ov006_021fee28_L78
ov006_021fee28_L3a:
    ldr r2, =0x0221c148
    ldr r1, =0x000004e6
    ldr r4, [r2, #0]
    mov r0, #0xfc
    ldrb r3, [r4, r1]
    bic r3, r0
    strb r3, [r4, r1]
    ldr r0, [r2, #0]
    sub r1, #0x66
    add r6, r0, r1
    mov r4, #0x0
    cmp r5, #0x0
    ble ov006_021fee28_L98
ov006_021fee28_L54:
    ldr r0, [sp]
    add r7, r0, r4
    ldrb r0, [r0, r4]
    bl native_fn_021ff614
    str r0, [sp, #0x4]
    ldrb r0, [r7, #0x1]
    bl native_fn_021ff614
    ldr r1, [sp, #0x4]
    add r4, r4, #0x2
    lsl r1, r1, #0x4
    add r0, r1, r0
    strb r0, [r6, #0]
    add r6, r6, #0x1
    cmp r4, r5
    blt ov006_021fee28_L54
    b ov006_021fee28_L98
ov006_021fee28_L78:
    ldr r3, =0x0221c148
    ldr r2, =0x000004e6
    ldr r0, [r3, #0]
    mov r1, #0xfc
    ldrb r4, [r0, r2]
    bic r4, r1
    mov r1, #0x4
    orr r1, r4
    strb r1, [r0, r2]
    ldr r1, [r3, #0]
    sub r2, #0x66
    add r1, r1, r2
    ldr r0, [sp]
    mov r2, #0x10
    blx native_fn_02008e0c
ov006_021fee28_L98:
    cmp r5, #0x5
    bgt ov006_021fee28_La4
    bge ov006_021fee28_Lcc
    cmp r5, #0x0
    beq ov006_021fee28_Lba
    b ov006_021fee28_Lf8
ov006_021fee28_La4:
    cmp r5, #0xd
    bgt ov006_021fee28_Lb4
    cmp r5, #0xa
    blt ov006_021fee28_Lf8
    beq ov006_021fee28_Lcc
    cmp r5, #0xd
    beq ov006_021fee28_Le2
    b ov006_021fee28_Lf8
ov006_021fee28_Lb4:
    cmp r5, #0x1a
    beq ov006_021fee28_Le2
    b ov006_021fee28_Lf8
ov006_021fee28_Lba:
    ldr r0, =0x0221c148
    ldr r1, =0x000004e6
    ldr r3, [r0, #0]
    mov r0, #0x3
    ldrb r2, [r3, r1]
    add sp, #0x8
    bic r2, r0
    strb r2, [r3, r1]
    pop {r3, r4, r5, r6, r7, pc}
ov006_021fee28_Lcc:
    ldr r0, =0x0221c148
    ldr r1, =0x000004e6
    ldr r3, [r0, #0]
    mov r0, #0x3
    ldrb r2, [r3, r1]
    add sp, #0x8
    bic r2, r0
    mov r0, #0x1
    orr r0, r2
    strb r0, [r3, r1]
    pop {r3, r4, r5, r6, r7, pc}
ov006_021fee28_Le2:
    ldr r0, =0x0221c148
    ldr r1, =0x000004e6
    ldr r3, [r0, #0]
    mov r0, #0x3
    ldrb r2, [r3, r1]
    add sp, #0x8
    bic r2, r0
    mov r0, #0x2
    orr r0, r2
    strb r0, [r3, r1]
    pop {r3, r4, r5, r6, r7, pc}
ov006_021fee28_Lf8:
    ldr r0, =0x0221c148
    ldr r1, =0x000004e6
    ldr r3, [r0, #0]
    mov r0, #0x3
    ldrb r2, [r3, r1]
    bic r2, r0
    mov r0, #0x3
    orr r0, r2
    strb r0, [r3, r1]
    add sp, #0x8
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
}
