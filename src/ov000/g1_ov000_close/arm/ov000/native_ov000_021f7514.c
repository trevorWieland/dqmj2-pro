/* ov000 row 0x021f7514: 460 bytes.
 *
 * What it does: 115 instructions; 12 call(s) to 0x02061c1c, 0x02061c1c, 0x02061c1c, +9 more; loops (back edge at +0x28); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: block fill.
 *
 *   branch +0x88 -> +0x1bc
 *   branch +0xa8 -> +0xc0
 *   branch +0xb0 -> +0xc8
 *   branch +0xbc -> +0xcc
 *   branch +0xc4 -> +0xcc
 *   back edge +0x1b8 -> +0x94
 *   test +0x80 cmp r7, #0
 *   test +0xac cmp r4, #1
 *   test +0xb4 cmp r4, #2
 *   test +0x1b0 cmp r7, r0, asr #24
 *   2 block transfer(s), 17 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f7514; the literal pool and
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

extern void native_fn_02061c1c(void);
extern void native_fn_02062aa0(void);
extern void native_fn_02062a50(void);
extern void native_fn_02044cdc(void);
extern void native_fn_021f7f7c(void);


asm u32 native_ov000_021f7514 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #12
    mov r0, #2
    str r0, [sp]
    mov r0, #0
    str r0, [sp, #0x4]
    mov r1, #7
    mov r2, #1
    mov r3, #11
    str r0, [sp, #0x8]
    bl native_fn_02061c1c
    mov r0, #2
    str r0, [sp]
    mov r4, #0
    str r4, [sp, #0x4]
    mov r0, #13
    mov r1, #23
    mov r2, #1
    mov r3, #8
    str r4, [sp, #0x8]
    bl native_fn_02061c1c
    mov r0, #2
    stmia sp, {r0, r4}
    mov r0, #14
    mov r1, #7
    mov r2, #4
    mov r3, #23
    str r4, [sp, #0x8]
    bl native_fn_02061c1c
    mov r8, #8
    bl native_fn_02062aa0
    mov r7, r0
    cmp r7, #0
    mov r5, r4
    ble ov000_021f7514_L1bc
    mov r6, #2
    mov r11, r4
ov000_021f7514_L94:
    mov r0, r5
    bl native_fn_02062a50
    ldrsh r0, [r0, #24]
    bl native_fn_02044cdc
    movs r4, r0
    beq ov000_021f7514_Lc0
    cmp r4, #1
    beq ov000_021f7514_Lc8
    cmp r4, #2
    moveq r10, #5
    b ov000_021f7514_Lcc
ov000_021f7514_Lc0:
    mov r10, #0
    b ov000_021f7514_Lcc
ov000_021f7514_Lc8:
    mov r10, #2
ov000_021f7514_Lcc:
    add r0, r8, r10
    and r9, r0, #255
    add r0, r5, #1
    stmia sp, {r6, r11}
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    mov r1, #7
    mov r2, r9
    mov r3, #11
    str r11, [sp, #0x8]
    bl native_fn_02061c1c
    mov r0, #2
    str r0, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    mov r0, #0
    str r0, [sp, #0x8]
    add r0, r5, #4
    add r9, r9, #2
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    mov r1, #7
    and r2, r9, #255
    mov r3, #5
    bl native_fn_02061c1c
    mov r0, #2
    str r0, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    mov r0, #0
    str r0, [sp, #0x8]
    add r0, r5, #7
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    mov r1, #14
    and r2, r9, #255
    mov r3, #7
    bl native_fn_02061c1c
    mov r0, #2
    str r0, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    mov r0, #0
    str r0, [sp, #0x8]
    add r0, r5, #10
    mov r0, r0, lsl #24
    and r2, r9, #255
    mov r0, r0, asr #24
    mov r1, #23
    mov r3, #7
    bl native_fn_02061c1c
    add r0, r4, #1
    add r0, r0, r0, lsl #2
    add r0, r8, r0
    and r8, r0, #255
    add r0, r5, #1
    mov r0, r0, lsl #24
    cmp r7, r0, asr #24
    mov r5, r0, asr #24
    bgt ov000_021f7514_L94
ov000_021f7514_L1bc:
    mov r0, #1
    bl native_fn_021f7f7c
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
