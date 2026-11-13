/* ov001 row 0x02224e40: 144 bytes.
 *
 * What it does: 36 instructions; 7 call(s) to 0x02008e0c, 0x021dbd30, 0x021dbcf0, +4 more; loops (back edge at +0x18); returns through pop {r4, r5, r6, r7, r8, r9, pc}
 *
 * Decoded shape: loop with 7 calls (36 instructions, 7 calls, 1 branch, 6 back edges, 0 literal slots).
 *
 *   branch +0x30 -> +0x50
 *   back edge +0x5c -> +0x28
 *   branch +0x70 -> +0x84
 *   test +0x2c cmp r0, #0
 *   test +0x48 cmp r6, r0
 *   test +0x54 cmp r8, #3
 *   test +0x6c cmp r5, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02224e40; the literal pool and
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
extern void ov001_record_field_1f2_021dbd30(void);
extern void native_fn_021dbcf0(void);
extern void ov001_count_candidates_02223f20(void);


asm u32 native_ov001_02224e40 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, lr}
    sub sp, sp, #12
    mov r9, r1
    add r1, sp, #0
    mov r2, #12
    mov r4, r0
    bl native_fn_02008e0c
    mov r8, #0
    mov r5, r8
    add r7, sp, #0
ov001_02224e40_L28:
    ldr r0, [r7, r8, lsl #2]
    cmp r0, #0
    beq ov001_02224e40_L50
    mov r0, r9
    bl ov001_record_field_1f2_021dbd30
    mov r6, r0
    mov r0, r9
    bl native_fn_021dbcf0
    cmp r6, r0
    streq r5, [r7, r8, lsl #2]
ov001_02224e40_L50:
    add r8, r8, #1
    cmp r8, #3
    add r9, r9, #1088
    blt ov001_02224e40_L28
    add r0, sp, #0
    bl ov001_count_candidates_02223f20
    mov r5, r0
    cmp r5, #0
    ble ov001_02224e40_L84
    add r0, sp, #0
    mov r1, r4
    mov r2, #12
    bl native_fn_02008e0c
ov001_02224e40_L84:
    mov r0, r5
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, r8, r9, pc}
}
