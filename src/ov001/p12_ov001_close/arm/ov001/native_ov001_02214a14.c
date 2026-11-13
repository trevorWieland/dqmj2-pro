/* ov001 row 0x02214a14: 344 bytes.
 *
 * What it does: 85 instructions; 16 call(s) to 0x021db438, 0x021db530, 0x0203d294, +13 more; loops (back edge at +0x28); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 16 calls (85 instructions, 16 calls, 4 branches, 16 back edges, 1 literal slot).
 *
 *   pool +0x154 -> constant 0x02242b94 (image word 0x02242b94)
 *   back edge +0x58 -> +0x3c
 *   branch +0x64 -> +0x140
 *   branch +0x80 -> +0x130
 *   branch +0x88 -> +0x130
 *   branch +0xc8 -> +0xd8
 *   back edge +0x13c -> +0x74
 *   test +0x18 cmp r0, #1
 *   test +0x54 cmp r0, #0
 *   test +0x5c cmp r8, #0
 *   test +0x7c cmp r0, #0
 *   test +0x84 cmp r6, r9
 *   test +0xc4 cmp r0, #1
 *   test +0x138 cmp r6, r8
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02214a14; the literal pool and
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

extern void ov001_side_slot_record_021db438(void);
extern void ov001_mode_byte_021db530(void);
extern void native_fn_0203d294(void);
extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_021f07dc(void);
extern void native_fn_021db578(void);
extern void native_fn_021dbd24(void);
extern void native_fn_021dc59c(void);
extern void native_fn_021f0eb4(void);
extern void native_fn_021d9494(void);
extern void native_fn_022024d4(void);
extern void native_fn_021ee78c(void);
extern void native_fn_021f949c(void);


asm u32 native_ov001_02214a14 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #12
    ldr r0, =0x02242b94
    mov r1, #0
    ldr r0, [r0, #0x8]
    ldrb r0, [r0, #0x31e]
    cmp r0, #1
    moveq r4, #0
    movne r4, #1
    mov r0, r4
    bl ov001_side_slot_record_021db438
    mov r10, r0
    mov r0, r4
    bl ov001_mode_byte_021db530
    mov r8, r0
ov001_02214a14_L3c:
    mov r0, r8
    bl native_fn_0203d294
    mov r9, r0
    add r0, r9, r9, lsl #4
    add r0, r10, r0, lsl #6
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_02214a14_L3c
    cmp r8, #0
    mov r6, #0
    ble ov001_02214a14_L140
    ldr r4, =0x02242b94
    mov r5, #1
    mov r11, r6
ov001_02214a14_L74:
    mov r0, r10
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_02214a14_L130
    cmp r6, r9
    bne ov001_02214a14_L130
    ldr r0, [r4, #0x8]
    mov r2, #0
    strb r5, [r0, #0x356]
    mov r0, #0
    str r0, [sp]
    str r0, [sp, #0x4]
    str r0, [sp, #0x8]
    ldr r0, [r4, #0x8]
    mov r1, r10
    mov r3, r2
    bl native_fn_021f07dc
    mov r7, r0
    mov r0, r11
    bl native_fn_021db578
    cmp r0, #1
    bne ov001_02214a14_Ld8
    mov r0, r10
    bl native_fn_021dbd24
    sub r7, r0, #1
ov001_02214a14_Ld8:
    mov r0, r10
    mov r1, #0
    bl native_fn_021dc59c
    mov r0, r10
    mov r1, r7
    mov r2, #0
    bl native_fn_021f0eb4
    mov r0, r10
    mov r1, #4
    mov r2, #1
    bl native_fn_021d9494
    ldrb r0, [r10, #0x31e]
    ldrb r1, [r10, #0x31f]
    mov r2, r7
    bl native_fn_022024d4
    mov r0, #0
    str r0, [sp]
    mov r1, r7
    mov r0, r10
    mov r2, #0
    mov r3, #1
    bl native_fn_021ee78c
ov001_02214a14_L130:
    add r10, r10, #1088
    add r6, r6, #1
    cmp r6, r8
    blt ov001_02214a14_L74
ov001_02214a14_L140:
    mov r0, #226
    mov r1, #1
    bl native_fn_021f949c
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
