/* ov001 row 0x0222470c: 248 bytes.
 *
 * What it does: 62 instructions; 10 call(s) to 0x02008e0c, 0x022244a0, 0x022244a0, +7 more; loops (back edge at +0x24); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: loop with 10 calls (62 instructions, 10 calls, 2 branches, 9 back edges, 0 literal slots).
 *
 *   branch +0x3c -> +0x68
 *   back edge +0x74 -> +0x34
 *   branch +0x8c -> +0xb8
 *   back edge +0xc4 -> +0x84
 *   branch +0xd8 -> +0xec
 *   test +0x38 cmp r0, #0
 *   test +0x60 cmp r0, r6
 *   test +0x6c cmp r5, #3
 *   test +0x88 cmp r0, #0
 *   test +0xb0 cmp r0, r6
 *   test +0xbc cmp r7, #3
 *   test +0xd4 cmp r4, #0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0222470c; the literal pool and
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
extern void native_fn_022244a0(void);
extern void ov001_count_candidates_02223f20(void);


asm u32 native_ov001_0222470c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #16
    mov r10, r1
    mov r9, r2
    add r1, sp, #4
    mov r2, #12
    str r0, [sp]
    mov r8, r3
    mov r6, #0
    bl native_fn_02008e0c
    mov r7, r10
    mov r5, r6
    add r11, sp, #4
ov001_0222470c_L34:
    ldr r0, [r11, r5, lsl #2]
    cmp r0, #0
    beq ov001_0222470c_L68
    mov r0, r7
    mov r1, r8
    bl native_fn_022244a0
    mov r4, r0
    mov r0, r7
    mov r1, r9
    bl native_fn_022244a0
    add r0, r4, r0, lsl #1
    cmp r0, r6
    movgt r6, r0
ov001_0222470c_L68:
    add r5, r5, #1
    cmp r5, #3
    add r7, r7, #1088
    blt ov001_0222470c_L34
    mov r7, #0
    mov r11, r7
    add r5, sp, #4
ov001_0222470c_L84:
    ldr r0, [r5, r7, lsl #2]
    cmp r0, #0
    beq ov001_0222470c_Lb8
    mov r0, r10
    mov r1, r8
    bl native_fn_022244a0
    mov r4, r0
    mov r0, r10
    mov r1, r9
    bl native_fn_022244a0
    add r0, r4, r0, lsl #1
    cmp r0, r6
    strlt r11, [r5, r7, lsl #2]
ov001_0222470c_Lb8:
    add r7, r7, #1
    cmp r7, #3
    add r10, r10, #1088
    blt ov001_0222470c_L84
    add r0, sp, #4
    bl ov001_count_candidates_02223f20
    mov r4, r0
    cmp r4, #0
    ble ov001_0222470c_Lec
    ldr r1, [sp]
    add r0, sp, #4
    mov r2, #12
    bl native_fn_02008e0c
ov001_0222470c_Lec:
    mov r0, r4
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
