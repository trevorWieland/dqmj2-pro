/* ov006 row 0x02201b78: 224 bytes.
 *
 * What it does: 96 instructions; 4 call(s) to 0x02008430, 0x02201270, 0x02012340, +1 more; loops (back edge at +0x12); returns through pop {r3, r4, r5, r6, r7, pc}; 6 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0xc8 -> constant 0x0221c164 (image word 0x0221c164)
 *   pool +0xcc -> constant 0x000012a4 (image word 0x000012a4)
 *   pool +0xd0 -> native_data_0220e788 (image word 0x0220e788)
 *   pool +0xd4 -> constant 0x000012a0 (image word 0x000012a0)
 *   pool +0xd8 -> native_data_0220e7a0 (image word 0x0220e7a0)
 *   pool +0xdc -> native_data_0220e7e8 (image word 0x0220e7e8)
 *   branch +0x10 -> +0x18
 *   branch +0x30 -> +0x3e
 *   branch +0x44 -> +0x54
 *   branch +0x98 -> +0x9c
 *   branch +0xa4 -> +0xae
 *   branch +0xa8 -> +0xae
 *   branch +0xac -> +0xb4
 *   branch +0xb8 -> +0xc4
 *   test +0x0e cmp r0, #0x1
 *   test +0x2e cmp r3, #0x0
 *   test +0x42 cmp r3, #0x0
 *   test +0x8c cmp r5, #0x2
 *   test +0x9e cmp r5, #0x0
 *   test +0xa6 cmp r5, #0x2
 *   test +0xaa cmp r5, #0x4
 *   test +0xb6 cmp r3, #0x0
 *   0 block transfer(s), 13 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02201b78; the literal pool and
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

extern void native_fn_02008430(void);
extern u8 native_data_0220e788[];
extern u8 native_data_0220e7a0[];
extern void native_fn_02201270(void);
extern void native_fn_02012340(void);
extern void native_fn_022012d4(void);
extern u8 native_data_0220e7e8[];


asm u32 native_ov006_02201b78 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    add r5, r0, #0x0
    ldr r0, =0x0221c164
    add r4, r1, #0x0
    ldr r0, [r0, #0x4]
    add r7, r2, #0x0
    ldr r0, [r0, #0x40]
    cmp r0, #0x1
    beq ov006_02201b78_L18
    blx native_fn_02008430
    mov r0, #0x0
ov006_02201b78_L18:
    ldr r2, =0x0221c164
    mov r1, #0x6
    ldr r0, [r2, #0x4]
    ldr r6, =0x000012a4
    lsl r1, r1, #0x6
    str r1, [r0, r6]
    ldr r1, [r2, #0x4]
    mov r3, #0xe0
    sub r0, r6, #0x4
    str r3, [r1, r0]
    ldr r3, [r2, #0]
    cmp r3, #0x0
    beq ov006_02201b78_L3e
    ldr r2, [r2, #0x4]
    mov r0, #0x2
    ldr r1, =native_data_0220e788
    ldr r2, [r2, r6]
    lsl r0, r0, #0x1a
    blx r3
ov006_02201b78_L3e:
    ldr r2, =0x0221c164
    ldr r3, [r2, #0]
    cmp r3, #0x0
    beq ov006_02201b78_L54
    ldr r6, [r2, #0x4]
    ldr r2, =0x000012a0
    mov r0, #0x2
    ldr r1, =native_data_0220e7a0
    ldr r2, [r6, r2]
    lsl r0, r0, #0x1a
    blx r3
ov006_02201b78_L54:
    ldr r0, =0x0221c164
    ldr r0, [r0, #0x4]
    str r5, [r0, #0x44]
    mov r0, #0x3
    bl native_fn_02201270
    ldr r0, =0x0221c164
    ldr r1, [r0, #0x4]
    strh r4, [r1, #0xc]
    ldr r0, [r0, #0x4]
    strh r7, [r0, #0x32]
    blx native_fn_02012340
    ldr r1, =0x0221c164
    mov r3, #0x1
    ldr r2, [r1, #0x4]
    strh r0, [r2, #0x18]
    ldr r0, [r1, #0x4]
    mov r2, #0xd0
    strh r2, [r0, #0x34]
    ldr r0, [r1, #0x4]
    mov r2, #0x44
    strh r2, [r0, #0x36]
    ldr r0, [r1, #0x4]
    mov r2, #0x2
    strh r2, [r0, #0x10]
    mov r2, #0x0
    ldr r0, [r1, #0x4]
    cmp r5, #0x2
    strh r2, [r0, #0x16]
    ldr r0, [r1, #0x4]
    strh r2, [r0, #0x12]
    ldr r0, [r1, #0x4]
    strh r3, [r0, #0xe]
    beq ov006_02201b78_L9c
    add r3, r2, #0x0
ov006_02201b78_L9c:
    ldr r0, =0x0221c164
    cmp r5, #0x0
    ldr r1, [r0, #0x4]
    strh r3, [r1, #0x14]
    beq ov006_02201b78_Lae
    cmp r5, #0x2
    beq ov006_02201b78_Lae
    cmp r5, #0x4
    bne ov006_02201b78_Lb4
ov006_02201b78_Lae:
    bl native_fn_022012d4
    pop {r3, r4, r5, r6, r7, pc}
ov006_02201b78_Lb4:
    ldr r3, [r0, #0]
    cmp r3, #0x0
    beq ov006_02201b78_Lc4
    mov r0, #0x2
    ldr r1, =native_data_0220e7e8
    lsl r0, r0, #0x1a
    add r2, r5, #0x0
    blx r3
ov006_02201b78_Lc4:
    mov r0, #0x0
    pop {r3, r4, r5, r6, r7, pc}
}
