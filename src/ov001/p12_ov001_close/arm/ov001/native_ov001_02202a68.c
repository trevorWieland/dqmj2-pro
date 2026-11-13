/* ov001 row 0x02202a68: 200 bytes.
 *
 * What it does: 50 instructions; 4 call(s) to 0x021db438, 0x021db8d0, 0x021dc1c0, +1 more; loops (back edge at +0x34); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: loop with 4 calls (50 instructions, 4 calls, 8 branches, 5 back edges, 0 literal slots).
 *
 *   branch +0x28 -> +0x7c
 *   branch +0x44 -> +0x6c
 *   branch +0x4c -> +0x60
 *   branch +0x5c -> +0x6c
 *   branch +0x68 -> +0x7c
 *   back edge +0x78 -> +0x2c
 *   branch +0x80 -> +0xbc
 *   branch +0x8c -> +0xbc
 *   back edge +0xb4 -> +0x00
 *   test +0x40 cmp r0, #0
 *   test +0x48 cmp r7, #0
 *   test +0x58 cmp r0, #0
 *   test +0x7c cmp r6, #0
 *   test +0x88 cmp r0, #0
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02202a68; the literal pool and
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
extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_021dc1c0(void);


asm u32 native_ov001_02202a68 (register u32 a0)
{
ov001_02202a68_L0:
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #12
    mov r9, r2
    str r9, [sp, #0x8]
    movs r5, r9
    mov r11, r0
    mov r10, r1
    mov r8, r3
    ldr r7, [sp, #0x34]
    mov r6, #0
    bmi ov001_02202a68_L7c
ov001_02202a68_L2c:
    mov r0, r10
    mov r1, r5
    bl ov001_side_slot_record_021db438
    mov r4, r0
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_02202a68_L6c
    cmp r7, #0
    beq ov001_02202a68_L60
    mov r0, r4
    bl native_fn_021dc1c0
    cmp r0, #0
    beq ov001_02202a68_L6c
ov001_02202a68_L60:
    str r5, [sp, #0x8]
    mov r6, #1
    b ov001_02202a68_L7c
ov001_02202a68_L6c:
    sub r0, r5, #1
    mov r0, r0, lsl #24
    movs r5, r0, asr #24
    bpl ov001_02202a68_L2c
ov001_02202a68_L7c:
    cmp r6, #0
    bne ov001_02202a68_Lbc
    ldrsb r0, [sp, #48]
    cmp r0, #0
    beq ov001_02202a68_Lbc
    sub r0, r8, #1
    mov r2, r0, lsl #24
    mov r0, #0
    str r0, [sp]
    mov r0, r11
    mov r1, r10
    mov r2, r2, asr #24
    and r3, r9, #255
    str r7, [sp, #0x4]
    bl ov001_02202a68_L0
    str r0, [sp, #0x8]
ov001_02202a68_Lbc:
    ldr r0, [sp, #0x8]
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
