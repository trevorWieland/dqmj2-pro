/* ov006 row 0x021f4464: 292 bytes.
 *
 * What it does: 118 instructions; 15 call(s) to 0x02203fac, 0x022038e8, 0x02203fac, +12 more; loops (back edge at +0x64); returns through pop {r3, r4, r5, r6, r7, pc}; 8 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x104 -> native_data_0220bb60 (image word 0x0220bb60)
 *   pool +0x108 -> constant 0x0221c060 (image word 0x0221c060)
 *   pool +0x10c -> native_data_0220b482 (image word 0x0220b482)
 *   pool +0x110 -> native_data_0220b430 (image word 0x0220b430)
 *   pool +0x114 -> native_data_0220b458 (image word 0x0220b458)
 *   pool +0x118 -> native_data_0220b438 (image word 0x0220b438)
 *   pool +0x11c -> native_data_0220b460 (image word 0x0220b460)
 *   pool +0x120 -> native_data_0220b43c (image word 0x0220b43c)
 *   branch +0x0c -> +0x100
 *   branch +0x34 -> +0x5e
 *   branch +0x40 -> +0x4c
 *   back edge +0x64 -> +0x22
 *   branch +0x80 -> +0xc0
 *   branch +0x84 -> +0x92
 *   branch +0x90 -> +0xa2
 *   branch +0x94 -> +0xac
 *   branch +0xa0 -> +0xac
 *   back edge +0xc6 -> +0x6e
 *   branch +0xe2 -> +0xf8
 *   back edge +0xfe -> +0xd0
 *   test +0x0a cmp r0, #0x0
 *   test +0x32 cmp r0, #0x0
 *   test +0x3e cmp r0, #0x0
 *   test +0x62 cmp r4, #0xa
 *   test +0x7e cmp r0, #0x0
 *   test +0x82 cmp r5, #0x0
 *   test +0x8e cmp r0, #0x0
 *   test +0x92 cmp r5, #0x1
 *   test +0x9e cmp r0, #0x0
 *   test +0xc4 cmp r5, #0x2
 *   test +0xe0 cmp r0, #0x0
 *   test +0xfc cmp r5, #0x2
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f4464; the literal pool and
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
extern void native_fn_02203fac(void);
extern u8 native_data_0220b482[];
extern u8 native_data_0220b430[];
extern void native_fn_022038e8(void);
extern void native_fn_021ff6d4(void);
extern u8 native_data_0220b458[];
extern u8 native_data_0220b438[];
extern u8 native_data_0220b460[];
extern u8 native_data_0220b43c[];


asm u32 native_ov006_021f4464 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x8
    ldr r0, =native_data_0220bb60
    bl native_fn_02203fac
    cmp r0, #0x0
    beq ov006_021f4464_L100
    ldr r0, =0x0221c060
    mov r1, #0x0
    ldr r0, [r0, #0]
    mvn r1, r1
    add r0, #0x61
    ldr r5, =native_data_0220b482
    ldr r7, =native_data_0220b430
    strb r1, [r0, #0]
    mov r4, #0x0
    add r6, sp, #0x0
ov006_021f4464_L22:
    add r0, r5, #0x0
    add r1, r7, #0x0
    add r2, r6, #0x0
    bl native_fn_022038e8
    add r0, r6, #0x0
    bl native_fn_02203fac
    cmp r0, #0x0
    beq ov006_021f4464_L5e
    ldr r0, =0x0221c060
    ldr r0, [r0, #0]
    add r0, #0x67
    ldrb r0, [r0, #0]
    cmp r0, #0x0
    bne ov006_021f4464_L4c
    mov r0, #0x9
    bl native_fn_021ff6d4
    add sp, #0x8
    pop {r3, r4, r5, r6, r7, pc}
ov006_021f4464_L4c:
    mov r0, #0x0
    bl native_fn_021ff6d4
    ldr r0, =0x0221c060
    add sp, #0x8
    ldr r0, [r0, #0]
    add r0, #0x61
    strb r4, [r0, #0]
    pop {r3, r4, r5, r6, r7, pc}
ov006_021f4464_L5e:
    add r4, r4, #0x1
    add r5, r5, #0x4
    cmp r4, #0xa
    blt ov006_021f4464_L22
    ldr r4, =native_data_0220b458
    ldr r7, =native_data_0220b438
    mov r5, #0x0
    add r6, sp, #0x0
ov006_021f4464_L6e:
    add r0, r4, #0x0
    add r1, r7, #0x0
    add r2, r6, #0x0
    bl native_fn_022038e8
    add r0, r6, #0x0
    bl native_fn_02203fac
    cmp r0, #0x0
    beq ov006_021f4464_Lc0
    cmp r5, #0x0
    bne ov006_021f4464_L92
    ldr r0, =0x0221c060
    ldr r0, [r0, #0]
    add r0, #0x66
    ldrb r0, [r0, #0]
    cmp r0, #0x0
    beq ov006_021f4464_La2
ov006_021f4464_L92:
    cmp r5, #0x1
    bne ov006_021f4464_Lac
    ldr r0, =0x0221c060
    ldr r0, [r0, #0]
    add r0, #0x68
    ldrb r0, [r0, #0]
    cmp r0, #0x0
    bne ov006_021f4464_Lac
ov006_021f4464_La2:
    mov r0, #0x9
    bl native_fn_021ff6d4
    add sp, #0x8
    pop {r3, r4, r5, r6, r7, pc}
ov006_021f4464_Lac:
    mov r0, #0x0
    bl native_fn_021ff6d4
    ldr r0, =0x0221c060
    add r5, #0xa
    ldr r0, [r0, #0]
    add sp, #0x8
    add r0, #0x61
    strb r5, [r0, #0]
    pop {r3, r4, r5, r6, r7, pc}
ov006_021f4464_Lc0:
    add r5, r5, #0x1
    add r4, r4, #0x4
    cmp r5, #0x2
    blt ov006_021f4464_L6e
    ldr r4, =native_data_0220b460
    ldr r7, =native_data_0220b43c
    mov r5, #0x0
    add r6, sp, #0x0
ov006_021f4464_Ld0:
    add r0, r4, #0x0
    add r1, r7, #0x0
    add r2, r6, #0x0
    bl native_fn_022038e8
    add r0, r6, #0x0
    bl native_fn_02203fac
    cmp r0, #0x0
    beq ov006_021f4464_Lf8
    mov r0, #0x0
    bl native_fn_021ff6d4
    ldr r0, =0x0221c060
    add r5, #0xc
    ldr r0, [r0, #0]
    add sp, #0x8
    add r0, #0x61
    strb r5, [r0, #0]
    pop {r3, r4, r5, r6, r7, pc}
ov006_021f4464_Lf8:
    add r5, r5, #0x1
    add r4, r4, #0x4
    cmp r5, #0x2
    blt ov006_021f4464_Ld0
ov006_021f4464_L100:
    add sp, #0x8
    pop {r3, r4, r5, r6, r7, pc}
}
