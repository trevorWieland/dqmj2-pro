/* ov001 row 0x02220fdc: 336 bytes.
 *
 * What it does: 84 instructions; 12 call(s) to 0x021db8d0, 0x0207afec, 0x02218430, +9 more; loops (back edge at +0x28); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: loop with 12 calls (84 instructions, 12 calls, 9 branches, 11 back edges, 0 literal slots).
 *
 *   branch +0x30 -> +0x108
 *   branch +0x40 -> +0x108
 *   branch +0x60 -> +0x108
 *   branch +0x80 -> +0x108
 *   branch +0x9c -> +0xfc
 *   branch +0xb0 -> +0xdc
 *   branch +0xc4 -> +0xdc
 *   branch +0xd8 -> +0xfc
 *   branch +0xf8 -> +0x108
 *   back edge +0x104 -> +0x8c
 *   back edge +0x11c -> +0x24
 *   branch +0x124 -> +0x144
 *   test +0x2c cmp r0, #0
 *   test +0x3c cmp r0, #0
 *   test +0x5c cmp r0, #1
 *   test +0x78 cmp r9, #0
 *   test +0x98 cmp r0, #0
 *   test +0xac tst r0, #4
 *   test +0xc0 tst r0, #1
 *   test +0xd4 tst r0, #8
 *   test +0x100 cmp r7, r9
 *   test +0x118 cmp r0, #3
 *   test +0x120 cmp r8, #0
 *   test +0x134 cmp r0, #1
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02220fdc; the literal pool and
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
extern void native_fn_0207afec(void);
extern void native_fn_02218430(void);
extern void native_fn_0207b004(void);
extern void native_fn_022180e0(void);
extern void native_fn_022189cc(void);
extern void native_fn_02026144(void);


asm u32 native_ov001_02220fdc (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #208
    ldr r1, [r0]
    mov r8, #0
    ldr r6, [r0, #0xc]
    ldr r10, [r0, #0x8]
    str r1, [sp, #0x4]
    mov r11, r8
    str r8, [sp]
ov001_02220fdc_L24:
    mov r0, r10
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_02220fdc_L108
    add r0, r10, #512
    ldrsb r0, [r0, #84]
    cmp r0, #0
    bne ov001_02220fdc_L108
    mov r0, r6
    bl native_fn_0207afec
    ldrb r0, [r0, #0x1f]
    ldr r1, [r10, #0x1e8]
    add r0, r1, r0
    ldrb r0, [r0, #0x86]
    cmp r0, #1
    bhi ov001_02220fdc_L108
    add r1, sp, #8
    mov r0, r10
    mov r2, #200
    bl native_fn_02218430
    mov r9, r0
    cmp r9, #0
    mov r7, #0
    ble ov001_02220fdc_L108
    add r5, sp, #8
    mov r4, #67108864
ov001_02220fdc_L8c:
    ldr r0, [r5, r7, lsl #2]
    mov r1, r4
    bl native_fn_0207b004
    cmp r0, #0
    beq ov001_02220fdc_Lfc
    ldr r0, [r5, r7, lsl #2]
    bl native_fn_022180e0
    ldrb r0, [r0, #0x4]
    tst r0, #4
    bne ov001_02220fdc_Ldc
    ldr r0, [r5, r7, lsl #2]
    bl native_fn_022180e0
    ldrb r0, [r0, #0x4]
    tst r0, #1
    bne ov001_02220fdc_Ldc
    ldr r0, [r5, r7, lsl #2]
    bl native_fn_022180e0
    ldrb r0, [r0, #0x4]
    tst r0, #8
    beq ov001_02220fdc_Lfc
ov001_02220fdc_Ldc:
    ldr r0, [sp, #0x4]
    mov r1, r10
    mov r2, r6
    mov r3, #1
    bl native_fn_022189cc
    add r11, r11, r0
    add r8, r8, #1
    b ov001_02220fdc_L108
ov001_02220fdc_Lfc:
    add r7, r7, #1
    cmp r7, r9
    blt ov001_02220fdc_L8c
ov001_02220fdc_L108:
    ldr r0, [sp]
    add r10, r10, #1088
    add r0, r0, #1
    str r0, [sp]
    cmp r0, #3
    blt ov001_02220fdc_L24
    cmp r8, #0
    beq ov001_02220fdc_L144
    mov r0, r11
    mov r1, r8
    bl native_fn_02026144
    cmp r0, #1
    addle sp, sp, #208
    movle r0, #1
    ldmleia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov001_02220fdc_L144:
    mov r0, #0
    add sp, sp, #208
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
