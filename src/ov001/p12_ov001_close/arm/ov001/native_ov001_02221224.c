/* ov001 row 0x02221224: 296 bytes.
 *
 * What it does: 74 instructions; 10 call(s) to 0x021db8d0, 0x0207afec, 0x02218430, +7 more; loops (back edge at +0x30); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: loop with 10 calls (74 instructions, 10 calls, 7 branches, 9 back edges, 0 literal slots).
 *
 *   branch +0x38 -> +0xe0
 *   branch +0x48 -> +0xe0
 *   branch +0x68 -> +0xe0
 *   branch +0x88 -> +0xe0
 *   branch +0x9c -> +0xd4
 *   branch +0xb0 -> +0xd4
 *   branch +0xd0 -> +0xe0
 *   back edge +0xdc -> +0x8c
 *   back edge +0xf4 -> +0x2c
 *   branch +0xfc -> +0x11c
 *   test +0x34 cmp r0, #0
 *   test +0x44 cmp r0, #0
 *   test +0x64 cmp r0, #1
 *   test +0x84 cmp r9, #0
 *   test +0x98 cmp r0, #0
 *   test +0xac tst r0, #4
 *   test +0xd8 cmp r7, r9
 *   test +0xf0 cmp r0, #3
 *   test +0xf8 cmp r8, #0
 *   test +0x10c cmp r0, #1
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02221224; the literal pool and
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


asm u32 native_ov001_02221224 (register u32 a0)
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
    add r5, sp, #8
    mov r4, #33554432
ov001_02221224_L2c:
    mov r0, r10
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_02221224_Le0
    add r0, r10, #512
    ldrsb r0, [r0, #85]
    cmp r0, #0
    bne ov001_02221224_Le0
    mov r0, r6
    bl native_fn_0207afec
    ldrb r0, [r0, #0x1f]
    ldr r1, [r10, #0x1e8]
    add r0, r1, r0
    ldrb r0, [r0, #0x86]
    cmp r0, #1
    bhi ov001_02221224_Le0
    mov r0, r10
    mov r1, r5
    mov r2, #200
    bl native_fn_02218430
    mov r9, r0
    mov r7, #0
    cmp r9, #0
    ble ov001_02221224_Le0
ov001_02221224_L8c:
    ldr r0, [r5, r7, lsl #2]
    mov r1, r4
    bl native_fn_0207b004
    cmp r0, #0
    beq ov001_02221224_Ld4
    ldr r0, [r5, r7, lsl #2]
    bl native_fn_022180e0
    ldrb r0, [r0, #0x4]
    tst r0, #4
    beq ov001_02221224_Ld4
    ldr r0, [sp, #0x4]
    mov r1, r10
    mov r2, r6
    mov r3, #1
    bl native_fn_022189cc
    add r11, r11, r0
    add r8, r8, #1
    b ov001_02221224_Le0
ov001_02221224_Ld4:
    add r7, r7, #1
    cmp r7, r9
    blt ov001_02221224_L8c
ov001_02221224_Le0:
    ldr r0, [sp]
    add r10, r10, #1088
    add r0, r0, #1
    str r0, [sp]
    cmp r0, #3
    blt ov001_02221224_L2c
    cmp r8, #0
    beq ov001_02221224_L11c
    mov r0, r11
    mov r1, r8
    bl native_fn_02026144
    cmp r0, #1
    addle sp, sp, #208
    movle r0, #1
    ldmleia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov001_02221224_L11c:
    mov r0, #0
    add sp, sp, #208
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
