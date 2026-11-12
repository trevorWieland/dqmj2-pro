/* ov006 row 0x021f34e4: 324 bytes.
 *
 * What it does: Writes one block of 4 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x11c -> native_data_0220bb60 (image word 0x0220bb60)
 *   pool +0x120 -> native_data_0220b1b4 (image word 0x0220b1b4)
 *   pool +0x124 -> native_data_0220b170 (image word 0x0220b170)
 *   pool +0x128 -> constant 0x0221c05c (image word 0x0221c05c)
 *   pool +0x12c -> constant 0x0000011e (image word 0x0000011e)
 *   pool +0x130 -> native_data_0220b1a4 (image word 0x0220b1a4)
 *   pool +0x134 -> native_data_0220b194 (image word 0x0220b194)
 *   pool +0x138 -> constant 0x00000122 (image word 0x00000122)
 *   pool +0x13c -> native_data_0220b184 (image word 0x0220b184)
 *   pool +0x140 -> native_data_0220b16c (image word 0x0220b16c)
 *   branch +0x0c -> +0x104
 *   branch +0x28 -> +0x3e
 *   branch +0x34 -> +0x104
 *   branch +0x3c -> +0x10c
 *   back edge +0x44 -> +0x16
 *   branch +0x60 -> +0xc0
 *   branch +0x70 -> +0x104
 *   branch +0x78 -> +0x116
 *   branch +0x8c -> +0x116
 *   branch +0x94 -> +0xac
 *   back edge +0xc8 -> +0x4e
 *   branch +0xe4 -> +0xfc
 *   branch +0xf2 -> +0x104
 *   branch +0xfa -> +0x10c
 *   back edge +0x102 -> +0xd2
 *   test +0x0a cmp r0, #0x0
 *   test +0x26 cmp r0, #0x0
 *   test +0x32 cmp r0, r4
 *   test +0x42 cmp r4, #0x2f
 *   test +0x5e cmp r0, #0x0
 *   test +0x6e cmp r1, r0
 *   test +0x76 cmp r6, #0x3
 *   test +0x8a cmp r1, #0x28
 *   test +0x92 cmp r1, #0x0
 *   test +0xc6 cmp r6, #0x4
 *   test +0xe2 cmp r0, #0x0
 *   test +0xf0 cmp r0, r5
 *   test +0x100 cmp r5, #0x2
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f34e4; the literal pool and
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
extern void native_fn_02203f4c(void);
extern u8 native_data_0220b1b4[];
extern u8 native_data_0220b170[];
extern void native_fn_022038e8(void);
extern void native_fn_021f3628(void);
extern u8 native_data_0220b1a4[];
extern u8 native_data_0220b194[];
extern void native_fn_021ff6d4(void);
extern u8 native_data_0220b184[];
extern u8 native_data_0220b16c[];


asm u32 native_ov006_021f34e4 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x8
    ldr r0, =native_data_0220bb60
    bl native_fn_02203f4c
    cmp r0, #0x0
    beq ov006_021f34e4_L104
    ldr r5, =native_data_0220b1b4
    ldr r7, =native_data_0220b170
    mov r4, #0x0
    add r6, sp, #0x0
ov006_021f34e4_L16:
    add r0, r5, #0x0
    add r1, r7, #0x0
    add r2, r6, #0x0
    bl native_fn_022038e8
    add r0, r6, #0x0
    bl native_fn_02203f4c
    cmp r0, #0x0
    beq ov006_021f34e4_L3e
    ldr r0, =0x0221c05c
    ldr r1, [r0, #0]
    ldr r0, =0x0000011e
    ldrsb r0, [r1, r0]
    cmp r0, r4
    bne ov006_021f34e4_L104
    add r0, r4, #0x0
    bl native_fn_021f3628
    b ov006_021f34e4_L10c
ov006_021f34e4_L3e:
    add r4, r4, #0x1
    add r5, r5, #0x4
    cmp r4, #0x2f
    blt ov006_021f34e4_L16
    ldr r4, =native_data_0220b1a4
    ldr r5, =native_data_0220b194
    mov r6, #0x2
    add r7, sp, #0x0
ov006_021f34e4_L4e:
    add r0, r5, #0x0
    add r1, r4, #0x0
    add r2, r7, #0x0
    bl native_fn_022038e8
    add r0, r7, #0x0
    bl native_fn_02203f4c
    cmp r0, #0x0
    beq ov006_021f34e4_Lc0
    ldr r0, =0x0221c05c
    ldr r1, [r0, #0]
    ldr r0, =0x0000011e
    ldrsb r1, [r1, r0]
    add r0, r6, #0x0
    add r0, #0x2f
    cmp r1, r0
    bne ov006_021f34e4_L104
    bl native_fn_021f3628
    cmp r6, #0x3
    bne ov006_021f34e4_L116
    ldr r3, =0x0221c05c
    ldr r2, =0x00000122
    ldr r1, [r3, #0]
    ldrb r0, [r1, r2]
    add r0, r0, #0x1
    strb r0, [r1, r2]
    ldr r0, [r3, #0]
    ldrb r1, [r0, r2]
    cmp r1, #0x28
    blo ov006_021f34e4_L116
    add r1, r2, #0x1
    ldrb r1, [r0, r1]
    cmp r1, #0x0
    bne ov006_021f34e4_Lac
    mov r0, #0x9
    bl native_fn_021ff6d4
    ldr r0, =0x0221c05c
    mov r2, #0x0
    ldr r1, [r0, #0]
    ldr r0, =0x0000011e
    mvn r2, r2
    strb r2, [r1, r0]
    add sp, #0x8
    pop {r3, r4, r5, r6, r7, pc}
ov006_021f34e4_Lac:
    mov r4, #0x80
    add r1, r4, #0x0
    add r1, #0x9c
    strb r4, [r0, r1]
    ldr r1, [r3, #0]
    add sp, #0x8
    ldrb r0, [r1, r2]
    sub r0, r0, #0x7
    strb r0, [r1, r2]
    pop {r3, r4, r5, r6, r7, pc}
ov006_021f34e4_Lc0:
    add r6, r6, #0x1
    add r4, r4, #0x4
    add r5, r5, #0x4
    cmp r6, #0x4
    blt ov006_021f34e4_L4e
    ldr r4, =native_data_0220b184
    ldr r7, =native_data_0220b16c
    mov r5, #0x0
    add r6, sp, #0x0
ov006_021f34e4_Ld2:
    add r0, r4, #0x0
    add r1, r7, #0x0
    add r2, r6, #0x0
    bl native_fn_022038e8
    add r0, r6, #0x0
    bl native_fn_02203f4c
    cmp r0, #0x0
    beq ov006_021f34e4_Lfc
    ldr r0, =0x0221c05c
    add r5, #0x33
    ldr r1, [r0, #0]
    ldr r0, =0x0000011e
    ldrsb r0, [r1, r0]
    cmp r0, r5
    bne ov006_021f34e4_L104
    add r0, r5, #0x0
    bl native_fn_021f3628
    b ov006_021f34e4_L10c
ov006_021f34e4_Lfc:
    add r5, r5, #0x1
    add r4, r4, #0x4
    cmp r5, #0x2
    blt ov006_021f34e4_Ld2
ov006_021f34e4_L104:
    mov r0, #0x0
    mvn r0, r0
    bl native_fn_021f3628
ov006_021f34e4_L10c:
    ldr r0, =0x0221c05c
    mov r2, #0x0
    ldr r1, [r0, #0]
    ldr r0, =0x00000122
    strb r2, [r1, r0]
ov006_021f34e4_L116:
    add sp, #0x8
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
}
