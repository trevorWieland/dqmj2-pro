/* ov006 row 0x022026d8: 260 bytes.
 *
 * What it does: Writes one block of 4 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0xfc -> constant 0x0221c16c (image word 0x0221c16c)
 *   pool +0x100 -> constant 0x00000a93 (image word 0x00000a93)
 *   branch +0x0c -> +0x32
 *   branch +0x30 -> +0x54
 *   branch +0x5a -> +0xf8
 *   branch +0x66 -> +0x78
 *   branch +0x82 -> +0x90
 *   branch +0x8e -> +0xae
 *   branch +0x9e -> +0xae
 *   branch +0xbe -> +0xe2
 *   branch +0xe0 -> +0xee
 *   back edge +0xf6 -> +0xb6
 *   test +0x0a cmp r6, #0x1
 *   test +0x58 cmp r0, #0x5
 *   test +0x64 cmp r0, #0x0
 *   test +0x80 cmp r1, #0x0
 *   test +0x9c cmp r0, #0x3
 *   test +0xbc cmp r0, #0x0
 *   test +0xf4 cmp r5, #0x2
 *   0 block transfer(s), 11 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x022026d8; the literal pool and
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

extern void native_fn_02008e0c(void);
extern void native_fn_02201820(void);
extern void native_fn_02201c84(void);
extern void native_fn_02201810(void);
extern void native_fn_02201c64(void);


asm u32 native_ov006_022026d8 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    ldr r4, =0x0221c16c
    ldr r3, =0x00000a93
    ldr r5, [r4, #0]
    ldrb r6, [r5, r3]
    cmp r6, #0x1
    bne ov006_022026d8_L32
    add r6, r3, #0x0
    add r6, #0x1d
    ldr r5, [r5, r6]
    strh r0, [r5, #0]
    add r0, r3, #0x0
    ldr r5, [r4, #0]
    add r0, #0x1d
    ldr r0, [r5, r0]
    add r3, #0x1d
    strh r1, [r0, #0x2]
    ldr r1, [r4, #0]
    add r0, r2, #0x0
    ldr r1, [r1, r3]
    mov r2, #0x40
    add r1, r1, #0x4
    blx native_fn_02008e0c
    b ov006_022026d8_L54
ov006_022026d8_L32:
    mov r0, #0x81
    lsl r0, r0, #0x2
    ldr r1, [r5, r0]
    mov r2, #0xbc
    add r1, r1, #0x1
    str r1, [r5, r0]
    add r0, r3, #0x0
    ldr r1, [r4, #0]
    add r0, #0x1d
    ldr r0, [r1, r0]
    strh r2, [r0, #0]
    sub r0, r3, #0x1
    ldr r2, [r4, #0]
    add r3, #0x1d
    ldrb r1, [r2, r0]
    ldr r0, [r2, r3]
    strb r1, [r0, #0x4]
ov006_022026d8_L54:
    bl native_fn_02201820
    cmp r0, #0x5
    bne ov006_022026d8_Lf8
    ldr r0, =0x0221c16c
    ldr r0, [r0, #0]
    bl native_fn_02201c84
    cmp r0, #0x0
    bne ov006_022026d8_L78
    ldr r0, =0x0221c16c
    ldr r2, [r0, #0]
    mov r0, #0x81
    lsl r0, r0, #0x2
    ldr r1, [r2, r0]
    add r1, r1, #0x4
    str r1, [r2, r0]
    pop {r3, r4, r5, r6, r7, pc}
ov006_022026d8_L78:
    ldr r0, =0x0221c16c
    ldr r1, =0x00000a93
    ldr r0, [r0, #0]
    ldrb r1, [r0, r1]
    cmp r1, #0x0
    bne ov006_022026d8_L90
    mov r1, #0x81
    lsl r1, r1, #0x2
    ldr r2, [r0, r1]
    add r2, r2, #0x1
    str r2, [r0, r1]
    b ov006_022026d8_Lae
ov006_022026d8_L90:
    mov r1, #0x81
    mov r2, #0x0
    lsl r1, r1, #0x2
    str r2, [r0, r1]
    bl native_fn_02201810
    cmp r0, #0x3
    beq ov006_022026d8_Lae
    ldr r0, =0x0221c16c
    mov r2, #0x1b
    ldr r1, [r0, #0]
    mov r0, #0xa9
    lsl r0, r0, #0x4
    strb r2, [r1, r0]
    pop {r3, r4, r5, r6, r7, pc}
ov006_022026d8_Lae:
    mov r5, #0x0
    ldr r4, =0x0221c16c
    add r7, r5, #0x0
    mov r6, #0x1
ov006_022026d8_Lb6:
    add r0, r5, #0x0
    bl native_fn_02201c64
    cmp r0, #0x0
    beq ov006_022026d8_Le2
    mov r1, #0x1
    ldr r2, [r4, #0]
    lsl r1, r1, #0x8
    add r1, r2, r1
    mov r2, #0x44
    mul r2, r5
    add r1, r1, r2
    mov r2, #0x44
    blx native_fn_02008e0c
    ldr r1, [r4, #0]
    lsl r0, r5, #0x2
    add r1, r1, r0
    mov r0, #0x82
    lsl r0, r0, #0x2
    str r6, [r1, r0]
    b ov006_022026d8_Lee
ov006_022026d8_Le2:
    ldr r1, [r4, #0]
    lsl r0, r5, #0x2
    add r1, r1, r0
    mov r0, #0x82
    lsl r0, r0, #0x2
    str r7, [r1, r0]
ov006_022026d8_Lee:
    add r0, r5, #0x1
    lsl r0, r0, #0x10
    lsr r5, r0, #0x10
    cmp r5, #0x2
    blo ov006_022026d8_Lb6
ov006_022026d8_Lf8:
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
}
