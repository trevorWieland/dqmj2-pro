/* ov000 row 0x021e7c28: 168 bytes.
 *
 * What it does: 41 instructions; 3 call(s) to 0x021e7bf4, 0x02008d78, 0x02008d78; loops (back edge at +0x14); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xa4 -> constant 0x0223526c (image word 0x0223526c)
 *   branch +0x1c -> +0x9c
 *   0 block transfer(s), 12 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e7c28; the literal pool and
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

extern void native_fn_021e7bf4(void);
extern void native_fn_02008d78(void);


asm u32 native_ov000_021e7c28 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    mov r9, r0
    mov r8, r1
    mov r7, r2
    mov r6, r3
    bl native_fn_021e7bf4
    movs r4, r0
    bmi ov000_021e7c28_L9c
    ldr r0, =0x0223526c
    mov r2, #716
    mla r5, r4, r2, r0
    mov r0, r5
    mov r1, #0
    bl native_fn_02008d78
    mov r0, r9, lsl #24
    mov r3, #1
    strb r3, [r5, #0x274]
    mov r2, r0, asr #24
    add r0, r5, #256
    ldr r1, [sp, #0x20]
    strh r2, [r0, #106]
    str r1, [r5, #0x28c]
    strb r3, [r5, #0x276]
    mov r1, #0
    strb r1, [r5, #0x2a9]
    mov r0, #3072
    str r0, [r5, #0x29c]
    mov r2, #40960
    ldrb r0, [sp, #0x24]
    str r2, [r5, #0x2a4]
    mov r2, #328
    str r2, [r5, #0x2a0]
    strb r0, [r5, #0x279]
    str r8, [r5, #0x280]
    str r7, [r5, #0x284]
    add r0, r5, #680
    mov r2, #12
    str r6, [r5, #0x288]
    bl native_fn_02008d78
ov000_021e7c28_L9c:
    mov r0, r4
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
