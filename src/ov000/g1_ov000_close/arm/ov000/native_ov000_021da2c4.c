/* ov000 row 0x021da2c4: 368 bytes.
 *
 * What it does: 85 instructions; 8 call(s) to 0x0205bf9c, 0x021df220, 0x0205bfd4, +5 more; loops (back edge at +0x30); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 7 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x154 -> native_data_0222b820 (image word 0x0222b820)
 *   pool +0x158 -> constant 0x022303e8 (image word 0x022303e8)
 *   pool +0x15c -> constant 0x0223142c (image word 0x0223142c)
 *   pool +0x160 -> native_data_0222e240 (image word 0x0222e240)
 *   pool +0x164 -> native_data_0222e258 (image word 0x0222e258)
 *   pool +0x168 -> native_data_0222e270 (image word 0x0222e270)
 *   pool +0x16c -> constant 0x00525441 (image word 0x00525441)
 *   branch +0x44 -> +0x148
 *   branch +0x84 -> +0xbc
 *   branch +0xb8 -> +0x104
 *   branch +0xc4 -> +0xe8
 *   branch +0xe4 -> +0x104
 *   branch +0x114 -> +0x13c
 *   branch +0x124 -> +0x148
 *   branch +0x138 -> +0x148
 *   back edge +0x144 -> +0x80
 *   test +0x40 cmp r0, #0
 *   test +0x48 cmp r4, #255
 *   test +0x80 cmp r8, #0
 *   test +0xbc cmp r8, #1
 *   test +0x110 cmp r0, #0
 *   test +0x120 cmp r2, r1
 *   test +0x140 cmp r8, #3
 *   2 block transfer(s), 10 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021da2c4; the literal pool and
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

extern u8 native_data_0222b820[];
extern void native_fn_0205bf9c(void);
extern void native_fn_021df220(void);
extern u8 native_data_0222e240[];
extern void native_fn_0205bfd4(void);
extern void native_fn_0201d444(void);
extern u8 native_data_0222e258[];
extern u8 native_data_0222e270[];
extern void native_fn_02040d18(void);


asm u32 native_ov000_021da2c4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #48
    ldr r3, =native_data_0222b820
    str r0, [sp, #0xc]
    ldr r0, [r3, #0x24]
    ldr r5, [r3, #0x20]
    str r0, [sp, #0x1c]
    mov r0, #0
    mov r4, r1
    mov r10, r2
    str r5, [sp, #0x18]
    str r0, [sp, #0x10]
    bl native_fn_0205bf9c
    ldr r1, =0x022303e8
    mov r9, r0
    ldr r0, [r1]
    cmp r0, #0
    beq ov000_021da2c4_L148
    cmp r4, #255
    ldreq r0, =0x0223142c
    add r1, sp, #22
    ldreqb r4, [r0, #0x7c0]
    add r2, sp, #21
    add r3, sp, #20
    mov r0, r4
    bl native_fn_021df220
    mov r8, #0
    ldr r11, =native_data_0222e240
    ldr r4, =0x022303e8
    mov r5, r8
    add r6, sp, #32
    add r7, sp, #24
ov000_021da2c4_L80:
    cmp r8, #0
    bne ov000_021da2c4_Lbc
    bl native_fn_0205bfd4
    str r10, [sp]
    ldrb r2, [sp, #0x14]
    ldr r1, [r7, r0, lsl #2]
    mov r0, r6
    str r2, [sp, #0x4]
    add r1, r9, r1
    str r1, [sp, #0x8]
    mov r1, r11
    ldrsb r2, [sp, #22]
    ldrb r3, [sp, #0x15]
    bl native_fn_0201d444
    b ov000_021da2c4_L104
ov000_021da2c4_Lbc:
    cmp r8, #1
    str r10, [sp]
    bne ov000_021da2c4_Le8
    ldrb r2, [sp, #0x14]
    ldr r1, =native_data_0222e258
    mov r0, r6
    stmib sp, {r2, r9}
    ldrsb r2, [sp, #22]
    ldrb r3, [sp, #0x15]
    bl native_fn_0201d444
    b ov000_021da2c4_L104
ov000_021da2c4_Le8:
    ldrb r2, [sp, #0x14]
    ldr r1, =native_data_0222e270
    mov r0, r6
    stmib sp, {r2, r5}
    ldrsb r2, [sp, #22]
    ldrb r3, [sp, #0x15]
    bl native_fn_0201d444
ov000_021da2c4_L104:
    ldr r0, [r4]
    mov r1, r6
    bl native_fn_02040d18
    cmp r0, #0
    beq ov000_021da2c4_L13c
    ldr r2, [r0]
    ldr r1, =0x00525441
    cmp r2, r1
    bne ov000_021da2c4_L148
    ldr r1, [sp, #0xc]
    str r0, [r1]
    mov r0, #1
    str r0, [sp, #0x10]
    b ov000_021da2c4_L148
ov000_021da2c4_L13c:
    add r8, r8, #1
    cmp r8, #3
    blt ov000_021da2c4_L80
ov000_021da2c4_L148:
    ldr r0, [sp, #0x10]
    add sp, sp, #48
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
