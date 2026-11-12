/* ov000 row 0x021d966c: 372 bytes.
 *
 * What it does: 86 instructions; 8 call(s) to 0x0205bf9c, 0x021df220, 0x021d9664, +5 more; loops (back edge at +0x24); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 7 literal slot(s) in the extent
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x158 -> native_data_0222b848 (image word 0x0222b848)
 *   pool +0x15c -> constant 0x022303e8 (image word 0x022303e8)
 *   pool +0x160 -> constant 0x0223142c (image word 0x0223142c)
 *   pool +0x164 -> constant 0x004e4353 (image word 0x004e4353)
 *   pool +0x168 -> native_data_0222e210 (image word 0x0222e210)
 *   pool +0x16c -> native_data_0222e228 (image word 0x0222e228)
 *   pool +0x170 -> constant 0x0223042c (image word 0x0223042c)
 *   branch +0x38 -> +0x14c
 *   branch +0x6c -> +0x12c
 *   branch +0x8c -> +0xbc
 *   branch +0xb8 -> +0xd8
 *   branch +0xe8 -> +0x11c
 *   branch +0xf4 -> +0x11c
 *   branch +0x118 -> +0x140
 *   back edge +0x124 -> +0x88
 *   branch +0x128 -> +0x140
 *   back edge +0x148 -> +0x60
 *   test +0x34 cmp r0, #0
 *   test +0x3c cmp r4, #255
 *   test +0x68 cmp r0, #0
 *   test +0x88 cmp r8, #0
 *   test +0xe4 cmp r0, #0
 *   test +0xf0 cmp r1, r11
 *   test +0x120 cmp r8, #2
 *   test +0x144 cmp r10, #3
 *   3 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021d966c; the literal pool and
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

extern u8 native_data_0222b848[];
extern void native_fn_0205bf9c(void);
extern void native_fn_021df220(void);
extern void native_fn_021d9664(void);
extern u8 native_data_0222e210[];
extern void native_fn_0201d444(void);
extern u8 native_data_0222e228[];
extern void native_fn_02040d18(void);


asm u32 native_ov000_021d966c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #44
    ldr r1, =native_data_0222b848
    add r3, sp, #16
    mov r4, r0
    ldmia r1, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    mov r0, #0
    str r0, [sp, #0x8]
    bl native_fn_0205bf9c
    ldr r1, =0x022303e8
    mov r9, r0
    ldr r0, [r1]
    cmp r0, #0
    beq ov000_021d966c_L14c
    cmp r4, #255
    ldreq r0, =0x0223142c
    add r1, sp, #14
    ldreqb r4, [r0, #0x7c0]
    add r2, sp, #13
    add r3, sp, #12
    mov r0, r4
    bl native_fn_021df220
    mov r10, #0
ov000_021d966c_L60:
    mov r0, r10
    bl native_fn_021d9664
    cmp r0, #0
    beq ov000_021d966c_L12c
    mov r8, #0
    ldr r11, =0x004e4353
    ldr r4, =0x022303e8
    mov r5, r8
    add r6, sp, #28
    add r7, sp, #16
ov000_021d966c_L88:
    cmp r8, #0
    bne ov000_021d966c_Lbc
    ldrb r2, [sp, #0xc]
    ldr r1, =native_data_0222e210
    mov r0, r6
    str r2, [sp]
    ldr r2, [r7, r10, lsl #2]
    add r2, r9, r2
    str r2, [sp, #0x4]
    ldrsb r2, [sp, #14]
    ldrb r3, [sp, #0xd]
    bl native_fn_0201d444
    b ov000_021d966c_Ld8
ov000_021d966c_Lbc:
    ldrb r2, [sp, #0xc]
    ldr r1, =native_data_0222e228
    mov r0, r6
    stmia sp, {r2, r5}
    ldrsb r2, [sp, #14]
    ldrb r3, [sp, #0xd]
    bl native_fn_0201d444
ov000_021d966c_Ld8:
    ldr r0, [r4]
    mov r1, r6
    bl native_fn_02040d18
    cmp r0, #0
    beq ov000_021d966c_L11c
    ldr r1, [r0]
    cmp r1, r11
    bne ov000_021d966c_L11c
    ldr r1, =0x0223042c
    mov r2, #1
    add r1, r1, r10, lsl #2
    add r1, r1, #4096
    str r0, [r1, #0x7a8]
    ldr r0, [sp, #0x8]
    orr r0, r0, r2, lsl r10
    str r0, [sp, #0x8]
    b ov000_021d966c_L140
ov000_021d966c_L11c:
    add r8, r8, #1
    cmp r8, #2
    blt ov000_021d966c_L88
    b ov000_021d966c_L140
ov000_021d966c_L12c:
    ldr r0, =0x0223042c
    mov r1, #0
    add r0, r0, r10, lsl #2
    add r0, r0, #4096
    str r1, [r0, #0x7a8]
ov000_021d966c_L140:
    add r10, r10, #1
    cmp r10, #3
    blt ov000_021d966c_L60
ov000_021d966c_L14c:
    ldr r0, [sp, #0x8]
    add sp, sp, #44
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
