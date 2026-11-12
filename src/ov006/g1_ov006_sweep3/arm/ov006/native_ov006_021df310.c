/* ov006 row 0x021df310: 328 bytes.
 *
 * What it does: 81 instructions; 16 call(s) to 0x021df134, 0x02049008, 0x021df134, +13 more; loops (back edge at +0x18); returns through pop {r3, r4, r5, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x144 -> constant 0x0220f594 (image word 0x0220f594)
 *   branch +0x14 -> +0x54
 *   branch +0x50 -> +0x98
 *   branch +0x5c -> +0x7c
 *   branch +0x78 -> +0x98
 *   branch +0xe8 -> +0x128
 *   branch +0xf8 -> +0x128
 *   back edge +0x138 -> +0xd4
 *   test +0x10 cmp r1, #1
 *   test +0x58 cmp r0, #0
 *   test +0xe4 cmp r0, #0
 *   test +0xf4 cmp r0, #127
 *   test +0x134 cmp r5, #31
 *   0 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021df310; the literal pool and
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

extern void native_fn_021df134(void);
extern void native_fn_02049008(void);
extern void native_fn_021df140(void);
extern void native_fn_021dde10(void);
extern void native_fn_02049ad0(void);
extern void native_fn_021dddc4(void);
extern void native_fn_021ddf44(void);
extern void native_fn_0206006c(void);


asm u32 native_ov006_021df310 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    sub sp, sp, #8
    ldr r0, =0x0220f594
    ldr r1, [r0, #0x2c]
    cmp r1, #1
    bne ov006_021df310_L54
    bl native_fn_021df134
    mov r1, #5
    mov r4, #0
    mov r2, r1
    mov r3, #7
    str r4, [sp]
    bl native_fn_02049008
    bl native_fn_021df134
    mov r3, r4
    str r3, [sp]
    mov r1, #14
    mov r2, #6
    mov r3, #8
    bl native_fn_02049008
    b ov006_021df310_L98
ov006_021df310_L54:
    ldr r0, [r0, #0x18]
    cmp r0, #0
    bne ov006_021df310_L7c
    bl native_fn_021df134
    mov r2, #0
    mov r1, #5
    mov r3, #1
    str r2, [sp]
    bl native_fn_02049008
    b ov006_021df310_L98
ov006_021df310_L7c:
    bl native_fn_021df134
    mov r2, #1
    mov r4, #0
    mov r3, r2
    mov r1, #5
    str r4, [sp]
    bl native_fn_02049008
ov006_021df310_L98:
    ldr r0, =0x0220f594
    mov r1, #16
    ldrb r0, [r0, #0x2]
    strh r1, [sp, #4]
    add r0, r0, #1
    mov r0, r0, lsl #3
    strh r0, [sp, #6]
    bl native_fn_021df134
    mov r4, r0
    bl native_fn_021df140
    mov r1, r0
    add r2, sp, #4
    mov r0, r4
    bl native_fn_021dde10
    mov r5, #0
ov006_021df310_Ld4:
    mov r0, r5
    bl native_fn_02049ad0
    mov r4, r0
    ldr r0, [r4]
    cmp r0, #0
    beq ov006_021df310_L128
    ldrsb r0, [r4, #5]
    bl native_fn_021dddc4
    cmp r0, #127
    beq ov006_021df310_L128
    ldr r1, [r4]
    mov r0, r0, lsl #24
    ldr r4, [r1, #0x4]
    mov r0, r0, asr #24
    bl native_fn_021ddf44
    ldrsb r1, [r4, #31]
    str r1, [sp]
    ldrsb r1, [r4, #28]
    ldrsb r2, [r4, #29]
    ldrsb r3, [r4, #30]
    bl native_fn_0206006c
ov006_021df310_L128:
    add r0, r5, #1
    mov r0, r0, lsl #24
    mov r5, r0, asr #24
    cmp r5, #31
    blt ov006_021df310_Ld4
    add sp, sp, #8
    ldmia sp!, {r3, r4, r5, pc}
}
