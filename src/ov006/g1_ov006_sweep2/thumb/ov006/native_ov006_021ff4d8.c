/* ov006 row 0x021ff4d8: 236 bytes.
 *
 * What it does: Writes one block of 2 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0xe0 -> constant 0x0221c148 (image word 0x0221c148)
 *   pool +0xe4 -> constant 0x000001ef (image word 0x000001ef)
 *   pool +0xe8 -> constant 0x000004f8 (image word 0x000004f8)
 *   branch +0x2e -> +0x90
 *   branch +0x3c -> +0x40
 *   branch +0x42 -> +0x6a
 *   branch +0x46 -> +0x6a
 *   branch +0x68 -> +0x90
 *   branch +0x6c -> +0x90
 *   branch +0x70 -> +0x90
 *   branch +0x9c -> +0xb4
 *   back edge +0xc0 -> +0x98
 *   test +0x2c cmp r5, #0x2
 *   test +0x3a tst r2, r4
 *   test +0x40 cmp r6, #0xff
 *   test +0x44 cmp r7, #0x0
 *   test +0x6a cmp r6, #0xff
 *   test +0x6e cmp r7, #0x0
 *   test +0x9a cmp r0, #0x0
 *   test +0xbe cmp r6, #0x4
 *   0 block transfer(s), 11 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ff4d8; the literal pool and
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
extern void native_fn_02019b80(void);
extern void native_fn_02203c08(void);
extern void native_fn_020a47ec(void);
extern void native_fn_02203c20(void);


asm u32 native_ov006_021ff4d8 (register u32 a0)
{
    push {r4, r5, r6, r7, lr}
    sub sp, #0x14
    add r5, r0, #0x0
    ldr r0, =0x0221c148
    mov r7, #0x0
    ldr r1, [r0, #0]
    lsl r0, r5, #0x8
    add r0, r1, r0
    add r0, #0xe7
    ldrb r6, [r0, #0]
    mov r0, #0x1
    add r4, r0, #0x0
    add r0, sp, #0x4
    add r1, r7, #0x0
    mov r2, #0x10
    lsl r4, r5
    blx native_fn_02008d78
    mov r0, #0x1
    lsl r2, r5, #0x2
    add r1, sp, #0x4
    str r0, [r1, r2]
    cmp r5, #0x2
    bgt ov006_021ff4d8_L90
    ldr r1, =0x0221c148
    ldr r1, [r1, #0]
    add r2, r1, #0x0
    add r2, #0xef
    ldrb r2, [r2, #0]
    tst r2, r4
    beq ov006_021ff4d8_L40
    add r7, r0, #0x0
ov006_021ff4d8_L40:
    cmp r6, #0xff
    bne ov006_021ff4d8_L6a
    cmp r7, #0x0
    beq ov006_021ff4d8_L6a
    add r2, r1, #0x0
    add r2, #0xef
    ldrb r2, [r2, #0]
    add r1, #0xef
    mvn r0, r4
    bic r2, r4
    strb r2, [r1, #0]
    ldr r1, =0x0221c148
    ldr r3, [r1, #0]
    ldr r1, =0x000001ef
    ldrb r2, [r3, r1]
    and r0, r2
    strb r0, [r3, r1]
    mov r0, #0x1
    str r0, [sp, #0x8]
    str r0, [sp, #0x4]
    b ov006_021ff4d8_L90
ov006_021ff4d8_L6a:
    cmp r6, #0xff
    beq ov006_021ff4d8_L90
    cmp r7, #0x0
    bne ov006_021ff4d8_L90
    add r0, r1, #0x0
    add r0, #0xef
    ldrb r0, [r0, #0]
    add r1, #0xef
    orr r0, r4
    strb r0, [r1, #0]
    ldr r0, =0x0221c148
    ldr r2, [r0, #0]
    ldr r0, =0x000001ef
    ldrb r1, [r2, r0]
    orr r1, r4
    strb r1, [r2, r0]
    mov r0, #0x1
    str r0, [sp, #0x8]
    str r0, [sp, #0x4]
ov006_021ff4d8_L90:
    mov r6, #0x0
    ldr r7, =0x0221c148
    add r4, sp, #0x4
    add r5, r6, #0x0
ov006_021ff4d8_L98:
    ldr r0, [r4, #0]
    cmp r0, #0x0
    beq ov006_021ff4d8_Lb4
    ldr r1, [r7, #0]
    ldr r0, =0x000004f8
    mov r2, #0xfe
    add r0, r1, r0
    add r1, r1, r5
    blx native_fn_02019b80
    ldr r1, [r7, #0]
    add r1, r1, r5
    add r1, #0xfe
    strh r0, [r1, #0]
ov006_021ff4d8_Lb4:
    mov r0, #0x1
    lsl r0, r0, #0x8
    add r6, r6, #0x1
    add r4, r4, #0x4
    add r5, r5, r0
    cmp r6, #0x4
    blt ov006_021ff4d8_L98
    mov r1, #0x20
    bl native_fn_02203c08
    add r2, r0, #0x0
    ldr r0, =0x0221c148
    add r1, sp, #0x4
    ldr r0, [r0, #0]
    str r2, [sp]
    bl native_fn_020a47ec
    add r0, sp, #0x0
    bl native_fn_02203c20
    add sp, #0x14
    pop {r4, r5, r6, r7, pc}
}
