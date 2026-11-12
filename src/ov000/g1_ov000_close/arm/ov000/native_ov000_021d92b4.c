/* ov000 row 0x021d92b4: 716 bytes.
 *
 * What it does: 167 instructions; 18 call(s) to 0x0205bf9c, 0x02008d78, 0x02008d78, +15 more; loops (back edge at +0x0c); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 12 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x29c -> constant 0x0223142c (image word 0x0223142c)
 *   pool +0x2a0 -> constant 0x02231be0 (image word 0x02231be0)
 *   pool +0x2a4 -> constant 0x02231bd4 (image word 0x02231bd4)
 *   pool +0x2a8 -> constant 0x02230488 (image word 0x02230488)
 *   pool +0x2ac -> native_data_0222e1d0 (image word 0x0222e1d0)
 *   pool +0x2b0 -> native_data_0222e1e4 (image word 0x0222e1e4)
 *   pool +0x2b4 -> native_data_0222e1f8 (image word 0x0222e1f8)
 *   pool +0x2b8 -> constant 0x022303e8 (image word 0x022303e8)
 *   pool +0x2bc -> native_data_0222e204 (image word 0x0222e204)
 *   pool +0x2c0 -> constant 0x005dc000 (image word 0x005dc000)
 *   pool +0x2c4 -> native_fn_021d915c (image word 0x021d915c)
 *   pool +0x2c8 -> constant 0x0223042c (image word 0x0223042c)
 *   branch +0x74 -> +0x264
 *   branch +0x90 -> +0xb8
 *   branch +0xb4 -> +0xd8
 *   branch +0x104 -> +0x258
 *   branch +0x110 -> +0x138
 *   branch +0x14c -> +0x264
 *   branch +0x168 -> +0x1a0
 *   branch +0x178 -> +0x1a0
 *   branch +0x188 -> +0x1a0
 *   branch +0x1c4 -> +0x224
 *   branch +0x1f0 -> +0x210
 *   branch +0x200 -> +0x210
 *   branch +0x254 -> +0x264
 *   back edge +0x260 -> +0x8c
 *   back edge +0x26c -> +0x68
 *   branch +0x278 -> +0x290
 *   test +0x14 cmp r4, #255
 *   test +0x70 cmp r0, #0
 *   test +0x8c cmp r8, #0
 *   test +0x100 cmp r0, #0
 *   test +0x10c cmp r0, #1
 *   test +0x148 cmp r0, #0
 *   test +0x158 cmp r0, #115
 *   test +0x16c cmp r0, #116
 *   test +0x17c cmp r0, #117
 *   test +0x18c cmp r0, #118
 *   test +0x1a4 cmp r0, #1
 *   test +0x1c0 cmp r0, #1
 *   test +0x1e4 cmp r0, #115
 *   test +0x1f4 cmp r0, #116
 *   test +0x204 cmp r0, #117
 *   test +0x25c cmp r8, #2
 *   test +0x268 cmp r7, #26
 *   test +0x274 cmp r0, #0
 *   2 block transfer(s), 21 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021d92b4; the literal pool and
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

extern void native_fn_0205bf9c(void);
extern void native_fn_02008d78(void);
extern void native_fn_021df220(void);
extern void native_fn_021d9128(void);
extern u8 native_data_0222e1d0[];
extern void native_fn_0201d444(void);
extern u8 native_data_0222e1e4[];
extern u8 native_data_0222e1f8[];
extern void native_fn_02040fd8(void);
extern u8 native_data_0222e204[];
extern void native_fn_02041024(void);
extern void native_fn_0204106c(void);
extern void native_fn_021d915c(void);
extern void native_fn_02029284(void);
extern void native_fn_021d91cc(void);
extern void native_fn_021d9240(void);


asm u32 native_ov000_021d92b4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #56
    mov r4, r0
    bl native_fn_0205bf9c
    mov r10, r0
    cmp r4, #255
    ldreq r0, =0x0223142c
    mov r1, #0
    ldreqb r4, [r0, #0x7c0]
    ldrne r0, =0x0223142c
    mov r2, #12
    strneb r4, [r0, #0x7c0]
    ldr r0, =0x02231be0
    bl native_fn_02008d78
    ldr r0, =0x02231bd4
    mov r1, #0
    mov r2, #12
    bl native_fn_02008d78
    add r1, sp, #22
    add r2, sp, #21
    add r3, sp, #20
    mov r0, r4
    bl native_fn_021df220
    mov r7, #0
    ldr r9, =0x02230488
    str r7, [sp, #0x10]
ov000_021d92b4_L68:
    mov r0, r7
    bl native_fn_021d9128
    cmp r0, #0
    beq ov000_021d92b4_L264
    mov r8, #0
    add r6, r7, #97
    mov r11, r8
    add r5, sp, #23
    add r4, sp, #39
ov000_021d92b4_L8c:
    cmp r8, #0
    bne ov000_021d92b4_Lb8
    ldrb r2, [sp, #0x14]
    ldr r1, =native_data_0222e1d0
    mov r0, r5
    stmia sp, {r2, r10}
    str r6, [sp, #0x8]
    ldrsb r2, [sp, #22]
    ldrb r3, [sp, #0x15]
    bl native_fn_0201d444
    b ov000_021d92b4_Ld8
ov000_021d92b4_Lb8:
    ldrb r2, [sp, #0x14]
    ldr r1, =native_data_0222e1e4
    mov r0, r5
    stmia sp, {r2, r11}
    str r6, [sp, #0x8]
    ldrsb r2, [sp, #22]
    ldrb r3, [sp, #0x15]
    bl native_fn_0201d444
ov000_021d92b4_Ld8:
    ldr r1, =native_data_0222e1f8
    mov r0, r4
    mov r2, r5
    bl native_fn_0201d444
    ldr r0, =0x022303e8
    mov r1, r9
    ldr r0, [r0]
    mov r2, r4
    mov r3, #1
    bl native_fn_02040fd8
    cmp r0, #0
    beq ov000_021d92b4_L258
    ldrb r0, [r9, #0x4]
    cmp r0, #1
    beq ov000_021d92b4_L138
    ldr r1, =native_data_0222e204
    add r0, sp, #39
    add r2, sp, #23
    bl native_fn_0201d444
    ldr r0, =0x022303e8
    add r2, sp, #39
    ldr r0, [r0]
    mov r1, r9
    bl native_fn_02041024
ov000_021d92b4_L138:
    mov r1, r9
    add r0, r9, #100
    mov r2, #0
    bl native_fn_0204106c
    cmp r0, #0
    beq ov000_021d92b4_L264
    add r1, r7, #97
    and r0, r1, #255
    cmp r0, #115
    strb r1, [r9, #0x171]
    moveq r0, #1
    streqb r0, [r9, #0x170]
    beq ov000_021d92b4_L1a0
    cmp r0, #116
    moveq r0, #1
    streqb r0, [r9, #0x170]
    beq ov000_021d92b4_L1a0
    cmp r0, #117
    moveq r0, #1
    streqb r0, [r9, #0x170]
    beq ov000_021d92b4_L1a0
    cmp r0, #118
    moveq r0, #2
    streqb r0, [r9, #0x170]
    movne r0, #0
    strneb r0, [r9, #0x170]
ov000_021d92b4_L1a0:
    ldrb r0, [r9, #0x170]
    cmp r0, #1
    moveq r1, #0
    movne r1, #31
    ldr r0, =0x005dc000
    strb r1, [r9, #0x172]
    str r0, [r9, #0x16c]
    ldrb r0, [r9, #0x170]
    cmp r0, #1
    bne ov000_021d92b4_L224
    ldr r3, =native_fn_021d915c
    str r9, [sp]
    add r0, r9, #100
    mov r1, #4
    mov r2, #2
    bl native_fn_02029284
    ldrb r0, [r9, #0x171]
    cmp r0, #115
    moveq r0, #0
    streq r0, [sp, #0xc]
    beq ov000_021d92b4_L210
    cmp r0, #116
    moveq r0, #1
    streq r0, [sp, #0xc]
    beq ov000_021d92b4_L210
    cmp r0, #117
    moveq r0, #2
    streq r0, [sp, #0xc]
ov000_021d92b4_L210:
    ldr r1, =0x0223042c
    ldr r0, [sp, #0xc]
    add r0, r1, r0, lsl #2
    add r0, r0, #4096
    str r9, [r0, #0x7b4]
ov000_021d92b4_L224:
    add r0, sp, #23
    mov r1, r9
    bl native_fn_021d91cc
    add r0, sp, #23
    mov r1, r9
    bl native_fn_021d9240
    add r0, r7, #100
    strb r0, [r9, #0x6f]
    ldr r0, [sp, #0x10]
    add r9, r9, #372
    add r0, r0, #1
    str r0, [sp, #0x10]
    b ov000_021d92b4_L264
ov000_021d92b4_L258:
    add r8, r8, #1
    cmp r8, #2
    blt ov000_021d92b4_L8c
ov000_021d92b4_L264:
    add r7, r7, #1
    cmp r7, #26
    blt ov000_021d92b4_L68
    ldr r0, [sp, #0x10]
    cmp r0, #0
    ble ov000_021d92b4_L290
    ldr r2, =0x0223042c
    ldr r1, =0x0223142c
    str r0, [r2, #0x58]
    mov r0, #1
    strb r0, [r1, #0x7c1]
ov000_021d92b4_L290:
    ldr r0, [sp, #0x10]
    add sp, sp, #56
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
