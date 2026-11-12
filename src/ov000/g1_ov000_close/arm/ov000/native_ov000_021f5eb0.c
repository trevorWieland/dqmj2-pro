/* ov000 row 0x021f5eb0: 344 bytes.
 *
 * What it does: 85 instructions; 9 call(s) to 0x01ffa8d8, 0x01ffb4ec, 0x01ffa8d8, +6 more; loops (back edge at +0x0c); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x154 -> constant 0x02236ee4 (image word 0x02236ee4)
 *   branch +0x58 -> +0x68
 *   branch +0x80 -> +0xe8
 *   branch +0x88 -> +0xc4
 *   branch +0x90 -> +0x110
 *   branch +0xc0 -> +0x13c
 *   branch +0xe4 -> +0x13c
 *   branch +0x10c -> +0x13c
 *   back edge +0x148 -> +0x34
 *   test +0x10 cmp r0, #0
 *   test +0x44 cmp r0, #4
 *   test +0x78 cmp r1, r5
 *   test +0x84 cmp r1, r4
 *   test +0x8c cmp r1, #0
 *   test +0x144 cmp r10, r0
 *   0 block transfer(s), 16 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f5eb0; the literal pool and
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

extern void native_fn_01ffa8d8(void);
extern void native_fn_01ffb4ec(void);
extern void native_fn_0204aeb4(void);


asm u32 native_ov000_021f5eb0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #16
    mov r10, #0
    bl native_fn_01ffa8d8
    cmp r0, #0
    addle sp, sp, #16
    ldmleia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    mvn r5, #1
    ldr r6, =0x02236ee4
    add r4, r5, #1
    mov r11, r10
    mov r8, r10
    mov r7, #1
ov000_021f5eb0_L34:
    and r0, r10, #255
    bl native_fn_01ffb4ec
    mov r9, r0
    bl native_fn_01ffa8d8
    cmp r0, #4
    add r0, r9, #256
    ldrnesb r0, [r0, #101]
    movne r0, r0, lsl #1
    addne r0, r0, #5
    bne ov000_021f5eb0_L68
    ldrsb r0, [r0, #101]
    mov r0, r0, lsl #2
    add r0, r0, #7
ov000_021f5eb0_L68:
    add r1, r9, #256
    ldrsb r1, [r1, #108]
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    cmp r1, r5
    mov r2, #2
    beq ov000_021f5eb0_Le8
    cmp r1, r4
    beq ov000_021f5eb0_Lc4
    cmp r1, #0
    bne ov000_021f5eb0_L110
    mov r1, #0
    str r1, [sp]
    mov r1, #1
    str r1, [sp, #0x4]
    str r0, [sp, #0x8]
    mov r0, #0
    str r0, [sp, #0xc]
    mov r1, #0
    ldr r0, [r6, #0x1c]
    mov r3, r1
    bl native_fn_0204aeb4
    b ov000_021f5eb0_L13c
ov000_021f5eb0_Lc4:
    str r8, [sp]
    str r7, [sp, #0x4]
    str r0, [sp, #0x8]
    str r8, [sp, #0xc]
    ldr r0, [r6, #0x1c]
    mov r1, r8
    mov r3, r7
    bl native_fn_0204aeb4
    b ov000_021f5eb0_L13c
ov000_021f5eb0_Le8:
    str r11, [sp]
    mov r1, #1
    str r1, [sp, #0x4]
    str r0, [sp, #0x8]
    str r11, [sp, #0xc]
    ldr r0, [r6, #0x1c]
    mov r1, r11
    mov r3, r2
    bl native_fn_0204aeb4
    b ov000_021f5eb0_L13c
ov000_021f5eb0_L110:
    add r3, r1, #2
    mov r1, #0
    str r1, [sp]
    mov r1, #1
    str r1, [sp, #0x4]
    str r0, [sp, #0x8]
    mov r0, #0
    str r0, [sp, #0xc]
    ldr r0, [r6, #0x1c]
    mov r1, #0
    bl native_fn_0204aeb4
ov000_021f5eb0_L13c:
    add r10, r10, #1
    bl native_fn_01ffa8d8
    cmp r10, r0
    blt ov000_021f5eb0_L34
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
