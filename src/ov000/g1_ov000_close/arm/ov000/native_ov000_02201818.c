/* ov000 row 0x02201818: 376 bytes.
 *
 * What it does: 88 instructions; 15 call(s) to 0x02215698, 0x02217814, 0x021e7b9c, +12 more; loops (back edge at +0x48); returns through pop {r4, r5, r6, r7, r8, pc}; 6 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x160 -> constant 0x02237d9c (image word 0x02237d9c)
 *   pool +0x164 -> constant 0x02237f7c (image word 0x02237f7c)
 *   pool +0x168 -> constant 0x02237d94 (image word 0x02237d94)
 *   pool +0x16c -> constant 0x02237e8c (image word 0x02237e8c)
 *   pool +0x170 -> constant 0x02237f80 (image word 0x02237f80)
 *   pool +0x174 -> native_data_0222f4cc (image word 0x0222f4cc)
 *   branch +0x20 -> +0x30
 *   branch +0x28 -> +0xb8
 *   branch +0x2c -> +0x158
 *   branch +0x40 -> +0x50
 *   branch +0x4c -> +0x158
 *   branch +0x60 -> +0xa0
 *   branch +0x9c -> +0x158
 *   branch +0xb4 -> +0x158
 *   branch +0xd8 -> +0xe8
 *   branch +0xe4 -> +0x158
 *   branch +0xf8 -> +0x108
 *   branch +0x104 -> +0x158
 *   branch +0x134 -> +0x158
 *   test +0x18 cmp r6, #1
 *   test +0x24 cmp r6, #3
 *   test +0x3c cmp r0, #0
 *   test +0x54 cmp r0, #12
 *   test +0x58 cmpne r0, #13
 *   test +0xcc cmp r0, #12
 *   test +0xd4 cmpne r0, #0
 *   test +0xf4 cmp r0, #0
 *   test +0x130 cmp r0, #12
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02201818; the literal pool and
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

extern void native_fn_02215698(void);
extern void native_fn_02217814(void);
extern void native_fn_021e7b9c(void);
extern void native_fn_0206332c(void);
extern void native_fn_0204b61c(void);
extern void native_fn_02202708(void);
extern void native_fn_02216664(void);
extern void native_fn_022017a8(void);
extern void native_fn_02201990(void);
extern u8 native_data_0222f4cc[];
extern void native_fn_02040790(void);


asm u32 native_ov000_02201818 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    mov r6, r0
    bl native_fn_02215698
    ldr r8, =0x02237d9c
    mov r7, r0
    ldr r0, [r8]
    cmp r6, #1
    and r4, r0, #255
    beq ov000_02201818_L30
    cmp r6, #3
    beq ov000_02201818_Lb8
    b ov000_02201818_L158
ov000_02201818_L30:
    ldr r5, =0x02237f7c
    ldrb r0, [r5, r4]
    bl native_fn_02217814
    cmp r0, #0
    bne ov000_02201818_L50
    mov r0, #84
    bl native_fn_021e7b9c
    b ov000_02201818_L158
ov000_02201818_L50:
    ldrb r0, [r5, r4]
    cmp r0, #12
    cmpne r0, #13
    sub r0, r0, #12
    bne ov000_02201818_La0
    and r0, r0, #255
    bl native_fn_0206332c
    add r0, r7, #16
    mov r1, #0
    bl native_fn_0204b61c
    mov r0, #0
    bl native_fn_02202708
    mov r0, r8
    bl native_fn_02216664
    ldr r1, =0x02237d94
    mov r2, #2
    mov r0, #82
    str r2, [r1]
    bl native_fn_021e7b9c
    b ov000_02201818_L158
ov000_02201818_La0:
    and r0, r0, #255
    bl native_fn_0206332c
    ldrb r1, [r5, r4]
    mov r0, r6
    bl native_fn_022017a8
    b ov000_02201818_L158
ov000_02201818_Lb8:
    ldr r0, =0x02237d94
    ldr r1, =0x02237f7c
    ldr r0, [r0, #0x8]
    ldr r5, =0x02237e8c
    ldrb r0, [r1, r0]
    cmp r0, #12
    ldrne r0, [r5]
    cmpne r0, #0
    beq ov000_02201818_Le8
    mov r0, r6
    bl native_fn_02201990
    b ov000_02201818_L158
ov000_02201818_Le8:
    ldr r7, =0x02237f7c
    ldrb r0, [r7, r4]
    bl native_fn_02217814
    cmp r0, #0
    bne ov000_02201818_L108
    mov r0, #84
    bl native_fn_021e7b9c
    b ov000_02201818_L158
ov000_02201818_L108:
    ldr r0, =0x02237d94
    mov r1, #7
    str r1, [r0, #0x4]
    ldrb r1, [r7, r4]
    mov r0, r6
    bl native_fn_022017a8
    ldr r0, =0x02237d94
    mov r1, r7
    ldr r0, [r0, #0x8]
    ldrb r0, [r1, r0]
    cmp r0, #12
    bne ov000_02201818_L158
    ldr r2, [r5]
    ldr r1, =0x02237f80
    mov r0, #6
    ldrb r2, [r1, r2]
    ldr r1, =native_data_0222f4cc
    smulbb r0, r2, r0
    ldrh r0, [r1, r0]
    bl native_fn_02040790
ov000_02201818_L158:
    mov r0, #0
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
