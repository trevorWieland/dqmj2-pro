/* ov006 row 0x021ec6f8: 504 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x1d8 -> constant 0x0221a474 (image word 0x0221a474)
 *   pool +0x1dc -> constant 0x00000117 (image word 0x00000117)
 *   pool +0x1e0 -> constant 0x0221a4e4 (image word 0x0221a4e4)
 *   pool +0x1e4 -> constant 0x0221a214 (image word 0x0221a214)
 *   pool +0x1e8 -> constant 0x0221a344 (image word 0x0221a344)
 *   pool +0x1ec -> constant 0x02219b4c (image word 0x02219b4c)
 *   pool +0x1f0 -> constant 0x00000133 (image word 0x00000133)
 *   pool +0x1f4 -> constant 0x00000116 (image word 0x00000116)
 *   branch +0x16 -> +0x20
 *   branch +0x3a -> +0x9e
 *   branch +0x84 -> +0x88
 *   branch +0x86 -> +0x1c4
 *   branch +0xa4 -> +0x10a
 *   branch +0xf2 -> +0x1c4
 *   branch +0x110 -> +0x162
 *   branch +0x122 -> +0x1c4
 *   branch +0x148 -> +0x1c4
 *   branch +0x168 -> +0x1ba
 *   branch +0x17a -> +0x1c4
 *   branch +0x1a0 -> +0x1c4
 *   test +0x38 tst r0, r1
 *   test +0x82 cmp r0, #0x0
 *   test +0xa2 tst r0, r1
 *   test +0xf0 cmp r0, #0x0
 *   test +0x10e tst r0, r1
 *   test +0x120 cmp r0, #0x0
 *   test +0x146 cmp r0, #0x0
 *   test +0x166 tst r0, r1
 *   test +0x178 cmp r0, #0x0
 *   test +0x19e cmp r0, #0x0
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ec6f8; the literal pool and
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

extern void native_fn_021edbac(void);
extern void native_fn_021edb9c(void);
extern void native_fn_021edcd0(void);
extern void native_fn_021ec8f0(void);


asm u32 native_ov006_021ec6f8 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x8
    add r7, r0, #0x0
    ldr r0, =0x0221a474
    ldr r2, =0x00000117
    str r0, [sp, #0x4]
    ldr r0, =0x0221a4e4
    add r4, r7, r2
    ldr r6, =0x0221a214
    ldr r5, =0x0221a344
    str r0, [sp]
    bne ov006_021ec6f8_L20
    mov r0, #0x0
    add sp, #0x8
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
ov006_021ec6f8_L20:
    ldr r1, =0x02219b4c
    add r2, #0x3d
    ldr r0, [r1, #0x2c]
    ldr r1, [r1, #0x30]
    and r0, r1
    strh r0, [r7, #0]
    add r0, r4, #0x0
    mov r1, #0x0
    bl native_fn_021edbac
    ldrh r1, [r7, #0]
    mov r0, #0x1
    tst r0, r1
    beq ov006_021ec6f8_L9e
    add r1, r6, #0x0
    ldr r2, [r6, #0x4]
    add r0, r4, #0x0
    add r1, #0x30
    bl native_fn_021edb9c
    add r1, r6, #0x0
    ldr r2, [r6, #0x4]
    add r0, r4, #0x6
    add r1, #0x70
    bl native_fn_021edb9c
    add r0, r4, #0x0
    add r1, r6, #0x0
    ldr r2, [r6, #0x4]
    add r0, #0xc
    add r1, #0xb0
    bl native_fn_021edb9c
    add r0, r4, #0x0
    add r1, r6, #0x0
    ldr r2, [r6, #0x4]
    add r0, #0x12
    add r1, #0xf0
    bl native_fn_021edb9c
    add r0, r6, #0x0
    add r0, #0x8
    bl native_fn_021edcd0
    add r1, r0, #0x0
    add r0, r6, #0x0
    add r0, #0x8
    bl native_fn_021ec8f0
    cmp r0, #0x0
    beq ov006_021ec6f8_L88
    b ov006_021ec6f8_L1c4
ov006_021ec6f8_L88:
    add r0, r6, #0x0
    add r0, #0x8
    bl native_fn_021edcd0
    add r2, r0, #0x0
    add r0, r4, #0x0
    add r6, #0x8
    add r0, #0x18
    add r1, r6, #0x0
    bl native_fn_021edb9c
ov006_021ec6f8_L9e:
    ldrh r1, [r7, #0]
    mov r0, #0x2
    tst r0, r1
    beq ov006_021ec6f8_L10a
    add r0, r4, #0x0
    add r1, r5, #0x0
    ldr r2, [r5, #0x4]
    add r0, #0x39
    add r1, #0x30
    bl native_fn_021edb9c
    add r0, r4, #0x0
    add r1, r5, #0x0
    ldr r2, [r5, #0x4]
    add r0, #0x47
    add r1, #0x70
    bl native_fn_021edb9c
    add r0, r4, #0x0
    add r1, r5, #0x0
    ldr r2, [r5, #0x4]
    add r0, #0x55
    add r1, #0xb0
    bl native_fn_021edb9c
    add r0, r4, #0x0
    add r1, r5, #0x0
    ldr r2, [r5, #0x4]
    add r0, #0x63
    add r1, #0xf0
    bl native_fn_021edb9c
    add r0, r5, #0x0
    add r0, #0x8
    bl native_fn_021edcd0
    add r1, r0, #0x0
    add r0, r5, #0x0
    add r0, #0x8
    bl native_fn_021ec8f0
    cmp r0, #0x0
    bne ov006_021ec6f8_L1c4
    add r0, r5, #0x0
    add r0, #0x8
    bl native_fn_021edcd0
    add r2, r0, #0x0
    add r0, r4, #0x0
    add r5, #0x8
    add r0, #0x71
    add r1, r5, #0x0
    bl native_fn_021edb9c
ov006_021ec6f8_L10a:
    ldrh r1, [r7, #0]
    mov r0, #0x4
    tst r0, r1
    beq ov006_021ec6f8_L162
    ldr r1, [sp, #0x4]
    ldr r0, [sp, #0x4]
    ldr r1, [r1, #0x4]
    add r0, #0x30
    sub r1, r1, #0x1
    bl native_fn_021ec8f0
    cmp r0, #0x0
    bne ov006_021ec6f8_L1c4
    ldr r2, [sp, #0x4]
    ldr r1, [sp, #0x4]
    add r0, r4, #0x0
    ldr r2, [r2, #0x4]
    add r0, #0x92
    add r1, #0x30
    bl native_fn_021edb9c
    ldr r0, [sp, #0x4]
    add r0, #0x8
    bl native_fn_021edcd0
    add r1, r0, #0x0
    ldr r0, [sp, #0x4]
    add r0, #0x8
    bl native_fn_021ec8f0
    cmp r0, #0x0
    bne ov006_021ec6f8_L1c4
    ldr r0, [sp, #0x4]
    add r0, #0x8
    bl native_fn_021edcd0
    ldr r1, [sp, #0x4]
    add r2, r0, #0x0
    add r0, r4, #0x0
    add r1, #0x8
    add r0, #0xd2
    str r1, [sp, #0x4]
    bl native_fn_021edb9c
ov006_021ec6f8_L162:
    ldrh r1, [r7, #0]
    mov r0, #0x8
    tst r0, r1
    beq ov006_021ec6f8_L1ba
    ldr r1, [sp]
    ldr r0, [sp]
    ldr r1, [r1, #0x4]
    add r0, #0x30
    sub r1, r1, #0x1
    bl native_fn_021ec8f0
    cmp r0, #0x0
    bne ov006_021ec6f8_L1c4
    ldr r2, [sp]
    ldr r1, [sp]
    add r0, r4, #0x0
    ldr r2, [r2, #0x4]
    add r0, #0xf3
    add r1, #0x30
    bl native_fn_021edb9c
    ldr r0, [sp]
    add r0, #0x8
    bl native_fn_021edcd0
    add r1, r0, #0x0
    ldr r0, [sp]
    add r0, #0x8
    bl native_fn_021ec8f0
    cmp r0, #0x0
    bne ov006_021ec6f8_L1c4
    ldr r0, [sp]
    add r0, #0x8
    bl native_fn_021edcd0
    add r2, r0, #0x0
    ldr r0, =0x00000133
    ldr r1, [sp]
    add r0, r4, r0
    add r1, #0x8
    str r1, [sp]
    bl native_fn_021edb9c
ov006_021ec6f8_L1ba:
    ldr r1, =0x00000116
    mov r0, #0x0
    add sp, #0x8
    strb r0, [r7, r1]
    pop {r3, r4, r5, r6, r7, pc}
ov006_021ec6f8_L1c4:
    mov r2, #0x55
    add r0, r4, #0x0
    mov r1, #0x0
    lsl r2, r2, #0x2
    bl native_fn_021edbac
    mov r0, #0x0
    mvn r0, r0
    add sp, #0x8
    pop {r3, r4, r5, r6, r7, pc}
}
