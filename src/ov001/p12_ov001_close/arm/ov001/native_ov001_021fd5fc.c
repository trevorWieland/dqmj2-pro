/* ov001 row 0x021fd5fc: 456 bytes.
 *
 * What it does: 113 instructions; 9 call(s) to 0x02202360, 0x02048f6c, 0x02045dc4, +6 more; loops (back edge at +0x2c); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill (113 instructions, 9 calls, 2 branches, 4 back edges, 1 literal slot).
 *
 *   pool +0x1c4 -> constant 0x02239c10 (image word 0x02239c10)
 *   branch +0xbc -> +0x12c
 *   back edge +0x128 -> +0xd4
 *   branch +0x13c -> +0x1a0
 *   test +0xb8 cmp r9, #0
 *   test +0x120 cmp r9, r0, asr #24
 *   test +0x134 cmp r0, #1
 *   test +0x138 cmpne r0, #4
 *   test +0x140 cmp r0, #1
 *   2 block transfer(s), 19 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021fd5fc; the literal pool and
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

extern void ov001_table_f0_entry_02202360(void);
extern void native_fn_02048f6c(void);
extern void native_fn_02045dc4(void);
extern void native_fn_021fe4ac(void);
extern void native_fn_02049604(void);
extern void native_fn_02204310(void);


asm u32 native_ov001_021fd5fc (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #28
    ldr r4, =0x02239c10
    mov r10, r0
    ldrsb r0, [r4, #12]
    mov r11, r3
    str r1, [sp, #0x14]
    str r2, [sp, #0x18]
    bl ov001_table_f0_entry_02202360
    mov r8, r0
    mov r0, #1
    bl native_fn_02048f6c
    str r11, [sp]
    mov r1, r0
    ldrb r3, [sp, #0x40]
    ldr r2, [sp, #0x14]
    mov r0, #1
    str r3, [sp, #0x4]
    ldr r3, [sp, #0x18]
    bl native_fn_02045dc4
    ldr r0, [sp, #0x18]
    ldrb r2, [sp, #0x40]
    stmia sp, {r0, r11}
    str r2, [sp, #0x8]
    mov r1, #0
    str r1, [sp, #0xc]
    str r1, [sp, #0x10]
    ldr r3, [sp, #0x14]
    mov r0, #8
    mov r1, r10
    mov r2, #30
    bl native_fn_021fe4ac
    ldr r0, [sp, #0x18]
    ldrb r2, [sp, #0x44]
    add r0, r0, #1
    and r7, r0, #255
    ldrb r1, [sp, #0x48]
    strh r2, [r8, #12]
    mov r0, #0
    strh r1, [r8, #14]
    str r0, [r8, #0x4]
    mov r0, r8
    mov r1, #1
    bl native_fn_02049604
    ldrb r9, [sp, #0x44]
    mov r6, #0
    cmp r9, #0
    ble ov001_021fd5fc_L12c
    ldr r0, [sp, #0x14]
    sub r1, r11, #2
    add r0, r0, #1
    and r5, r1, #255
    and r4, r0, #255
ov001_021fd5fc_Ld4:
    str r7, [sp]
    str r5, [sp, #0x4]
    mov r0, #2
    str r0, [sp, #0x8]
    mov r0, #0
    str r0, [sp, #0xc]
    mov r0, #1
    str r0, [sp, #0x10]
    add r0, r6, #9
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    mov r1, r10
    mov r2, #22
    mov r3, r4
    bl native_fn_021fe4ac
    add r0, r7, #2
    and r7, r0, #255
    add r0, r6, #1
    mov r0, r0, lsl #24
    cmp r9, r0, asr #24
    mov r6, r0, asr #24
    bgt ov001_021fd5fc_Ld4
ov001_021fd5fc_L12c:
    ldr r0, =0x02239c10
    ldrsb r0, [r0, #12]
    cmp r0, #1
    cmpne r0, #4
    bne ov001_021fd5fc_L1a0
    cmp r0, #1
    moveq r0, #11
    movne r0, #8
    and r3, r0, #255
    ldrb r1, [sp, #0x40]
    ldr r0, [sp, #0x18]
    sub r2, r11, r3
    add r0, r0, r1
    sub r0, r0, #1
    and r0, r0, #255
    stmia sp, {r0, r3}
    ldr r0, [sp, #0x14]
    mov r1, #2
    add r2, r0, r2
    str r1, [sp, #0x8]
    mov r0, #0
    str r0, [sp, #0xc]
    mov r4, #1
    and r3, r2, #255
    mov r1, r10
    mov r0, #27
    mov r2, #31
    str r4, [sp, #0x10]
    bl native_fn_021fe4ac
ov001_021fd5fc_L1a0:
    mov r1, #244
    mov r4, #104
    mov r3, r1
    add r0, r8, #168
    mov r2, #16
    str r4, [sp]
    bl native_fn_02204310
    add sp, sp, #28
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
