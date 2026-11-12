/* ov000 row 0x021eae2c: 516 bytes.
 *
 * What it does: 127 instructions; 7 call(s) to 0x02044cdc, 0x0200235c, 0x0205caf4, +4 more; loops (back edge at +0x38); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x1fc -> constant 0x02236950 (image word 0x02236950)
 *   pool +0x200 -> constant 0x0000013b (image word 0x0000013b)
 *   branch +0x40 -> +0x19c
 *   branch +0x198 -> +0x1bc
 *   test +0x18 cmp r0, #0
 *   test +0x2c cmp r2, r1
 *   test +0x3c cmp r0, #2
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021eae2c; the literal pool and
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

extern void native_fn_02044cdc(void);
extern void native_fn_0200235c(void);
extern void native_fn_0205caf4(void);
extern void native_fn_021eaa0c(void);
extern void native_fn_0205ce38(void);
extern void native_fn_0205cea4(void);


asm u32 native_ov000_021eae2c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #20
    ldr r1, =0x02236950
    ldr r0, [r1, #0x18]
    add r0, r0, #256
    ldrsh r0, [r0, #240]
    cmp r0, #0
    addeq sp, sp, #20
    ldmeqia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    ldr r2, [r1, #0x28]
    mvn r1, #0
    cmp r2, r1
    addne sp, sp, #20
    ldmneia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    bl native_fn_02044cdc
    cmp r0, #2
    bne ov000_021eae2c_L19c
    ldr r1, =0x02236950
    ldr r0, [r1, #0x20]
    ldr r7, [r1, #0x18]
    ldr r6, [r0, #0x8]
    ldr r2, [r0, #0x14]
    ldr r9, [r0, #0xc]
    ldr r3, [r0, #0x18]
    sub r5, r2, r6
    ldr r4, [r7, #0x1e0]
    sub r8, r3, r9
    ldr r3, [r0, #0x10]
    ldr r1, [r7, #0x1e4]
    ldr r2, [r7, #0x1e8]
    ldr r0, [r0, #0x1c]
    sub r6, r4, r6
    sub r7, r2, r3
    sub r4, r0, r3
    smull r0, r3, r7, r4
    sub r1, r1, r9
    adds r9, r0, #2048
    smull r0, r2, r6, r5
    adc r12, r3, #0
    adds r3, r0, #2048
    mov lr, r9, lsr #12
    smull r9, r0, r1, r8
    adc r2, r2, #0
    adds r1, r9, #2048
    smull r9, r10, r4, r4
    adc r0, r0, #0
    mov r3, r3, lsr #12
    mov r1, r1, lsr #12
    str r10, [sp, #0xc]
    adds r11, r9, #2048
    smull r9, r10, r5, r5
    orr r3, r3, r2, lsl #20
    orr r1, r1, r0, lsl #20
    add r0, r3, r1
    ldr r1, [sp, #0xc]
    orr lr, lr, r12, lsl #20
    adc r2, r1, #0
    mov r1, r11, lsr #12
    str r9, [sp, #0x10]
    str r10, [sp]
    smull r10, r9, r8, r8
    orr r1, r1, r2, lsl #20
    ldr r2, [sp, #0x10]
    add r0, lr, r0
    adds r3, r2, #2048
    ldr r2, [sp]
    mov r8, r3, lsr #12
    adc r2, r2, #0
    orr r8, r8, r2, lsl #20
    mov r2, r10
    adds r3, r2, #2048
    mov r2, r9
    adc r2, r2, #0
    mov r3, r3, lsr #12
    orr r3, r3, r2, lsl #20
    add r2, r8, r3
    add r1, r1, r2
    str r9, [sp, #0x8]
    str r10, [sp, #0x4]
    bl native_fn_0200235c
    smull r5, r3, r0, r5
    smull r2, r1, r0, r4
    adds r4, r5, #2048
    adc r0, r3, #0
    mov r3, r4, lsr #12
    orr r3, r3, r0, lsl #20
    adds r2, r2, #2048
    adc r0, r1, #0
    mov r1, r2, lsr #12
    orr r1, r1, r0, lsl #20
    sub r4, r3, r6
    sub r3, r1, r7
    ldr r1, =0x02236950
    ldr r0, =0x0000013b
    ldr r5, [r1, #0x18]
    ldr r1, [r5, #0x1e0]
    ldr r2, [r5, #0x1e4]
    add r1, r1, r4
    ldr r4, [r5, #0x1e8]
    add r3, r4, r3
    bl native_fn_0205caf4
    ldr r1, =0x02236950
    b ov000_021eae2c_L1bc
ov000_021eae2c_L19c:
    ldr r1, =0x02236950
    ldr r0, =0x0000013b
    ldr r3, [r1, #0x18]
    ldr r1, [r3, #0x1e0]
    ldr r2, [r3, #0x1e4]
    ldr r3, [r3, #0x1e8]
    bl native_fn_0205caf4
    ldr r1, =0x02236950
ov000_021eae2c_L1bc:
    str r0, [r1, #0x28]
    ldr r0, =0x02236950
    ldr r0, [r0, #0x18]
    add r0, r0, #256
    ldrsh r0, [r0, #240]
    bl native_fn_021eaa0c
    ldr r2, =0x02236950
    mov r1, r0
    ldr r0, [r2, #0x28]
    bl native_fn_0205ce38
    ldr r0, =0x02236950
    mov r1, #1
    ldr r0, [r0, #0x28]
    bl native_fn_0205cea4
    add sp, sp, #20
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
