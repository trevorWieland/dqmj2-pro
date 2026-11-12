/* ov000 row 0x0220c164: 472 bytes.
 *
 * What it does: 118 instructions; 13 call(s) to 0x02041f74, 0x021e6158, 0x021d8c18, +10 more; loops (back edge at +0x18); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: chunk loop.
 *
 *   branch +0x38 -> +0x64
 *   branch +0x48 -> +0x5c
 *   branch +0x58 -> +0x64
 *   back edge +0x60 -> +0x24
 *   branch +0x68 -> +0x150
 *   branch +0x90 -> +0x114
 *   branch +0xe8 -> +0x104
 *   back edge +0x110 -> +0xa0
 *   branch +0x160 -> +0x1a8
 *   test +0x44 cmp r0, #0
 *   test +0x50 cmp r4, #16
 *   test +0x64 cmp r4, #0
 *   test +0x88 cmp r4, #0
 *   test +0x108 cmp r9, r4
 *   test +0x15c cmp r0, #0
 *   18 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0220c164; the literal pool and
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

extern void native_fn_02041f74(void);
extern void native_fn_021e6158(void);
extern void native_fn_021d8c18(void);
extern void native_fn_021e07b8(void);
extern void native_fn_021e61c0(void);
extern void native_fn_02041f34(void);
extern void native_fn_021e61f8(void);


asm u32 native_ov000_0220c164 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #64
    mov r6, #0
    add r1, sp, #16
    mov r10, r0
    mov r4, r6
    bl native_fn_02041f74
    add r7, sp, #0
    add r5, sp, #52
ov000_0220c164_L24:
    ldrb r2, [r10, #0x2c0]
    mov r0, r6
    mov r1, r5
    bl native_fn_021e6158
    movs r6, r0
    bmi ov000_0220c164_L64
    mov r0, r5
    bl native_fn_021d8c18
    cmp r0, #0
    beq ov000_0220c164_L5c
    add r4, r4, #1
    cmp r4, #16
    strb r6, [r7], #1
    bge ov000_0220c164_L64
ov000_0220c164_L5c:
    add r6, r6, #1
    b ov000_0220c164_L24
ov000_0220c164_L64:
    cmp r4, #0
    ble ov000_0220c164_L150
    mov r6, #0
    mov r0, r6
    mov r5, r6
    bl native_fn_021e07b8
    add r3, sp, #28
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    cmp r4, #0
    mov r9, r6
    ble ov000_0220c164_L114
    ldr r11, [sp, #0x20]
    ldr r8, [sp, #0x24]
    add r7, sp, #0
ov000_0220c164_La0:
    ldrb r0, [r7]
    add r1, sp, #52
    bl native_fn_021e61c0
    ldr r0, [sp, #0x38]
    ldr r3, [sp, #0x3c]
    sub r0, r0, r11
    smull r2, r1, r0, r0
    ldr r0, [sp, #0x34]
    ldr r12, [sp, #0x1c]
    sub r3, r3, r8
    sub r0, r0, r12
    smlal r2, r1, r0, r0
    smlal r2, r1, r3, r3
    mov r12, r2, lsr #12
    orr r12, r12, r1, lsl #20
    subs r0, r6, r12
    mov r3, r1, asr #12
    sbcs r0, r5, r1, asr #12
    bge ov000_0220c164_L104
    add r0, sp, #52
    add r5, sp, #40
    ldmia r0, {r0, r1, r2}
    stmia r5, {r0, r1, r2}
    mov r6, r12
    mov r5, r3
ov000_0220c164_L104:
    add r9, r9, #1
    cmp r9, r4
    add r7, r7, #1
    blt ov000_0220c164_La0
ov000_0220c164_L114:
    add r0, sp, #40
    add r3, r10, #656
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    ldr r1, [sp, #0x28]
    ldr r2, [sp, #0x14]
    ldr r3, [sp, #0x30]
    mov r0, r10
    bl native_fn_02041f34
    add r0, r10, #112
    add r3, r10, #272
    ldmia r0, {r0, r1, r2}
    add sp, sp, #64
    stmia r3, {r0, r1, r2}
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov000_0220c164_L150:
    ldrb r1, [r10, #0x2c0]
    add r0, sp, #52
    bl native_fn_021e61f8
    cmp r0, #0
    ble ov000_0220c164_L1a8
    add r1, sp, #52
    bl native_fn_021e61c0
    add r0, sp, #52
    add r3, r10, #656
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    ldr r1, [sp, #0x34]
    ldr r2, [sp, #0x14]
    ldr r3, [sp, #0x3c]
    mov r0, r10
    bl native_fn_02041f34
    add r0, r10, #112
    add r3, r10, #272
    ldmia r0, {r0, r1, r2}
    add sp, sp, #64
    stmia r3, {r0, r1, r2}
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov000_0220c164_L1a8:
    add r5, r10, #680
    add r3, r10, #656
    ldmia r5, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    add r4, r10, #112
    ldmia r5, {r0, r1, r2}
    stmia r4, {r0, r1, r2}
    add r3, r10, #272
    ldmia r4, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    add sp, sp, #64
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
