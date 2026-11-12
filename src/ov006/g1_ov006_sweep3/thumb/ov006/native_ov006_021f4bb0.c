/* ov006 row 0x021f4bb0: 132 bytes.
 *
 * What it does: 60 instructions; 2 call(s) to 0x021f4b50, 0x021ff6d4; loops (back edge at +0x70); returns through pop {r4, r5, r6, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x7c -> constant 0x0221c060 (image word 0x0221c060)
 *   pool +0x80 -> native_data_0220b4e2 (image word 0x0220b4e2)
 *   branch +0x1c -> +0x2c
 *   branch +0x20 -> +0x26
 *   branch +0x24 -> +0x2c
 *   branch +0x2a -> +0x70
 *   branch +0x32 -> +0x50
 *   branch +0x3a -> +0x40
 *   branch +0x3e -> +0x48
 *   branch +0x46 -> +0x70
 *   branch +0x4e -> +0x70
 *   branch +0x54 -> +0x70
 *   branch +0x5c -> +0x62
 *   branch +0x60 -> +0x6a
 *   branch +0x68 -> +0x70
 *   test +0x1a cmp r3, #0xd
 *   test +0x1e cmp r0, #0x1
 *   test +0x22 cmp r0, #0x3
 *   test +0x30 cmp r3, r0
 *   test +0x38 cmp r0, #0x1
 *   test +0x3c cmp r0, #0xa
 *   test +0x52 cmp r3, r0
 *   test +0x5a cmp r0, #0x1
 *   test +0x5e cmp r0, #0xa
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f4bb0; the literal pool and
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

extern u8 native_data_0220b4e2[];
extern void native_fn_021f4b50(void);
extern void native_fn_021ff6d4(void);


asm u32 native_ov006_021f4bb0 (register u32 a0)
{
    push {r4, r5, r6, lr}
    ldr r4, =0x0221c060
    mov r3, #0x63
    ldr r1, [r4, #0]
    ldr r5, =native_data_0220b4e2
    ldrsb r2, [r1, r3]
    add r1, #0x63
    lsl r6, r2, #0x2
    add r5, r5, r6
    ldrsb r5, [r0, r5]
    strb r5, [r1, #0]
    ldr r1, [r4, #0]
    ldrsb r3, [r1, r3]
    cmp r3, #0xd
    bne ov006_021f4bb0_L2c
    cmp r0, #0x1
    beq ov006_021f4bb0_L26
    cmp r0, #0x3
    bne ov006_021f4bb0_L2c
ov006_021f4bb0_L26:
    add r1, #0x64
    strb r2, [r1, #0]
    b ov006_021f4bb0_L70
ov006_021f4bb0_L2c:
    mov r0, #0x0
    mvn r0, r0
    cmp r3, r0
    bne ov006_021f4bb0_L50
    mov r0, #0x64
    ldrsb r0, [r1, r0]
    cmp r0, #0x1
    beq ov006_021f4bb0_L40
    cmp r0, #0xa
    bne ov006_021f4bb0_L48
ov006_021f4bb0_L40:
    mov r0, #0xa
    add r1, #0x63
    strb r0, [r1, #0]
    b ov006_021f4bb0_L70
ov006_021f4bb0_L48:
    mov r0, #0xb
    add r1, #0x63
    strb r0, [r1, #0]
    b ov006_021f4bb0_L70
ov006_021f4bb0_L50:
    sub r0, r0, #0x1
    cmp r3, r0
    bne ov006_021f4bb0_L70
    mov r0, #0x64
    ldrsb r0, [r1, r0]
    cmp r0, #0x1
    beq ov006_021f4bb0_L62
    cmp r0, #0xa
    bne ov006_021f4bb0_L6a
ov006_021f4bb0_L62:
    mov r0, #0x1
    add r1, #0x63
    strb r0, [r1, #0]
    b ov006_021f4bb0_L70
ov006_021f4bb0_L6a:
    mov r0, #0x2
    add r1, #0x63
    strb r0, [r1, #0]
ov006_021f4bb0_L70:
    bl native_fn_021f4b50
    mov r0, #0x8
    bl native_fn_021ff6d4
    pop {r4, r5, r6, pc}
}
