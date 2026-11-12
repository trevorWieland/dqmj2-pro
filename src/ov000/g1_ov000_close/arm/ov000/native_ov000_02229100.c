/* ov000 row 0x02229100: 1644 bytes.
 *
 * What it does: 407 instructions; 24 call(s) to 0x02062a10, 0x02062a10, 0x02044e44, +21 more; loops (back edge at +0x14); returns through pop {r4, r5, r6, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: block load.
 *
 *   pool +0x65c -> constant 0x02247480 (image word 0x02247480)
 *   pool +0x660 -> constant 0x022474c8 (image word 0x022474c8)
 *   pool +0x664 -> constant 0x0224751a (image word 0x0224751a)
 *   pool +0x668 -> constant 0x0224752e (image word 0x0224752e)
 *   branch +0xe4 -> +0x120
 *   branch +0x160 -> +0x19c
 *   branch +0x1dc -> +0x218
 *   branch +0x258 -> +0x294
 *   branch +0x2d4 -> +0x310
 *   branch +0x350 -> +0x38c
 *   branch +0x3d4 -> +0x418
 *   branch +0x3f4 -> +0x408
 *   branch +0x404 -> +0x40c
 *   branch +0x414 -> +0x488
 *   branch +0x41c -> +0x468
 *   branch +0x42c -> +0x44c
 *   branch +0x448 -> +0x488
 *   branch +0x464 -> +0x488
 *   branch +0x5a8 -> +0x5bc
 *   branch +0x5c0 -> +0x5d4
 *   branch +0x5d8 -> +0x5ec
 *   branch +0x5f0 -> +0x604
 *   branch +0x608 -> +0x61c
 *   test +0xe0 cmp r6, r0
 *   test +0x15c cmp r6, r0
 *   test +0x1d8 cmp r6, r0
 *   test +0x254 cmp r6, r0
 *   test +0x2d0 cmp r6, r0
 *   test +0x34c cmp r6, r0
 *   test +0x3d0 cmp r0, #20
 *   test +0x3e0 cmp r2, r1
 *   test +0x3f0 cmp r0, #99
 *   test +0x3f8 cmp r2, r1
 *   test +0x418 cmp r0, #40
 *   test +0x428 cmp r0, r1
 *   test +0x438 cmp r1, #99
 *   test +0x454 cmp r1, #99
 *   test +0x478 cmp r1, #99
 *   test +0x498 cmp r1, #0
 *   test +0x54c cmp r1, r2
 *   test +0x564 cmp r1, #99
 *   test +0x584 tst r1, #1
 *   test +0x5a4 cmp lr, #0
 *   test +0x5bc cmp r0, #0
 *   test +0x5d4 cmp r1, #0
 *   test +0x5ec cmp r2, #0
 *   test +0x604 cmp r3, #0
 *   test +0x644 cmp r2, r1
 *   1 block transfer(s), 72 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02229100; the literal pool and
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

extern void native_fn_02062a10(void);
extern void native_fn_02044e44(void);
extern void native_fn_02044e80(void);
extern void native_fn_02044ebc(void);
extern void native_fn_02044ef8(void);
extern void native_fn_02044f34(void);
extern void native_fn_02044f70(void);
extern void native_fn_020634cc(void);
extern void native_fn_02008e0c(void);


asm u32 native_ov000_02229100 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    sub sp, sp, #8
    mov r6, r1
    mov r5, r2
    mov r4, r3
    bl native_fn_02062a10
    ldr r1, =0x02247480
    str r0, [r1, #0x4]
    mov r0, r6
    bl native_fn_02062a10
    ldr r2, =0x02247480
    ldr r1, =0x022474c8
    str r0, [r2, #0x8]
    ldr r3, [r2, #0x4]
    strh r5, [r1, #24]
    strb r4, [r1, #0x1a]
    ldrsh r6, [r3, #32]
    ldrsh r2, [r0, #32]
    add r2, r6, r2
    mov r2, r2, asr #2
    strh r2, [r1, #32]
    ldrsh r6, [r3, #34]
    ldrsh r2, [r0, #34]
    add r2, r6, r2
    mov r2, r2, asr #2
    strh r2, [r1, #34]
    ldrsh r6, [r3, #40]
    ldrsh r2, [r0, #40]
    add r2, r6, r2
    mov r2, r2, asr #2
    strh r2, [r1, #40]
    ldrsh r6, [r3, #42]
    ldrsh r2, [r0, #42]
    add r2, r6, r2
    mov r2, r2, asr #2
    strh r2, [r1, #42]
    ldrsh r6, [r3, #44]
    ldrsh r2, [r0, #44]
    add r2, r6, r2
    mov r2, r2, asr #2
    strh r2, [r1, #44]
    ldrsh r6, [r3, #46]
    ldrsh r2, [r0, #46]
    add r2, r6, r2
    mov r2, r2, asr #2
    strh r2, [r1, #46]
    ldrsh r6, [r1, #32]
    ldrsh r2, [r0, #24]
    str r2, [sp]
    ldrb r0, [r0, #0x1a]
    str r0, [sp, #0x4]
    ldrsh r0, [r1, #24]
    ldrb r1, [r1, #0x1a]
    ldrsh r2, [r3, #24]
    ldrb r3, [r3, #0x1a]
    bl native_fn_02044e44
    cmp r6, r0
    blt ov000_02229100_L120
    ldr r0, =0x02247480
    ldr r1, =0x022474c8
    ldr r2, [r0, #0x8]
    ldr r3, [r0, #0x4]
    ldrsh r0, [r2, #24]
    str r0, [sp]
    ldrb r0, [r2, #0x1a]
    str r0, [sp, #0x4]
    ldrsh r0, [r1, #24]
    ldrb r1, [r1, #0x1a]
    ldrsh r2, [r3, #24]
    ldrb r3, [r3, #0x1a]
    bl native_fn_02044e44
    mov r6, r0
ov000_02229100_L120:
    ldr r1, =0x022474c8
    ldr r0, =0x02247480
    strh r6, [r1, #32]
    ldr r12, [r0, #0x8]
    ldrsh r6, [r1, #34]
    ldrsh r2, [r12, #24]
    ldr r3, [r0, #0x4]
    str r2, [sp]
    ldrb r0, [r12, #0x1a]
    str r0, [sp, #0x4]
    ldrsh r0, [r1, #24]
    ldrb r1, [r1, #0x1a]
    ldrsh r2, [r3, #24]
    ldrb r3, [r3, #0x1a]
    bl native_fn_02044e80
    cmp r6, r0
    blt ov000_02229100_L19c
    ldr r0, =0x02247480
    ldr r1, =0x022474c8
    ldr r2, [r0, #0x8]
    ldr r3, [r0, #0x4]
    ldrsh r0, [r2, #24]
    str r0, [sp]
    ldrb r0, [r2, #0x1a]
    str r0, [sp, #0x4]
    ldrsh r0, [r1, #24]
    ldrb r1, [r1, #0x1a]
    ldrsh r2, [r3, #24]
    ldrb r3, [r3, #0x1a]
    bl native_fn_02044e80
    mov r6, r0
ov000_02229100_L19c:
    ldr r1, =0x022474c8
    ldr r0, =0x02247480
    strh r6, [r1, #34]
    ldr r12, [r0, #0x8]
    ldrsh r6, [r1, #40]
    ldrsh r2, [r12, #24]
    ldr r3, [r0, #0x4]
    str r2, [sp]
    ldrb r0, [r12, #0x1a]
    str r0, [sp, #0x4]
    ldrsh r0, [r1, #24]
    ldrb r1, [r1, #0x1a]
    ldrsh r2, [r3, #24]
    ldrb r3, [r3, #0x1a]
    bl native_fn_02044ebc
    cmp r6, r0
    blt ov000_02229100_L218
    ldr r0, =0x02247480
    ldr r1, =0x022474c8
    ldr r2, [r0, #0x8]
    ldr r3, [r0, #0x4]
    ldrsh r0, [r2, #24]
    str r0, [sp]
    ldrb r0, [r2, #0x1a]
    str r0, [sp, #0x4]
    ldrsh r0, [r1, #24]
    ldrb r1, [r1, #0x1a]
    ldrsh r2, [r3, #24]
    ldrb r3, [r3, #0x1a]
    bl native_fn_02044ebc
    mov r6, r0
ov000_02229100_L218:
    ldr r1, =0x022474c8
    ldr r0, =0x02247480
    strh r6, [r1, #40]
    ldr r12, [r0, #0x8]
    ldrsh r6, [r1, #42]
    ldrsh r2, [r12, #24]
    ldr r3, [r0, #0x4]
    str r2, [sp]
    ldrb r0, [r12, #0x1a]
    str r0, [sp, #0x4]
    ldrsh r0, [r1, #24]
    ldrb r1, [r1, #0x1a]
    ldrsh r2, [r3, #24]
    ldrb r3, [r3, #0x1a]
    bl native_fn_02044ef8
    cmp r6, r0
    blt ov000_02229100_L294
    ldr r0, =0x02247480
    ldr r1, =0x022474c8
    ldr r2, [r0, #0x8]
    ldr r3, [r0, #0x4]
    ldrsh r0, [r2, #24]
    str r0, [sp]
    ldrb r0, [r2, #0x1a]
    str r0, [sp, #0x4]
    ldrsh r0, [r1, #24]
    ldrb r1, [r1, #0x1a]
    ldrsh r2, [r3, #24]
    ldrb r3, [r3, #0x1a]
    bl native_fn_02044ef8
    mov r6, r0
ov000_02229100_L294:
    ldr r1, =0x022474c8
    ldr r0, =0x02247480
    strh r6, [r1, #42]
    ldr r12, [r0, #0x8]
    ldrsh r6, [r1, #44]
    ldrsh r2, [r12, #24]
    ldr r3, [r0, #0x4]
    str r2, [sp]
    ldrb r0, [r12, #0x1a]
    str r0, [sp, #0x4]
    ldrsh r0, [r1, #24]
    ldrb r1, [r1, #0x1a]
    ldrsh r2, [r3, #24]
    ldrb r3, [r3, #0x1a]
    bl native_fn_02044f34
    cmp r6, r0
    blt ov000_02229100_L310
    ldr r0, =0x02247480
    ldr r1, =0x022474c8
    ldr r2, [r0, #0x8]
    ldr r3, [r0, #0x4]
    ldrsh r0, [r2, #24]
    str r0, [sp]
    ldrb r0, [r2, #0x1a]
    str r0, [sp, #0x4]
    ldrsh r0, [r1, #24]
    ldrb r1, [r1, #0x1a]
    ldrsh r2, [r3, #24]
    ldrb r3, [r3, #0x1a]
    bl native_fn_02044f34
    mov r6, r0
ov000_02229100_L310:
    ldr r1, =0x022474c8
    ldr r0, =0x02247480
    strh r6, [r1, #44]
    ldr r12, [r0, #0x8]
    ldrsh r6, [r1, #46]
    ldrsh r2, [r12, #24]
    ldr r3, [r0, #0x4]
    str r2, [sp]
    ldrb r0, [r12, #0x1a]
    str r0, [sp, #0x4]
    ldrsh r0, [r1, #24]
    ldrb r1, [r1, #0x1a]
    ldrsh r2, [r3, #24]
    ldrb r3, [r3, #0x1a]
    bl native_fn_02044f70
    cmp r6, r0
    blt ov000_02229100_L38c
    ldr r0, =0x02247480
    ldr r1, =0x022474c8
    ldr r2, [r0, #0x8]
    ldr r3, [r0, #0x4]
    ldrsh r0, [r2, #24]
    str r0, [sp]
    ldrb r0, [r2, #0x1a]
    str r0, [sp, #0x4]
    ldrsh r0, [r1, #24]
    ldrb r1, [r1, #0x1a]
    ldrsh r2, [r3, #24]
    ldrb r3, [r3, #0x1a]
    bl native_fn_02044f70
    mov r6, r0
ov000_02229100_L38c:
    ldr r3, =0x022474c8
    mov r0, r5
    strh r6, [r3, #46]
    ldrsh r5, [r3, #32]
    mov r1, r4
    mov r2, #2
    strh r5, [r3, #36]
    ldrsh r4, [r3, #34]
    strh r4, [r3, #38]
    bl native_fn_020634cc
    ldr r2, =0x022474c8
    ldr r1, =0x02247480
    str r0, [r2, #0x38]
    ldmib r1, {r2, r3}
    ldrb r0, [r3, #0x30]
    ldrb r1, [r2, #0x30]
    add r0, r1, r0
    cmp r0, #20
    bgt ov000_02229100_L418
    ldrb r1, [r3, #0x1c]
    ldrb r2, [r2, #0x1c]
    cmp r2, r1
    movhi r0, r2
    movls r0, r1
    add r0, r0, #1
    cmp r0, #99
    bge ov000_02229100_L408
    cmp r2, r1
    movls r2, r1
    add r1, r2, #1
    b ov000_02229100_L40c
ov000_02229100_L408:
    mov r1, #99
ov000_02229100_L40c:
    ldr r0, =0x022474c8
    strb r1, [r0, #0x1c]
    b ov000_02229100_L488
ov000_02229100_L418:
    cmp r0, #40
    bgt ov000_02229100_L468
    ldrb r1, [r3, #0x1c]
    ldrb r0, [r2, #0x1c]
    cmp r0, r1
    blo ov000_02229100_L44c
    add r0, r0, r1, lsr #1
    add r1, r0, #1
    cmp r1, #99
    ldr r0, =0x022474c8
    movge r1, #99
    strb r1, [r0, #0x1c]
    b ov000_02229100_L488
ov000_02229100_L44c:
    add r0, r1, r0, lsr #1
    add r1, r0, #1
    cmp r1, #99
    ldr r0, =0x022474c8
    movge r1, #99
    strb r1, [r0, #0x1c]
    b ov000_02229100_L488
ov000_02229100_L468:
    ldrb r1, [r2, #0x1c]
    ldrb r0, [r3, #0x1c]
    add r0, r1, r0
    add r1, r0, #1
    cmp r1, #99
    ldr r0, =0x022474c8
    movge r1, #99
    strb r1, [r0, #0x1c]
ov000_02229100_L488:
    ldr r0, =0x022474c8
    ldr r3, =0x022474c8
    ldrsh r1, [r0, #32]
    mov r2, #20
    cmp r1, #0
    movle r1, #1
    strleh r1, [r0, #36]
    strleh r1, [r0, #32]
    ldr r0, =0x02247480
    ldr r1, =0x0224751a
    ldr r0, [r0, #0x4]
    ldrsh r4, [r0, #24]
    strh r4, [r3, #64]
    ldrb r4, [r0, #0x1a]
    strb r4, [r3, #0x4c]
    bl native_fn_02008e0c
    ldr r0, =0x02247480
    ldr r3, =0x022474c8
    ldr r0, [r0, #0x8]
    ldr r1, =0x0224752e
    ldrsh r4, [r0, #24]
    mov r2, #20
    strh r4, [r3, #66]
    ldrb r4, [r0, #0x1a]
    strb r4, [r3, #0x4d]
    bl native_fn_02008e0c
    ldr r1, =0x02247480
    ldr r0, =0x022474c8
    ldr r4, [r1, #0x4]
    ldr r6, =0x022474c8
    ldrsh r2, [r4, #64]
    strh r2, [r0, #68]
    ldrb r2, [r4, #0x4c]
    strb r2, [r0, #0x4e]
    ldrsh r2, [r4, #66]
    strh r2, [r0, #72]
    ldrb r2, [r4, #0x4d]
    strb r2, [r0, #0x50]
    ldr r5, [r1, #0x8]
    ldrsh r1, [r5, #64]
    strh r1, [r0, #70]
    ldrb r1, [r5, #0x4c]
    strb r1, [r0, #0x4f]
    ldrsh r1, [r5, #66]
    strh r1, [r0, #74]
    ldrb r1, [r5, #0x4d]
    strb r1, [r0, #0x51]
    ldrb r2, [r5, #0x1e]
    ldrb r1, [r4, #0x1e]
    cmp r1, r2
    addhi r1, r1, #1
    addls r1, r2, #1
    strb r1, [r0, #0x1e]
    ldr r0, =0x022474c8
    ldrb r1, [r0, #0x1e]
    cmp r1, #99
    movhi r1, #99
    strhib r1, [r0, #0x1e]
    ldrb r3, [r5, #0x1d]
    ldrb r1, [r4, #0x1d]
    mov r0, #0
    and lr, r3, #1
    strb r0, [r6, #0x1d]
    tst r1, #1
    ldrneb r12, [r6, #0x1d]
    and r0, r1, #2
    and r2, r3, #2
    orrne r12, r12, #2
    strneb r12, [r6, #0x1d]
    and r1, r1, #4
    and r3, r3, #4
    cmp lr, #0
    beq ov000_02229100_L5bc
    ldr r6, =0x022474c8
    ldrb r12, [r6, #0x1d]
    orr r12, r12, #4
    strb r12, [r6, #0x1d]
ov000_02229100_L5bc:
    cmp r0, #0
    beq ov000_02229100_L5d4
    ldr r0, =0x022474c8
    ldrb r6, [r0, #0x1d]
    orr r6, r6, #8
    strb r6, [r0, #0x1d]
ov000_02229100_L5d4:
    cmp r1, #0
    beq ov000_02229100_L5ec
    ldr r0, =0x022474c8
    ldrb r1, [r0, #0x1d]
    orr r1, r1, #16
    strb r1, [r0, #0x1d]
ov000_02229100_L5ec:
    cmp r2, #0
    beq ov000_02229100_L604
    ldr r0, =0x022474c8
    ldrb r1, [r0, #0x1d]
    orr r1, r1, #32
    strb r1, [r0, #0x1d]
ov000_02229100_L604:
    cmp r3, #0
    beq ov000_02229100_L61c
    ldr r0, =0x022474c8
    ldrb r1, [r0, #0x1d]
    orr r1, r1, #64
    strb r1, [r0, #0x1d]
ov000_02229100_L61c:
    ldr r0, =0x022474c8
    mov r6, #1
    strb r6, [r0, #0x30]
    ldrsh r2, [r4, #60]
    ldrsh r0, [r5, #60]
    ldr r3, [sp, #0x18]
    rsb r1, r6, #1000
    add r0, r2, r0
    add r0, r0, r0, lsr #31
    add r2, r3, r0, asr #1
    cmp r2, r1
    ldr r0, =0x022474c8
    movgt r2, r1
    strh r2, [r0, #60]
    add sp, sp, #8
    ldmia sp!, {r4, r5, r6, pc}
}
