/* ov000 row 0x021fc458: 740 bytes.
 *
 * What it does: 184 instructions; 29 call(s) to 0x02215698, 0x02062aa0, 0x02062a50, +26 more; loops (back edge at +0x54); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x2e0 -> constant 0x022372a8 (image word 0x022372a8)
 *   branch +0x30 -> +0x40
 *   branch +0x38 -> +0xc4
 *   branch +0x3c -> +0x238
 *   branch +0x50 -> +0xb4
 *   branch +0x5c -> +0x70
 *   branch +0x6c -> +0x84
 *   branch +0xb0 -> +0x238
 *   branch +0xc0 -> +0x238
 *   branch +0xd0 -> +0x154
 *   branch +0xdc -> +0x13c
 *   branch +0xfc -> +0x13c
 *   branch +0x118 -> +0x13c
 *   branch +0x138 -> +0x144
 *   branch +0x150 -> +0x224
 *   branch +0x160 -> +0x174
 *   branch +0x170 -> +0x224
 *   branch +0x188 -> +0x1a0
 *   branch +0x19c -> +0x204
 *   branch +0x1a4 -> +0x1dc
 *   branch +0x1c8 -> +0x1dc
 *   branch +0x1d8 -> +0x1e8
 *   branch +0x1e4 -> +0x204
 *   branch +0x228 -> +0x238
 *   branch +0x23c -> +0x2d4
 *   test +0x28 cmp r0, #2
 *   test +0x34 cmp r0, #4
 *   test +0x4c cmp r6, r0
 *   test +0x58 cmp r6, r0
 *   test +0xcc cmp r2, #0
 *   test +0xd8 cmp r0, #0
 *   test +0xf8 cmp r0, #0
 *   test +0x114 cmp r0, r2
 *   test +0x15c cmp r2, r0
 *   test +0x184 cmp r6, r0
 *   test +0x1a0 cmp r6, #0
 *   test +0x1c4 cmp r0, #0
 *   test +0x1d4 cmp r0, #0
 *   test +0x224 cmp r8, #0
 *   test +0x238 cmp r8, #0
 *   0 block transfer(s), 12 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021fc458; the literal pool and
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

extern void ov000_display_context_02215698(void);
extern void native_fn_02062aa0(void);
extern void native_fn_02062a50(void);
extern void native_fn_02062a88(void);
extern void native_fn_0204b61c(void);
extern void native_fn_021e7b9c(void);
extern void native_fn_021fc73c(void);
extern void native_fn_0221570c(void);
extern void native_fn_02065d88(void);
extern void native_fn_02211064(void);
extern void native_fn_02062d04(void);
extern void native_fn_021fdad8(void);
extern void native_fn_020c4c9c(void);
extern void native_fn_020c4c58(void);
extern void native_fn_021fcd4c(void);
extern void native_fn_02217bdc(void);
extern void native_fn_02060a20(void);
extern void native_fn_02047d40(void);
extern void native_fn_02217cf0(void);


asm u32 native_ov000_021fc458 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    sub sp, sp, #8
    bl ov000_display_context_02215698
    ldr r1, =0x022372a8
    mov r8, #0
    ldr r4, [r1, #0xc]
    mov r5, r0
    ldr r0, [r4]
    mov r6, r8
    mov r9, r8
    cmp r0, #2
    sub r7, r8, #1
    beq ov000_021fc458_L40
    cmp r0, #4
    beq ov000_021fc458_Lc4
    b ov000_021fc458_L238
ov000_021fc458_L40:
    ldrh r0, [r4, #24]
    ldr r6, [r4, #0xc]
    sub r0, r0, #1
    cmp r6, r0
    beq ov000_021fc458_Lb4
    bl native_fn_02062aa0
    cmp r6, r0
    bge ov000_021fc458_L70
    mov r0, r6
    bl native_fn_02062a50
    ldr r1, =0x022372a8
    b ov000_021fc458_L84
ov000_021fc458_L70:
    bl native_fn_02062aa0
    ldr r1, [r4, #0xc]
    sub r0, r1, r0
    bl native_fn_02062a88
    ldr r1, =0x022372a8
ov000_021fc458_L84:
    ldr r1, [r1, #0xc]
    str r0, [r1, #0x5f4]
    add r0, r5, #16
    mov r1, #0
    bl native_fn_0204b61c
    ldr r0, =0x022372a8
    mov r2, #3
    ldr r1, [r0, #0xc]
    mov r0, #82
    str r2, [r1, #0x4]
    bl native_fn_021e7b9c
    b ov000_021fc458_L238
ov000_021fc458_Lb4:
    bl native_fn_021fc73c
    mov r0, #1
    bl native_fn_0221570c
    b ov000_021fc458_L238
ov000_021fc458_Lc4:
    ldr r2, [r4, #0xfc]
    add r0, r4, #252
    cmp r2, #0
    bne ov000_021fc458_L154
    ldr r0, [r4, #0x5f8]
    cmp r0, #0
    beq ov000_021fc458_L13c
    bl native_fn_02065d88
    ldr r1, =0x022372a8
    ldr r2, [r1, #0xc]
    ldrb r1, [r0, #0x2d]
    ldr r0, [r2, #0x5f4]
    bl native_fn_02211064
    cmp r0, #0
    beq ov000_021fc458_L13c
    ldr r0, =0x022372a8
    ldr r0, [r0, #0xc]
    ldr r1, [r0, #0x5f4]
    ldr r2, [r0, #0x5f8]
    ldrb r0, [r1, #0x31]
    cmp r0, r2
    beq ov000_021fc458_L13c
    mov r0, #93
    strb r2, [r1, #0x31]
    bl native_fn_021e7b9c
    ldr r0, =0x022372a8
    mov r8, #1
    ldr r0, [r0, #0xc]
    ldr r6, [r0, #0x5f8]
    b ov000_021fc458_L144
ov000_021fc458_L13c:
    mov r0, #84
    bl native_fn_021e7b9c
ov000_021fc458_L144:
    ldr r0, =0x022372a8
    ldr r0, [r0, #0xc]
    ldr r7, [r0, #0xc]
    b ov000_021fc458_L224
ov000_021fc458_L154:
    ldrh r0, [r0, #14]
    sub r0, r0, #1
    cmp r2, r0
    bne ov000_021fc458_L174
    bl native_fn_021fc73c
    mov r0, #82
    bl native_fn_021e7b9c
    b ov000_021fc458_L224
ov000_021fc458_L174:
    ldr r1, [r4, #0x5f4]
    add r2, r4, r2, lsl #2
    ldrb r0, [r1, #0x31]
    ldr r6, [r2, #0x1ec]
    cmp r6, r0
    bne ov000_021fc458_L1a0
    mov r0, #93
    strb r8, [r1, #0x31]
    bl native_fn_021e7b9c
    mov r9, #1
    b ov000_021fc458_L204
ov000_021fc458_L1a0:
    cmp r6, #0
    beq ov000_021fc458_L1dc
    mov r0, r6
    bl native_fn_02065d88
    ldr r1, =0x022372a8
    ldr r2, [r1, #0xc]
    ldrb r1, [r0, #0x2d]
    ldr r0, [r2, #0x5f4]
    bl native_fn_02211064
    cmp r0, #0
    beq ov000_021fc458_L1dc
    mov r0, r6
    bl native_fn_02062d04
    cmp r0, #0
    bgt ov000_021fc458_L1e8
ov000_021fc458_L1dc:
    mov r0, #84
    bl native_fn_021e7b9c
    b ov000_021fc458_L204
ov000_021fc458_L1e8:
    ldr r1, =0x022372a8
    mov r0, #93
    ldr r1, [r1, #0xc]
    ldr r1, [r1, #0x5f4]
    strb r6, [r1, #0x31]
    bl native_fn_021e7b9c
    mov r8, #1
ov000_021fc458_L204:
    ldr r0, =0x022372a8
    ldr r0, [r0, #0xc]
    ldr r0, [r0, #0x5f4]
    bl native_fn_021fdad8
    ldr r1, =0x022372a8
    ldr r1, [r1, #0xc]
    str r0, [r1, #0x5f8]
    bl native_fn_020c4c9c
ov000_021fc458_L224:
    cmp r8, #0
    beq ov000_021fc458_L238
    mov r0, r6
    mov r1, r7
    bl native_fn_020c4c58
ov000_021fc458_L238:
    cmp r8, #0
    beq ov000_021fc458_L2d4
    ldr r0, =0x022372a8
    mov r1, #1
    strb r1, [r0]
    ldr r0, [r0, #0xc]
    ldr r0, [r0]
    bl native_fn_021fcd4c
    mov r3, #1
    str r3, [sp]
    sub r4, r3, #2
    mov r0, #5
    mov r1, #6
    mov r2, #0
    str r4, [sp, #0x4]
    bl native_fn_02217bdc
    ldr r0, =0x022372a8
    mov r1, #32
    ldr r0, [r0, #0xc]
    ldr r0, [r0, #0x5f4]
    ldrb r0, [r0, #0x31]
    bl native_fn_02060a20
    ldr r0, =0x022372a8
    ldr r0, [r0, #0xc]
    ldr r0, [r0, #0x5f4]
    ldrb r0, [r0, #0x31]
    bl native_fn_02047d40
    add r0, r5, #16
    bl native_fn_02217cf0
    ldr r0, =0x022372a8
    mov r2, #4
    ldr r1, [r0, #0xc]
    mov r3, #5
    str r2, [r1, #0x8]
    ldr r2, [r0, #0xc]
    mov r1, #1
    str r3, [r2]
    ldr r0, [r0, #0xc]
    str r1, [r0, #0x5fc]
ov000_021fc458_L2d4:
    mov r0, r9
    add sp, sp, #8
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
