/* ov000 row 0x0220a120: 356 bytes.
 *
 * What it does: 87 instructions; 12 call(s) to 0x0220a144, 0x02002480, 0x02026144, +9 more; loops (back edge at +0x1c); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x15c -> constant 0x022385b8 (image word 0x022385b8)
 *   pool +0x160 -> constant 0x022385d4 (image word 0x022385d4)
 *   branch +0x14 -> +0x24
 *   branch +0x40 -> +0x58
 *   branch +0x54 -> +0x60
 *   test +0x0c cmp r1, #0
 *   test +0x2c cmp r1, #0
 *   test +0x3c cmp r0, #1000
 *   test +0x64 cmp r9, #0
 *   test +0x74 cmp r1, #4
 *   2 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0220a120; the literal pool and
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

extern void native_fn_02002480(void);
extern void native_fn_02026144(void);
extern void native_fn_020449d4(void);
extern void native_fn_020c58c0(void);
extern void native_fn_021d8a50(void);


asm u32 native_ov000_0220a120 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r10, r0
    ldr r1, [r10, #0x2bc]
    cmp r1, #0
    movle r1, #24
    ble ov000_0220a120_L24
    mov r0, #98304
    bl native_fn_02002480
    mov r1, r0
ov000_0220a120_L24:
    ldrb r0, [r10, #0x161]
    bl native_fn_02026144
    cmp r1, #0
    ldmneia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    add r0, r10, #512
    ldrsh r0, [r0, #118]
    cmp r0, #1000
    bne ov000_0220a120_L58
    add r0, r10, #256
    ldrsh r0, [r0, #106]
    sub r0, r0, #52
    bl native_fn_020449d4
    b ov000_0220a120_L60
ov000_0220a120_L58:
    bl native_fn_020c58c0
    bl native_fn_020449d4
ov000_0220a120_L60:
    ldrb r9, [r0, #0x61]
    cmp r9, #0
    ldmleia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    ldr r0, =0x022385b8
    ldrsb r1, [r0, #1]
    cmp r1, #4
    ldmgeia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    mov r0, #24
    mul r7, r1, r0
    ldr r1, =0x022385d4
    mov r0, #0
    add r8, r1, r7
    bl native_fn_021d8a50
    mov r6, r0
    mov r0, #0
    bl native_fn_021d8a50
    mov r5, r0
    mov r0, #0
    bl native_fn_021d8a50
    mov r4, r0
    mov r0, #0
    bl native_fn_021d8a50
    mov r11, r0
    mov r0, #0
    bl native_fn_021d8a50
    str r0, [sp]
    mov r0, #0
    bl native_fn_021d8a50
    ldr r3, [r4]
    ldr r2, [r11]
    ldr r11, [r10, #0x70]
    ldr r1, [sp]
    sub r3, r11, r3
    sub r2, r11, r2
    ldr r1, [r1, #0x4]
    ldr r11, [r10, #0x74]
    ldr r0, [r0, #0x4]
    ldr r4, [r10, #0x78]
    ldr r6, [r6, #0x8]
    sub r1, r11, r1
    sub r0, r11, r0
    smull r11, r0, r1, r0
    smlal r11, r0, r3, r2
    ldr r5, [r5, #0x8]
    sub r6, r4, r6
    sub r4, r4, r5
    smlal r11, r0, r6, r4
    mov r2, r11, lsr #12
    mov r1, r0, asr #12
    orr r2, r2, r0, lsl #20
    ldr r0, =0x022385d4
    ldr r3, =0x022385b8
    str r2, [r0, r7]
    add r10, r10, #112
    str r1, [r8, #0x4]
    add r5, r8, #8
    ldmia r10, {r0, r1, r2}
    stmia r5, {r0, r1, r2}
    ldrsb r0, [r3, #1]
    str r9, [r8, #0x14]
    add r0, r0, #1
    strb r0, [r3, #0x1]
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
