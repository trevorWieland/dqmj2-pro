/* ov000 row 0x02213758: 384 bytes.
 *
 * What it does: 94 instructions; 5 call(s) to 0x021d8a50, 0x021d8aa0, 0x022138b4, +2 more; loops (back edge at +0x0c); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: block load.
 *
 *   pool +0x178 -> constant 0x02243e3c (image word 0x02243e3c)
 *   pool +0x17c -> constant 0x009c4000 (image word 0x009c4000)
 *   branch +0x7c -> +0x15c
 *   branch +0xc8 -> +0x15c
 *   branch +0x14c -> +0x15c
 *   back edge +0x168 -> +0x74
 *   test +0x78 cmp r0, #0
 *   test +0x148 cmp r1, #0
 *   test +0x164 cmp r4, #16
 *   1 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02213758; the literal pool and
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

extern void native_fn_021d8a50(void);
extern void native_fn_021d8aa0(void);
extern void native_fn_0203caa4(void);


asm u32 native_ov000_02213758 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    sub sp, sp, #24
    mov r0, #0
    bl native_fn_021d8a50
    mov r5, r0
    mov r0, #0
    bl native_fn_021d8aa0
    ldr r1, [r5, #0x4]
    ldmia r0, {r3, r4}
    sub r1, r4, r1
    ldr r2, [r5]
    str r1, [sp, #0x10]
    sub r1, r3, r2
    str r1, [sp, #0x8]
    ldr r1, [r0, #0x8]
    ldr r0, [r5, #0x8]
    ldr r6, =0x02243e3c
    sub r0, r1, r0
    str r0, [sp]
    ldr r0, [sp, #0x10]
    mov r4, #0
    mov r0, r0, asr #31
    str r0, [sp, #0x14]
    ldr r0, [sp, #0x8]
    mov r0, r0, asr #31
    str r0, [sp, #0xc]
    ldr r0, [sp]
    mov r0, r0, asr #31
    str r0, [sp, #0x4]
ov000_02213758_L74:
    ldrb r0, [r6, #0x105]
    cmp r0, #0
    beq ov000_02213758_L15c
    ldr r8, [r6, #0x74]
    ldr r7, [r5, #0x4]
    ldr r3, [r6, #0x70]
    sub r0, r7, r8
    smull r9, r12, r0, r0
    ldr r2, [r5]
    ldr r1, [r6, #0x78]
    sub r0, r2, r3
    smlal r9, r12, r0, r0
    ldr r0, [r5, #0x8]
    sub lr, r0, r1
    smlal r9, r12, lr, lr
    mov lr, r9, lsr #12
    ldr r9, =0x009c4000
    orr lr, lr, r12, lsl #20
    subs r9, lr, r9
    mov r9, #0
    rscs r9, r9, r12, asr #12
    bge ov000_02213758_L15c
    sub r12, r1, r0
    ldr lr, [sp]
    sub r1, r8, r7
    mov r9, r12, asr #31
    umull r8, r7, r14, r12
    mla r7, r14, r9, r7
    sub r3, r3, r2
    ldr lr, [sp, #0x4]
    ldr r9, [sp, #0x8]
    mla r7, r14, r12, r7
    mov r2, r3, asr #31
    umull r14, r12, r9, r3
    mla r12, r9, r2, r12
    ldr r2, [sp, #0xc]
    mov r0, r1, asr #31
    mla r12, r2, r3, r12
    ldr r2, [sp, #0x10]
    umull r9, r3, r2, r1
    mla r3, r2, r0, r3
    ldr r0, [sp, #0x14]
    adds r9, lr, r9
    mla r3, r0, r1, r3
    adc r0, r12, r3
    adds r2, r8, r9
    adc r1, r7, r0
    mov r0, #2048
    adds r2, r2, r0
    mov r0, #0
    adc r0, r1, r0
    mov r1, r2, lsr #12
    orr r1, r1, r0, lsl #20
    cmp r1, #0
    ble ov000_02213758_L15c
    mov r0, r6
    mov r1, #65
    bl native_fn_0203caa4
ov000_02213758_L15c:
    add r6, r6, #268
    add r4, r4, #1
    cmp r4, #16
    blt ov000_02213758_L74
    mov r0, #0
    add sp, sp, #24
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
