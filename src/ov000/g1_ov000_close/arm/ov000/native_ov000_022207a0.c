/* ov000 row 0x022207a0: 304 bytes.
 *
 * What it does: 74 instructions; 7 call(s) to 0x022207cc, 0x02220680, 0x02220680, +4 more; loops (back edge at +0x38); returns through pop {r4, r5, r6, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x128 -> constant 0x022463b0 (image word 0x022463b0)
 *   pool +0x12c -> constant 0x022463dc (image word 0x022463dc)
 *   branch +0x18 -> +0x2c
 *   branch +0x20 -> +0xb8
 *   branch +0x28 -> +0xb8
 *   branch +0x30 -> +0x50
 *   branch +0x40 -> +0x70
 *   branch +0x54 -> +0x70
 *   branch +0xb4 -> +0x11c
 *   branch +0xc4 -> +0x110
 *   branch +0x100 -> +0x11c
 *   test +0x14 cmp r4, #1
 *   test +0x1c cmp r5, #0
 *   test +0x24 cmp r4, #2
 *   test +0x2c cmp r4, #0
 *   test +0x3c cmp r0, #0
 *   test +0x50 cmp r4, #1
 *   test +0x60 cmp r0, #0
 *   test +0xc0 cmp r0, #0
 *   test +0xc8 cmp r5, #0
 *   test +0xfc cmp r0, #0
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022207a0; the literal pool and
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

extern void native_fn_02220680(void);
extern void native_fn_0221c8dc(void);
extern void native_fn_02049008(void);
extern void native_fn_02220714(void);
extern void native_fn_02220778(void);


asm u32 native_ov000_022207a0 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    sub sp, sp, #8
    mov r6, r0
    ldr r4, [r6]
    mov r5, r1
    cmp r4, #1
    ble ov000_022207a0_L2c
    cmp r5, #0
    beq ov000_022207a0_Lb8
    cmp r4, #2
    bne ov000_022207a0_Lb8
ov000_022207a0_L2c:
    cmp r4, #0
    bne ov000_022207a0_L50
    mov r0, #0
    bl native_fn_02220680
    cmp r0, #0
    bne ov000_022207a0_L70
    add sp, sp, #8
    mov r0, #0
    ldmia sp!, {r4, r5, r6, pc}
ov000_022207a0_L50:
    cmp r4, #1
    bne ov000_022207a0_L70
    mov r0, #1
    bl native_fn_02220680
    cmp r0, #0
    addeq sp, sp, #8
    moveq r0, #0
    ldmeqia sp!, {r4, r5, r6, pc}
ov000_022207a0_L70:
    mov r0, #4
    mov r1, #3
    str r0, [sp]
    mov r3, #1
    mov r0, r6
    mov r2, r1
    str r3, [sp, #0x4]
    mov r3, #10
    bl native_fn_0221c8dc
    mov r0, r6
    str r4, [r6]
    mov r12, #2
    mov r1, #10
    mov r2, #4
    mov r3, #1
    str r12, [sp]
    bl native_fn_02049008
    b ov000_022207a0_L11c
ov000_022207a0_Lb8:
    mov r0, r5
    bl native_fn_02220714
    cmp r0, #0
    beq ov000_022207a0_L110
    cmp r5, #0
    ldr r1, [r6]
    ldrne r0, =0x022463b0
    subne r1, r1, #3
    ldreq r0, =0x022463b0
    subeq r1, r1, #2
    strb r1, [r0, #0x3]
    ldr r0, =0x022463b0
    ldr r1, =0x022463dc
    ldrb r0, [r0, #0x3]
    mov r0, r0, lsl #1
    ldrsh r0, [r1, r0]
    bl native_fn_02220778
    cmp r0, #0
    bne ov000_022207a0_L11c
    add sp, sp, #8
    mov r0, #0
    ldmia sp!, {r4, r5, r6, pc}
ov000_022207a0_L110:
    add sp, sp, #8
    mov r0, #0
    ldmia sp!, {r4, r5, r6, pc}
ov000_022207a0_L11c:
    mov r0, #1
    add sp, sp, #8
    ldmia sp!, {r4, r5, r6, pc}
}
