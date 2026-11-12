/* ov000 row 0x021e6544: 272 bytes.
 *
 * What it does: 66 instructions; 2 call(s) to 0x021e6644, 0x02002480; loops (back edge at +0x24); returns through pop {r3, r4, r5, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x108 -> constant 0x0b60b60b (image word 0x0b60b60b)
 *   pool +0x10c -> constant 0x020d3fe0 (image word 0x020d3fe0)
 *   branch +0x14 -> +0x100
 *   test +0x10 cmp r1, #0
 *   test +0xf0 cmp r2, r0
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e6544; the literal pool and
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

extern void native_fn_02002480(void);


asm u32 native_ov000_021e6544 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    mov r4, r1
    ldrsh r1, [r5, #2]
    cmp r1, #0
    ble ov000_021e6544_L100
    ldrsh r2, [r5]
    mov r0, #368640
    mul r0, r2, r0
    bl native_fn_02002480
    ldr r1, =0x0b60b60b
    mov r2, #182
    umull r12, r3, r0, r1
    mla r3, r0, r2, r3
    mov r0, r0, asr #31
    mla r3, r0, r1, r3
    adds r0, r12, #0
    adc r0, r3, #2048
    mov r0, r0, lsl #4
    mov r0, r0, lsr #16
    mov r1, r0, asr #4
    ldr r0, =0x020d3fe0
    mov r1, r1, lsl #2
    ldrsh r0, [r0, r1]
    ldr r12, [r5, #0x4]
    ldr r2, [r5, #0x10]
    mov r1, #0
    sub r2, r2, r12
    smull r3, r2, r0, r2
    adds r3, r3, #2048
    adc r2, r2, #0
    mov r3, r3, lsr #12
    orr r3, r3, r2, lsl #20
    add r2, r12, r3
    str r2, [r4]
    ldr r12, [r5, #0x8]
    ldr r2, [r5, #0x14]
    sub r2, r2, r12
    smull r3, r2, r0, r2
    adds r3, r3, #2048
    adc r2, r2, #0
    mov r3, r3, lsr #12
    orr r3, r3, r2, lsl #20
    add r2, r12, r3
    str r2, [r4, #0x4]
    ldr r12, [r5, #0xc]
    ldr r2, [r5, #0x18]
    sub r2, r2, r12
    smull r3, r2, r0, r2
    adds r3, r3, #2048
    adc r0, r2, #0
    mov r2, r3, lsr #12
    orr r2, r2, r0, lsl #20
    add r0, r12, r2
    str r0, [r4, #0x8]
    ldrsh r0, [r5]
    add r0, r0, #1
    strh r0, [r5]
    ldrsh r2, [r5]
    ldrsh r0, [r5, #2]
    cmp r2, r0
    strgeh r1, [r5, #2]
    mov r0, #1
    ldmia sp!, {r3, r4, r5, pc}
ov000_021e6544_L100:
    mov r0, #0
    ldmia sp!, {r3, r4, r5, pc}
}
