/* ov001 row 0x022241d8: 228 bytes.
 *
 * What it does: 57 instructions; 8 call(s) to 0x02008e0c, 0x021dbd24, 0x02223f48, +5 more; loops (back edge at +0x24); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: loop with 8 calls (57 instructions, 8 calls, 2 branches, 7 back edges, 0 literal slots).
 *
 *   branch +0x3c -> +0x70
 *   back edge +0x7c -> +0x34
 *   branch +0x98 -> +0xa8
 *   back edge +0xb0 -> +0x90
 *   branch +0xc4 -> +0xd8
 *   test +0x38 cmp r0, #0
 *   test +0x64 cmp r0, r6
 *   test +0x74 cmp r7, #3
 *   test +0x94 cmp r1, #0
 *   test +0xa0 cmp r1, r6
 *   test +0xac cmp r4, #3
 *   test +0xc0 cmp r4, #0
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022241d8; the literal pool and
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
extern void native_fn_021dbd24(void);
extern void native_fn_02223f48(void);
extern void ov001_count_candidates_02223f20(void);


asm u32 native_ov001_022241d8 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #28
    mov r10, r1
    mov r9, r2
    add r1, sp, #4
    mov r2, #12
    str r0, [sp]
    mov r8, r3
    mov r6, #0
    bl native_fn_02008e0c
    mov r7, r6
    add r11, sp, #16
    add r5, sp, #4
ov001_022241d8_L34:
    ldr r0, [r5, r7, lsl #2]
    cmp r0, #0
    beq ov001_022241d8_L70
    mov r0, r9
    bl native_fn_021dbd24
    mov r4, r0
    mov r0, r10
    mov r1, r9
    mov r2, r8
    mov r3, #2
    bl native_fn_02223f48
    sub r0, r4, r0
    cmp r0, r6
    str r0, [r11, r7, lsl #2]
    movgt r6, r0
ov001_022241d8_L70:
    add r7, r7, #1
    cmp r7, #3
    add r9, r9, #1088
    blt ov001_022241d8_L34
    mov r4, #0
    mov r0, r4
    add r2, sp, #16
    add r3, sp, #4
ov001_022241d8_L90:
    ldr r1, [r3, r4, lsl #2]
    cmp r1, #0
    beq ov001_022241d8_La8
    ldr r1, [r2, r4, lsl #2]
    cmp r1, r6
    strlt r0, [r3, r4, lsl #2]
ov001_022241d8_La8:
    add r4, r4, #1
    cmp r4, #3
    blt ov001_022241d8_L90
    add r0, sp, #4
    bl ov001_count_candidates_02223f20
    mov r4, r0
    cmp r4, #0
    ble ov001_022241d8_Ld8
    ldr r1, [sp]
    add r0, sp, #4
    mov r2, #12
    bl native_fn_02008e0c
ov001_022241d8_Ld8:
    mov r0, r4
    add sp, sp, #28
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
