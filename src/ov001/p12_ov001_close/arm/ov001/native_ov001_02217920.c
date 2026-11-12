/* ov001 row 0x02217920: 348 bytes.
 *
 * What it does: 86 instructions; 14 call(s) to 0x0207b6e8, 0x0207afec, 0x021f1c68, +11 more; loops (back edge at +0x18); returns through pop {r3, r4, r5, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 14 calls (86 instructions, 14 calls, 12 branches, 14 back edges, 1 literal slot).
 *
 *   pool +0x158 -> constant 0x02242bf4 (image word 0x02242bf4)
 *   branch +0x14 -> +0xd4
 *   branch +0x38 -> +0x90
 *   branch +0x74 -> +0x80
 *   branch +0x8c -> +0xd4
 *   branch +0xa0 -> +0xd4
 *   branch +0xe0 -> +0x114
 *   branch +0xec -> +0x150
 *   branch +0x110 -> +0x150
 *   branch +0x118 -> +0x138
 *   branch +0x124 -> +0x150
 *   branch +0x134 -> +0x150
 *   branch +0x13c -> +0x150
 *   test +0x10 cmp r1, #0
 *   test +0x34 cmp r0, #1
 *   test +0x6c cmp r4, #195
 *   test +0x90 cmp r1, #3
 *   test +0xdc cmp r1, #10
 *   test +0xe8 cmp r0, #0
 *   test +0x114 cmp r1, #20
 *   test +0x120 cmp r0, #0
 *   test +0x138 cmp r1, #100
 *   0 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02217920; the literal pool and
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

extern void native_fn_0207b6e8(void);
extern void native_fn_0207afec(void);
extern void native_fn_021f1c68(void);
extern void native_fn_021f1bf0(void);
extern void native_fn_021f9248(void);
extern void native_fn_021f9264(void);
extern void native_fn_021f1c58(void);
extern void native_fn_02214308(void);
extern void native_fn_022142d0(void);
extern void native_fn_022148a0(void);
extern void native_fn_021f90b4(void);
extern void native_fn_02214818(void);


asm u32 native_ov001_02217920 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    ldr r1, =0x02242bf4
    mov r4, r0
    ldrsb r1, [r1, #5]
    cmp r1, #0
    bne ov001_02217920_Ld4
    bl native_fn_0207b6e8
    mov r5, r0
    bl native_fn_0207afec
    ldrh r0, [r0, #8]
    mov r0, r0, lsl #28
    mov r1, r0, lsr #28
    sub r0, r1, #5
    cmp r0, #1
    bhi ov001_02217920_L90
    mov r0, #1
    bl native_fn_021f1c68
    mov r0, r5
    bl native_fn_021f1bf0
    mov r2, r4
    mov r0, #11
    mov r1, #0
    mov r3, #2
    bl native_fn_021f9248
    mov r0, #0
    bl native_fn_021f9264
    ldr r1, =0x02242bf4
    cmp r4, #195
    strb r0, [r1, #0x3]
    bne ov001_02217920_L80
    mov r0, #1
    bl native_fn_021f1c58
ov001_02217920_L80:
    ldr r0, =0x02242bf4
    mov r1, #10
    strb r1, [r0, #0x5]
    b ov001_02217920_Ld4
ov001_02217920_L90:
    cmp r1, #3
    ldrne r0, =0x02242bf4
    movne r1, #100
    strneb r1, [r0, #0x5]
    bne ov001_02217920_Ld4
    mov r0, #1
    bl native_fn_02214308
    mov r0, r5
    bl native_fn_022142d0
    mov r2, r4
    mov r0, #11
    mov r1, #0
    mov r3, #2
    bl native_fn_022148a0
    ldr r0, =0x02242bf4
    mov r1, #20
    strb r1, [r0, #0x5]
ov001_02217920_Ld4:
    ldr r0, =0x02242bf4
    ldrsb r1, [r0, #5]
    cmp r1, #10
    bne ov001_02217920_L114
    bl native_fn_021f90b4
    cmp r0, #0
    beq ov001_02217920_L150
    ldr r0, =0x02242bf4
    ldrb r0, [r0, #0x3]
    bl native_fn_021f9264
    mov r0, #0
    bl native_fn_021f1c58
    ldr r0, =0x02242bf4
    mov r1, #100
    strb r1, [r0, #0x5]
    b ov001_02217920_L150
ov001_02217920_L114:
    cmp r1, #20
    bne ov001_02217920_L138
    bl native_fn_02214818
    cmp r0, #0
    beq ov001_02217920_L150
    ldr r0, =0x02242bf4
    mov r1, #100
    strb r1, [r0, #0x5]
    b ov001_02217920_L150
ov001_02217920_L138:
    cmp r1, #100
    bne ov001_02217920_L150
    mov r1, #0
    strb r1, [r0, #0x5]
    mov r0, #1
    ldmia sp!, {r3, r4, r5, pc}
ov001_02217920_L150:
    mov r0, #0
    ldmia sp!, {r3, r4, r5, pc}
}
