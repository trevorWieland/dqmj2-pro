/* ov001 row 0x0220e134: 428 bytes.
 *
 * What it does: 106 instructions; 15 call(s) to 0x0220d6f0, 0x021ee9fc, 0x0207afec, +12 more; loops (back edge at +0x1c); returns through pop {r3, r4, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 15 calls (106 instructions, 15 calls, 9 branches, 14 back edges, 1 literal slot).
 *
 *   pool +0x1a8 -> constant 0x0223e0d8 (image word 0x0223e0d8)
 *   branch +0x18 -> +0x78
 *   branch +0x74 -> +0x19c
 *   branch +0x7c -> +0xa0
 *   branch +0x9c -> +0x19c
 *   branch +0xa4 -> +0x140
 *   branch +0x13c -> +0x19c
 *   branch +0x144 -> +0x168
 *   branch +0x164 -> +0x19c
 *   branch +0x16c -> +0x19c
 *   test +0x14 cmp r1, #0
 *   test +0x78 cmp r1, #10
 *   test +0x8c cmp r1, #30
 *   test +0xa0 cmp r1, #20
 *   test +0xd8 cmp r0, #0
 *   test +0x140 cmp r1, #30
 *   test +0x154 cmp r1, #30
 *   test +0x168 cmp r1, #100
 *   0 block transfer(s), 11 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0220e134; the literal pool and
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

extern void native_fn_0220d6f0(void);
extern void native_fn_021ee9fc(void);
extern void native_fn_0207afec(void);
extern void native_fn_0220d7e0(void);
extern void native_fn_021f1354(void);
extern void native_fn_021f1438(void);
extern void native_fn_021dbcf0(void);
extern void native_fn_0220f960(void);
extern void native_fn_021dcda8(void);
extern void native_fn_021db834(void);
extern void native_fn_021ee78c(void);
extern void native_fn_022024d4(void);
extern void native_fn_021f14a4(void);
extern void native_fn_0220d820(void);


asm u32 native_ov001_0220e134 (register u32 a0)
{
    stmdb sp!, {r3, r4, lr}
    sub sp, sp, #4
    ldr r0, =0x0223e0d8
    mov r4, #0
    ldrb r1, [r0, #0x5]
    cmp r1, #0
    bne ov001_0220e134_L78
    bl native_fn_0220d6f0
    ldr r0, =0x0223e0d8
    ldr r0, [r0, #0xc]
    bl native_fn_021ee9fc
    mov r0, #78
    bl native_fn_0207afec
    ldr r2, =0x0223e0d8
    ldrsh r1, [r0, #12]
    ldr r0, [r2, #0xc]
    bl native_fn_0220d7e0
    mov r0, #11
    mov r1, r4
    mov r2, #58
    mov r3, #1
    bl native_fn_021f1354
    mov r0, #2
    bl native_fn_021f1438
    ldr r0, =0x0223e0d8
    mov r2, #10
    mov r1, r4
    strb r2, [r0, #0x5]
    strb r1, [r0, #0x4]
    b ov001_0220e134_L19c
ov001_0220e134_L78:
    cmp r1, #10
    bne ov001_0220e134_La0
    ldrb r1, [r0, #0x4]
    add r2, r1, #1
    and r1, r2, #255
    cmp r1, #30
    strb r2, [r0, #0x4]
    movhi r1, #20
    strhib r1, [r0, #0x5]
    b ov001_0220e134_L19c
ov001_0220e134_La0:
    cmp r1, #20
    bne ov001_0220e134_L140
    ldr r0, [r0, #0xc]
    bl native_fn_021dbcf0
    ldr r2, =0x0223e0d8
    mov r1, r0
    ldr r0, [r2, #0xc]
    ldr r0, [r0, #0x1e8]
    add r0, r0, #70
    bl native_fn_0220f960
    ldr r1, =0x0223e0d8
    add r4, r4, r0
    ldr r0, [r1, #0xc]
    bl native_fn_021dcda8
    cmp r0, #0
    ldr r0, =0x0223e0d8
    movne r4, #0
    ldr r0, [r0, #0xc]
    mov r1, r4
    bl native_fn_021db834
    mov r2, #0
    str r2, [sp]
    ldr r0, =0x0223e0d8
    mov r1, r4
    ldr r0, [r0, #0xc]
    sub r2, r2, #1
    mov r3, #2
    bl native_fn_021ee78c
    ldr r0, =0x0223e0d8
    mov r2, r4
    ldr r1, [r0, #0xc]
    ldrb r0, [r1, #0x31e]
    ldrb r1, [r1, #0x31f]
    bl native_fn_022024d4
    ldr r0, =0x0223e0d8
    mov r1, #0
    strb r1, [r0, #0x4]
    mov r1, #30
    strb r1, [r0, #0x5]
    b ov001_0220e134_L19c
ov001_0220e134_L140:
    cmp r1, #30
    bne ov001_0220e134_L168
    ldrb r1, [r0, #0x4]
    add r2, r1, #1
    and r1, r2, #255
    cmp r1, #30
    strb r2, [r0, #0x4]
    movhi r1, #100
    strhib r1, [r0, #0x5]
    b ov001_0220e134_L19c
ov001_0220e134_L168:
    cmp r1, #100
    bne ov001_0220e134_L19c
    bl native_fn_021f14a4
    ldr r0, =0x0223e0d8
    mov r1, r4
    strb r1, [r0, #0x5]
    mov r0, #78
    bl native_fn_0207afec
    ldrsh r0, [r0, #12]
    bl native_fn_0220d820
    ldr r0, =0x0223e0d8
    mov r1, #3
    strb r1, [r0, #0x2]
ov001_0220e134_L19c:
    mov r0, #0
    add sp, sp, #4
    ldmia sp!, {r3, r4, pc}
}
