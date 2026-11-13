/* ov001 row 0x0222649c: 252 bytes.
 *
 * What it does: 63 instructions; 8 call(s) to 0x02008e0c, 0x0201af84, 0x022264d4, +5 more; loops (back edge at +0x20); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: loop with 8 calls (63 instructions, 8 calls, 4 branches, 7 back edges, 0 literal slots).
 *
 *   branch +0x40 -> +0x68
 *   back edge +0x74 -> +0x38
 *   branch +0x90 -> +0xbc
 *   branch +0xa4 -> +0xb8
 *   branch +0xb4 -> +0xbc
 *   back edge +0xc8 -> +0x88
 *   branch +0xdc -> +0xf0
 *   test +0x3c cmp r0, #0
 *   test +0x60 cmp r0, r7
 *   test +0x6c cmp r6, #3
 *   test +0x8c cmp r0, #0
 *   test +0xa0 cmp r7, r0
 *   test +0xb0 cmp r1, r0
 *   test +0xc0 cmp r6, #3
 *   test +0xd8 cmp r4, #0
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0222649c; the literal pool and
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
extern void native_fn_0201af84(void);
extern void ov001_count_candidates_02223f20(void);


asm u32 native_ov001_0222649c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #28
    mov r10, r1
    mov r9, r2
    add r1, sp, #4
    mov r2, #12
    str r0, [sp]
    mov r7, #99
    bl native_fn_02008e0c
    mov r8, r9
    mov r6, #0
    add r4, r10, #512
    add r11, sp, #16
    add r5, sp, #4
ov001_0222649c_L38:
    ldr r0, [r5, r6, lsl #2]
    cmp r0, #0
    beq ov001_0222649c_L68
    add r0, r8, #512
    ldrsb r1, [r4, #52]
    ldrsb r0, [r0, #52]
    add r1, r1, r0
    sub r0, r1, #4
    str r1, [r11, r6, lsl #2]
    bl native_fn_0201af84
    cmp r0, r7
    movlt r7, r0
ov001_0222649c_L68:
    add r6, r6, #1
    cmp r6, #3
    add r8, r8, #1088
    blt ov001_0222649c_L38
    mov r6, #0
    add r4, sp, #16
    mov r8, r6
    add r5, sp, #4
ov001_0222649c_L88:
    ldr r0, [r5, r6, lsl #2]
    cmp r0, #0
    beq ov001_0222649c_Lbc
    ldr r0, [r4, r6, lsl #2]
    sub r0, r0, #4
    bl native_fn_0201af84
    cmp r7, r0
    bne ov001_0222649c_Lb8
    ldrb r1, [r10, #0x31f]
    ldrb r0, [r9, #0x31f]
    cmp r1, r0
    bne ov001_0222649c_Lbc
ov001_0222649c_Lb8:
    str r8, [r5, r6, lsl #2]
ov001_0222649c_Lbc:
    add r6, r6, #1
    cmp r6, #3
    add r9, r9, #1088
    blt ov001_0222649c_L88
    add r0, sp, #4
    bl ov001_count_candidates_02223f20
    mov r4, r0
    cmp r4, #0
    ble ov001_0222649c_Lf0
    ldr r1, [sp]
    add r0, sp, #4
    mov r2, #12
    bl native_fn_02008e0c
ov001_0222649c_Lf0:
    mov r0, r4
    add sp, sp, #28
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
