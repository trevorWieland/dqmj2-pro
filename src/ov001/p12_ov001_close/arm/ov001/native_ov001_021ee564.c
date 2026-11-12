/* ov001 row 0x021ee564: 552 bytes.
 *
 * What it does: 137 instructions; 10 call(s) to 0x021eec7c, 0x021e13c8, 0x021eed78, +7 more; loops (back edge at +0x78); returns through pop {r4, r5, r6, r7, r8, r9, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill (137 instructions, 10 calls, 13 branches, 5 back edges, 1 literal slot).
 *
 *   pool +0x224 -> constant 0x66666667 (image word 0x66666667)
 *   branch +0x48 -> +0x218
 *   branch +0x50 -> +0x70
 *   branch +0x6c -> +0x90
 *   branch +0x80 -> +0x90
 *   branch +0xbc -> +0x100
 *   branch +0xd4 -> +0x14c
 *   branch +0xfc -> +0x14c
 *   branch +0x150 -> +0x1fc
 *   branch +0x16c -> +0x17c
 *   branch +0x178 -> +0x184
 *   branch +0x194 -> +0x1a0
 *   branch +0x1ac -> +0x1d8
 *   branch +0x1d4 -> +0x1fc
 *   branch +0x204 -> +0x218
 *   test +0x18 cmp r9, #0
 *   test +0x4c cmp r6, #0
 *   test +0x7c cmp r0, #0
 *   test +0xb0 cmp r1, #0
 *   test +0xb8 cmplt r0, #0
 *   test +0xd0 cmp r0, #0
 *   test +0x14c cmp r4, #0
 *   test +0x164 cmp r0, #0
 *   test +0x170 cmp r5, #1
 *   test +0x17c cmp r5, #1
 *   test +0x18c cmp r6, #32
 *   test +0x198 cmp r6, #224
 *   test +0x1a8 cmp r0, #0
 *   test +0x200 cmp r0, #0
 *   1 block transfer(s), 13 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021ee564; the literal pool and
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

extern void native_fn_021eec7c(void);
extern void native_fn_021e13c8(void);
extern void native_fn_021eed78(void);
extern void native_fn_02041f74(void);
extern void native_fn_020299ac(void);
extern void native_fn_0203d294(void);
extern void native_fn_02210f64(void);
extern void native_fn_022112c4(void);
extern void native_fn_02041510(void);


asm u32 native_ov001_021ee564 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, lr}
    sub sp, sp, #28
    ldr r9, [sp, #0x38]
    mov r4, #0
    mov r8, r0
    sub r12, r4, #100
    cmp r9, #0
    movne r0, #228
    mov r7, r1
    mov r6, r2
    moveq r0, #1
    mov r1, r8
    mov r2, #1
    mov r5, r3
    str r12, [sp, #0xc]
    str r12, [sp, #0x8]
    bl native_fn_021eec7c
    movs r9, r0
    bmi ov001_021ee564_L218
    cmp r6, #0
    bge ov001_021ee564_L70
    mov r0, #0
    strb r0, [r8, #0x357]
    sub r1, r0, #1
    add r0, r8, #768
    strh r1, [r0, #64]
    strh r1, [r0, #66]
    b ov001_021ee564_L90
ov001_021ee564_L70:
    mov r0, r8
    mov r1, r6
    bl native_fn_021e13c8
    cmp r0, #0
    beq ov001_021ee564_L90
    mov r0, r9
    mov r1, #2048
    bl native_fn_021eed78
ov001_021ee564_L90:
    add r1, sp, #16
    mov r0, r8
    bl native_fn_02041f74
    ldr r1, [sp, #0x14]
    add r0, r8, #768
    add r1, r1, #8192
    str r1, [sp, #0x14]
    ldrsh r1, [r0, #64]
    cmp r1, #0
    ldrltsh r0, [r0, #66]
    cmplt r0, #0
    bge ov001_021ee564_L100
    add r0, sp, #16
    add r1, sp, #12
    add r2, sp, #8
    bl native_fn_020299ac
    cmp r0, #0
    beq ov001_021ee564_L14c
    ldr r1, [sp, #0xc]
    add r0, r8, #768
    strh r1, [r0, #64]
    ldr r1, [sp, #0x8]
    mov r4, #1
    strh r1, [r0, #66]
    ldr r0, [sp, #0xc]
    sub r0, r0, #16
    str r0, [sp, #0xc]
    b ov001_021ee564_L14c
ov001_021ee564_L100:
    mov r0, #64
    bl native_fn_0203d294
    add r1, r8, #768
    ldrsh r4, [r1, #64]
    ldr r3, =0x66666667
    mov r2, #5
    add r4, r4, #32
    sub r0, r4, r0
    str r0, [sp, #0xc]
    ldrb r6, [r8, #0x357]
    ldrsh lr, [r1, #66]
    mov r4, #1
    mov r0, r6, lsr #31
    smull r1, r12, r3, r6
    add r12, r0, r12, asr #1
    smull r0, r1, r2, r12
    sub r12, r6, r0
    sub r0, lr, r12, lsl #4
    str r0, [sp, #0x8]
ov001_021ee564_L14c:
    cmp r4, #0
    beq ov001_021ee564_L1fc
    ldrb r1, [r8, #0x357]
    ldrb r0, [r8, #0x31e]
    mov r1, r1, lsl #1
    rsb r1, r1, #24
    cmp r0, #0
    and r3, r1, #255
    bne ov001_021ee564_L17c
    cmp r5, #1
    moveq r1, #86
    b ov001_021ee564_L184
ov001_021ee564_L17c:
    cmp r5, #1
    moveq r1, #85
ov001_021ee564_L184:
    ldr r6, [sp, #0xc]
    movne r1, #98
    cmp r6, #32
    movlt r6, #32
    blt ov001_021ee564_L1a0
    cmp r6, #224
    movgt r6, #224
ov001_021ee564_L1a0:
    ldr r0, [sp, #0x3c]
    str r6, [sp, #0xc]
    cmp r0, #0
    beq ov001_021ee564_L1d8
    stmia sp, {r1, r5}
    ldr r2, [sp, #0x8]
    mov r0, r7, lsl #16
    mov r1, r6, lsl #16
    mov r2, r2, lsl #16
    mov r0, r0, asr #16
    mov r1, r1, asr #16
    mov r2, r2, asr #16
    bl native_fn_02210f64
    b ov001_021ee564_L1fc
ov001_021ee564_L1d8:
    str r5, [sp]
    ldr r2, [sp, #0x8]
    mov r0, r7, lsl #16
    mov r1, r6, lsl #16
    mov r2, r2, lsl #16
    mov r0, r0, asr #16
    mov r1, r1, asr #16
    mov r2, r2, asr #16
    bl native_fn_022112c4
ov001_021ee564_L1fc:
    ldr r0, [sp, #0x38]
    cmp r0, #0
    beq ov001_021ee564_L218
    mov r0, #0
    mov r1, #3
    mov r2, #20
    bl native_fn_02041510
ov001_021ee564_L218:
    mov r0, r4
    add sp, sp, #28
    ldmia sp!, {r4, r5, r6, r7, r8, r9, pc}
}
