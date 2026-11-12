/* ov000 row 0x02221ec0: 368 bytes.
 *
 * What it does: 90 instructions; 23 call(s) to 0x0202a634, 0x02041814, 0x0206a0fc, +20 more; loops (back edge at +0x04); returns through pop {r3, r4, r5, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x168 -> constant 0x02246438 (image word 0x02246438)
 *   pool +0x16c -> constant 0x02246464 (image word 0x02246464)
 *   branch +0x18 -> +0x40
 *   branch +0x24 -> +0x154
 *   branch +0x3c -> +0x154
 *   branch +0x44 -> +0x124
 *   branch +0x54 -> +0xc8
 *   branch +0x60 -> +0xc8
 *   branch +0x6c -> +0xb0
 *   branch +0x7c -> +0xc0
 *   branch +0xac -> +0xc0
 *   branch +0xb4 -> +0xc0
 *   branch +0xc4 -> +0xfc
 *   branch +0xcc -> +0xfc
 *   branch +0xd4 -> +0xfc
 *   branch +0x104 -> +0x114
 *   branch +0x110 -> +0x154
 *   branch +0x120 -> +0x154
 *   branch +0x12c -> +0x154
 *   test +0x14 cmp r0, #0
 *   test +0x20 cmp r0, #1
 *   test +0x40 cmp r0, #10
 *   test +0x5c cmp r0, #0
 *   test +0x68 tst r0, #1
 *   test +0x78 cmp r0, #0
 *   test +0xb0 tst r0, #2
 *   test +0xc8 cmp r5, #0
 *   test +0xd0 cmp r5, #1
 *   test +0x100 cmp r0, #0
 *   test +0x128 cmp r0, #1
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02221ec0; the literal pool and
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

extern void native_fn_0202a634(void);
extern void native_fn_02041814(void);
extern void native_fn_0206a0fc(void);
extern void native_fn_0206c0b0(void);
extern void native_fn_020698f4(void);
extern void native_fn_02041538(void);
extern void native_fn_020612b8(void);
extern void native_fn_021e7b9c(void);
extern void native_fn_0206a06c(void);
extern void native_fn_0206940c(void);
extern void native_fn_0206be2c(void);
extern void native_fn_02062a10(void);
extern void native_fn_0206dcd0(void);
extern void native_fn_0206bf34(void);
extern void native_fn_0206bf44(void);
extern void native_fn_02215780(void);
extern void native_fn_02222790(void);
extern void native_fn_02222410(void);


asm u32 native_ov000_02221ec0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    bl native_fn_0202a634
    ldr r1, =0x02246438
    mov r4, r0
    ldrb r0, [r1, #0x4]
    cmp r0, #0
    bne ov000_02221ec0_L40
    bl native_fn_02041814
    cmp r0, #1
    beq ov000_02221ec0_L154
    ldr r0, =0x02246438
    mov r1, #10
    strb r1, [r0, #0x4]
    mov r1, #0
    strb r1, [r0, #0x3]
    b ov000_02221ec0_L154
ov000_02221ec0_L40:
    cmp r0, #10
    bne ov000_02221ec0_L124
    mov r0, #1
    bl native_fn_0206a0fc
    movs r5, r0
    bne ov000_02221ec0_Lc8
    bl native_fn_0206c0b0
    cmp r0, #0
    bne ov000_02221ec0_Lc8
    ldrh r0, [r4, #2]
    tst r0, #1
    beq ov000_02221ec0_Lb0
    mov r0, #0
    bl native_fn_020698f4
    cmp r0, #0
    beq ov000_02221ec0_Lc0
    ldr r3, =0x02246438
    mov r12, #100
    mov r0, #1
    mov r1, #2
    mov r2, #10
    strb r12, [r3, #0x4]
    bl native_fn_02041538
    mov r0, #0
    bl native_fn_020612b8
    mov r0, #82
    bl native_fn_021e7b9c
    b ov000_02221ec0_Lc0
ov000_02221ec0_Lb0:
    tst r0, #2
    beq ov000_02221ec0_Lc0
    mov r0, #1
    bl native_fn_0206a06c
ov000_02221ec0_Lc0:
    bl native_fn_0206940c
    b ov000_02221ec0_Lfc
ov000_02221ec0_Lc8:
    cmp r5, #0
    beq ov000_02221ec0_Lfc
    cmp r5, #1
    bne ov000_02221ec0_Lfc
    ldr r3, =0x02246438
    mov r12, #100
    mov r0, #1
    mov r1, #2
    mov r2, #10
    strb r12, [r3, #0x4]
    bl native_fn_02041538
    mov r0, #0
    bl native_fn_020612b8
ov000_02221ec0_Lfc:
    bl native_fn_0206be2c
    cmp r0, #0
    beq ov000_02221ec0_L114
    bl native_fn_02062a10
    bl native_fn_0206dcd0
    b ov000_02221ec0_L154
ov000_02221ec0_L114:
    bl native_fn_0206bf34
    bl native_fn_02062a10
    bl native_fn_0206dcd0
    b ov000_02221ec0_L154
ov000_02221ec0_L124:
    bl native_fn_02041814
    cmp r0, #1
    beq ov000_02221ec0_L154
    bl native_fn_0206bf44
    ldr r1, =0x02246438
    mov r0, #6
    str r0, [r1, #0x18]
    mov r0, #0
    strb r0, [r1, #0x4]
    bl native_fn_02215780
    mov r0, #0
    ldmia sp!, {r3, r4, r5, pc}
ov000_02221ec0_L154:
    ldr r0, =0x02246464
    bl native_fn_02222790
    bl native_fn_02222410
    mov r0, #0
    ldmia sp!, {r3, r4, r5, pc}
}
