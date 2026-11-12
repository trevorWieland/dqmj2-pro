/* ov006 row 0x021dc878: 660 bytes.
 *
 * What it does: Writes one block of 2 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x28c -> native_data9_0220f4d8 (image word 0x0220f4d8)
 *   pool +0x290 -> constant 0x021c9698 (image word 0x021c9698)
 *   branch +0x14 -> +0x24
 *   branch +0x20 -> +0x2c
 *   branch +0x48 -> +0x58
 *   branch +0x54 -> +0x60
 *   branch +0x90 -> +0xfc
 *   branch +0xf8 -> +0x1cc
 *   branch +0x13c -> +0x15c
 *   branch +0x158 -> +0x174
 *   branch +0x184 -> +0x1ac
 *   branch +0x1a8 -> +0x1cc
 *   back edge +0x1d8 -> +0x80
 *   test +0x10 cmp r0, #0
 *   test +0x40 cmp r0, #0
 *   test +0x8c cmp r0, #0
 *   test +0x138 cmp r0, #1
 *   test +0x180 cmp r0, #0
 *   test +0x1d4 cmp r9, #5
 *   1 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021dc878; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity proves the instruction stream, not the meaning of the fields, blocks and callee contracts it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data9_0220f4d8[];
extern void native_fn_02063ef8(void);
extern void native_fn_02067904(void);
extern void native_fn_021d79e4(void);
extern void native_fn_021d79f8(void);
extern void native_fn_02046af4(void);
extern void native_fn_021d7ad0(void);
extern void native_fn_021d8414(void);


asm u32 native_ov006_021dc878 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #72
    ldr r0, =native_data9_0220f4d8
    ldr r0, [r0, #0x4]
    cmp r0, #0
    bne ov006_021dc878_L24
    bl native_fn_02063ef8
    ldr r1, =native_data9_0220f4d8
    b ov006_021dc878_L2c
ov006_021dc878_L24:
    bl native_fn_02067904
    ldr r1, =native_data9_0220f4d8
ov006_021dc878_L2c:
    str r0, [r1]
    ldr r0, =native_data9_0220f4d8
    mov r1, #15
    ldr r0, [r0, #0x4]
    mov r2, #2
    cmp r0, #0
    mov r0, #0
    bne ov006_021dc878_L58
    mov r3, #155
    bl native_fn_021d79e4
    b ov006_021dc878_L60
ov006_021dc878_L58:
    mov r3, #156
    bl native_fn_021d79e4
ov006_021dc878_L60:
    mov r9, #0
    mov r5, #2
    ldr r4, =native_data9_0220f4d8
    mov r10, r9
    add r7, sp, #8
    mov r11, #255
    mov r6, r5
    mov r8, #40
ov006_021dc878_L80:
    ldr r1, [r4]
    add r0, r1, r10
    ldrb r0, [r0, #0x10]
    cmp r0, #0
    bne ov006_021dc878_Lfc
    add r0, r9, #8
    and r0, r0, #255
    mov r1, #15
    mov r2, #0
    mov r3, #1
    bl native_fn_021d79e4
    add r0, r9, #13
    and r0, r0, #255
    mov r1, #15
    mov r2, #0
    mov r3, #1
    bl native_fn_021d79e4
    add r0, r9, #18
    and r0, r0, #255
    mov r1, #15
    mov r2, #0
    mov r3, #1
    bl native_fn_021d79e4
    add r0, r9, #18
    and r0, r0, #255
    mov r1, #15
    mov r2, #2
    mov r3, #122
    str r8, [sp]
    bl native_fn_021d79f8
    b ov006_021dc878_L1cc
ov006_021dc878_Lfc:
    add r0, r1, #16
    add r1, r0, r10
    ldr r0, =0x021c9698
    mov r2, #31
    mov r3, #0
    stmia sp, {r7, r11}
    bl native_fn_02046af4
    add r0, r9, #8
    and r0, r0, #255
    mov r1, r7
    bl native_fn_021d7ad0
    ldr r0, [r4]
    mov r1, #15
    add r0, r0, r10
    ldr r0, [r0, #0x34]
    cmp r0, #1
    bne ov006_021dc878_L15c
    add r0, r9, #13
    and r0, r0, #255
    mov r2, r6
    mov r3, #158
    str r6, [sp]
    bl native_fn_021d79f8
    b ov006_021dc878_L174
ov006_021dc878_L15c:
    add r0, r9, #13
    and r0, r0, #255
    mov r2, r5
    mov r3, #159
    str r5, [sp]
    bl native_fn_021d79f8
ov006_021dc878_L174:
    ldr r0, [r4]
    add r0, r0, r10
    ldr r0, [r0, #0x30]
    cmp r0, #0
    bne ov006_021dc878_L1ac
    mov r0, #40
    str r0, [sp]
    add r0, r9, #18
    and r0, r0, #255
    mov r1, #15
    mov r2, #2
    mov r3, #122
    bl native_fn_021d79f8
    b ov006_021dc878_L1cc
ov006_021dc878_L1ac:
    mov r1, r7
    mov r2, #16
    mov r3, #6
    bl native_fn_021d8414
    add r0, r9, #18
    and r0, r0, #255
    mov r1, r7
    bl native_fn_021d7ad0
ov006_021dc878_L1cc:
    add r10, r10, #48
    add r9, r9, #1
    cmp r9, #5
    blt ov006_021dc878_L80
    ldr r0, =native_data9_0220f4d8
    add r1, sp, #8
    ldr r3, [r0]
    mov r2, #16
    ldrb r0, [r3, #0x3]
    ldr r4, [r3, #0xc]
    mov r3, #4
    sub r0, r4, r0
    bl native_fn_021d8414
    add r1, sp, #8
    mov r0, #4
    bl native_fn_021d7ad0
    ldr r0, =native_data9_0220f4d8
    add r1, sp, #8
    ldr r0, [r0]
    mov r2, #16
    ldr r0, [r0, #0x8]
    mov r3, #4
    bl native_fn_021d8414
    add r1, sp, #8
    mov r0, #5
    bl native_fn_021d7ad0
    ldr r0, =native_data9_0220f4d8
    add r1, sp, #8
    ldr r0, [r0]
    mov r2, #16
    ldrh r0, [r0, #6]
    mov r3, #4
    bl native_fn_021d8414
    mov r0, #6
    add r1, sp, #8
    bl native_fn_021d7ad0
    ldr r0, =native_data9_0220f4d8
    add r1, sp, #8
    ldr r0, [r0]
    mov r2, #16
    ldrh r0, [r0, #4]
    mov r3, #4
    bl native_fn_021d8414
    mov r0, #7
    add r1, sp, #8
    bl native_fn_021d7ad0
    add sp, sp, #72
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
