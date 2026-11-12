/* ov006 row 0x021f46ac: 328 bytes.
 *
 * What it does: 136 instructions; 16 call(s) to 0x02203f4c, 0x022038e8, 0x02203f4c, +13 more; loops (back edge at +0x46); returns through pop {r3, r4, r5, r6, r7, pc}; 8 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x128 -> native_data_0220bb60 (image word 0x0220bb60)
 *   pool +0x12c -> native_data_0220b482 (image word 0x0220b482)
 *   pool +0x130 -> native_data_0220b430 (image word 0x0220b430)
 *   pool +0x134 -> constant 0x0221c060 (image word 0x0221c060)
 *   pool +0x138 -> native_data_0220b458 (image word 0x0220b458)
 *   pool +0x13c -> native_data_0220b438 (image word 0x0220b438)
 *   pool +0x140 -> native_data_0220b460 (image word 0x0220b460)
 *   pool +0x144 -> native_data_0220b43c (image word 0x0220b43c)
 *   branch +0x0c -> +0x10
 *   branch +0x0e -> +0x112
 *   branch +0x2a -> +0x40
 *   branch +0x36 -> +0x112
 *   branch +0x3e -> +0x11a
 *   back edge +0x46 -> +0x18
 *   branch +0x62 -> +0xd0
 *   branch +0x72 -> +0x112
 *   branch +0x7a -> +0x11a
 *   branch +0x96 -> +0x124
 *   branch +0xa0 -> +0xb8
 *   back edge +0xd6 -> +0x50
 *   branch +0xf2 -> +0x10a
 *   branch +0x100 -> +0x112
 *   branch +0x108 -> +0x11a
 *   back edge +0x110 -> +0xe0
 *   test +0x0a cmp r0, #0x0
 *   test +0x28 cmp r0, #0x0
 *   test +0x34 cmp r0, r4
 *   test +0x44 cmp r4, #0xa
 *   test +0x60 cmp r0, #0x0
 *   test +0x70 cmp r1, r0
 *   test +0x78 cmp r5, #0x0
 *   test +0x94 cmp r0, #0x28
 *   test +0x9e cmp r0, #0x0
 *   test +0xd4 cmp r5, #0x2
 *   test +0xf0 cmp r0, #0x0
 *   test +0xfe cmp r0, r5
 *   test +0x10e cmp r5, #0x2
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f46ac; the literal pool and
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
extern void native_fn_02203f4c(void);
extern u8 native_data_0220b482[];
extern u8 native_data_0220b430[];
extern void native_fn_022038e8(void);
extern void native_fn_021f47f4(void);
extern u8 native_data_0220b458[];
extern u8 native_data_0220b438[];
extern void native_fn_021ff6d4(void);
extern u8 native_data_0220b460[];
extern u8 native_data_0220b43c[];


asm u32 native_ov006_021f46ac (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x8
    ldr r0, =native_data_0220bb60
    bl native_fn_02203f4c
    cmp r0, #0x0
    bne ov006_021f46ac_L10
    b ov006_021f46ac_L112
ov006_021f46ac_L10:
    ldr r5, =native_data_0220b482
    ldr r7, =native_data_0220b430
    mov r4, #0x0
    add r6, sp, #0x0
ov006_021f46ac_L18:
    add r0, r5, #0x0
    add r1, r7, #0x0
    add r2, r6, #0x0
    bl native_fn_022038e8
    add r0, r6, #0x0
    bl native_fn_02203f4c
    cmp r0, #0x0
    beq ov006_021f46ac_L40
    ldr r0, =0x0221c060
    ldr r1, [r0, #0]
    mov r0, #0x61
    ldrsb r0, [r1, r0]
    cmp r0, r4
    bne ov006_021f46ac_L112
    add r0, r4, #0x0
    bl native_fn_021f47f4
    b ov006_021f46ac_L11a
ov006_021f46ac_L40:
    add r4, r4, #0x1
    add r5, r5, #0x4
    cmp r4, #0xa
    blt ov006_021f46ac_L18
    ldr r4, =native_data_0220b458
    ldr r7, =native_data_0220b438
    mov r5, #0x0
    add r6, sp, #0x0
ov006_021f46ac_L50:
    add r0, r4, #0x0
    add r1, r7, #0x0
    add r2, r6, #0x0
    bl native_fn_022038e8
    add r0, r6, #0x0
    bl native_fn_02203f4c
    cmp r0, #0x0
    beq ov006_021f46ac_Ld0
    ldr r0, =0x0221c060
    ldr r1, [r0, #0]
    mov r0, #0x61
    ldrsb r1, [r1, r0]
    add r0, r5, #0x0
    add r0, #0xa
    cmp r1, r0
    bne ov006_021f46ac_L112
    bl native_fn_021f47f4
    cmp r5, #0x0
    bne ov006_021f46ac_L11a
    ldr r1, =0x0221c060
    ldr r2, [r1, #0]
    add r0, r2, #0x0
    add r0, #0x65
    ldrb r0, [r0, #0]
    add r2, #0x65
    add r0, r0, #0x1
    strb r0, [r2, #0]
    ldr r2, [r1, #0]
    add r0, r2, #0x0
    add r0, #0x65
    ldrb r0, [r0, #0]
    cmp r0, #0x28
    blo ov006_021f46ac_L124
    add r0, r2, #0x0
    add r0, #0x66
    ldrb r0, [r0, #0]
    cmp r0, #0x0
    bne ov006_021f46ac_Lb8
    mov r0, #0x9
    bl native_fn_021ff6d4
    ldr r0, =0x0221c060
    mov r1, #0x0
    ldr r0, [r0, #0]
    mvn r1, r1
    add r0, #0x61
    strb r1, [r0, #0]
    add sp, #0x8
    pop {r3, r4, r5, r6, r7, pc}
ov006_021f46ac_Lb8:
    mov r0, #0x10
    add r2, #0x60
    strb r0, [r2, #0]
    ldr r1, [r1, #0]
    add sp, #0x8
    add r0, r1, #0x0
    add r0, #0x65
    ldrb r0, [r0, #0]
    add r1, #0x65
    sub r0, r0, #0x7
    strb r0, [r1, #0]
    pop {r3, r4, r5, r6, r7, pc}
ov006_021f46ac_Ld0:
    add r5, r5, #0x1
    add r4, r4, #0x4
    cmp r5, #0x2
    blt ov006_021f46ac_L50
    ldr r4, =native_data_0220b460
    ldr r7, =native_data_0220b43c
    mov r5, #0x0
    add r6, sp, #0x0
ov006_021f46ac_Le0:
    add r0, r4, #0x0
    add r1, r7, #0x0
    add r2, r6, #0x0
    bl native_fn_022038e8
    add r0, r6, #0x0
    bl native_fn_02203f4c
    cmp r0, #0x0
    beq ov006_021f46ac_L10a
    ldr r0, =0x0221c060
    add r5, #0xc
    ldr r1, [r0, #0]
    mov r0, #0x61
    ldrsb r0, [r1, r0]
    cmp r0, r5
    bne ov006_021f46ac_L112
    add r0, r5, #0x0
    bl native_fn_021f47f4
    b ov006_021f46ac_L11a
ov006_021f46ac_L10a:
    add r5, r5, #0x1
    add r4, r4, #0x4
    cmp r5, #0x2
    blt ov006_021f46ac_Le0
ov006_021f46ac_L112:
    mov r0, #0x0
    mvn r0, r0
    bl native_fn_021f47f4
ov006_021f46ac_L11a:
    ldr r0, =0x0221c060
    mov r1, #0x0
    ldr r0, [r0, #0]
    add r0, #0x65
    strb r1, [r0, #0]
ov006_021f46ac_L124:
    add sp, #0x8
    pop {r3, r4, r5, r6, r7, pc}
}
