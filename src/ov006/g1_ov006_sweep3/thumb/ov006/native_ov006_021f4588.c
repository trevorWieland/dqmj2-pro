/* ov006 row 0x021f4588: 292 bytes.
 *
 * What it does: 114 instructions; 13 call(s) to 0x0220406c, 0x022038e8, 0x0220406c, +10 more; loops (back edge at +0x5c); returns through pop {r3, r4, r5, r6, r7, pc}; 11 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0xf8 -> constant 0x0221c060 (image word 0x0221c060)
 *   pool +0xfc -> native_data_0220bb60 (image word 0x0220bb60)
 *   pool +0x100 -> native_data_0220b482 (image word 0x0220b482)
 *   pool +0x104 -> native_data_0220b430 (image word 0x0220b430)
 *   pool +0x108 -> native_data_0220b51c (image word 0x0220b51c)
 *   pool +0x10c -> native_data_0220b458 (image word 0x0220b458)
 *   pool +0x110 -> native_data_0220b438 (image word 0x0220b438)
 *   pool +0x114 -> native_data_0220b42c (image word 0x0220b42c)
 *   pool +0x118 -> native_data_0220b460 (image word 0x0220b460)
 *   pool +0x11c -> native_data_0220b43c (image word 0x0220b43c)
 *   pool +0x120 -> native_data_0220b428 (image word 0x0220b428)
 *   branch +0x16 -> +0xf2
 *   branch +0x32 -> +0x56
 *   branch +0x3e -> +0xf2
 *   back edge +0x5c -> +0x20
 *   branch +0x78 -> +0xa0
 *   branch +0x88 -> +0xf2
 *   back edge +0xa6 -> +0x66
 *   branch +0xc2 -> +0xea
 *   branch +0xd2 -> +0xf2
 *   back edge +0xf0 -> +0xb0
 *   test +0x14 cmp r0, #0x0
 *   test +0x30 cmp r0, #0x0
 *   test +0x3c cmp r0, r4
 *   test +0x5a cmp r4, #0xa
 *   test +0x76 cmp r0, #0x0
 *   test +0x86 cmp r1, r3
 *   test +0xa4 cmp r5, #0x2
 *   test +0xc0 cmp r0, #0x0
 *   test +0xd0 cmp r1, r3
 *   test +0xee cmp r5, #0x2
 *   0 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f4588; the literal pool and
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

extern u8 native_data_0220bb60[];
extern void native_fn_0220406c(void);
extern u8 native_data_0220b482[];
extern u8 native_data_0220b430[];
extern void native_fn_022038e8(void);
extern u8 native_data_0220b51c[];
extern void native_fn_021f4b50(void);
extern u8 native_data_0220b458[];
extern u8 native_data_0220b438[];
extern u8 native_data_0220b42c[];
extern u8 native_data_0220b460[];
extern u8 native_data_0220b43c[];
extern u8 native_data_0220b428[];


asm u32 native_ov006_021f4588 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x8
    ldr r0, =0x0221c060
    mov r1, #0x0
    ldr r0, [r0, #0]
    add r0, #0x60
    strb r1, [r0, #0]
    ldr r0, =native_data_0220bb60
    bl native_fn_0220406c
    cmp r0, #0x0
    beq ov006_021f4588_Lf2
    ldr r5, =native_data_0220b482
    ldr r7, =native_data_0220b430
    mov r4, #0x0
    add r6, sp, #0x0
ov006_021f4588_L20:
    add r0, r5, #0x0
    add r1, r7, #0x0
    add r2, r6, #0x0
    bl native_fn_022038e8
    add r0, r6, #0x0
    bl native_fn_0220406c
    cmp r0, #0x0
    beq ov006_021f4588_L56
    ldr r1, =0x0221c060
    mov r0, #0x61
    ldr r2, [r1, #0]
    ldrsb r0, [r2, r0]
    cmp r0, r4
    bne ov006_021f4588_Lf2
    ldr r0, =native_data_0220b51c
    add r2, #0x60
    ldrb r0, [r0, r4]
    strb r0, [r2, #0]
    ldr r0, [r1, #0]
    add r0, #0x63
    strb r4, [r0, #0]
    bl native_fn_021f4b50
    add sp, #0x8
    pop {r3, r4, r5, r6, r7, pc}
ov006_021f4588_L56:
    add r4, r4, #0x1
    add r5, r5, #0x4
    cmp r4, #0xa
    blt ov006_021f4588_L20
    ldr r4, =native_data_0220b458
    ldr r7, =native_data_0220b438
    mov r5, #0x0
    add r6, sp, #0x0
ov006_021f4588_L66:
    add r0, r4, #0x0
    add r1, r7, #0x0
    add r2, r6, #0x0
    bl native_fn_022038e8
    add r0, r6, #0x0
    bl native_fn_0220406c
    cmp r0, #0x0
    beq ov006_021f4588_La0
    ldr r2, =0x0221c060
    add r3, r5, #0x0
    ldr r0, [r2, #0]
    mov r1, #0x61
    ldrsb r1, [r0, r1]
    add r3, #0xa
    cmp r1, r3
    bne ov006_021f4588_Lf2
    ldr r1, =native_data_0220b42c
    add r0, #0x60
    ldrb r1, [r1, r5]
    strb r1, [r0, #0]
    ldr r0, [r2, #0]
    add r0, #0x63
    strb r3, [r0, #0]
    bl native_fn_021f4b50
    add sp, #0x8
    pop {r3, r4, r5, r6, r7, pc}
ov006_021f4588_La0:
    add r5, r5, #0x1
    add r4, r4, #0x4
    cmp r5, #0x2
    blt ov006_021f4588_L66
    ldr r4, =native_data_0220b460
    ldr r7, =native_data_0220b43c
    mov r5, #0x0
    add r6, sp, #0x0
ov006_021f4588_Lb0:
    add r0, r4, #0x0
    add r1, r7, #0x0
    add r2, r6, #0x0
    bl native_fn_022038e8
    add r0, r6, #0x0
    bl native_fn_0220406c
    cmp r0, #0x0
    beq ov006_021f4588_Lea
    ldr r2, =0x0221c060
    add r3, r5, #0x0
    ldr r0, [r2, #0]
    mov r1, #0x61
    ldrsb r1, [r0, r1]
    add r3, #0xc
    cmp r1, r3
    bne ov006_021f4588_Lf2
    ldr r1, =native_data_0220b428
    add r0, #0x60
    ldrb r1, [r1, r5]
    strb r1, [r0, #0]
    ldr r0, [r2, #0]
    add r0, #0x63
    strb r3, [r0, #0]
    bl native_fn_021f4b50
    add sp, #0x8
    pop {r3, r4, r5, r6, r7, pc}
ov006_021f4588_Lea:
    add r5, r5, #0x1
    add r4, r4, #0x4
    cmp r5, #0x2
    blt ov006_021f4588_Lb0
ov006_021f4588_Lf2:
    add sp, #0x8
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
}
