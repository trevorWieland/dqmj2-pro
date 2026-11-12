/* ov000 row 0x021dcd34: 608 bytes.
 *
 * What it does: 152 instructions; 10 call(s) to 0x021dcb60, 0x021dcce8, 0x021dcce8, +7 more; loops (back edge at +0xb8); returns through pop {r4, r5, r6, r7, r8, pc}
 *
 * Decoded shape: chunk loop.
 *
 *   branch +0x2c -> +0x40
 *   branch +0x3c -> +0x4c
 *   branch +0x94 -> +0xf4
 *   branch +0xc0 -> +0xf4
 *   branch +0xd8 -> +0xf4
 *   branch +0xf8 -> +0x198
 *   branch +0x138 -> +0x198
 *   branch +0x164 -> +0x198
 *   branch +0x17c -> +0x198
 *   branch +0x19c -> +0x23c
 *   branch +0x1dc -> +0x23c
 *   branch +0x208 -> +0x23c
 *   branch +0x220 -> +0x23c
 *   branch +0x240 -> +0x254
 *   test +0x10 cmp r4, #0
 *   test +0xbc cmp r0, #0
 *   test +0xd4 cmp r0, #0
 *   test +0xec cmp r0, #0
 *   test +0xf4 cmp r4, #0
 *   test +0x160 cmp r0, #0
 *   test +0x178 cmp r0, #0
 *   test +0x190 cmp r0, #0
 *   test +0x198 cmp r4, #0
 *   test +0x204 cmp r0, #0
 *   test +0x21c cmp r0, #0
 *   test +0x234 cmp r0, #0
 *   test +0x23c cmp r4, #0
 *   7 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021dcd34; the literal pool and
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

extern void native_fn_021dcb60(void);
extern void native_fn_021dcce8(void);


asm u32 native_ov000_021dcd34 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    sub sp, sp, #40
    ldr r4, [sp, #0x40]
    mov r7, r3
    cmp r4, #0
    mov r12, r0
    mov r6, r1
    mov r8, r2
    mvn r4, #0
    add r5, sp, #28
    add r3, sp, #16
    bne ov000_021dcd34_L40
    ldmia r12, {r0, r1, r2}
    stmia r5, {r0, r1, r2}
    ldmia r6, {r0, r1, r2}
    b ov000_021dcd34_L4c
ov000_021dcd34_L40:
    ldmia r6, {r0, r1, r2}
    stmia r5, {r0, r1, r2}
    ldmia r12, {r0, r1, r2}
ov000_021dcd34_L4c:
    stmia r3, {r0, r1, r2}
    ldr r6, [sp, #0x1c]
    ldr r3, [r8]
    ldr r0, [r8, #0xc]
    ldr r5, [sp, #0x24]
    ldr r2, [r8, #0x14]
    ldr r1, [r8, #0x8]
    sub r3, r3, r6
    sub r2, r2, r5
    sub r1, r1, r5
    sub r0, r0, r6
    smull r14, r12, r3, r2
    smull r2, r0, r1, r0
    subs r3, lr, r2
    mov r1, #0
    sbc r2, r12, r0
    subs r0, r1, r3
    sbcs r0, r1, r2
    bge ov000_021dcd34_Lf4
    add r0, sp, #16
    str r0, [sp]
    add r12, sp, #28
    add r0, sp, #12
    add r1, sp, #8
    mov r2, r8
    add r3, r8, #12
    str r12, [sp, #0x4]
    bl native_fn_021dcb60
    cmp r0, #0
    beq ov000_021dcd34_Lf4
    ldr r0, [r8]
    ldr r1, [r8, #0xc]
    ldr r2, [sp, #0xc]
    bl native_fn_021dcce8
    cmp r0, #0
    beq ov000_021dcd34_Lf4
    ldr r0, [r8, #0x8]
    ldr r1, [r8, #0x14]
    ldr r2, [sp, #0x8]
    bl native_fn_021dcce8
    cmp r0, #0
    movne r4, #0
ov000_021dcd34_Lf4:
    cmp r4, #0
    bge ov000_021dcd34_L198
    ldr r3, [r8, #0xc]
    ldr r2, [r8, #0x20]
    ldr r1, [r8, #0x14]
    ldr r0, [r8, #0x18]
    sub r3, r3, r6
    sub r2, r2, r5
    sub r1, r1, r5
    sub r0, r0, r6
    smull r14, r12, r3, r2
    smull r2, r0, r1, r0
    subs r3, lr, r2
    mov r1, #0
    sbc r2, r12, r0
    subs r0, r1, r3
    sbcs r0, r1, r2
    bge ov000_021dcd34_L198
    add r0, sp, #16
    str r0, [sp]
    add r12, sp, #28
    add r0, sp, #12
    add r1, sp, #8
    add r2, r8, #12
    add r3, r8, #24
    str r12, [sp, #0x4]
    bl native_fn_021dcb60
    cmp r0, #0
    beq ov000_021dcd34_L198
    ldr r0, [r8, #0xc]
    ldr r1, [r8, #0x18]
    ldr r2, [sp, #0xc]
    bl native_fn_021dcce8
    cmp r0, #0
    beq ov000_021dcd34_L198
    ldr r0, [r8, #0x14]
    ldr r1, [r8, #0x20]
    ldr r2, [sp, #0x8]
    bl native_fn_021dcce8
    cmp r0, #0
    movne r4, #1
ov000_021dcd34_L198:
    cmp r4, #0
    bge ov000_021dcd34_L23c
    ldr r3, [r8, #0x18]
    ldr r2, [r8, #0x8]
    ldr r1, [r8, #0x20]
    ldr r0, [r8]
    sub r3, r3, r6
    sub r2, r2, r5
    sub r1, r1, r5
    sub r0, r0, r6
    smull r6, r5, r3, r2
    smull r2, r0, r1, r0
    subs r3, r6, r2
    mov r1, #0
    sbc r2, r5, r0
    subs r0, r1, r3
    sbcs r0, r1, r2
    bge ov000_021dcd34_L23c
    add r0, sp, #16
    str r0, [sp]
    add r5, sp, #28
    add r0, sp, #12
    add r1, sp, #8
    mov r3, r8
    add r2, r8, #24
    str r5, [sp, #0x4]
    bl native_fn_021dcb60
    cmp r0, #0
    beq ov000_021dcd34_L23c
    ldr r0, [r8, #0x18]
    ldr r1, [r8]
    ldr r2, [sp, #0xc]
    bl native_fn_021dcce8
    cmp r0, #0
    beq ov000_021dcd34_L23c
    ldr r0, [r8, #0x20]
    ldr r1, [r8, #0x8]
    ldr r2, [sp, #0x8]
    bl native_fn_021dcce8
    cmp r0, #0
    movne r4, #2
ov000_021dcd34_L23c:
    cmp r4, #0
    blt ov000_021dcd34_L254
    ldr r0, [sp, #0xc]
    str r0, [r7]
    ldr r0, [sp, #0x8]
    str r0, [r7, #0x8]
ov000_021dcd34_L254:
    mov r0, r4
    add sp, sp, #40
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
