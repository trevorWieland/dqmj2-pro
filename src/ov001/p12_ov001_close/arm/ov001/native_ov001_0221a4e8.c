/* ov001 row 0x0221a4e8: 292 bytes.
 *
 * What it does: 73 instructions; 12 call(s) to 0x021db8d0, 0x021e2b1c, 0x02218524, +9 more; loops (back edge at +0x20); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: loop with 12 calls (73 instructions, 12 calls, 7 branches, 11 back edges, 0 literal slots).
 *
 *   branch +0x28 -> +0x108
 *   branch +0x3c -> +0x108
 *   branch +0x44 -> +0x58
 *   branch +0x54 -> +0x108
 *   branch +0x68 -> +0x108
 *   branch +0x88 -> +0x108
 *   branch +0xa4 -> +0xfc
 *   branch +0xc0 -> +0xfc
 *   back edge +0x104 -> +0x94
 *   back edge +0x114 -> +0x1c
 *   test +0x24 cmp r0, #0
 *   test +0x38 cmp r0, r1
 *   test +0x40 cmp r11, #0
 *   test +0x50 cmp r0, #0
 *   test +0x64 cmp r0, #0
 *   test +0x80 cmp r9, #0
 *   test +0xa0 cmp r0, #0
 *   test +0xbc cmp r0, #1
 *   test +0xec cmp r4, r0
 *   test +0x100 cmp r8, r9
 *   test +0x10c cmp r7, #3
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221a4e8; the literal pool and
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
extern void native_fn_021e2b1c(void);
extern void native_fn_02218524(void);
extern void native_fn_02218430(void);
extern void native_fn_0207b004(void);
extern void native_fn_0207afec(void);
extern void ov001_record_field_1f2_021dbd30(void);
extern void native_fn_0207b244(void);


asm u32 native_ov001_0221a4e8 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #204
    ldr r1, [r0]
    ldr r11, [r0, #0x14]
    ldr r10, [r0, #0x4]
    str r1, [sp]
    mov r7, #0
ov001_0221a4e8_L1c:
    mov r0, r10
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_0221a4e8_L108
    ldr r0, [sp]
    ldrb r1, [r10, #0x31f]
    ldrb r0, [r0, #0x31f]
    cmp r0, r1
    beq ov001_0221a4e8_L108
    cmp r11, #0
    beq ov001_0221a4e8_L58
    ldrb r0, [r10, #0x31e]
    bl native_fn_021e2b1c
    cmp r0, #0
    bne ov001_0221a4e8_L108
ov001_0221a4e8_L58:
    mov r0, r10
    mov r1, #128
    bl native_fn_02218524
    cmp r0, #0
    beq ov001_0221a4e8_L108
    add r1, sp, #4
    mov r0, r10
    mov r2, #200
    bl native_fn_02218430
    mov r9, r0
    cmp r9, #0
    mov r8, #0
    ble ov001_0221a4e8_L108
    add r6, sp, #4
    mov r5, #8
ov001_0221a4e8_L94:
    ldr r0, [r6, r8, lsl #2]
    mov r1, r5
    bl native_fn_0207b004
    cmp r0, #0
    beq ov001_0221a4e8_Lfc
    ldr r0, [r6, r8, lsl #2]
    bl native_fn_0207afec
    ldrh r0, [r0, #8]
    mov r0, r0, lsl #20
    mov r0, r0, lsr #28
    cmp r0, #1
    bne ov001_0221a4e8_Lfc
    mov r0, r10
    bl ov001_record_field_1f2_021dbd30
    mov r4, r0
    mov r0, r10
    bl ov001_record_field_1f2_021dbd30
    ldr r2, [r10, #0x1e8]
    mov r1, r0
    ldr r0, [r6, r8, lsl #2]
    add r2, r2, #70
    bl native_fn_0207b244
    cmp r4, r0
    addlt sp, sp, #204
    movlt r0, #1
    ldmltia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov001_0221a4e8_Lfc:
    add r8, r8, #1
    cmp r8, r9
    blt ov001_0221a4e8_L94
ov001_0221a4e8_L108:
    add r7, r7, #1
    cmp r7, #3
    add r10, r10, #1088
    blt ov001_0221a4e8_L1c
    mov r0, #0
    add sp, sp, #204
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
