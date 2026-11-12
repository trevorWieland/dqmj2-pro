/* ov006 row 0x021f4828: 284 bytes.
 *
 * What it does: 120 instructions; 14 call(s) to 0x02203eec, 0x021f4bb0, 0x02203eec, +11 more; no back edge; returns through pop {r3, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x10c -> constant 0x0221c060 (image word 0x0221c060)
 *   pool +0x110 -> native_data_0220b51c (image word 0x0220b51c)
 *   pool +0x114 -> native_data_0220b42c (image word 0x0220b42c)
 *   pool +0x118 -> native_data_0220b428 (image word 0x0220b428)
 *   branch +0x0a -> +0x12
 *   branch +0x1a -> +0x22
 *   branch +0x2a -> +0x32
 *   branch +0x3a -> +0x42
 *   branch +0x4a -> +0xba
 *   branch +0x56 -> +0x74
 *   branch +0x60 -> +0x6c
 *   branch +0x7a -> +0xb0
 *   branch +0x7e -> +0x8a
 *   branch +0x88 -> +0x9c
 *   branch +0x90 -> +0xa4
 *   branch +0x9a -> +0xa4
 *   branch +0xc2 -> +0xf4
 *   branch +0xd0 -> +0xec
 *   branch +0xd8 -> +0x108
 *   branch +0xfc -> +0x108
 *   test +0x08 cmp r0, #0x0
 *   test +0x18 cmp r0, #0x0
 *   test +0x28 cmp r0, #0x0
 *   test +0x38 cmp r0, #0x0
 *   test +0x48 cmp r0, #0x0
 *   test +0x54 cmp r0, #0xa
 *   test +0x5e cmp r2, #0x0
 *   test +0x78 cmp r2, #0x2
 *   test +0x7c cmp r2, #0x0
 *   test +0x86 cmp r2, #0x0
 *   test +0x8e cmp r2, #0x1
 *   test +0x98 cmp r2, #0x0
 *   test +0xc0 cmp r0, #0x0
 *   test +0xce cmp r0, #0x0
 *   test +0xd6 cmp r0, #0x0
 *   test +0xfa cmp r0, #0x0
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f4828; the literal pool and
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

extern void native_fn_02203eec(void);
extern void native_fn_021f4bb0(void);
extern void native_fn_02203ebc(void);
extern u8 native_data_0220b51c[];
extern void native_fn_021ff6d4(void);
extern u8 native_data_0220b42c[];
extern u8 native_data_0220b428[];
extern void native_fn_02203f1c(void);


asm u32 native_ov006_021f4828 (register u32 a0)
{
    push {r3, lr}
    mov r0, #0x20
    bl native_fn_02203eec
    cmp r0, #0x0
    beq ov006_021f4828_L12
    mov r0, #0x0
    bl native_fn_021f4bb0
ov006_021f4828_L12:
    mov r0, #0x40
    bl native_fn_02203eec
    cmp r0, #0x0
    beq ov006_021f4828_L22
    mov r0, #0x1
    bl native_fn_021f4bb0
ov006_021f4828_L22:
    mov r0, #0x10
    bl native_fn_02203eec
    cmp r0, #0x0
    beq ov006_021f4828_L32
    mov r0, #0x2
    bl native_fn_021f4bb0
ov006_021f4828_L32:
    mov r0, #0x80
    bl native_fn_02203eec
    cmp r0, #0x0
    beq ov006_021f4828_L42
    mov r0, #0x3
    bl native_fn_021f4bb0
ov006_021f4828_L42:
    mov r0, #0x1
    bl native_fn_02203ebc
    cmp r0, #0x0
    beq ov006_021f4828_Lba
    ldr r0, =0x0221c060
    ldr r1, [r0, #0]
    mov r0, #0x63
    ldrsb r0, [r1, r0]
    cmp r0, #0xa
    bge ov006_021f4828_L74
    add r2, r1, #0x0
    add r2, #0x67
    ldrb r2, [r2, #0]
    cmp r2, #0x0
    beq ov006_021f4828_L6c
    ldr r2, =native_data_0220b51c
    add r1, #0x60
    ldrb r0, [r2, r0]
    strb r0, [r1, #0]
    pop {r3, pc}
ov006_021f4828_L6c:
    mov r0, #0x9
    bl native_fn_021ff6d4
    pop {r3, pc}
ov006_021f4828_L74:
    add r2, r0, #0x0
    sub r2, #0xa
    cmp r2, #0x2
    bge ov006_021f4828_Lb0
    cmp r2, #0x0
    bne ov006_021f4828_L8a
    add r2, r1, #0x0
    add r2, #0x66
    ldrb r2, [r2, #0]
    cmp r2, #0x0
    beq ov006_021f4828_L9c
ov006_021f4828_L8a:
    add r2, r0, #0x0
    sub r2, #0xa
    cmp r2, #0x1
    bne ov006_021f4828_La4
    add r2, r1, #0x0
    add r2, #0x68
    ldrb r2, [r2, #0]
    cmp r2, #0x0
    bne ov006_021f4828_La4
ov006_021f4828_L9c:
    mov r0, #0x9
    bl native_fn_021ff6d4
    pop {r3, pc}
ov006_021f4828_La4:
    ldr r2, =native_data_0220b42c
    sub r0, #0xa
    ldrb r0, [r2, r0]
    add r1, #0x60
    strb r0, [r1, #0]
    pop {r3, pc}
ov006_021f4828_Lb0:
    ldr r2, =native_data_0220b428
    sub r0, #0xc
    ldrb r0, [r2, r0]
    add r1, #0x60
    strb r0, [r1, #0]
ov006_021f4828_Lba:
    mov r0, #0x2
    bl native_fn_02203eec
    cmp r0, #0x0
    beq ov006_021f4828_Lf4
    ldr r0, =0x0221c060
    ldr r1, [r0, #0]
    add r0, r1, #0x0
    add r0, #0x66
    ldrb r0, [r0, #0]
    cmp r0, #0x0
    bne ov006_021f4828_Lec
    add r1, #0x69
    ldrb r0, [r1, #0]
    cmp r0, #0x0
    bne ov006_021f4828_L108
    mov r0, #0x9
    bl native_fn_021ff6d4
    ldr r0, =0x0221c060
    mov r1, #0x1
    ldr r0, [r0, #0]
    add r0, #0x69
    strb r1, [r0, #0]
    pop {r3, pc}
ov006_021f4828_Lec:
    mov r0, #0x10
    add r1, #0x60
    strb r0, [r1, #0]
    pop {r3, pc}
ov006_021f4828_Lf4:
    mov r0, #0x2
    bl native_fn_02203f1c
    cmp r0, #0x0
    beq ov006_021f4828_L108
    ldr r0, =0x0221c060
    mov r1, #0x0
    ldr r0, [r0, #0]
    add r0, #0x69
    strb r1, [r0, #0]
ov006_021f4828_L108:
    pop {r3, pc}
    mov r8, r8
}
