/* ov000 row 0x021e59e4: 488 bytes.
 *
 * What it does: 121 instructions; 7 call(s) to 0x021e5a20, 0x021e5bac, 0x021e58ec, +4 more; loops (back edge at +0x5c); returns through pop {r4, r5, r6, r7, r8, r9, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x1e4 -> constant 0x022332e8 (image word 0x022332e8)
 *   branch +0x28 -> +0x1c8
 *   back edge +0x5c -> +0x3c
 *   branch +0x74 -> +0x1c8
 *   branch +0x94 -> +0xb8
 *   branch +0xbc -> +0x140
 *   branch +0xcc -> +0x1d8
 *   branch +0x104 -> +0x1d8
 *   branch +0x128 -> +0x1d8
 *   branch +0x13c -> +0x1d8
 *   branch +0x144 -> +0x1c8
 *   branch +0x154 -> +0x1d8
 *   branch +0x18c -> +0x1d8
 *   branch +0x1b0 -> +0x1d8
 *   branch +0x1c4 -> +0x1d8
 *   back edge +0x1d4 -> +0x20
 *   test +0x24 cmp r0, #0
 *   test +0x44 cmp r12, r2
 *   test +0x4c cmp r12, r3
 *   test +0x54 cmp r0, #4
 *   test +0x68 cmp r0, r1
 *   test +0x70 cmpgt r1, r0
 *   test +0x8c cmp r0, #0
 *   test +0xac cmp r0, #0
 *   test +0xb8 cmp r0, #1
 *   test +0xc8 cmp r0, #0
 *   test +0x100 cmp r7, #0
 *   test +0x124 cmp r0, #0
 *   test +0x140 cmp r0, #2
 *   test +0x150 cmp r0, #0
 *   test +0x188 cmp r7, #0
 *   test +0x1ac cmp r0, #0
 *   test +0x1cc cmp r9, #32
 *   16 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e59e4; the literal pool and
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

extern void native_fn_021e58ec(void);
extern void native_fn_021dcf94(void);


asm u32 native_ov000_021e59e4 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, lr}
    sub sp, sp, #52
    mov r4, #0
    ldr r5, =0x022332e8
    mov r8, r0
    mov r7, r1
    mov r6, r2
    mov r9, r4
ov000_021e59e4_L20:
    ldrb r0, [r5]
    cmp r0, #0
    beq ov000_021e59e4_L1c8
    ldr r2, [r5, #0x14]
    add r1, r5, #12
    mov r3, r2
    mov r0, #1
ov000_021e59e4_L3c:
    ldr r12, [r1, #0x14]
    add r0, r0, #1
    cmp r12, r2
    movgt r2, r12
    cmp r12, r3
    movlt r3, r12
    cmp r0, #4
    add r1, r1, #12
    blt ov000_021e59e4_L3c
    ldr r1, [r8, #0x4]
    add r0, r2, #4096
    cmp r0, r1
    subgt r0, r3, #4096
    cmpgt r1, r0
    ble ov000_021e59e4_L1c8
    mov r0, r8
    add r1, r5, #16
    add r2, r5, #28
    add r3, r5, #40
    bl native_fn_021e58ec
    cmp r0, #0
    moveq r0, #1
    beq ov000_021e59e4_Lb8
    mov r0, r8
    add r1, r5, #40
    add r2, r5, #52
    add r3, r5, #16
    bl native_fn_021e58ec
    cmp r0, #0
    moveq r0, #2
    movne r0, #0
ov000_021e59e4_Lb8:
    cmp r0, #1
    bne ov000_021e59e4_L140
    ldrb r0, [r5, #0x1]
    mov r4, #2
    cmp r0, #0
    beq ov000_021e59e4_L1d8
    add r0, r5, #16
    add r12, sp, #16
    ldmia r0, {r0, r1, r2}
    stmia r12, {r0, r1, r2}
    add r0, r5, #28
    add r3, sp, #28
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    add r0, r5, #40
    add r3, sp, #40
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    cmp r7, #0
    beq ov000_021e59e4_L1d8
    mov r5, #1
    add r3, sp, #4
    mov r0, r8
    mov r1, r7
    mov r2, r12
    str r5, [sp]
    bl native_fn_021dcf94
    cmp r0, #0
    beq ov000_021e59e4_L1d8
    add r0, sp, #4
    ldmia r0, {r0, r1, r2}
    mov r4, r5
    stmia r6, {r0, r1, r2}
    b ov000_021e59e4_L1d8
ov000_021e59e4_L140:
    cmp r0, #2
    bne ov000_021e59e4_L1c8
    ldrb r0, [r5, #0x1]
    mov r4, #2
    cmp r0, #0
    beq ov000_021e59e4_L1d8
    add r0, r5, #40
    add r12, sp, #16
    ldmia r0, {r0, r1, r2}
    stmia r12, {r0, r1, r2}
    add r0, r5, #52
    add r3, sp, #28
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    add r0, r5, #16
    add r3, sp, #40
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    cmp r7, #0
    beq ov000_021e59e4_L1d8
    mov r5, #1
    add r3, sp, #4
    mov r0, r8
    mov r1, r7
    mov r2, r12
    str r5, [sp]
    bl native_fn_021dcf94
    cmp r0, #0
    beq ov000_021e59e4_L1d8
    add r0, sp, #4
    ldmia r0, {r0, r1, r2}
    mov r4, r5
    stmia r6, {r0, r1, r2}
    b ov000_021e59e4_L1d8
ov000_021e59e4_L1c8:
    add r9, r9, #1
    cmp r9, #32
    add r5, r5, #64
    blt ov000_021e59e4_L20
ov000_021e59e4_L1d8:
    mov r0, r4
    add sp, sp, #52
    ldmia sp!, {r4, r5, r6, r7, r8, r9, pc}
}
