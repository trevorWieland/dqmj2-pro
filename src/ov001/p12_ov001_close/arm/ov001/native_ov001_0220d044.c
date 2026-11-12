/* ov001 row 0x0220d044: 428 bytes.
 *
 * What it does: 104 instructions; 17 call(s) to 0x0220b794, 0x021db438, 0x0220b770, +14 more; loops (back edge at +0x04); returns through pop {r4, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: loop with 17 calls (104 instructions, 17 calls, 16 branches, 17 back edges, 3 literal slots).
 *
 *   pool +0x1a0 -> constant 0x0223e088 (image word 0x0223e088)
 *   pool +0x1a4 -> constant 0x0223e0a8 (image word 0x0223e0a8)
 *   pool +0x1a8 -> constant 0x000001b7 (image word 0x000001b7)
 *   branch +0x28 -> +0x6c
 *   branch +0x38 -> +0x5c
 *   branch +0x44 -> +0x5c
 *   branch +0x58 -> +0x198
 *   branch +0x68 -> +0x198
 *   branch +0x70 -> +0xbc
 *   branch +0xb8 -> +0x198
 *   branch +0xc0 -> +0x110
 *   branch +0xd0 -> +0x198
 *   branch +0x10c -> +0x198
 *   branch +0x114 -> +0x150
 *   branch +0x120 -> +0x198
 *   branch +0x14c -> +0x198
 *   branch +0x154 -> +0x178
 *   branch +0x174 -> +0x198
 *   branch +0x17c -> +0x198
 *   test +0x24 cmp r1, #0
 *   test +0x34 cmp r0, #0
 *   test +0x40 cmp r0, #0
 *   test +0x6c cmp r1, #10
 *   test +0xbc cmp r1, #20
 *   test +0xcc cmp r0, #0
 *   test +0x110 cmp r1, #50
 *   test +0x11c cmp r0, #0
 *   test +0x150 cmp r1, #60
 *   test +0x164 cmp r1, #30
 *   test +0x178 cmp r1, #100
 *   0 block transfer(s), 13 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0220d044; the literal pool and
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

extern void native_fn_0220b794(void);
extern void native_fn_021db438(void);
extern void native_fn_0220b770(void);
extern void native_fn_02044424(void);
extern void native_fn_021fc15c(void);
extern void native_fn_021fc13c(void);
extern void native_fn_0202ac08(void);
extern void native_fn_021eea10(void);
extern void native_fn_0205d790(void);
extern void native_fn_021eec7c(void);
extern void native_fn_0205d6f4(void);
extern void native_fn_021eeb70(void);
extern void native_fn_0202ac4c(void);
extern void native_fn_021f1354(void);
extern void native_fn_021f14e4(void);
extern void native_fn_021f14a4(void);


asm u32 native_ov001_0220d044 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    bl native_fn_0220b794
    mov r1, r0
    mov r0, #1
    bl native_fn_021db438
    mov r4, r0
    bl native_fn_0220b770
    ldr r0, =0x0223e088
    ldrb r1, [r0, #0x4]
    cmp r1, #0
    bne ov001_0220d044_L6c
    mov r0, #-2147483648
    bl native_fn_02044424
    cmp r0, #0
    beq ov001_0220d044_L5c
    bl native_fn_021fc15c
    cmp r0, #0
    bne ov001_0220d044_L5c
    bl native_fn_021fc13c
    ldr r0, =0x0223e088
    mov r1, #10
    strb r1, [r0, #0x4]
    b ov001_0220d044_L198
ov001_0220d044_L5c:
    ldr r0, =0x0223e088
    mov r1, #50
    strb r1, [r0, #0x4]
    b ov001_0220d044_L198
ov001_0220d044_L6c:
    cmp r1, #10
    bne ov001_0220d044_Lbc
    ldr r0, =0x0223e0a8
    bl native_fn_0202ac08
    ldr r0, =0x000001b7
    mov r1, #0
    bl native_fn_021eea10
    ldr r0, =0x000001b7
    bl native_fn_0205d790
    mov r2, r0
    ldr r0, =0x000001b7
    mov r1, r4
    bl native_fn_021eec7c
    ldr r1, =0x0223e088
    mov r2, #20
    strb r0, [r1, #0x2]
    strb r2, [r1, #0x4]
    mov r0, #0
    strb r0, [r1, #0x8]
    b ov001_0220d044_L198
ov001_0220d044_Lbc:
    cmp r1, #20
    bne ov001_0220d044_L110
    ldrsb r0, [r0, #2]
    bl native_fn_0205d6f4
    cmp r0, #0
    bne ov001_0220d044_L198
    ldr r0, =0x000001b7
    bl native_fn_021eeb70
    ldr r0, =0x0223e0a8
    bl native_fn_0202ac4c
    mov r0, #1
    mov r3, r0
    mov r1, #0
    mov r2, #8
    bl native_fn_021f1354
    ldr r0, =0x0223e088
    mov r1, #60
    strb r1, [r0, #0x4]
    mov r1, #0
    strb r1, [r0, #0x8]
    b ov001_0220d044_L198
ov001_0220d044_L110:
    cmp r1, #50
    bne ov001_0220d044_L150
    bl native_fn_021f14e4
    cmp r0, #0
    bne ov001_0220d044_L198
    mov r0, #1
    mov r3, r0
    mov r1, #0
    mov r2, #43
    bl native_fn_021f1354
    ldr r0, =0x0223e088
    mov r1, #60
    strb r1, [r0, #0x4]
    mov r1, #0
    strb r1, [r0, #0x8]
    b ov001_0220d044_L198
ov001_0220d044_L150:
    cmp r1, #60
    bne ov001_0220d044_L178
    ldrb r1, [r0, #0x8]
    add r2, r1, #1
    and r1, r2, #255
    cmp r1, #30
    strb r2, [r0, #0x8]
    movhs r1, #100
    strhsb r1, [r0, #0x4]
    b ov001_0220d044_L198
ov001_0220d044_L178:
    cmp r1, #100
    bne ov001_0220d044_L198
    bl native_fn_021f14a4
    ldr r0, =0x0223e088
    mov r1, #14
    strb r1, [r0, #0x3]
    mov r1, #0
    strb r1, [r0, #0x4]
ov001_0220d044_L198:
    mov r0, #0
    ldmia sp!, {r4, pc}
}
