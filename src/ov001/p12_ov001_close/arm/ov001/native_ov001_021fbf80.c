/* ov001 row 0x021fbf80: 356 bytes.
 *
 * What it does: 88 instructions; 19 call(s) to 0x02041538, 0x020414b0, 0x02041510, +16 more; loops (back edge at +0x6c); returns through pop {r4, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 19 calls (88 instructions, 19 calls, 21 branches, 17 back edges, 1 literal slot).
 *
 *   pool +0x160 -> constant 0x02239a14 (image word 0x02239a14)
 *   branch +0x18 -> +0x3c
 *   branch +0x1c -> +0xc0
 *   branch +0x24 -> +0x30
 *   branch +0x28 -> +0x60
 *   branch +0x2c -> +0x158
 *   branch +0x34 -> +0xa0
 *   branch +0x38 -> +0x158
 *   branch +0x40 -> +0x54
 *   branch +0x44 -> +0x11c
 *   branch +0x4c -> +0xf8
 *   branch +0x50 -> +0x158
 *   branch +0x58 -> +0x140
 *   branch +0x5c -> +0x158
 *   branch +0x9c -> +0x158
 *   branch +0xa8 -> +0x158
 *   branch +0xbc -> +0x158
 *   branch +0xf4 -> +0x158
 *   branch +0x104 -> +0x158
 *   branch +0x118 -> +0x158
 *   branch +0x124 -> +0x158
 *   branch +0x13c -> +0x158
 *   test +0x14 cmp r2, #15
 *   test +0x20 cmp r2, #0
 *   test +0x30 cmp r2, #10
 *   test +0x3c cmp r2, #25
 *   test +0x48 cmp r2, #20
 *   test +0x54 cmp r2, #30
 *   test +0xa4 cmp r0, #1
 *   test +0x100 cmp r0, #0
 *   test +0x120 cmp r0, #1
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021fbf80; the literal pool and
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

extern void native_fn_02041538(void);
extern void native_fn_020414b0(void);
extern void native_fn_02041510(void);
extern void native_fn_02041560(void);
extern void native_fn_02041814(void);
extern void native_fn_0220266c(void);
extern void native_fn_021fbec4(void);
extern void native_fn_020406a8(void);
extern void native_fn_020612ec(void);
extern void native_fn_020406c8(void);
extern void native_fn_0206157c(void);
extern void native_fn_0220a5a0(void);
extern void native_fn_02062328(void);
extern void native_fn_02041800(void);
extern void native_fn_0206dec8(void);
extern void native_fn_02061898(void);
extern void native_fn_021fbf28(void);


asm u32 native_ov001_021fbf80 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    ldr r1, =0x02239a14
    mov r0, #0
    ldr r2, [r1, #0x38]
    mov r4, r0
    cmp r2, #15
    bgt ov001_021fbf80_L3c
    bge ov001_021fbf80_Lc0
    cmp r2, #0
    bgt ov001_021fbf80_L30
    beq ov001_021fbf80_L60
    b ov001_021fbf80_L158
ov001_021fbf80_L30:
    cmp r2, #10
    beq ov001_021fbf80_La0
    b ov001_021fbf80_L158
ov001_021fbf80_L3c:
    cmp r2, #25
    bgt ov001_021fbf80_L54
    bge ov001_021fbf80_L11c
    cmp r2, #20
    beq ov001_021fbf80_Lf8
    b ov001_021fbf80_L158
ov001_021fbf80_L54:
    cmp r2, #30
    beq ov001_021fbf80_L140
    b ov001_021fbf80_L158
ov001_021fbf80_L60:
    mov r0, #1
    mov r1, #2
    mov r2, #15
    bl native_fn_02041538
    mov r0, #1
    bl native_fn_020414b0
    mov r0, #1
    mov r1, #2
    mov r2, #5
    bl native_fn_02041510
    mov r0, #10
    bl native_fn_02041560
    ldr r0, =0x02239a14
    mov r1, #10
    str r1, [r0, #0x38]
    b ov001_021fbf80_L158
ov001_021fbf80_La0:
    bl native_fn_02041814
    cmp r0, #1
    beq ov001_021fbf80_L158
    bl native_fn_0220266c
    ldr r0, =0x02239a14
    mov r1, #15
    str r1, [r0, #0x38]
    b ov001_021fbf80_L158
ov001_021fbf80_Lc0:
    bl native_fn_021fbec4
    mov r0, #1
    bl native_fn_020406a8
    mov r1, r4
    mov r3, r1
    mov r0, #1
    mov r2, #24576
    bl native_fn_020612ec
    mov r0, r4
    bl native_fn_020406c8
    ldr r0, =0x02239a14
    mov r1, #20
    str r1, [r0, #0x38]
    b ov001_021fbf80_L158
ov001_021fbf80_Lf8:
    bl native_fn_0206157c
    bl native_fn_0220a5a0
    cmp r0, #0
    beq ov001_021fbf80_L158
    ldr r0, =0x02239a14
    mov r1, #25
    str r1, [r0, #0x38]
    bl native_fn_02062328
    b ov001_021fbf80_L158
ov001_021fbf80_L11c:
    bl native_fn_02041800
    cmp r0, #1
    beq ov001_021fbf80_L158
    mov r0, #63
    bl native_fn_020414b0
    ldr r0, =0x02239a14
    mov r1, #30
    str r1, [r0, #0x38]
    b ov001_021fbf80_L158
ov001_021fbf80_L140:
    str r0, [r1, #0x38]
    mov r4, #1
    bl native_fn_020406a8
    bl native_fn_0206dec8
    bl native_fn_02061898
    bl native_fn_021fbf28
ov001_021fbf80_L158:
    mov r0, r4
    ldmia sp!, {r4, pc}
}
