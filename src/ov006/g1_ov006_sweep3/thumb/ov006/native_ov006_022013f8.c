/* ov006 row 0x022013f8: 228 bytes.
 *
 * What it does: 99 instructions; 8 call(s) to 0x022012c0, 0x02201270, 0x022014ba, +5 more; loops (back edge at +0x14); returns through pop {r4, r5, r6, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0xd4 -> constant 0x0221c164 (image word 0x0221c164)
 *   pool +0xd8 -> native_data_0220e6b8 (image word 0x0220e6b8)
 *   pool +0xdc -> native_data_0220e6e4 (image word 0x0220e6e4)
 *   pool +0xe0 -> native_data_0220e710 (image word 0x0220e710)
 *   branch +0x12 -> +0x20
 *   branch +0x24 -> +0x38
 *   branch +0x26 -> +0x3e
 *   branch +0x2a -> +0xc2
 *   branch +0x2e -> +0xc2
 *   branch +0x30 -> +0xb2
 *   branch +0x34 -> +0xd2
 *   branch +0x36 -> +0xc2
 *   branch +0x3a -> +0x8c
 *   branch +0x3c -> +0xc2
 *   branch +0x44 -> +0x50
 *   branch +0x58 -> +0x7a
 *   branch +0x60 -> +0x7a
 *   branch +0x6c -> +0xd2
 *   branch +0x92 -> +0x9e
 *   branch +0xb8 -> +0xd2
 *   branch +0xc8 -> +0xd2
 *   test +0x10 cmp r0, #0x0
 *   test +0x22 cmp r2, #0x7
 *   test +0x28 cmp r2, #0x2
 *   test +0x2c cmp r2, #0x0
 *   test +0x32 cmp r2, #0x2
 *   test +0x38 cmp r2, #0x9
 *   test +0x42 cmp r6, #0x0
 *   test +0x56 cmp r1, #0x0
 *   test +0x5e cmp r0, #0x0
 *   test +0x6a cmp r0, #0x2
 *   test +0x90 cmp r5, #0x0
 *   test +0xb6 cmp r0, #0x0
 *   test +0xc6 cmp r3, #0x0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x022013f8; the literal pool and
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

extern void native_fn_022012c0(void);
extern void native_fn_02201270(void);
extern u8 native_data_0220e6b8[];
extern void native_fn_02012d84(void);
extern u8 native_data_0220e6e4[];
extern void native_fn_022014dc(void);
extern u8 native_data_0220e710[];


asm u32 native_ov006_022013f8 (register u32 a0)
{
    push {r4, r5, r6, lr}
    add r5, r0, #0x0
    ldrh r3, [r5, #0x10]
    mov r0, #0x1
    lsl r0, r3
    lsl r0, r0, #0x10
    lsr r4, r0, #0x10
    ldrh r0, [r5, #0x2]
    cmp r0, #0x0
    beq ov006_022013f8_L20
    bl native_fn_022012c0
    mov r0, #0x9
    bl native_fn_02201270
    pop {r4, r5, r6, pc}
ov006_022013f8_L20:
    ldrh r2, [r5, #0x8]
    cmp r2, #0x7
    bgt ov006_022013f8_L38
    bge ov006_022013f8_L3e
    cmp r2, #0x2
    bgt ov006_022013f8_Lc2
    cmp r2, #0x0
    blt ov006_022013f8_Lc2
    beq ov006_022013f8_Lb2
    cmp r2, #0x2
    beq ov006_022013f8_Ld2
    b ov006_022013f8_Lc2
ov006_022013f8_L38:
    cmp r2, #0x9
    beq ov006_022013f8_L8c
    b ov006_022013f8_Lc2
ov006_022013f8_L3e:
    ldr r0, =0x0221c164
    ldr r6, [r0, #0]
    cmp r6, #0x0
    beq ov006_022013f8_L50
    mov r0, #0x2
    ldr r1, =native_data_0220e6b8
    lsl r0, r0, #0x1a
    add r2, r3, #0x0
    blx r6
ov006_022013f8_L50:
    ldr r0, =0x0221c164
    ldr r0, [r0, #0x4]
    ldr r1, [r0, #0x4c]
    cmp r1, #0x0
    beq ov006_022013f8_L7a
    add r0, r5, #0x0
    blx r1
    cmp r0, #0x0
    bne ov006_022013f8_L7a
    ldrh r1, [r5, #0x10]
    mov r0, #0x0
    blx native_fn_02012d84
    cmp r0, #0x2
    beq ov006_022013f8_Ld2
    bl native_fn_022012c0
    mov r0, #0x9
    bl native_fn_02201270
    pop {r4, r5, r6, pc}
ov006_022013f8_L7a:
    ldr r0, =0x0221c164
    ldr r1, [r0, #0x4]
    add r0, r1, #0x0
    add r0, #0x52
    ldrh r0, [r0, #0]
    add r1, #0x52
    orr r0, r4
    strh r0, [r1, #0]
    pop {r4, r5, r6, pc}
ov006_022013f8_L8c:
    ldr r0, =0x0221c164
    ldr r5, [r0, #0]
    cmp r5, #0x0
    beq ov006_022013f8_L9e
    mov r0, #0x2
    ldr r1, =native_data_0220e6e4
    lsl r0, r0, #0x1a
    add r2, r3, #0x0
    blx r5
ov006_022013f8_L9e:
    ldr r0, =0x0221c164
    ldr r2, [r0, #0x4]
    add r0, r2, #0x0
    add r0, #0x52
    ldrh r1, [r0, #0]
    mvn r0, r4
    add r2, #0x52
    and r0, r1
    strh r0, [r2, #0]
    pop {r4, r5, r6, pc}
ov006_022013f8_Lb2:
    bl native_fn_022014dc
    cmp r0, #0x0
    bne ov006_022013f8_Ld2
    mov r0, #0x9
    bl native_fn_02201270
    pop {r4, r5, r6, pc}
ov006_022013f8_Lc2:
    ldr r0, =0x0221c164
    ldr r3, [r0, #0]
    cmp r3, #0x0
    beq ov006_022013f8_Ld2
    mov r0, #0x2
    ldr r1, =native_data_0220e710
    lsl r0, r0, #0x1a
    blx r3
ov006_022013f8_Ld2:
    pop {r4, r5, r6, pc}
}
