/* ov000 row 0x0220aac4: 388 bytes.
 *
 * What it does: 97 instructions; 12 call(s) to 0x0220aa68, 0x021e07b8, 0x020c56b4, +9 more; loops (back edge at +0x14); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: chunk loop.
 *
 *   branch +0x1c -> +0x178
 *   branch +0x58 -> +0x74
 *   branch +0x70 -> +0x8c
 *   branch +0xbc -> +0x178
 *   branch +0x118 -> +0x178
 *   branch +0x140 -> +0x14c
 *   test +0x18 cmp r0, #0
 *   test +0x54 cmp r0, #2
 *   test +0x6c cmp r0, #3
 *   test +0x7c cmp r1, r0
 *   test +0xb8 cmp r1, r0, lsl #1
 *   test +0x138 cmp r9, #0
 *   test +0x144 cmp r5, #737280
 *   test +0x170 cmp r0, r5, lsl #1
 *   4 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0220aac4; the literal pool and
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

extern void native_fn_0220aa68(void);
extern void native_fn_021e07b8(void);
extern void native_fn_020c56b4(void);
extern void native_fn_0220a960(void);
extern void native_fn_0220a7f4(void);
extern void native_fn_0220a8d0(void);
extern void native_fn_0220aa0c(void);
extern void native_fn_02042c2c(void);
extern void native_fn_0202818c(void);
extern void native_fn_02028158(void);


asm u32 native_ov000_0220aac4 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #28
    mov r10, r0
    mov r9, r1
    mov r7, #0
    bl native_fn_0220aa68
    cmp r0, #0
    beq ov000_0220aac4_L178
    mov r0, r7
    bl native_fn_021e07b8
    add r3, sp, #16
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    add r0, r10, #112
    add r4, sp, #4
    ldmia r0, {r0, r1, r2}
    add r3, r10, #512
    stmia r4, {r0, r1, r2}
    ldrsh r0, [r3, #118]
    bl native_fn_020c56b4
    ldrb r0, [r0, #0x6]
    cmp r0, #2
    beq ov000_0220aac4_L74
    add r0, r10, #512
    ldrsh r0, [r0, #118]
    bl native_fn_020c56b4
    ldrb r0, [r0, #0x6]
    cmp r0, #3
    bne ov000_0220aac4_L8c
ov000_0220aac4_L74:
    ldr r1, [sp, #0x14]
    ldr r0, [sp, #0x8]
    cmp r1, r0
    movlt r0, #0
    strlt r0, [sp, #0x14]
    strlt r0, [sp, #0x8]
ov000_0220aac4_L8c:
    add r0, r10, #512
    ldrsh r0, [r0, #118]
    bl native_fn_020c56b4
    ldrb r11, [r0, #0x5]
    mov r0, r10
    mov r1, r11
    bl native_fn_0220a960
    ldr r2, [sp, #0x14]
    ldr r1, [sp, #0x8]
    sub r1, r2, r1
    add r1, r1, r0
    cmp r1, r0, lsl #1
    bhs ov000_0220aac4_L178
    mov r0, r10
    mov r1, r11
    bl native_fn_0220a7f4
    ldr r3, [sp, #0x8]
    ldr r2, [sp, #0x14]
    ldr r5, [sp, #0x4]
    sub r6, r3, r2
    ldr r4, [sp, #0x10]
    smull r3, r2, r6, r6
    sub r4, r5, r4
    smlal r3, r2, r4, r4
    ldr r5, [sp, #0xc]
    ldr r4, [sp, #0x18]
    mov r6, r0
    sub r0, r5, r4
    smlal r3, r2, r0, r0
    mov r5, r3, lsr #12
    orr r5, r5, r2, lsl #20
    mov r8, r1
    mov r4, r2, asr #12
    subs r0, r5, r6
    sbcs r0, r4, r8
    bge ov000_0220aac4_L178
    mov r0, r11
    bl native_fn_0220a8d0
    mov r3, r5
    mov r1, r6
    mov r2, r8
    str r4, [sp]
    bl native_fn_0220aa0c
    cmp r9, #0
    mov r5, r0, asr #1
    beq ov000_0220aac4_L14c
    cmp r5, #737280
    movgt r5, #737280
ov000_0220aac4_L14c:
    mov r0, r10
    bl native_fn_02042c2c
    mov r4, r0
    add r0, sp, #4
    add r1, sp, #16
    bl native_fn_0202818c
    sub r0, r4, r0
    bl native_fn_02028158
    add r0, r0, r5
    cmp r0, r5, lsl #1
    movlo r7, #1
ov000_0220aac4_L178:
    mov r0, r7
    add sp, sp, #28
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
