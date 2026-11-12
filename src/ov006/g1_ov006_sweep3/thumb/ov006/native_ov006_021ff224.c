/* ov006 row 0x021ff224: 288 bytes.
 *
 * What it does: 137 instructions; 6 call(s) to 0x02008d78, 0x02008e0c, 0x02008e0c, +3 more; loops (back edge at +0x12); returns through pop {r3, r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x11c -> constant 0x0221c148 (image word 0x0221c148)
 *   branch +0x2a -> +0x36
 *   branch +0x2e -> +0x56
 *   branch +0x32 -> +0x76
 *   branch +0x34 -> +0x98
 *   branch +0x54 -> +0xb4
 *   branch +0x74 -> +0xb4
 *   branch +0x96 -> +0xb4
 *   back edge +0xea -> +0xd8
 *   test +0x28 cmp r0, #0x1
 *   test +0x2c cmp r0, #0x2
 *   test +0x30 cmp r0, #0x3
 *   test +0xe8 cmp r7, #0x4
 *   0 block transfer(s), 12 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ff224; the literal pool and
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

extern void native_fn_02008d78(void);
extern void native_fn_02008e0c(void);
extern void native_fn_021ff174(void);


asm u32 native_ov006_021ff224 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    add r5, r0, #0x0
    ldr r0, =0x0221c148
    mov r1, #0x0
    ldr r6, [r0, #0]
    mov r0, #0x1
    lsl r0, r0, #0xa
    add r0, r6, r0
    mov r2, #0xef
    blx native_fn_02008d78
    mov r1, #0x1
    lsl r1, r1, #0xa
    add r1, r6, r1
    add r0, r5, #0x0
    add r1, #0x40
    mov r2, #0x20
    blx native_fn_02008e0c
    ldr r0, [r5, #0x20]
    cmp r0, #0x1
    beq ov006_021ff224_L36
    cmp r0, #0x2
    beq ov006_021ff224_L56
    cmp r0, #0x3
    beq ov006_021ff224_L76
    b ov006_021ff224_L98
ov006_021ff224_L36:
    mov r0, #0x1
    lsl r0, r0, #0xa
    add r0, r6, r0
    add r0, #0xe6
    ldrb r1, [r0, #0]
    mov r0, #0x3
    bic r1, r0
    mov r0, #0x1
    orr r1, r0
    lsl r0, r0, #0xa
    add r0, r6, r0
    add r0, #0xe6
    strb r1, [r0, #0]
    mov r0, #0x5
    str r0, [sp]
    b ov006_021ff224_Lb4
ov006_021ff224_L56:
    mov r0, #0x1
    lsl r0, r0, #0xa
    add r0, r6, r0
    add r0, #0xe6
    ldrb r1, [r0, #0]
    mov r0, #0x3
    bic r1, r0
    mov r0, #0x2
    orr r1, r0
    lsl r0, r0, #0x9
    add r0, r6, r0
    add r0, #0xe6
    strb r1, [r0, #0]
    mov r0, #0xd
    str r0, [sp]
    b ov006_021ff224_Lb4
ov006_021ff224_L76:
    mov r0, #0x1
    lsl r0, r0, #0xa
    add r0, r6, r0
    add r0, #0xe6
    ldrb r1, [r0, #0]
    mov r0, #0x3
    bic r1, r0
    mov r0, #0x3
    orr r1, r0
    mov r0, #0x1
    lsl r0, r0, #0xa
    add r0, r6, r0
    add r0, #0xe6
    strb r1, [r0, #0]
    mov r0, #0x10
    str r0, [sp]
    b ov006_021ff224_Lb4
ov006_021ff224_L98:
    mov r0, #0x1
    lsl r0, r0, #0xa
    add r0, r6, r0
    add r0, #0xe6
    ldrb r1, [r0, #0]
    mov r0, #0x3
    bic r1, r0
    mov r0, #0x1
    lsl r0, r0, #0xa
    add r0, r6, r0
    add r0, #0xe6
    strb r1, [r0, #0]
    mov r0, #0x0
    str r0, [sp]
ov006_021ff224_Lb4:
    mov r0, #0x1
    lsl r0, r0, #0xa
    add r0, r6, r0
    add r0, #0xe6
    ldrb r1, [r0, #0]
    mov r0, #0xfc
    mov r7, #0x0
    bic r1, r0
    mov r0, #0x1
    lsl r0, r0, #0xa
    add r0, r6, r0
    add r0, #0xe6
    strb r1, [r0, #0]
    mov r0, #0x1
    lsl r0, r0, #0xa
    add r4, r6, r0
    add r4, #0x80
    add r5, #0x28
ov006_021ff224_Ld8:
    ldr r2, [sp]
    add r0, r5, #0x0
    add r1, r4, #0x0
    blx native_fn_02008e0c
    add r7, r7, #0x1
    add r4, #0x10
    add r5, #0x20
    cmp r7, #0x4
    blt ov006_021ff224_Ld8
    mov r1, #0x2
    lsl r0, r1, #0x9
    add r0, r6, r0
    add r0, #0xe7
    strb r1, [r0, #0]
    lsl r0, r1, #0x9
    add r0, r6, r0
    add r0, #0xf0
    mov r1, #0x0
    mov r2, #0x4
    blx native_fn_02008d78
    mov r1, #0x1
    lsl r0, r1, #0xa
    add r0, r6, r0
    add r0, #0xf5
    strb r1, [r0, #0]
    lsl r0, r1, #0xa
    add r0, r6, r0
    add r0, #0xf6
    strb r1, [r0, #0]
    bl native_fn_021ff174
    pop {r3, r4, r5, r6, r7, pc}
}
