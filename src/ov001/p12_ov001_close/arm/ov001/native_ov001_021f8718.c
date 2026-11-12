/* ov001 row 0x021f8718: 532 bytes.
 *
 * What it does: 131 instructions; 19 call(s) to 0x021db8d0, 0x021f82d8, 0x0202ac08, +16 more; loops (back edge at +0x18); returns through pop {r3, r4, r5, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 19 calls (131 instructions, 19 calls, 12 branches, 17 back edges, 2 literal slots).
 *
 *   pool +0x20c -> constant 0x0223989c (image word 0x0223989c)
 *   pool +0x210 -> constant 0x0223992c (image word 0x0223992c)
 *   branch +0x10 -> +0x98
 *   branch +0x20 -> +0x38
 *   branch +0x94 -> +0x204
 *   branch +0x9c -> +0xc0
 *   branch +0xbc -> +0x204
 *   branch +0xc4 -> +0x1b0
 *   branch +0xec -> +0x138
 *   branch +0x134 -> +0x198
 *   branch +0x1ac -> +0x204
 *   branch +0x1b4 -> +0x1d8
 *   branch +0x1d4 -> +0x204
 *   branch +0x1dc -> +0x204
 *   test +0x0c cmp r1, #0
 *   test +0x1c cmp r0, #0
 *   test +0x98 cmp r1, #10
 *   test +0xac cmp r1, #30
 *   test +0xc0 cmp r1, #20
 *   test +0xe8 tst r0, #32
 *   test +0x1b0 cmp r1, #30
 *   test +0x1c4 cmp r1, #30
 *   test +0x1d8 cmp r1, #100
 *   0 block transfer(s), 12 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f8718; the literal pool and
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

extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_021f82d8(void);
extern void native_fn_0202ac08(void);
extern void native_fn_021eea10(void);
extern void native_fn_0205d790(void);
extern void ov001_effect_resource_create_021eec7c(void);
extern void native_fn_021ee9fc(void);
extern void native_fn_021dca04(void);
extern void native_fn_0207afec(void);
extern void native_fn_021e29e8(void);
extern void native_fn_021f0f0c(void);
extern void native_fn_021ee7d4(void);
extern void native_fn_022024d4(void);
extern void native_fn_021f0eb4(void);
extern void native_fn_021ee78c(void);
extern void native_fn_021d9494(void);
extern void native_fn_021eeb70(void);
extern void native_fn_0202ac4c(void);


asm u32 native_ov001_021f8718 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    ldr r0, =0x0223989c
    ldrb r1, [r0, #0x25]
    cmp r1, #0
    bne ov001_021f8718_L98
    ldr r0, [r0, #0x78]
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    bne ov001_021f8718_L38
    ldr r0, =0x0223989c
    mov r1, #27
    strb r1, [r0, #0x1b]
    mov r0, #0
    ldmia sp!, {r3, r4, r5, pc}
ov001_021f8718_L38:
    ldr r0, =0x0223989c
    ldr r0, [r0, #0x78]
    bl native_fn_021f82d8
    ldr r0, =0x0223992c
    bl native_fn_0202ac08
    mov r0, #138
    mov r1, #0
    bl native_fn_021eea10
    mov r0, #138
    bl native_fn_0205d790
    ldr r1, =0x0223989c
    mov r2, r0
    ldr r1, [r1, #0x78]
    mov r0, #138
    bl ov001_effect_resource_create_021eec7c
    ldr r0, =0x0223989c
    ldr r0, [r0, #0x78]
    bl native_fn_021ee9fc
    ldr r0, =0x0223989c
    mov r1, #10
    strb r1, [r0, #0x25]
    mov r1, #0
    strb r1, [r0, #0x24]
    b ov001_021f8718_L204
ov001_021f8718_L98:
    cmp r1, #10
    bne ov001_021f8718_Lc0
    ldrb r1, [r0, #0x24]
    add r2, r1, #1
    and r1, r2, #255
    cmp r1, #30
    strb r2, [r0, #0x24]
    movhs r1, #20
    strhsb r1, [r0, #0x25]
    b ov001_021f8718_L204
ov001_021f8718_Lc0:
    cmp r1, #20
    bne ov001_021f8718_L1b0
    ldr r0, [r0, #0x78]
    bl native_fn_021dca04
    ldr r1, =0x0223989c
    mov r4, r0
    ldrh r0, [r1, #80]
    bl native_fn_0207afec
    ldrb r5, [r0, #0x1e]
    bl native_fn_021e29e8
    tst r0, #32
    bne ov001_021f8718_L138
    ldr r0, =0x0223989c
    mov r1, r4
    ldrh r2, [r0, #80]
    ldr r0, [r0, #0x78]
    bl native_fn_021f0f0c
    mov r4, r0
    ldr r0, =0x0223989c
    mov r1, r4
    ldr r0, [r0, #0x78]
    mov r2, r5
    bl native_fn_021ee7d4
    ldr r0, =0x0223989c
    rsb r2, r4, #0
    ldr r1, [r0, #0x78]
    ldrb r0, [r1, #0x31e]
    ldrb r1, [r1, #0x31f]
    bl native_fn_022024d4
    b ov001_021f8718_L198
ov001_021f8718_L138:
    ldr r0, =0x0223989c
    mov r1, r4
    ldrh r2, [r0, #80]
    ldr r0, [r0, #0x78]
    bl native_fn_021f0eb4
    mov r1, #0
    ldr r0, =0x0223989c
    str r1, [sp]
    ldrh r2, [r0, #80]
    ldr r0, [r0, #0x78]
    mov r1, r4
    mov r3, r5
    bl native_fn_021ee78c
    ldr r0, =0x0223989c
    mov r2, r4
    ldr r1, [r0, #0x78]
    ldrb r0, [r1, #0x31e]
    ldrb r1, [r1, #0x31f]
    bl native_fn_022024d4
    ldr r0, =0x0223989c
    mov r1, #4
    ldr r0, [r0, #0x78]
    mov r2, #1
    bl native_fn_021d9494
ov001_021f8718_L198:
    ldr r0, =0x0223989c
    mov r1, #30
    strb r1, [r0, #0x25]
    mov r1, #0
    strb r1, [r0, #0x24]
    b ov001_021f8718_L204
ov001_021f8718_L1b0:
    cmp r1, #30
    bne ov001_021f8718_L1d8
    ldrb r1, [r0, #0x24]
    add r2, r1, #1
    and r1, r2, #255
    cmp r1, #30
    strb r2, [r0, #0x24]
    movhs r1, #100
    strhsb r1, [r0, #0x25]
    b ov001_021f8718_L204
ov001_021f8718_L1d8:
    cmp r1, #100
    bne ov001_021f8718_L204
    mov r0, #138
    bl native_fn_021eeb70
    ldr r0, =0x0223992c
    bl native_fn_0202ac4c
    ldr r0, =0x0223989c
    mov r1, #0
    strb r1, [r0, #0x25]
    mov r1, #27
    strb r1, [r0, #0x1b]
ov001_021f8718_L204:
    mov r0, #0
    ldmia sp!, {r3, r4, r5, pc}
}
