/* ov001 row 0x022029a8: 192 bytes.
 *
 * What it does: 48 instructions; 4 call(s) to 0x021db438, 0x021db8d0, 0x021dc1c0, +1 more; loops (back edge at +0x38); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: block fill (48 instructions, 4 calls, 8 branches, 5 back edges, 0 literal slots).
 *
 *   branch +0x2c -> +0x84
 *   branch +0x48 -> +0x70
 *   branch +0x50 -> +0x64
 *   branch +0x60 -> +0x70
 *   branch +0x6c -> +0x84
 *   back edge +0x80 -> +0x30
 *   branch +0x88 -> +0xb4
 *   branch +0x94 -> +0xb4
 *   back edge +0xac -> +0x00
 *   test +0x20 cmp r6, r8
 *   test +0x44 cmp r0, #0
 *   test +0x4c cmp r7, #0
 *   test +0x5c cmp r0, #0
 *   test +0x78 cmp r8, r0, asr #24
 *   test +0x84 cmp r5, #0
 *   test +0x90 cmp r0, #0
 *   1 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022029a8; the literal pool and
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

extern void native_fn_021db438(void);
extern void native_fn_021db8d0(void);
extern void native_fn_021dc1c0(void);


asm u32 native_ov001_022029a8 (register u32 a0)
{
ov001_022029a8_L0:
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #12
    mov r9, r2
    str r9, [sp, #0x8]
    mov r8, r3
    mov r6, r9
    mov r11, r0
    mov r10, r1
    cmp r6, r8
    ldr r7, [sp, #0x34]
    mov r5, #0
    bge ov001_022029a8_L84
ov001_022029a8_L30:
    mov r0, r10
    mov r1, r6
    bl native_fn_021db438
    mov r4, r0
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_022029a8_L70
    cmp r7, #0
    beq ov001_022029a8_L64
    mov r0, r4
    bl native_fn_021dc1c0
    cmp r0, #0
    beq ov001_022029a8_L70
ov001_022029a8_L64:
    str r6, [sp, #0x8]
    mov r5, #1
    b ov001_022029a8_L84
ov001_022029a8_L70:
    add r0, r6, #1
    mov r0, r0, lsl #24
    cmp r8, r0, asr #24
    mov r6, r0, asr #24
    bgt ov001_022029a8_L30
ov001_022029a8_L84:
    cmp r5, #0
    bne ov001_022029a8_Lb4
    ldrsb r0, [sp, #48]
    cmp r0, #0
    beq ov001_022029a8_Lb4
    mov r2, #0
    mov r0, r11
    mov r1, r10
    and r3, r9, #255
    stmia sp, {r2, r7}
    bl ov001_022029a8_L0
    str r0, [sp, #0x8]
ov001_022029a8_Lb4:
    ldr r0, [sp, #0x8]
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
