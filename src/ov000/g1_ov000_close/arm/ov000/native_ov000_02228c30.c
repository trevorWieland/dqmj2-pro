/* ov000 row 0x02228c30: 216 bytes.
 *
 * What it does: 54 instructions; 6 call(s) to 0x0222a080, 0x02228c78, 0x02228d10, +3 more; loops (back edge at +0x5c); returns through popeq {r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   back edge +0x5c -> +0x48
 *   back edge +0xd4 -> +0x24
 *   test +0x34 cmp r0, r11
 *   test +0x58 cmp r1, #4
 *   test +0xb8 cmp r0, #4
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02228c30; the literal pool and
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

extern void native_fn_0222a080(void);
extern void native_fn_02228d10(void);


asm u32 native_ov000_02228c30 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #20
    mov r8, #0
    mov r10, r0
    mov r9, r1
    mov r6, r8
    add r5, sp, #4
    add r4, sp, #0
    mvn r11, #0
ov000_02228c30_L24:
    mov r0, r8
    bl native_fn_0222a080
    mov r7, r0
    ldrsh r0, [r7]
    cmp r0, r11
    addeq sp, sp, #20
    mvneq r0, #0
    ldmeqia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    mov r1, #0
ov000_02228c30_L48:
    add r0, r1, #1
    mov r0, r0, lsl #24
    str r6, [r5, r1, lsl #2]
    mov r1, r0, asr #24
    cmp r1, #4
    blt ov000_02228c30_L48
    strb r6, [sp]
    ldrsh r1, [r10, #64]
    mov r0, r7
    mov r2, r5
    mov r3, r4
    bl native_fn_02228d10
    ldrsh r1, [r10, #66]
    mov r0, r7
    mov r2, r5
    mov r3, r4
    bl native_fn_02228d10
    ldrsh r1, [r9, #64]
    mov r0, r7
    mov r2, r5
    mov r3, r4
    bl native_fn_02228d10
    ldrsh r1, [r9, #66]
    mov r0, r7
    mov r2, r5
    mov r3, r4
    bl native_fn_02228d10
    ldrsb r0, [sp]
    cmp r0, #4
    addeq sp, sp, #20
    ldreqsh r0, [r7]
    ldmeqia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    add r0, r8, #1
    mov r0, r0, lsl #24
    mov r8, r0, asr #24
    b ov000_02228c30_L24
}
