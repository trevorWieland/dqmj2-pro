/* ov006 row 0x021f32b8: 476 bytes.
 *
 * What it does: Writes one block of 4 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x198 -> constant 0x0221c05c (image word 0x0221c05c)
 *   pool +0x19c -> native_data_0220bb60 (image word 0x0220bb60)
 *   pool +0x1a0 -> native_data_0220b1b4 (image word 0x0220b1b4)
 *   pool +0x1a4 -> native_data_0220b170 (image word 0x0220b170)
 *   pool +0x1a8 -> constant 0x0000011e (image word 0x0000011e)
 *   pool +0x1ac -> native_data_0220d790 (image word 0x0220d790)
 *   pool +0x1b0 -> constant 0x00000121 (image word 0x00000121)
 *   pool +0x1b4 -> native_data_0220b1a4 (image word 0x0220b1a4)
 *   pool +0x1b8 -> native_data_0220b194 (image word 0x0220b194)
 *   pool +0x1bc -> native_data_0220b1ac (image word 0x0220b1ac)
 *   pool +0x1c0 -> native_data_0220b184 (image word 0x0220b184)
 *   pool +0x1c4 -> native_data_0220b16c (image word 0x0220b16c)
 *   pool +0x1c8 -> native_data_0220b160 (image word 0x0220b160)
 *   pool +0x1cc -> native_data_0220b18c (image word 0x0220b18c)
 *   pool +0x1d0 -> native_data_0220b19c (image word 0x0220b19c)
 *   pool +0x1d4 -> native_data_0220b190 (image word 0x0220b190)
 *   pool +0x1d8 -> native_data_0220b1a0 (image word 0x0220b1a0)
 *   branch +0x18 -> +0x42
 *   branch +0x34 -> +0x74
 *   branch +0x40 -> +0x44
 *   branch +0x42 -> +0x192
 *   branch +0x5c -> +0x64
 *   back edge +0x7a -> +0x22
 *   branch +0x96 -> +0xd2
 *   branch +0xa6 -> +0x192
 *   branch +0xb8 -> +0xc0
 *   back edge +0xda -> +0x84
 *   branch +0xf6 -> +0x11e
 *   branch +0x106 -> +0x192
 *   back edge +0x124 -> +0xe4
 *   branch +0x138 -> +0x15e
 *   branch +0x144 -> +0x192
 *   branch +0x170 -> +0x192
 *   branch +0x17c -> +0x192
 *   test +0x16 cmp r0, #0x0
 *   test +0x32 cmp r0, #0x0
 *   test +0x3e cmp r1, r4
 *   test +0x5a cmp r0, #0x1
 *   test +0x78 cmp r4, #0x2f
 *   test +0x94 cmp r0, #0x0
 *   test +0xa4 cmp r4, r1
 *   test +0xb6 cmp r0, #0x1
 *   test +0xd8 cmp r6, #0x4
 *   test +0xf4 cmp r0, #0x0
 *   test +0x104 cmp r2, r0
 *   test +0x122 cmp r5, #0x2
 *   test +0x136 cmp r0, #0x0
 *   test +0x142 cmp r0, #0x2f
 *   test +0x16e cmp r0, #0x0
 *   test +0x17a cmp r0, #0x30
 *   0 block transfer(s), 9 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f32b8; the literal pool and
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

extern u8 native_data_0220bb60[];
extern void native_fn_0220406c(void);
extern u8 native_data_0220b1b4[];
extern u8 native_data_0220b170[];
extern void native_fn_022038e8(void);
extern u8 native_data_0220d790[];
extern void native_fn_021f3984(void);
extern void native_fn_021f3a78(void);
extern u8 native_data_0220b1a4[];
extern u8 native_data_0220b194[];
extern u8 native_data_0220b1ac[];
extern u8 native_data_0220b184[];
extern u8 native_data_0220b16c[];
extern u8 native_data_0220b160[];
extern u8 native_data_0220b18c[];
extern u8 native_data_0220b19c[];
extern void native_fn_021f3494(void);
extern u8 native_data_0220b190[];
extern u8 native_data_0220b1a0[];
extern void native_fn_021f34bc(void);


asm u32 native_ov006_021f32b8 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x8
    ldr r0, =0x0221c05c
    mov r2, #0x0
    ldr r1, [r0, #0]
    mov r0, #0x47
    lsl r0, r0, #0x2
    strb r2, [r1, r0]
    ldr r0, =native_data_0220bb60
    bl native_fn_0220406c
    cmp r0, #0x0
    beq ov006_021f32b8_L42
    ldr r5, =native_data_0220b1b4
    ldr r7, =native_data_0220b170
    mov r4, #0x0
    add r6, sp, #0x0
ov006_021f32b8_L22:
    add r0, r5, #0x0
    add r1, r7, #0x0
    add r2, r6, #0x0
    bl native_fn_022038e8
    add r0, r6, #0x0
    bl native_fn_0220406c
    cmp r0, #0x0
    beq ov006_021f32b8_L74
    ldr r3, =0x0221c05c
    ldr r2, =0x0000011e
    ldr r0, [r3, #0]
    ldrsb r1, [r0, r2]
    cmp r1, r4
    beq ov006_021f32b8_L44
ov006_021f32b8_L42:
    b ov006_021f32b8_L192
ov006_021f32b8_L44:
    sub r1, r2, #0x1
    ldrb r1, [r0, r1]
    lsl r5, r1, #0x2
    ldr r1, =native_data_0220d790
    ldr r1, [r1, r5]
    ldrb r5, [r1, r4]
    sub r1, r2, #0x2
    strb r5, [r0, r1]
    ldr r1, [r3, #0]
    sub r0, r2, #0x1
    ldrb r0, [r1, r0]
    cmp r0, #0x1
    bne ov006_021f32b8_L64
    mov r0, #0x0
    bl native_fn_021f3984
ov006_021f32b8_L64:
    ldr r0, =0x0221c05c
    ldr r1, [r0, #0]
    ldr r0, =0x00000121
    strb r4, [r1, r0]
    bl native_fn_021f3a78
    add sp, #0x8
    pop {r3, r4, r5, r6, r7, pc}
ov006_021f32b8_L74:
    add r4, r4, #0x1
    add r5, r5, #0x4
    cmp r4, #0x2f
    blt ov006_021f32b8_L22
    ldr r4, =native_data_0220b1a4
    ldr r5, =native_data_0220b194
    mov r6, #0x2
    add r7, sp, #0x0
ov006_021f32b8_L84:
    add r0, r5, #0x0
    add r1, r4, #0x0
    add r2, r7, #0x0
    bl native_fn_022038e8
    add r0, r7, #0x0
    bl native_fn_0220406c
    cmp r0, #0x0
    beq ov006_021f32b8_Ld2
    ldr r3, =0x0221c05c
    add r1, r6, #0x0
    ldr r0, [r3, #0]
    ldr r2, =0x0000011e
    add r1, #0x2f
    ldrsb r4, [r0, r2]
    cmp r4, r1
    bne ov006_021f32b8_L192
    ldr r1, =native_data_0220b1ac
    ldrb r4, [r1, r6]
    sub r1, r2, #0x2
    strb r4, [r0, r1]
    ldr r1, [r3, #0]
    sub r0, r2, #0x1
    ldrb r0, [r1, r0]
    cmp r0, #0x1
    bne ov006_021f32b8_Lc0
    mov r0, #0x0
    bl native_fn_021f3984
ov006_021f32b8_Lc0:
    ldr r0, =0x0221c05c
    add r6, #0x2f
    ldr r1, [r0, #0]
    ldr r0, =0x00000121
    strb r6, [r1, r0]
    bl native_fn_021f3a78
    add sp, #0x8
    pop {r3, r4, r5, r6, r7, pc}
ov006_021f32b8_Ld2:
    add r6, r6, #0x1
    add r4, r4, #0x4
    add r5, r5, #0x4
    cmp r6, #0x4
    blt ov006_021f32b8_L84
    ldr r4, =native_data_0220b184
    ldr r7, =native_data_0220b16c
    mov r5, #0x0
    add r6, sp, #0x0
ov006_021f32b8_Le4:
    add r0, r4, #0x0
    add r1, r7, #0x0
    add r2, r6, #0x0
    bl native_fn_022038e8
    add r0, r6, #0x0
    bl native_fn_0220406c
    cmp r0, #0x0
    beq ov006_021f32b8_L11e
    ldr r4, =0x0221c05c
    add r0, r5, #0x0
    ldr r1, [r4, #0]
    ldr r3, =0x0000011e
    add r0, #0x33
    ldrsb r2, [r1, r3]
    cmp r2, r0
    bne ov006_021f32b8_L192
    ldr r2, =native_data_0220b160
    ldrb r5, [r2, r5]
    sub r2, r3, #0x2
    strb r5, [r1, r2]
    ldr r2, [r4, #0]
    add r1, r3, #0x3
    strb r0, [r2, r1]
    bl native_fn_021f3a78
    add sp, #0x8
    pop {r3, r4, r5, r6, r7, pc}
ov006_021f32b8_L11e:
    add r5, r5, #0x1
    add r4, r4, #0x4
    cmp r5, #0x2
    blt ov006_021f32b8_Le4
    ldr r0, =native_data_0220b18c
    ldr r1, =native_data_0220b19c
    add r2, sp, #0x0
    bl native_fn_022038e8
    add r0, sp, #0x0
    bl native_fn_0220406c
    cmp r0, #0x0
    beq ov006_021f32b8_L15e
    ldr r0, =0x0221c05c
    ldr r1, [r0, #0]
    ldr r0, =0x0000011e
    ldrsb r0, [r1, r0]
    cmp r0, #0x2f
    bne ov006_021f32b8_L192
    bl native_fn_021f3494
    ldr r0, =0x0221c05c
    mov r2, #0x2f
    ldr r1, [r0, #0]
    add r0, r2, #0x0
    add r0, #0xf2
    strb r2, [r1, r0]
    bl native_fn_021f3a78
    add sp, #0x8
    pop {r3, r4, r5, r6, r7, pc}
ov006_021f32b8_L15e:
    ldr r0, =native_data_0220b190
    ldr r1, =native_data_0220b1a0
    add r2, sp, #0x0
    bl native_fn_022038e8
    add r0, sp, #0x0
    bl native_fn_0220406c
    cmp r0, #0x0
    beq ov006_021f32b8_L192
    ldr r0, =0x0221c05c
    ldr r1, [r0, #0]
    ldr r0, =0x0000011e
    ldrsb r0, [r1, r0]
    cmp r0, #0x30
    bne ov006_021f32b8_L192
    bl native_fn_021f34bc
    ldr r0, =0x0221c05c
    mov r2, #0x30
    ldr r1, [r0, #0]
    add r0, r2, #0x0
    add r0, #0xf1
    strb r2, [r1, r0]
    bl native_fn_021f3a78
ov006_021f32b8_L192:
    add sp, #0x8
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
}
