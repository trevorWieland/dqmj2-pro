/* ov000 row 0x021ee1b0: 336 bytes.
 *
 * What it does: 80 instructions; 10 call(s) to 0x021ec718, 0x02084808, 0x021ee248, +7 more; loops (back edge at +0x0c); returns through pop {r4, r5, r6, r7, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x140 -> constant 0x02236bc4 (image word 0x02236bc4)
 *   pool +0x144 -> native_fn_021ee078 (image word 0x021ee078)
 *   pool +0x148 -> native_fn_021ee088 (image word 0x021ee088)
 *   pool +0x14c -> native_fn_021ee098 (image word 0x021ee098)
 *   branch +0x30 -> +0xb4
 *   branch +0x38 -> +0x4c
 *   branch +0x40 -> +0xb4
 *   branch +0x54 -> +0x98
 *   branch +0x68 -> +0x8c
 *   back edge +0x94 -> +0x58
 *   branch +0xb0 -> +0x118
 *   branch +0xbc -> +0x100
 *   branch +0xd0 -> +0xf4
 *   back edge +0xfc -> +0xc4
 *   test +0x2c cmp r4, #0
 *   test +0x34 cmp r4, #1
 *   test +0x3c cmp r4, #2
 *   test +0x4c cmp r5, #1
 *   test +0x64 cmp r0, #0
 *   test +0x90 cmp r4, r5
 *   test +0xb4 cmp r5, #1
 *   test +0xcc cmp r0, #0
 *   test +0xf8 cmp r4, r5
 *   0 block transfer(s), 11 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021ee1b0; the literal pool and
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

extern void native_fn_021ec718(void);
extern void native_fn_02084808(void);
extern void native_fn_02084830(void);
extern void native_fn_021ee078(void);
extern void native_fn_021ee088(void);
extern void native_fn_021ee098(void);
extern void native_fn_02063144(void);
extern void native_fn_021ee0a4(void);


asm u32 native_ov000_021ee1b0 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, lr}
    sub sp, sp, #12
    mov r4, r0
    bl native_fn_021ec718
    mov r6, r0
    bl native_fn_02084808
    ldr r7, =0x02236bc4
    mov r2, #0
    ldr r1, [r7, #0x4]
    mov r5, r0
    strb r2, [r1, #0x504]
    cmp r4, #0
    beq ov000_021ee1b0_Lb4
    cmp r4, #1
    beq ov000_021ee1b0_L4c
    cmp r4, #2
    beq ov000_021ee1b0_Lb4
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, pc}
ov000_021ee1b0_L4c:
    cmp r5, #1
    mov r4, #1
    bls ov000_021ee1b0_L98
ov000_021ee1b0_L58:
    mov r0, r4
    mov r1, r6
    bl native_fn_02084830
    cmp r0, #0
    beq ov000_021ee1b0_L8c
    ldr r1, [r7, #0x4]
    ldrb r0, [r1, #0x504]
    add r0, r1, r0, lsl #2
    str r4, [r0, #0x104]
    ldr r1, [r7, #0x4]
    ldrb r0, [r1, #0x504]
    add r0, r0, #1
    strb r0, [r1, #0x504]
ov000_021ee1b0_L8c:
    add r4, r4, #1
    cmp r4, r5
    blo ov000_021ee1b0_L58
ov000_021ee1b0_L98:
    ldr r2, =native_fn_021ee078
    ldr r1, =native_fn_021ee088
    ldr r0, =native_fn_021ee098
    str r2, [sp]
    str r1, [sp, #0x4]
    str r0, [sp, #0x8]
    b ov000_021ee1b0_L118
ov000_021ee1b0_Lb4:
    cmp r5, #1
    mov r4, #1
    bls ov000_021ee1b0_L100
    ldr r6, =0x02236bc4
ov000_021ee1b0_Lc4:
    mov r0, r4
    bl native_fn_02063144
    cmp r0, #0
    ble ov000_021ee1b0_Lf4
    ldr r1, [r6, #0x4]
    ldrb r0, [r1, #0x504]
    add r0, r1, r0, lsl #2
    str r4, [r0, #0x104]
    ldr r1, [r6, #0x4]
    ldrb r0, [r1, #0x504]
    add r0, r0, #1
    strb r0, [r1, #0x504]
ov000_021ee1b0_Lf4:
    add r4, r4, #1
    cmp r4, r5
    blo ov000_021ee1b0_Lc4
ov000_021ee1b0_L100:
    ldr r2, =native_fn_021ee078
    ldr r1, =native_fn_021ee088
    ldr r0, =native_fn_021ee098
    str r2, [sp]
    str r1, [sp, #0x4]
    str r0, [sp, #0x8]
ov000_021ee1b0_L118:
    ldr r0, =0x02236bc4
    add r2, sp, #0
    ldr r0, [r0, #0x4]
    ldrb r3, [r0, #0x50a]
    ldrb r1, [r0, #0x504]
    add r0, r0, #260
    ldr r2, [r2, r3, lsl #2]
    bl native_fn_021ee0a4
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, pc}
}
