/* ov000 row 0x0220c884: 332 bytes.
 *
 * What it does: 83 instructions; 4 call(s) to 0x02042c0c, 0x0221089c, 0x020c56b4, +1 more; loops (back edge at +0x40); returns through pop {r4, r5, pc}
 *
 * Decoded shape: chunk loop.
 *
 *   branch +0x1c -> +0x5c
 *   branch +0x58 -> +0x140
 *   branch +0x60 -> +0x140
 *   branch +0xcc -> +0xec
 *   branch +0xfc -> +0x114
 *   branch +0x118 -> +0x140
 *   test +0x18 cmp r1, #0
 *   test +0x5c cmp r1, #10
 *   test +0xa4 cmp lr, r1
 *   test +0xc0 cmp lr, #0
 *   test +0xf8 cmp r2, r1
 *   test +0x114 cmp r0, #0
 *   6 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0220c884; the literal pool and
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

extern void native_fn_02042c0c(void);
extern void native_fn_0221089c(void);
extern void native_fn_020c56b4(void);
extern void native_fn_021dc374(void);


asm u32 native_ov000_0220c884 (register u32 a0)
{
    stmdb sp!, {r4, r5, lr}
    sub sp, sp, #12
    mov r5, r0
    ldrb r1, [r5, #0x279]
    mov r4, #0
    mov r0, r4
    cmp r1, #0
    bne ov000_0220c884_L5c
    add r0, r5, #112
    add r3, r5, #656
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    mov r2, #1
    mov r0, r5
    mov r1, #31
    strb r2, [r5, #0x2c1]
    bl native_fn_02042c0c
    mov r0, r5
    mov r1, #1
    bl native_fn_0221089c
    mov r0, #10
    strb r0, [r5, #0x279]
    b ov000_0220c884_L140
ov000_0220c884_L5c:
    cmp r1, #10
    bne ov000_0220c884_L140
    add r1, r5, #512
    ldrsh r3, [r1, #122]
    mov r1, #89
    ldr r2, [r5, #0x288]
    smulbb r1, r3, r1
    mul r1, r3, r1
    sub lr, r2, r1, asr #1
    ldr r3, [r5, #0x284]
    ldr r2, [r5, #0x70]
    ldr r12, [r5, #0x28c]
    add r2, r2, r3
    str r2, [r5, #0x70]
    ldr r2, [r5, #0x78]
    sub r1, r4, #8192
    add r2, r2, r12
    str r2, [r5, #0x78]
    cmp lr, r1
    movlt lr, r1
    ldr r2, [r5, #0x74]
    add r1, r5, #512
    add r2, r2, lr
    str r2, [r5, #0x74]
    ldrsh r2, [r1, #122]
    cmp lr, #0
    add r2, r2, #1
    strh r2, [r1, #122]
    bge ov000_0220c884_Lec
    ldrsh r0, [r1, #118]
    bl native_fn_020c56b4
    ldrb r3, [r0, #0xc]
    add r2, sp, #0
    add r0, r5, #112
    add r1, r5, #528
    bl native_fn_021dc374
ov000_0220c884_Lec:
    ldr r1, [r5, #0x294]
    ldr r2, [r5, #0x74]
    sub r1, r1, #4194304
    cmp r2, r1
    bge ov000_0220c884_L114
    add r0, r5, #112
    add r3, sp, #0
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    mov r0, #1
ov000_0220c884_L114:
    cmp r0, #0
    beq ov000_0220c884_L140
    add r0, sp, #0
    add r3, r5, #112
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    mov r0, #0
    strb r0, [r5, #0x2c1]
    mov r0, #20
    strb r0, [r5, #0x279]
    mov r4, #1
ov000_0220c884_L140:
    mov r0, r4
    add sp, sp, #12
    ldmia sp!, {r4, r5, pc}
}
