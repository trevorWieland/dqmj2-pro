/* ov000 row 0x0220f6cc: 396 bytes.
 *
 * What it does: 97 instructions; 17 call(s) to 0x0220a2a4, 0x0220f018, 0x02025a28, +14 more; loops (back edge at +0x3c); returns through pop {r4, r5, r6, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x184 -> constant 0x41a00000 (image word 0x41a00000)
 *   pool +0x188 -> constant 0x45800000 (image word 0x45800000)
 *   branch +0x2c -> +0x74
 *   branch +0x7c -> +0x154
 *   branch +0x98 -> +0xb0
 *   branch +0xd8 -> +0x104
 *   branch +0x100 -> +0x124
 *   branch +0x15c -> +0x17c
 *   test +0x10 cmp r0, #0
 *   test +0x18 cmpne r0, #0
 *   test +0x28 cmp r0, #0
 *   test +0x78 cmp r0, #10
 *   test +0x94 cmp r0, #0
 *   test +0x158 cmp r0, #30
 *   0 block transfer(s), 12 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0220f6cc; the literal pool and
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

extern void native_fn_0220a2a4(void);
extern void native_fn_0220f018(void);
extern void native_fn_02025a28(void);
extern void native_fn_02025578(void);
extern void native_fn_0202537c(void);
extern void native_fn_02025ab8(void);
extern void native_fn_02024e0c(void);
extern void native_fn_02025ca4(void);
extern void native_fn_020259b4(void);
extern void native_fn_02042c0c(void);
extern void native_fn_0221089c(void);


asm u32 native_ov000_0220f6cc (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r5, r0
    ldrb r0, [r5, #0x1e2]
    mov r4, #0
    cmp r0, #0
    ldrneb r0, [r5, #0x160]
    cmpne r0, #0
    moveq r0, #30
    streqb r0, [r5, #0x279]
    ldrb r0, [r5, #0x279]
    cmp r0, #0
    bne ov000_0220f6cc_L74
    mov r1, #0
    mov r0, r5
    mov r2, r1
    bl native_fn_0220a2a4
    mov r0, #1
    strb r0, [r5, #0x2c1]
    add r0, r5, #512
    mov r1, #31
    strh r1, [r0, #122]
    mov r0, #10
    strb r0, [r5, #0x279]
    ldrb r1, [r5, #0x2c2]
    mov r0, r5
    bic r1, r1, #15
    orr r1, r1, #1
    strb r1, [r5, #0x2c2]
    bl native_fn_0220f018
ov000_0220f6cc_L74:
    ldrb r0, [r5, #0x279]
    cmp r0, #10
    bne ov000_0220f6cc_L154
    add r0, r5, #512
    ldrsh r1, [r0, #122]
    sub r1, r1, #1
    strh r1, [r0, #122]
    ldrsh r0, [r0, #122]
    cmp r0, #0
    bgt ov000_0220f6cc_Lb0
    mov r0, #0
    strb r0, [r5, #0x1e2]
    mov r0, #30
    strb r0, [r5, #0x279]
    mov r4, #1
ov000_0220f6cc_Lb0:
    add r0, r5, #512
    ldrsh r0, [r0, #122]
    rsb r6, r0, #31
    mov r0, r6
    bl native_fn_02025a28
    ldr r1, =0x41a00000
    bl native_fn_02025578
    mov r1, #0
    bl native_fn_0202537c
    mov r0, r6
    bls ov000_0220f6cc_L104
    bl native_fn_02025a28
    ldr r1, =0x41a00000
    bl native_fn_02025578
    mov r1, r0
    ldr r0, =0x45800000
    bl native_fn_02025ab8
    mov r1, r0
    mov r0, #1056964608
    bl native_fn_02024e0c
    b ov000_0220f6cc_L124
ov000_0220f6cc_L104:
    bl native_fn_02025a28
    ldr r1, =0x41a00000
    bl native_fn_02025578
    mov r1, r0
    ldr r0, =0x45800000
    bl native_fn_02025ab8
    mov r1, #1056964608
    bl native_fn_02025ca4
ov000_0220f6cc_L124:
    bl native_fn_020259b4
    ldr r2, [r5, #0x74]
    add r1, r5, #512
    add r0, r2, r0
    str r0, [r5, #0x74]
    ldrsh r1, [r1, #122]
    mov r0, r5
    and r1, r1, #255
    bl native_fn_02042c0c
    mov r0, r5
    mov r1, #0
    bl native_fn_0221089c
ov000_0220f6cc_L154:
    ldrb r0, [r5, #0x279]
    cmp r0, #30
    bne ov000_0220f6cc_L17c
    mov r0, #0
    strb r0, [r5, #0x1e2]
    strb r0, [r5, #0x2c1]
    ldrb r0, [r5, #0x2c2]
    mov r4, #1
    bic r0, r0, #15
    strb r0, [r5, #0x2c2]
ov000_0220f6cc_L17c:
    mov r0, r4
    ldmia sp!, {r4, r5, r6, pc}
}
