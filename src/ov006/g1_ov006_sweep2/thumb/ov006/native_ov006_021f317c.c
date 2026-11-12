/* ov006 row 0x021f317c: 316 bytes.
 *
 * What it does: Writes one block of 4 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x110 -> native_data_0220bb60 (image word 0x0220bb60)
 *   pool +0x114 -> constant 0x0221c05c (image word 0x0221c05c)
 *   pool +0x118 -> constant 0x0000011e (image word 0x0000011e)
 *   pool +0x11c -> native_data_0220b1b4 (image word 0x0220b1b4)
 *   pool +0x120 -> native_data_0220b170 (image word 0x0220b170)
 *   pool +0x124 -> native_data_0220b19c (image word 0x0220b19c)
 *   pool +0x128 -> native_data_0220b18c (image word 0x0220b18c)
 *   pool +0x12c -> constant 0x00000123 (image word 0x00000123)
 *   pool +0x130 -> native_data_0220d7a8 (image word 0x0220d7a8)
 *   pool +0x134 -> native_data_0220b184 (image word 0x0220b184)
 *   pool +0x138 -> native_data_0220b16c (image word 0x0220b16c)
 *   branch +0x0c -> +0x10a
 *   branch +0x34 -> +0x60
 *   branch +0x42 -> +0x4e
 *   back edge +0x66 -> +0x22
 *   branch +0x82 -> +0xc8
 *   branch +0x86 -> +0x94
 *   branch +0x92 -> +0xa6
 *   branch +0x96 -> +0xb0
 *   branch +0xa4 -> +0xb0
 *   back edge +0xd0 -> +0x70
 *   branch +0xec -> +0x102
 *   back edge +0x108 -> +0xda
 *   test +0x0a cmp r0, #0x0
 *   test +0x32 cmp r0, #0x0
 *   test +0x40 cmp r0, #0x0
 *   test +0x64 cmp r4, #0x2f
 *   test +0x80 cmp r0, #0x0
 *   test +0x84 cmp r6, #0x3
 *   test +0x90 cmp r0, #0x0
 *   test +0x94 cmp r6, #0x2
 *   test +0xa2 cmp r0, #0x0
 *   test +0xce cmp r6, #0x4
 *   test +0xea cmp r0, #0x0
 *   test +0x106 cmp r5, #0x2
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f317c; the literal pool and
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
extern void native_fn_02203fac(void);
extern u8 native_data_0220b1b4[];
extern u8 native_data_0220b170[];
extern void native_fn_022038e8(void);
extern void native_fn_021ff6d4(void);
extern u8 native_data_0220b19c[];
extern u8 native_data_0220b18c[];
extern u8 native_data_0220d7a8[];
extern u8 native_data_0220b184[];
extern u8 native_data_0220b16c[];


asm u32 native_ov006_021f317c (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x8
    ldr r0, =native_data_0220bb60
    bl native_fn_02203fac
    cmp r0, #0x0
    beq ov006_021f317c_L10a
    ldr r0, =0x0221c05c
    mov r2, #0x0
    ldr r1, [r0, #0]
    ldr r0, =0x0000011e
    mvn r2, r2
    ldr r5, =native_data_0220b1b4
    ldr r7, =native_data_0220b170
    strb r2, [r1, r0]
    mov r4, #0x0
    add r6, sp, #0x0
ov006_021f317c_L22:
    add r0, r5, #0x0
    add r1, r7, #0x0
    add r2, r6, #0x0
    bl native_fn_022038e8
    add r0, r6, #0x0
    bl native_fn_02203fac
    cmp r0, #0x0
    beq ov006_021f317c_L60
    ldr r0, =0x0221c05c
    ldr r1, [r0, #0]
    mov r0, #0x49
    lsl r0, r0, #0x2
    ldrb r0, [r1, r0]
    cmp r0, #0x0
    bne ov006_021f317c_L4e
    mov r0, #0x9
    bl native_fn_021ff6d4
    add sp, #0x8
    pop {r3, r4, r5, r6, r7, pc}
ov006_021f317c_L4e:
    mov r0, #0x0
    bl native_fn_021ff6d4
    ldr r0, =0x0221c05c
    add sp, #0x8
    ldr r1, [r0, #0]
    ldr r0, =0x0000011e
    strb r4, [r1, r0]
    pop {r3, r4, r5, r6, r7, pc}
ov006_021f317c_L60:
    add r4, r4, #0x1
    add r5, r5, #0x4
    cmp r4, #0x2f
    blt ov006_021f317c_L22
    ldr r4, =native_data_0220b19c
    ldr r5, =native_data_0220b18c
    mov r6, #0x0
    add r7, sp, #0x0
ov006_021f317c_L70:
    add r0, r5, #0x0
    add r1, r4, #0x0
    add r2, r7, #0x0
    bl native_fn_022038e8
    add r0, r7, #0x0
    bl native_fn_02203fac
    cmp r0, #0x0
    beq ov006_021f317c_Lc8
    cmp r6, #0x3
    bne ov006_021f317c_L94
    ldr r0, =0x0221c05c
    ldr r1, [r0, #0]
    ldr r0, =0x00000123
    ldrb r0, [r1, r0]
    cmp r0, #0x0
    beq ov006_021f317c_La6
ov006_021f317c_L94:
    cmp r6, #0x2
    bne ov006_021f317c_Lb0
    ldr r0, =0x0221c05c
    ldr r1, [r0, #0]
    mov r0, #0x49
    lsl r0, r0, #0x2
    ldrb r0, [r1, r0]
    cmp r0, #0x0
    bne ov006_021f317c_Lb0
ov006_021f317c_La6:
    mov r0, #0x9
    bl native_fn_021ff6d4
    add sp, #0x8
    pop {r3, r4, r5, r6, r7, pc}
ov006_021f317c_Lb0:
    ldr r0, =native_data_0220d7a8
    lsl r1, r6, #0x2
    ldr r0, [r0, r1]
    bl native_fn_021ff6d4
    ldr r0, =0x0221c05c
    add r6, #0x2f
    ldr r1, [r0, #0]
    ldr r0, =0x0000011e
    add sp, #0x8
    strb r6, [r1, r0]
    pop {r3, r4, r5, r6, r7, pc}
ov006_021f317c_Lc8:
    add r6, r6, #0x1
    add r4, r4, #0x4
    add r5, r5, #0x4
    cmp r6, #0x4
    blt ov006_021f317c_L70
    ldr r4, =native_data_0220b184
    ldr r7, =native_data_0220b16c
    mov r5, #0x0
    add r6, sp, #0x0
ov006_021f317c_Lda:
    add r0, r4, #0x0
    add r1, r7, #0x0
    add r2, r6, #0x0
    bl native_fn_022038e8
    add r0, r6, #0x0
    bl native_fn_02203fac
    cmp r0, #0x0
    beq ov006_021f317c_L102
    mov r0, #0x0
    bl native_fn_021ff6d4
    ldr r0, =0x0221c05c
    add r5, #0x33
    ldr r1, [r0, #0]
    ldr r0, =0x0000011e
    add sp, #0x8
    strb r5, [r1, r0]
    pop {r3, r4, r5, r6, r7, pc}
ov006_021f317c_L102:
    add r5, r5, #0x1
    add r4, r4, #0x4
    cmp r5, #0x2
    blt ov006_021f317c_Lda
ov006_021f317c_L10a:
    add sp, #0x8
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
}
