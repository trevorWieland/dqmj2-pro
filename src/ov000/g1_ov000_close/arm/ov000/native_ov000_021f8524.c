/* ov000 row 0x021f8524: 100 bytes.
 *
 * What it does: 25 instructions; 6 call(s) to 0x02215698, 0x0221742c, 0x021f9614, +3 more; loops (back edge at +0x5c); returns through pop {r4, r5, r6, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x30 -> +0x40
 *   test +0x2c cmp r0, #14
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f8524; the literal pool and
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

extern void ov000_display_context_02215698(void);
extern void native_fn_0221742c(void);
extern void native_fn_021f9614(void);
extern void native_fn_021f94b4(void);
extern void native_fn_022178e8(void);
extern void native_fn_02065818(void);


asm u32 native_ov000_021f8524 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r6, r0
    mov r5, r1
    bl ov000_display_context_02215698
    mov r0, r6, lsl #24
    mov r0, r0, asr #24
    bl native_fn_0221742c
    mov r4, r0
    mov r0, r6
    bl native_fn_021f9614
    bl native_fn_021f94b4
    cmp r0, #14
    bne ov000_021f8524_L40
    mov r0, r6
    mov r1, #0
    bl native_fn_022178e8
ov000_021f8524_L40:
    ldrsh r1, [r5]
    ldrsh r2, [r5, #2]
    mov r0, r4
    mov r1, r1, lsl #21
    mov r2, r2, lsl #21
    mov r1, r1, asr #24
    mov r2, r2, asr #24
    bl native_fn_02065818
    ldmia sp!, {r4, r5, r6, pc}
}
