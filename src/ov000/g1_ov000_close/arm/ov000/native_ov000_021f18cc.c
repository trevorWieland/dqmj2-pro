/* ov000 row 0x021f18cc: 156 bytes.
 *
 * What it does: 39 instructions; 4 call(s) to 0x02044dc4, 0x02044dc4, 0x020449d4, +1 more; loops (back edge at +0x20); returns through pop {r3, r4, r5, r6, r7, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   test +0x64 cmp r5, r4
 *   test +0x74 cmp r5, r4
 *   test +0x80 cmp r6, r0, lsr #19
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f18cc; the literal pool and
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

extern void native_fn_02044dc4(void);
extern void native_fn_020449d4(void);


asm u32 native_ov000_021f18cc (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    mov r7, r0
    ldr r2, [r7]
    mov r6, r1
    mov r0, r2, lsl #16
    mov r1, r2, lsr #16
    mov r0, r0, asr #16
    and r1, r1, #255
    bl native_fn_02044dc4
    ldr r1, [r6]
    mov r5, r0
    mov r0, r1, lsl #16
    mov r1, r1, lsr #16
    mov r0, r0, asr #16
    and r1, r1, #255
    bl native_fn_02044dc4
    mov r4, r0
    ldrh r0, [r7]
    bl native_fn_020449d4
    ldrh r1, [r0, #6]
    ldrh r0, [r6]
    mov r1, r1, lsl #19
    mov r6, r1, lsr #19
    bl native_fn_020449d4
    ldrh r0, [r0, #6]
    cmp r5, r4
    mov r0, r0, lsl #19
    movgt r0, #1
    ldmgtia sp!, {r3, r4, r5, r6, r7, pc}
    cmp r5, r4
    mvnlt r0, #0
    ldmltia sp!, {r3, r4, r5, r6, r7, pc}
    cmp r6, r0, lsr #19
    movhi r0, #1
    ldmhiia sp!, {r3, r4, r5, r6, r7, pc}
    movlo r0, #1
    movhs r0, #0
    rsb r0, r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
