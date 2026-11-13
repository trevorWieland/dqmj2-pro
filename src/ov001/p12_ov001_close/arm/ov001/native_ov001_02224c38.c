/* ov001 row 0x02224c38: 296 bytes.
 *
 * What it does: 74 instructions; 14 call(s) to 0x02008e0c, 0x021dbcf0, 0x021dbd30, +11 more; loops (back edge at +0x1c); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: loop with 14 calls (74 instructions, 14 calls, 4 branches, 13 back edges, 0 literal slots).
 *
 *   branch +0x3c -> +0x7c
 *   branch +0x50 -> +0x74
 *   back edge +0x88 -> +0x34
 *   branch +0xa8 -> +0xe8
 *   branch +0xbc -> +0xe0
 *   back edge +0xf4 -> +0xa0
 *   branch +0x108 -> +0x11c
 *   test +0x38 cmp r0, #0
 *   test +0x48 cmp r0, #0
 *   test +0x74 cmp r0, r8
 *   test +0x80 cmp r7, #3
 *   test +0xa4 cmp r0, #0
 *   test +0xb4 cmp r0, #0
 *   test +0xe0 cmp r0, r8
 *   test +0xec cmp r9, #3
 *   test +0x104 cmp r4, #0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02224c38; the literal pool and
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

extern void native_fn_02008e0c(void);
extern void native_fn_021dbcf0(void);
extern void ov001_record_field_1f2_021dbd30(void);
extern void native_fn_02026144(void);
extern void ov001_count_candidates_02223f20(void);


asm u32 native_ov001_02224c38 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #16
    mov r10, r1
    add r1, sp, #4
    mov r2, #12
    str r0, [sp]
    mov r8, #100
    bl native_fn_02008e0c
    mov r9, r10
    mov r7, #0
    mov r11, r8
    add r6, sp, #4
    mov r4, r8
ov001_02224c38_L34:
    ldr r0, [r6, r7, lsl #2]
    cmp r0, #0
    beq ov001_02224c38_L7c
    mov r0, r9
    bl native_fn_021dbcf0
    cmp r0, #0
    moveq r0, r11
    beq ov001_02224c38_L74
    mov r0, r9
    bl ov001_record_field_1f2_021dbd30
    mov r5, r0
    mov r0, r9
    bl native_fn_021dbcf0
    mov r1, r0
    mul r0, r5, r4
    bl native_fn_02026144
ov001_02224c38_L74:
    cmp r0, r8
    movlt r8, r0
ov001_02224c38_L7c:
    add r7, r7, #1
    cmp r7, #3
    add r9, r9, #1088
    blt ov001_02224c38_L34
    mov r9, #0
    mov r11, #100
    mov r5, r9
    add r7, sp, #4
    mov r4, r11
ov001_02224c38_La0:
    ldr r0, [r7, r9, lsl #2]
    cmp r0, #0
    beq ov001_02224c38_Le8
    mov r0, r10
    bl native_fn_021dbcf0
    cmp r0, #0
    moveq r0, r11
    beq ov001_02224c38_Le0
    mov r0, r10
    bl ov001_record_field_1f2_021dbd30
    mov r6, r0
    mov r0, r10
    bl native_fn_021dbcf0
    mov r1, r0
    mul r0, r6, r4
    bl native_fn_02026144
ov001_02224c38_Le0:
    cmp r0, r8
    strgt r5, [r7, r9, lsl #2]
ov001_02224c38_Le8:
    add r9, r9, #1
    cmp r9, #3
    add r10, r10, #1088
    blt ov001_02224c38_La0
    add r0, sp, #4
    bl ov001_count_candidates_02223f20
    mov r4, r0
    cmp r4, #0
    ble ov001_02224c38_L11c
    ldr r1, [sp]
    add r0, sp, #4
    mov r2, #12
    bl native_fn_02008e0c
ov001_02224c38_L11c:
    mov r0, r4
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
