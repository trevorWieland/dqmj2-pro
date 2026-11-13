/* ov001 row 0x02222bb0: 248 bytes.
 *
 * What it does: 62 instructions; 10 call(s) to 0x02218430, 0x02222c78, 0x0207b004, +7 more; loops (back edge at +0x28); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: loop with 10 calls (62 instructions, 10 calls, 3 branches, 8 back edges, 0 literal slots).
 *
 *   branch +0x38 -> +0xc8
 *   branch +0x54 -> +0xb8
 *   branch +0x70 -> +0xb8
 *   branch +0x88 -> +0xa8
 *   back edge +0xb4 -> +0x7c
 *   back edge +0xc4 -> +0x44
 *   branch +0xcc -> +0xec
 *   test +0x30 cmp r0, #0
 *   test +0x50 cmp r0, #0
 *   test +0x6c cmp r0, #1
 *   test +0x84 cmp r0, #0
 *   test +0xac cmp r7, #3
 *   test +0xc0 cmp r6, r0
 *   test +0xc8 cmp r9, #0
 *   test +0xdc cmp r0, #5
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02222bb0; the literal pool and
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

extern void native_fn_02218430(void);
extern void native_fn_0207b004(void);
extern void native_fn_0207afec(void);
extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_022189cc(void);
extern void native_fn_02026144(void);


asm u32 native_ov001_02222bb0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #208
    ldr r5, [r0]
    ldr r0, [r0, #0x8]
    mov r8, #0
    str r0, [sp, #0x4]
    add r1, sp, #8
    mov r0, r5
    mov r2, #200
    mov r9, r8
    bl native_fn_02218430
    str r0, [sp]
    cmp r0, #0
    mov r6, r8
    ble ov001_02222bb0_Lc8
    add r4, sp, #8
    mov r11, #1
ov001_02222bb0_L44:
    ldr r0, [r4, r6, lsl #2]
    mov r1, #128
    bl native_fn_0207b004
    cmp r0, #0
    beq ov001_02222bb0_Lb8
    ldr r0, [r4, r6, lsl #2]
    bl native_fn_0207afec
    ldrh r0, [r0, #8]
    mov r0, r0, lsl #24
    mov r0, r0, lsr #28
    cmp r0, #1
    bne ov001_02222bb0_Lb8
    ldr r10, [sp, #0x4]
    mov r7, #0
ov001_02222bb0_L7c:
    mov r0, r10
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_02222bb0_La8
    ldr r2, [r4, r6, lsl #2]
    mov r0, r5
    mov r1, r10
    mov r3, r11
    bl native_fn_022189cc
    add r8, r8, r0
    add r9, r9, #1
ov001_02222bb0_La8:
    add r7, r7, #1
    cmp r7, #3
    add r10, r10, #1088
    blt ov001_02222bb0_L7c
ov001_02222bb0_Lb8:
    ldr r0, [sp]
    add r6, r6, #1
    cmp r6, r0
    blt ov001_02222bb0_L44
ov001_02222bb0_Lc8:
    cmp r9, #0
    ble ov001_02222bb0_Lec
    mov r0, r8
    mov r1, r9
    bl native_fn_02026144
    cmp r0, #5
    addge sp, sp, #208
    movge r0, #1
    ldmgeia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov001_02222bb0_Lec:
    mov r0, #0
    add sp, sp, #208
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
