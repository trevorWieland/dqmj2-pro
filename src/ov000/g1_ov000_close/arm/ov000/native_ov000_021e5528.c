/* ov000 row 0x021e5528: 108 bytes.
 *
 * What it does: 27 instructions; 1 call(s) to 0x021e54f4; loops (back edge at +0x18); returns through pop {r4, r5, r6, r7, r8, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x20 -> +0x64
 *   test +0x1c cmp r0, #0
 *   0 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e5528; the literal pool and
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

extern void native_fn_021e54f4(void);


asm u32 native_ov000_021e5528 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    mov r8, r0
    mov r6, r1
    mov r5, r2
    mov r4, r3
    mov r7, #0
    bl native_fn_021e54f4
    cmp r0, #0
    beq ov000_021e5528_L64
    ldr r3, [sp, #0x18]
    and r12, r8, #255
    smull r2, r1, r3, r3
    adds r3, r2, #2048
    adc r2, r1, #0
    mov r3, r3, lsr #12
    ldrb r1, [sp, #0x1c]
    strh r12, [r0]
    orr r3, r3, r2, lsl #20
    str r3, [r0, #0x10]
    strb r1, [r0, #0x2]
    mov r7, #1
    strb r7, [r0, #0x3]
    str r6, [r0, #0x4]
    str r5, [r0, #0x8]
    str r4, [r0, #0xc]
ov000_021e5528_L64:
    mov r0, r7
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
