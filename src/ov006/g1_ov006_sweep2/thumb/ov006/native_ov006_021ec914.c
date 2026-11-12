/* ov006 row 0x021ec914: 124 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x78 -> native_data_0220d43c (image word 0x0220d43c)
 *   branch +0x10 -> +0x18
 *   branch +0x1a -> +0x20
 *   branch +0x26 -> +0x62
 *   branch +0x32 -> +0x56
 *   branch +0x3e -> +0x56
 *   branch +0x52 -> +0x56
 *   back edge +0x60 -> +0x2c
 *   branch +0x64 -> +0x6a
 *   branch +0x6c -> +0x72
 *   test +0x0e cmp r0, #0x0
 *   test +0x18 cmp r0, #0x40
 *   test +0x24 cmp r0, #0x0
 *   test +0x30 tst r0, r1
 *   test +0x3c cmp r1, r0
 *   test +0x50 cmp r0, #0x0
 *   test +0x5e cmp r7, r0
 *   test +0x62 cmp r4, #0x1
 *   test +0x6a cmp r4, #0x0
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ec914; the literal pool and
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

extern u8 native_data_0220d43c[];
extern void native_fn_021edcd0(void);
extern void native_fn_021edb7c(void);


asm u32 native_ov006_021ec914 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x8
    add r5, r0, #0x0
    ldr r0, [r5, #0]
    mov r4, #0x0
    str r4, [sp, #0x4]
    str r0, [sp]
    cmp r0, #0x0
    bne ov006_021ec914_L18
    add sp, #0x8
    mov r0, #0x5
    pop {r3, r4, r5, r6, r7, pc}
ov006_021ec914_L18:
    cmp r0, #0x40
    bls ov006_021ec914_L20
    mov r0, #0x40
    str r0, [sp]
ov006_021ec914_L20:
    ldr r0, [sp]
    mov r7, #0x0
    cmp r0, #0x0
    ble ov006_021ec914_L62
    add r6, r5, #0x0
    add r6, #0x8
ov006_021ec914_L2c:
    ldr r1, [r5, #0x54]
    mov r0, #0x1
    tst r0, r1
    beq ov006_021ec914_L56
    ldr r0, =native_data_0220d43c
    bl native_fn_021edcd0
    ldr r1, [r5, #0x4]
    cmp r1, r0
    bne ov006_021ec914_L56
    ldr r0, =native_data_0220d43c
    bl native_fn_021edcd0
    add r2, r0, #0x0
    ldr r1, =native_data_0220d43c
    add r0, r6, #0x0
    bl native_fn_021edb7c
    cmp r0, #0x0
    bne ov006_021ec914_L56
    add r4, r4, #0x1
ov006_021ec914_L56:
    ldr r0, [sp]
    add r7, r7, #0x1
    add r5, #0x54
    add r6, #0x54
    cmp r7, r0
    blt ov006_021ec914_L2c
ov006_021ec914_L62:
    cmp r4, #0x1
    ble ov006_021ec914_L6a
    mov r0, #0x4
    str r0, [sp, #0x4]
ov006_021ec914_L6a:
    cmp r4, #0x0
    bne ov006_021ec914_L72
    mov r0, #0x5
    str r0, [sp, #0x4]
ov006_021ec914_L72:
    ldr r0, [sp, #0x4]
    add sp, #0x8
    pop {r3, r4, r5, r6, r7, pc}
}
