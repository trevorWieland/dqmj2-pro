/* ov000 row 0x021f96a8: 192 bytes.
 *
 * What it does: 48 instructions; 7 call(s) to 0x02215698, 0x021f95b0, 0x021f9614, +4 more; loops (back edge at +0x28); returns through pop {r3, r4, r5, r6, r7, r8, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x34 -> +0x88
 *   branch +0x70 -> +0x88
 *   back edge +0x98 -> +0x20
 *   back edge +0xb0 -> +0x1c
 *   test +0x30 cmp r0, #127
 *   test +0x6c cmp r0, #0
 *   test +0x94 cmp r6, #4
 *   test +0xa8 cmp r7, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f96a8; the literal pool and
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

extern void native_fn_02215698(void);
extern void native_fn_021f95b0(void);
extern void native_fn_021f9614(void);
extern void native_fn_021f9484(void);
extern void native_fn_0204b920(void);


asm u32 native_ov000_021f96a8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, lr}
    sub sp, sp, #4
    bl native_fn_02215698
    mov r7, #0
    mov r8, r7
    add r4, sp, #0
    mov r5, r7
ov000_021f96a8_L1c:
    mov r6, r5
ov000_021f96a8_L20:
    add r0, r6, r8
    and r0, r0, #255
    bl native_fn_021f95b0
    bl native_fn_021f9614
    cmp r0, #127
    beq ov000_021f96a8_L88
    mov r0, r4
    mov r1, r6
    mov r2, r7
    bl native_fn_021f9484
    ldrsh r1, [sp, #2]
    ldrsh r0, [sp]
    add r3, r1, #40
    add r2, r0, #40
    and r0, r0, #255
    and r1, r1, #255
    and r2, r2, #255
    and r3, r3, #255
    bl native_fn_0204b920
    cmp r0, #0
    beq ov000_021f96a8_L88
    add r0, r6, r7, lsl #2
    mov r0, r0, lsl #24
    add sp, sp, #4
    mov r0, r0, asr #24
    ldmia sp!, {r3, r4, r5, r6, r7, r8, pc}
ov000_021f96a8_L88:
    add r0, r6, #1
    mov r0, r0, lsl #24
    mov r6, r0, asr #24
    cmp r6, #4
    blt ov000_021f96a8_L20
    add r0, r7, #1
    mov r0, r0, lsl #24
    mov r7, r0, asr #24
    cmp r7, #3
    add r8, r8, #4
    blt ov000_021f96a8_L1c
    mvn r0, #0
    add sp, sp, #4
    ldmia sp!, {r3, r4, r5, r6, r7, r8, pc}
}
