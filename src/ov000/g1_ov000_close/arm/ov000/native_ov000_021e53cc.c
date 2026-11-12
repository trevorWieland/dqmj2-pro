/* ov000 row 0x021e53cc: 248 bytes.
 *
 * What it does: 60 instructions; 3 call(s) to 0x021e47cc, 0x021e53fc, 0x021e031c; loops (back edge at +0xb0); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xf0 -> constant 0x27100000 (image word 0x27100000)
 *   pool +0xf4 -> constant 0x02234388 (image word 0x02234388)
 *   branch +0x38 -> +0xb8
 *   branch +0x4c -> +0xb8
 *   branch +0x94 -> +0xb8
 *   back edge +0xc4 -> +0x30
 *   branch +0xd0 -> +0xe8
 *   test +0x34 cmp r0, #0
 *   test +0x40 cmp r0, #6
 *   test +0x48 cmpeq r0, #1
 *   test +0xbc cmp r4, #64
 *   test +0xc8 cmp r7, #0
 *   test +0xcc cmpne r2, #0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e53cc; the literal pool and
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

extern void native_fn_021e47cc(void);
extern void native_fn_021e031c(void);


asm u32 native_ov000_021e53cc (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r1, #0
    ldr r6, =0x27100000
    ldr r8, =0x02234388
    str r1, [sp]
    mov r9, r0
    mov r7, r1
    mov r2, r1
    mov r5, r1
    mov r4, r1
    mov r10, #6
    mov r11, r1
ov000_021e53cc_L30:
    ldrb r0, [r8, #0x1c]
    cmp r0, #0
    beq ov000_021e53cc_Lb8
    ldrb r0, [r8, #0x1d]
    cmp r0, #6
    ldreqsb r0, [r8, #32]
    cmpeq r0, #1
    bne ov000_021e53cc_Lb8
    ldr r1, [r9, #0x74]
    ldr r0, [r8, #0x4]
    ldr lr, [r9, #0x70]
    sub r3, r1, r0
    smull r1, r0, r3, r3
    ldr r12, [r8]
    ldr r3, [r9, #0x78]
    sub r12, lr, r12
    smlal r1, r0, r12, r12
    ldr r12, [r8, #0x8]
    sub r3, r3, r12
    smlal r1, r0, r3, r3
    mov r3, r1, lsr #12
    orr r3, r3, r0, lsl #20
    mov r12, r0, asr #12
    subs r0, r3, r6
    sbcs r0, r12, r5
    bge ov000_021e53cc_Lb8
    ldrsb r1, [r8, #30]
    mov r0, r10
    mov r2, r11
    mov r6, r3
    mov r5, r12
    mov r7, r8
    bl native_fn_021e47cc
    mov r2, r0
ov000_021e53cc_Lb8:
    add r4, r4, #1
    cmp r4, #64
    add r8, r8, #52
    blt ov000_021e53cc_L30
    cmp r7, #0
    cmpne r2, #0
    beq ov000_021e53cc_Le8
    mov r0, r9
    mov r1, r7
    bl native_fn_021e031c
    mov r0, #1
    str r0, [sp]
ov000_021e53cc_Le8:
    ldr r0, [sp]
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
