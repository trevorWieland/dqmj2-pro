/* ov006 row 0x021ecd28: 244 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xec -> native_data2_0220d448 (image word 0x0220d448)
 *   pool +0xf0 -> native_data2_0221a8ac (image word 0x0221a8ac)
 *   branch +0x2e -> +0x3e
 *   branch +0x4c -> +0xe6
 *   branch +0x5a -> +0x66
 *   branch +0x70 -> +0x78
 *   branch +0x86 -> +0x94
 *   branch +0xae -> +0xca
 *   branch +0xbc -> +0xc4
 *   test +0x2c cmp r0, r1
 *   test +0x4a cmp r0, #0x0
 *   test +0x58 cmp r0, r1
 *   test +0x6e tst r0, r1
 *   test +0xac cmp r0, #0x0
 *   test +0xba cmp r0, #0x2
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ecd28; the literal pool and
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

extern void native_fn_021edb9c(void);
extern u8 native_data2_0220d448[];
extern void native_fn_021edcd0(void);
extern void native_fn_021ed9d4(void);
extern void native_fn_021ec6e0(void);
extern void native_fn_021edcb8(void);
extern void native_fn_021ece1c(void);
extern u8 native_data2_0221a8ac[];
extern void native_fn_021ebb1c(void);
extern void native_fn_021ed7e4(void);
extern void native_fn_021ebb2c(void);
extern void native_fn_021ec6ec(void);
extern void native_fn_021edc78(void);


asm u32 native_ov006_021ecd28 (register u32 a0)
{
    push {r4, r5, r6, r7, lr}
    sub sp, #0x14
    add r5, r0, #0x0
    add r1, r5, #0x0
    add r4, r5, #0x0
    add r0, sp, #0xc
    add r1, #0x10
    mov r2, #0x8
    add r4, #0x18
    bl native_fn_021edb9c
    ldr r0, =native_data2_0220d448
    bl native_fn_021edcd0
    add r3, r0, #0x0
    ldr r2, =native_data2_0220d448
    add r0, sp, #0xc
    mov r1, #0x8
    bl native_fn_021ed9d4
    mov r1, #0x0
    mvn r1, r1
    cmp r0, r1
    bne ov006_021ecd28_L3e
    mov r0, #0x2
    bl native_fn_021ec6e0
    mov r0, #0x63
    add sp, #0x14
    mvn r0, r0
    pop {r4, r5, r6, r7, pc}
ov006_021ecd28_L3e:
    ldrh r0, [r5, #0x6]
    bl native_fn_021edcb8
    add r1, sp, #0xc
    bl native_fn_021ece1c
    cmp r0, #0x0
    bne ov006_021ecd28_Le6
    ldrh r0, [r5, #0x6]
    bl native_fn_021edcb8
    mov r1, #0x1
    lsl r1, r1, #0xc
    cmp r0, r1
    bne ov006_021ecd28_L66
    ldr r0, =native_data2_0221a8ac
    add r1, sp, #0xc
    mov r2, #0x8
    bl native_fn_021edb9c
ov006_021ecd28_L66:
    ldrh r0, [r5, #0xc]
    bl native_fn_021edcb8
    mov r1, #0xf
    tst r0, r1
    bne ov006_021ecd28_L78
    add sp, #0x14
    mov r0, #0x0
    pop {r4, r5, r6, r7, pc}
ov006_021ecd28_L78:
    ldrh r0, [r4, #0]
    bl native_fn_021edcb8
    add r6, r0, #0x0
    bl native_fn_021ebb1c
    add r7, r0, #0x0
    bne ov006_021ecd28_L94
    mov r0, #0x2
    bl native_fn_021ec6e0
    add sp, #0x14
    mov r0, #0x64
    pop {r4, r5, r6, r7, pc}
ov006_021ecd28_L94:
    add r0, r4, #0x2
    str r0, [sp]
    ldr r0, =native_data2_0221a8ac
    add r1, r7, #0x0
    str r0, [sp, #0x4]
    mov r0, #0x8
    str r0, [sp, #0x8]
    ldrb r3, [r5, #0xe]
    add r0, r4, #0x4
    add r2, r6, #0x0
    bl native_fn_021ed7e4
    cmp r0, #0x0
    bge ov006_021ecd28_Lca
    add r0, r7, #0x0
    bl native_fn_021ebb2c
    bl native_fn_021ec6ec
    cmp r0, #0x2
    bne ov006_021ecd28_Lc4
    add sp, #0x14
    mov r0, #0x64
    pop {r4, r5, r6, r7, pc}
ov006_021ecd28_Lc4:
    add sp, #0x14
    mov r0, #0xc8
    pop {r4, r5, r6, r7, pc}
ov006_021ecd28_Lca:
    add r0, r4, #0x0
    add r1, r7, #0x0
    add r2, r6, #0x0
    bl native_fn_021edb9c
    lsl r0, r6, #0x10
    lsr r0, r0, #0x10
    bl native_fn_021edc78
    strh r0, [r5, #0xa]
    add r0, r7, #0x0
    bl native_fn_021ebb2c
    mov r0, #0x0
ov006_021ecd28_Le6:
    add sp, #0x14
    pop {r4, r5, r6, r7, pc}
    mov r8, r8
}
