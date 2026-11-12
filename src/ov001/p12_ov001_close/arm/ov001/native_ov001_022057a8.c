/* ov001 row 0x022057a8: 272 bytes.
 *
 * What it does: 68 instructions; 4 call(s) to 0x02204df0, 0x02204d60, 0x02204df0, +1 more; loops (back edge at +0x54); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: block fill (68 instructions, 4 calls, 5 branches, 5 back edges, 0 literal slots).
 *
 *   branch +0x34 -> +0x7c
 *   branch +0x78 -> +0x100
 *   branch +0xa4 -> +0x100
 *   branch +0xc4 -> +0xd0
 *   back edge +0xfc -> +0x30
 *   test +0x14 cmp r8, r7
 *   test +0x30 cmp r8, r7
 *   test +0x3c cmp r0, #0
 *   test +0xa0 cmp r0, r4
 *   test +0xbc cmp r1, #4
 *   test +0xc8 cmp r1, #1
 *   test +0xd8 cmp r7, r2, asr #16
 *   2 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022057a8; the literal pool and
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

extern void native_fn_02204df0(void);
extern void native_fn_02204d60(void);


asm u32 native_ov001_022057a8 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #12
    mov r10, r0
    mov r8, r2
    mov r7, r3
    cmp r8, r7
    ldr r6, [sp, #0x30]
    ldr r5, [r10, #0x40]
    mov r9, r1
    movgt r8, r7
    mov r11, #7
    mvn r4, #0
ov001_022057a8_L30:
    cmp r8, r7
    bne ov001_022057a8_L7c
    ldr r0, [r10, #0x34]
    cmp r0, #0
    moveq r0, #17
    movne r0, #19
    mov r1, r0, lsl #24
    mov r0, r10
    mov r1, r1, asr #24
    bl native_fn_02204df0
    mov r3, r0
    stmia sp, {r8, r9}
    mov r0, #7
    str r0, [sp, #0x8]
    ldrsb r1, [r10, #36]
    mov r0, r10
    mov r2, r6
    bl native_fn_02204d60
    b ov001_022057a8_L100
ov001_022057a8_L7c:
    mov r0, r10
    mov r1, #0
    bl native_fn_02204df0
    stmia sp, {r8, r9, r11}
    mov r3, r0
    ldrsb r1, [r10, #36]
    mov r0, r10
    mov r2, r6
    bl native_fn_02204d60
    cmp r0, r4
    beq ov001_022057a8_L100
    sub r1, r7, r8
    add r2, r1, #7
    mov r1, r2, asr #2
    add r1, r2, r1, lsr #29
    mov r1, r1, asr #3
    cmp r1, #4
    movgt r1, #4
    bgt ov001_022057a8_Ld0
    cmp r1, #1
    movlt r1, #1
ov001_022057a8_Ld0:
    add r2, r8, r1, lsl #3
    mov r2, r2, lsl #16
    cmp r7, r2, asr #16
    mov r8, r2, asr #16
    mov r2, #12
    mla r2, r0, r2, r5
    add r0, r6, r1
    mov r0, r0, lsl #24
    movlt r8, r7
    strb r1, [r2, #0x6]
    mov r6, r0, asr #24
    b ov001_022057a8_L30
ov001_022057a8_L100:
    mov r0, #0
    strh r0, [r10, #38]
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
