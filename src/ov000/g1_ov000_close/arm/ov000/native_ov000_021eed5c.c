/* ov000 row 0x021eed5c: 476 bytes.
 *
 * What it does: 109 instructions; 17 call(s) to 0x02048404, 0x0204854c, 0x0204b1a0, +14 more; loops (back edge at +0x18); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}; 10 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x1b4 -> native_data_0222ee68 (image word 0x0222ee68)
 *   pool +0x1b8 -> constant 0x02236bd0 (image word 0x02236bd0)
 *   pool +0x1bc -> constant 0x02236be4 (image word 0x02236be4)
 *   pool +0x1c0 -> constant 0x02236bd8 (image word 0x02236bd8)
 *   pool +0x1c4 -> constant 0x02236bdc (image word 0x02236bdc)
 *   pool +0x1c8 -> constant 0x02236be0 (image word 0x02236be0)
 *   pool +0x1cc -> constant 0x02236c04 (image word 0x02236c04)
 *   pool +0x1d0 -> constant 0x02236bec (image word 0x02236bec)
 *   pool +0x1d4 -> native_data_0222b908 (image word 0x0222b908)
 *   pool +0x1d8 -> constant 0x02101ae8 (image word 0x02101ae8)
 *   branch +0x2c -> +0x1a8
 *   branch +0x44 -> +0x198
 *   branch +0x54 -> +0x194
 *   back edge +0x134 -> +0x104
 *   back edge +0x174 -> +0x14c
 *   test +0x24 cmp r1, #255
 *   test +0x3c cmp r0, #0
 *   test +0x50 cmp r2, #0
 *   test +0x104 cmp r8, #3
 *   test +0x12c cmp r8, #6
 *   test +0x16c cmp r8, #6
 *   0 block transfer(s), 10 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021eed5c; the literal pool and
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

extern u8 native_data_0222ee68[];
extern void native_fn_02048404(void);
extern void native_fn_0204854c(void);
extern void native_fn_0204b1a0(void);
extern void native_fn_020c1c20(void);
extern void native_fn_020c1de0(void);
extern void native_fn_020c1c30(void);
extern void native_fn_02048a60(void);
extern void native_fn_020c1cf4(void);
extern u8 native_data_0222b908[];
extern void native_fn_0203cfe0(void);
extern void native_fn_02048308(void);
extern void native_fn_020485b4(void);
extern void native_fn_020484dc(void);


asm u32 native_ov000_021eed5c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    sub sp, sp, #8
    ldr r1, =native_data_0222ee68
    mov r0, #1
    mov r2, #4
    mov r3, #2
    bl native_fn_02048404
    mov r1, r0
    ldr r0, =0x02236bd0
    cmp r1, #255
    strb r1, [r0]
    beq ov000_021eed5c_L1a8
    mov r0, #1
    bl native_fn_0204854c
    ldr r1, =0x02236bd0
    cmp r0, #0
    str r0, [r1, #0x4]
    beq ov000_021eed5c_L198
    ldr r2, [r0, #0x4]
    str r2, [r1, #0x18]
    cmp r2, #0
    beq ov000_021eed5c_L194
    mov r0, r2
    bl native_fn_0204b1a0
    ldr r0, =0x02236bd0
    ldr r0, [r0, #0x18]
    bl native_fn_020c1c20
    mov r0, #0
    str r0, [sp]
    mov r4, #32
    ldr r1, =0x02236be4
    mov r0, #2
    mov r2, #1
    mov r3, #36
    str r4, [sp, #0x4]
    bl native_fn_020c1de0
    mov r0, #2
    ldr r1, =0x02236bd8
    mov r2, #30
    mov r3, #1
    str r0, [sp]
    bl native_fn_020c1c30
    ldr r0, =0x02236bd0
    mov r1, #160
    ldr r0, [r0, #0x8]
    mov r2, #24
    bl native_fn_02048a60
    mvn r0, #2
    str r0, [sp]
    ldr r1, =0x02236bdc
    mov r0, #2
    mov r2, #45
    mov r3, #1
    bl native_fn_020c1c30
    mov r2, #1
    ldr r1, =0x02236be0
    mov r0, #2
    sub r3, r2, #5
    bl native_fn_020c1cf4
    mov r8, #0
    ldr r9, =0x02236c04
    mov r6, #29
    mov r7, #28
    mov r5, r8
    mov r4, #2
ov000_021eed5c_L104:
    cmp r8, #3
    movlt r2, r7
    movge r2, r6
    mov r0, r4
    mov r1, r9
    mov r3, r5
    and r2, r2, #255
    str r5, [sp]
    bl native_fn_020c1c30
    add r8, r8, #1
    cmp r8, #6
    add r9, r9, #4
    blt ov000_021eed5c_L104
    mov r8, #0
    ldr r7, =0x02236bec
    ldr r5, =native_data_0222b908
    mov r6, #2
    mov r4, r8
ov000_021eed5c_L14c:
    bl native_fn_0203cfe0
    ldrb r2, [r5, r0]
    mov r0, r6
    mov r1, r7
    mov r3, r4
    str r6, [sp]
    bl native_fn_020c1c30
    add r8, r8, #1
    cmp r8, #6
    add r7, r7, #4
    blt ov000_021eed5c_L14c
    ldr r0, =0x02101ae8
    mov r1, #1
    str r1, [r0, #0xc84]
    bl native_fn_02048308
    add sp, sp, #8
    mov r0, #1
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
ov000_021eed5c_L194:
    bl native_fn_020485b4
ov000_021eed5c_L198:
    ldr r1, =0x02236bd0
    mov r0, #1
    ldrb r1, [r1]
    bl native_fn_020484dc
ov000_021eed5c_L1a8:
    mov r0, #0
    add sp, sp, #8
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
