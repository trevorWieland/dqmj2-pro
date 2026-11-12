/* ov000 row 0x021e0078: 364 bytes.
 *
 * What it does: 88 instructions; 11 call(s) to 0x0200285c, 0x02025a28, 0x02025578, +8 more; loops (back edge at +0x10); returns through pop {r3, r4, r5, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x160 -> constant 0x45800000 (image word 0x45800000)
 *   pool +0x164 -> constant 0x0b60b60b (image word 0x0b60b60b)
 *   pool +0x168 -> constant 0x020d3fe0 (image word 0x020d3fe0)
 *   branch +0x48 -> +0x60
 *   branch +0x5c -> +0x6c
 *   test +0x40 cmp r1, #0
 *   test +0x150 cmp r1, r4
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e0078; the literal pool and
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

extern void native_fn_0200285c(void);
extern void native_fn_02025a28(void);
extern void native_fn_02025578(void);
extern void native_fn_020259b4(void);
extern void native_fn_02024e0c(void);
extern void native_fn_02025ca4(void);
extern void native_fn_02002480(void);


asm u32 native_ov000_021e0078 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    add r0, r5, #500
    add r1, r5, #488
    bl native_fn_0200285c
    mov r1, #30
    mul r1, r0, r1
    mov r0, r1, asr #2
    add r0, r1, r0, lsr #29
    mov r0, r0, asr #3
    bl native_fn_02025a28
    ldr r1, =0x45800000
    bl native_fn_02025578
    bl native_fn_020259b4
    ldr r1, [r5, #0x20c]
    mov r4, r0
    cmp r1, #0
    mov r0, r1, lsl #12
    ble ov000_021e0078_L60
    bl native_fn_02025a28
    mov r1, r0
    mov r0, #1056964608
    bl native_fn_02024e0c
    b ov000_021e0078_L6c
ov000_021e0078_L60:
    bl native_fn_02025a28
    mov r1, #1056964608
    bl native_fn_02025ca4
ov000_021e0078_L6c:
    bl native_fn_020259b4
    mov r1, r4
    bl native_fn_02002480
    mov r1, #180
    mul r3, r0, r1
    ldr r1, =0x0b60b60b
    mov r2, #182
    umull r14, r12, r3, r1
    mla r12, r3, r2, r12
    mov r2, r3, asr #31
    mla r12, r2, r1, r12
    mov r0, #0
    adds r1, lr, r0
    adc r1, r12, #2048
    mov r1, r1, lsl #4
    mov r1, r1, lsr #16
    mov r1, r1, asr #4
    mov r1, r1, lsl #1
    add r2, r1, #1
    ldr r1, =0x020d3fe0
    mov r2, r2, lsl #1
    ldrsh r1, [r1, r2]
    ldr r12, [r5, #0x1f4]
    ldr r2, [r5, #0x1e8]
    add r1, r1, #4096
    mov r1, r1, asr #1
    rsb r1, r1, #4096
    sub r2, r2, r12
    smull r3, r2, r1, r2
    adds r3, r3, #2048
    adc r2, r2, r0
    mov r3, r3, lsr #12
    orr r3, r3, r2, lsl #20
    add r2, r12, r3
    str r2, [r5, #0x70]
    ldr r12, [r5, #0x1f8]
    ldr r2, [r5, #0x1ec]
    sub r2, r2, r12
    smull r3, r2, r1, r2
    adds r3, r3, #2048
    adc r2, r2, r0
    mov r3, r3, lsr #12
    orr r3, r3, r2, lsl #20
    add r2, r12, r3
    str r2, [r5, #0x74]
    ldr r12, [r5, #0x1fc]
    ldr r2, [r5, #0x1f0]
    sub r2, r2, r12
    smull r3, r2, r1, r2
    adds r3, r3, #2048
    adc r1, r2, r0
    mov r2, r3, lsr #12
    orr r2, r2, r1, lsl #20
    add r1, r12, r2
    str r1, [r5, #0x78]
    ldr r1, [r5, #0x20c]
    add r1, r1, #1
    cmp r1, r4
    str r1, [r5, #0x20c]
    movgt r0, #1
    ldmia sp!, {r3, r4, r5, pc}
}
