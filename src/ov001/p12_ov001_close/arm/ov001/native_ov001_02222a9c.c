/* ov001 row 0x02222a9c: 236 bytes.
 *
 * What it does: 59 instructions; 8 call(s) to 0x021db8d0, 0x02218430, 0x02222b5c, +5 more; loops (back edge at +0x28); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: loop with 8 calls (59 instructions, 8 calls, 4 branches, 7 back edges, 0 literal slots).
 *
 *   branch +0x30 -> +0xc0
 *   branch +0x40 -> +0xc0
 *   branch +0x60 -> +0xc0
 *   branch +0x74 -> +0xb4
 *   branch +0x88 -> +0xb4
 *   back edge +0xbc -> +0x64
 *   back edge +0xd4 -> +0x24
 *   test +0x2c cmp r0, #0
 *   test +0x3c cmp r0, #0
 *   test +0x5c cmp r8, #0
 *   test +0x70 cmp r0, #0
 *   test +0x84 tst r0, #4
 *   test +0xa4 cmp r0, #3
 *   test +0xb8 cmp r7, r8
 *   test +0xd0 cmp r0, #3
 *   test +0xd8 cmp r9, #0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02222a9c; the literal pool and
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

extern void native_fn_021db8d0(void);
extern void native_fn_02218430(void);
extern void native_fn_0207b004(void);
extern void native_fn_022180e0(void);
extern void native_fn_022189cc(void);


asm u32 native_ov001_02222a9c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #204
    mov r9, #0
    ldr r6, [r0]
    ldr r10, [r0, #0x8]
    str r9, [sp]
    mov r11, #1
    add r5, sp, #4
    mov r4, #8
ov001_02222a9c_L24:
    mov r0, r10
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_02222a9c_Lc0
    add r0, r10, #512
    ldrsb r0, [r0, #62]
    cmp r0, #0
    bne ov001_02222a9c_Lc0
    mov r0, r10
    mov r1, r5
    mov r2, #200
    bl native_fn_02218430
    mov r8, r0
    mov r7, #0
    cmp r8, #0
    ble ov001_02222a9c_Lc0
ov001_02222a9c_L64:
    ldr r0, [r5, r7, lsl #2]
    mov r1, r4
    bl native_fn_0207b004
    cmp r0, #0
    beq ov001_02222a9c_Lb4
    ldr r0, [r5, r7, lsl #2]
    bl native_fn_022180e0
    ldrb r0, [r0, #0x4]
    tst r0, #4
    beq ov001_02222a9c_Lb4
    ldr r2, [r5, r7, lsl #2]
    mov r0, r10
    mov r1, r6
    mov r3, r11
    mov r9, r11
    bl native_fn_022189cc
    cmp r0, #3
    addlt sp, sp, #204
    movlt r0, #0
    ldmltia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov001_02222a9c_Lb4:
    add r7, r7, #1
    cmp r7, r8
    blt ov001_02222a9c_L64
ov001_02222a9c_Lc0:
    ldr r0, [sp]
    add r10, r10, #1088
    add r0, r0, #1
    str r0, [sp]
    cmp r0, #3
    blt ov001_02222a9c_L24
    cmp r9, #0
    movne r0, #1
    moveq r0, #0
    add sp, sp, #204
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
