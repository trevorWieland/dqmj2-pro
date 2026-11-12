/* ov001 row 0x02219394: 744 bytes.
 *
 * What it does: 184 instructions; 23 call(s) to 0x021dbd30, 0x0207b244, 0x02044cdc, +20 more; loops (back edge at +0x20); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: block fill (184 instructions, 23 calls, 15 branches, 23 back edges, 2 literal slots).
 *
 *   pool +0x2e0 -> constant 0x0000270f (image word 0x0000270f)
 *   pool +0x2e4 -> constant 0x00002710 (image word 0x00002710)
 *   branch +0x5c -> +0xdc
 *   branch +0x70 -> +0xdc
 *   branch +0x88 -> +0xc8
 *   back edge +0xd4 -> +0x7c
 *   branch +0xd8 -> +0x13c
 *   branch +0xf4 -> +0x12c
 *   back edge +0x138 -> +0xe8
 *   branch +0x14c -> +0x16c
 *   branch +0x168 -> +0x228
 *   branch +0x180 -> +0x228
 *   branch +0x198 -> +0x214
 *   branch +0x1b8 -> +0x1e4
 *   branch +0x1e0 -> +0x208
 *   back edge +0x220 -> +0x18c
 *   branch +0x224 -> +0x2c4
 *   branch +0x240 -> +0x2b4
 *   branch +0x260 -> +0x28c
 *   branch +0x288 -> +0x2b4
 *   back edge +0x2c0 -> +0x234
 *   test +0x40 cmp r1, #0
 *   test +0x58 cmp r0, #2
 *   test +0x6c cmp r0, #4
 *   test +0x84 cmp r0, #0
 *   test +0xc0 cmp r10, r0
 *   test +0xcc cmp r11, #3
 *   test +0xf0 cmp r0, #0
 *   test +0x130 cmp r11, #3
 *   test +0x148 cmp r0, #2
 *   test +0x164 cmp r0, #1
 *   test +0x194 cmp r0, #0
 *   test +0x1b0 cmp r0, #1
 *   test +0x208 cmp r9, r0
 *   test +0x20c cmpgt r0, #0
 *   test +0x218 cmp r8, #3
 *   test +0x23c cmp r0, #0
 *   test +0x258 cmp r0, #1
 *   test +0x2b8 cmp r8, #3
 *   test +0x2c4 cmp r10, r9
 *   test +0x2cc cmplt r9, r0
 *   2 block transfer(s), 15 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02219394; the literal pool and
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

extern void ov001_record_field_1f2_021dbd30(void);
extern void native_fn_0207b244(void);
extern void native_fn_02044cdc(void);
extern void native_fn_02065d88(void);
extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_021f07dc(void);
extern void native_fn_0207afec(void);
extern void native_fn_021f0858(void);


asm u32 native_ov001_02219394 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #12
    ldr r4, [r0]
    ldr r10, =0x0000270f
    ldr r7, [r0, #0x8]
    ldr r5, [r0, #0xc]
    mov r0, r4
    add r9, r10, #1
    bl ov001_record_field_1f2_021dbd30
    ldr r2, [r4, #0x1e8]
    mov r1, r0
    mov r0, r5
    add r2, r2, #70
    bl native_fn_0207b244
    ldrb r1, [r4, #0x356]
    mov r6, r0
    cmp r1, #0
    moveq r0, #1
    streqb r0, [r4, #0x356]
    ldr r0, [r4, #0x1e8]
    ldrsh r0, [r0, #42]
    bl native_fn_02044cdc
    cmp r0, #2
    beq ov001_02219394_Ldc
    ldrb r0, [r4, #0x1fd]
    bl native_fn_02065d88
    ldrb r0, [r0, #0x2d]
    cmp r0, #4
    beq ov001_02219394_Ldc
    mov r8, r7
    mov r11, #0
ov001_02219394_L7c:
    mov r0, r8
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_02219394_Lc8
    mov r0, #0
    mov r2, #0
    str r0, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    mov r12, r2
    mov r0, r4
    mov r1, r8
    mov r3, r2
    str r12, [sp, #0x8]
    bl native_fn_021f07dc
    ldrb r1, [r4, #0x356]
    mul r0, r1, r0
    cmp r10, r0
    movgt r10, r0
ov001_02219394_Lc8:
    add r11, r11, #1
    cmp r11, #3
    add r8, r8, #1088
    blt ov001_02219394_L7c
    b ov001_02219394_L13c
ov001_02219394_Ldc:
    mov r10, #0
    mov r11, r10
    mov r8, r7
ov001_02219394_Le8:
    mov r0, r8
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_02219394_L12c
    mov r0, #0
    mov r2, #0
    str r0, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    mov r12, r2
    mov r0, r4
    mov r1, r8
    mov r3, r2
    str r12, [sp, #0x8]
    bl native_fn_021f07dc
    ldrb r1, [r4, #0x356]
    mla r10, r1, r0, r10
ov001_02219394_L12c:
    add r11, r11, #1
    cmp r11, #3
    add r8, r8, #1088
    blt ov001_02219394_Le8
ov001_02219394_L13c:
    ldr r0, [r4, #0x1e8]
    ldrsh r0, [r0, #42]
    bl native_fn_02044cdc
    cmp r0, #2
    bne ov001_02219394_L16c
    mov r0, r5
    bl native_fn_0207afec
    ldrh r0, [r0, #8]
    mov r0, r0, lsl #28
    mov r0, r0, lsr #28
    cmp r0, #1
    beq ov001_02219394_L228
ov001_02219394_L16c:
    mov r0, r5
    bl native_fn_0207afec
    ldrh r0, [r0, #8]
    mov r0, r0, lsl #16
    movs r0, r0, lsr #28
    bne ov001_02219394_L228
    mov r8, #0
    mov r11, #1
ov001_02219394_L18c:
    mov r0, r7
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_02219394_L214
    mov r0, r5
    bl native_fn_0207afec
    ldrh r0, [r0, #8]
    mov r0, r0, lsl #28
    mov r0, r0, lsr #28
    cmp r0, #1
    mov r0, #0
    bne ov001_02219394_L1e4
    stmia sp, {r0, r11}
    mov r3, #0
    mov r0, r4
    mov r1, r7
    mov r2, r5
    str r3, [sp, #0x8]
    bl native_fn_021f07dc
    ldrb r1, [r4, #0x356]
    mul r0, r1, r0
    b ov001_02219394_L208
ov001_02219394_L1e4:
    str r0, [sp]
    str r0, [sp, #0x4]
    mov r3, #1
    str r3, [sp, #0x8]
    mov r0, r4
    mov r1, r7
    mov r2, r6
    mov r3, r5
    bl native_fn_021f0858
ov001_02219394_L208:
    cmp r9, r0
    cmpgt r0, #0
    movgt r9, r0
ov001_02219394_L214:
    add r8, r8, #1
    cmp r8, #3
    add r7, r7, #1088
    blt ov001_02219394_L18c
    b ov001_02219394_L2c4
ov001_02219394_L228:
    mov r9, #0
    mov r8, r9
    mov r11, #1
ov001_02219394_L234:
    mov r0, r7
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_02219394_L2b4
    mov r0, r5
    bl native_fn_0207afec
    ldrh r0, [r0, #8]
    mov r0, r0, lsl #28
    mov r0, r0, lsr #28
    cmp r0, #1
    mov r0, #0
    bne ov001_02219394_L28c
    stmia sp, {r0, r11}
    mov r3, #0
    mov r0, r4
    mov r1, r7
    mov r2, r5
    str r3, [sp, #0x8]
    bl native_fn_021f07dc
    ldrb r1, [r4, #0x356]
    mla r9, r1, r0, r9
    b ov001_02219394_L2b4
ov001_02219394_L28c:
    str r0, [sp]
    str r0, [sp, #0x4]
    mov r3, #1
    str r3, [sp, #0x8]
    mov r0, r4
    mov r1, r7
    mov r2, r6
    mov r3, r5
    bl native_fn_021f0858
    add r9, r9, r0
ov001_02219394_L2b4:
    add r8, r8, #1
    cmp r8, #3
    add r7, r7, #1088
    blt ov001_02219394_L234
ov001_02219394_L2c4:
    cmp r10, r9
    ldrlt r0, =0x00002710
    cmplt r9, r0
    movlt r0, #1
    movge r0, #0
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
