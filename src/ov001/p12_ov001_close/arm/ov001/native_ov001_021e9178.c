/* ov001 row 0x021e9178: 1120 bytes.
 *
 * What it does: 277 instructions; 14 call(s) to 0x02002618, 0x02000ce8, 0x02028044, +11 more; loops (back edge at +0x104); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: block copy loop (277 instructions, 14 calls, 6 branches, 13 back edges, 3 literal slots).
 *
 *   pool +0x454 -> constant 0x02238d7c (image word 0x02238d7c)
 *   pool +0x458 -> constant 0x0b60b60b (image word 0x0b60b60b)
 *   pool +0x45c -> constant 0x020d3fe0 (image word 0x020d3fe0)
 *   branch +0x74 -> +0x238
 *   branch +0x23c -> +0x364
 *   branch +0x244 -> +0x360
 *   branch +0x27c -> +0x294
 *   branch +0x290 -> +0x2a0
 *   branch +0x35c -> +0x364
 *   branch +0x368 -> +0x3e4
 *   test +0x6c cmp r6, #0
 *   test +0x238 cmp r6, #10
 *   test +0x240 cmp r7, r8
 *   test +0x274 cmp r0, #0
 *   test +0x364 cmp r6, #20
 *   30 block transfer(s), 30 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021e9178; the literal pool and
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

extern void native_fn_02002618(void);
extern void native_fn_02000ce8(void);
extern void native_fn_02028044(void);
extern void native_fn_0200103c(void);
extern void native_fn_021d9534(void);
extern void native_fn_02041f74(void);
extern void native_fn_02026144(void);
extern void native_fn_02025a28(void);
extern void native_fn_02024e0c(void);
extern void native_fn_02025ca4(void);
extern void native_fn_020259b4(void);
extern void native_fn_0200235c(void);


asm u32 native_ov001_021e9178 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    sub sp, sp, #120
    mov r4, r0
    ldmib r4, {r6, r7, r8}
    add r0, r4, #20
    add r5, sp, #108
    ldmia r0, {r0, r1, r2}
    stmia r5, {r0, r1, r2}
    add r3, r4, #32
    ldmia r3, {r0, r1, r2}
    add r9, sp, #96
    stmia r9, {r0, r1, r2}
    add r5, r4, #44
    ldmia r5, {r0, r1, r2}
    add r3, sp, #84
    stmia r3, {r0, r1, r2}
    add r0, r4, #56
    add lr, sp, #72
    ldmia r0, {r0, r1, r2}
    add r12, r4, #68
    stmia lr, {r0, r1, r2}
    ldmia r12, {r0, r1, r2}
    add r9, sp, #48
    add r5, r4, #80
    stmia r9, {r0, r1, r2}
    add r3, sp, #60
    ldmia r5, {r0, r1, r2}
    cmp r6, #0
    stmia r3, {r0, r1, r2}
    bne ov001_021e9178_L238
    ldr r1, =0x02238d7c
    add r0, sp, #36
    ldr r3, [r1, #0x60]
    ldr r6, [r1, #0x54]
    ldr r2, [r3, #0x328]
    ldr r5, [r6, #0x328]
    mov r1, r0
    add r2, r5, r2
    mov r2, r2, asr #1
    str r2, [sp, #0x24]
    ldr r7, [r6, #0x32c]
    ldr r5, [r3, #0x32c]
    add r5, r7, r5
    mov r8, r5, asr #1
    str r8, [sp, #0x28]
    ldr r7, [r6, #0x330]
    ldr r5, [r3, #0x330]
    add r5, r7, r5
    mov r5, r5, asr #1
    str r5, [sp, #0x2c]
    str r2, [sp, #0x6c]
    str r8, [sp, #0x70]
    str r5, [sp, #0x74]
    ldr r5, [r3, #0x328]
    ldr r2, [r6, #0x328]
    sub r2, r5, r2
    str r2, [sp, #0x24]
    ldr r5, [r3, #0x32c]
    ldr r2, [r6, #0x32c]
    sub r2, r5, r2
    str r2, [sp, #0x28]
    ldr r3, [r3, #0x330]
    ldr r2, [r6, #0x330]
    sub r2, r3, r2
    str r2, [sp, #0x2c]
    bl native_fn_02002618
    ldr r7, [sp, #0x24]
    ldr r3, [sp, #0x28]
    mov r2, r7, asr #31
    mov r0, r3, asr #31
    mov r8, r2, lsl #16
    mov r5, r0, lsl #16
    ldr r1, [sp, #0x2c]
    orr r8, r8, r7, lsr #16
    mov r0, r1, asr #31
    mov r2, r0, lsl #16
    mov r0, #2048
    adds r9, r0, r7, lsl #16
    adc r8, r8, #0
    adds r7, r0, r3, lsl #16
    orr r5, r5, r3, lsr #16
    adc r5, r5, #0
    mov r9, r9, lsr #12
    mov r7, r7, lsr #12
    orr r9, r9, r8, lsl #20
    orr r7, r7, r5, lsl #20
    adds r3, r0, r1, lsl #16
    orr r2, r2, r1, lsr #16
    adc r0, r2, #0
    mov r1, r3, lsr #12
    orr r1, r1, r0, lsl #20
    add r0, sp, #0
    str r9, [sp, #0x24]
    str r7, [sp, #0x28]
    str r1, [sp, #0x2c]
    bl native_fn_02000ce8
    add r0, sp, #0
    mov r1, #368640
    bl native_fn_02028044
    add r0, sp, #36
    add r1, sp, #0
    mov r2, r0
    bl native_fn_0200103c
    ldr r2, [sp, #0x24]
    ldr r0, [sp, #0x6c]
    ldr r1, [sp, #0x28]
    add r5, r2, r0
    ldr r0, [sp, #0x70]
    ldr r2, [sp, #0x2c]
    add r7, r1, r0
    ldr r1, [sp, #0x74]
    str r5, [sp, #0x24]
    add r3, r2, r1
    str r7, [sp, #0x28]
    str r3, [sp, #0x2c]
    ldr r1, [r6, #0x328]
    add r1, r5, r1
    mov r5, r1, asr #1
    str r5, [sp, #0x24]
    ldr r1, [r6, #0x32c]
    add r1, r7, r1
    mov r2, r1, asr #1
    str r2, [sp, #0x28]
    ldr r1, [r6, #0x330]
    add r1, r3, r1
    mov r8, r1, asr #1
    str r8, [sp, #0x2c]
    ldr r1, =0x02238d7c
    add r7, r0, #6144
    ldr r0, [r1, #0x60]
    add r6, r2, #6144
    mvn r1, #0
    mov r2, #1
    mov r3, #0
    str r5, [sp, #0x60]
    str r8, [sp, #0x68]
    str r7, [sp, #0x70]
    str r6, [sp, #0x64]
    bl native_fn_021d9534
    mov r8, r0
    mov r7, #0
    mov r6, #10
ov001_021e9178_L238:
    cmp r6, #10
    bne ov001_021e9178_L364
    cmp r7, r8
    bgt ov001_021e9178_L360
    ldr r0, =0x02238d7c
    add r1, sp, #60
    ldr r0, [r0, #0x60]
    bl native_fn_02041f74
    mov r0, #90
    ldr r1, [sp, #0x40]
    mul r0, r7, r0
    add r2, r1, #6144
    mov r1, r8
    str r2, [sp, #0x40]
    bl native_fn_02026144
    cmp r0, #0
    mov r0, r0, lsl #12
    ble ov001_021e9178_L294
    bl native_fn_02025a28
    mov r1, r0
    mov r0, #1056964608
    bl native_fn_02024e0c
    b ov001_021e9178_L2a0
ov001_021e9178_L294:
    bl native_fn_02025a28
    mov r1, #1056964608
    bl native_fn_02025ca4
ov001_021e9178_L2a0:
    bl native_fn_020259b4
    ldr r1, =0x0b60b60b
    mov r2, #182
    umull r5, r3, r0, r1
    mla r3, r0, r2, r3
    mov r0, r0, asr #31
    mla r3, r0, r1, r3
    adds r0, r5, #0
    adc r0, r3, #2048
    mov r0, r0, lsl #4
    mov r0, r0, lsr #16
    mov r0, r0, asr #4
    mov r0, r0, lsl #1
    add r1, r0, #1
    ldr r0, =0x020d3fe0
    mov r1, r1, lsl #1
    ldrsh r2, [r0, r1]
    ldr r0, [sp, #0x6c]
    ldr r1, [sp, #0x60]
    rsb r5, r2, #4096
    sub r1, r1, r0
    smull r1, r2, r5, r1
    adds r3, r1, #2048
    ldr r9, [sp, #0x70]
    ldr r1, [sp, #0x64]
    adc r2, r2, #0
    mov r3, r3, lsr #12
    orr r3, r3, r2, lsl #20
    add r2, r0, r3
    sub r0, r1, r9
    mul r0, r7, r0
    mov r1, r8
    str r2, [sp, #0x30]
    bl native_fn_0200235c
    add r1, r9, r0
    ldr r2, [sp, #0x74]
    ldr r0, [sp, #0x68]
    str r1, [sp, #0x34]
    sub r0, r0, r2
    smull r1, r0, r5, r0
    adds r1, r1, #2048
    adc r0, r0, #0
    mov r1, r1, lsr #12
    orr r1, r1, r0, lsl #20
    add r0, r2, r1
    str r0, [sp, #0x38]
    add r7, r7, #1
    b ov001_021e9178_L364
ov001_021e9178_L360:
    mov r6, #20
ov001_021e9178_L364:
    cmp r6, #20
    bne ov001_021e9178_L3e4
    ldr r0, =0x02238d7c
    ldr r2, [sp, #0x30]
    ldr r1, [sp, #0x6c]
    ldr r6, [r0, #0x54]
    add r0, r2, r1
    mov r3, r0, asr #1
    str r3, [sp, #0x6c]
    add r3, r6, #808
    ldr r7, [sp, #0x34]
    ldr r5, [sp, #0x70]
    ldr r2, [sp, #0x38]
    add r5, r7, r5
    mov r12, r5, asr #1
    ldr r1, [sp, #0x74]
    add r0, sp, #60
    add r1, r2, r1
    mov r9, r1, asr #1
    add r7, sp, #84
    ldmia r0, {r0, r1, r2}
    stmia r7, {r0, r1, r2}
    add r5, sp, #72
    str r12, [sp, #0x70]
    str r9, [sp, #0x74]
    ldmia r3, {r0, r1, r2}
    stmia r5, {r0, r1, r2}
    ldr r0, [sp, #0x4c]
    mov r7, #0
    add r0, r0, #6144
    str r0, [sp, #0x4c]
    mov r6, #30
ov001_021e9178_L3e4:
    stmib r4, {r6, r7, r8}
    add r0, sp, #108
    add r3, r4, #20
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    add r0, sp, #96
    add r3, r4, #32
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    add r0, sp, #84
    add r3, r4, #44
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    add r0, sp, #72
    add r3, r4, #56
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    add r0, sp, #48
    add r5, r4, #68
    ldmia r0, {r0, r1, r2}
    stmia r5, {r0, r1, r2}
    add r0, sp, #60
    add r3, r4, #80
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    mov r0, #0
    add sp, sp, #120
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
