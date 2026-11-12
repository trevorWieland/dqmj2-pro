/* ov000 row 0x021f662c: 220 bytes.
 *
 * What it does: 54 instructions; 3 call(s) to 0x02003e54, 0x021f66f0, 0x021f6668; loops (back edge at +0x3c); returns through pop {r3, r4, r5, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xd8 -> constant 0x02236ee4 (image word 0x02236ee4)
 *   branch +0x98 -> +0xc4
 *   branch +0xa4 -> +0xc4
 *   back edge +0xcc -> +0x3c
 *   test +0x10 cmp r1, r0
 *   test +0x2c cmp r0, #15
 *   test +0x94 cmp r0, #15
 *   test +0xa0 cmp r2, #0
 *   test +0xc8 cmp r4, #2
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f662c; the literal pool and
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

extern void native_fn_02003e54(void);


asm u32 native_ov000_021f662c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    ldr r5, =0x02236ee4
    mvn r0, #0
    ldrsb r1, [r5, #3]
    cmp r1, r0
    moveq r0, #1
    ldmeqia sp!, {r3, r4, r5, pc}
    ldr r0, [r5, #0x10]
    ldrh r0, [r0]
    mov r0, r0, lsl #28
    mov r0, r0, lsr #28
    cmp r0, #15
    moveq r0, #1
    ldmeqia sp!, {r3, r4, r5, pc}
    mov r4, #0
ov000_021f662c_L3c:
    bl native_fn_02003e54
    ldr r1, [r5, #0x10]
    ldrh r3, [r1]
    mov r1, r3, lsl #18
    mov r1, r1, lsr #27
    mov r2, r3, lsl #23
    mov r1, r1, lsl #5
    add r1, r1, r2, lsr #27
    mov r12, r1, lsl #1
    ldrh r2, [r0, r12]
    mov r1, r3, lsl #28
    mov r1, r1, lsr #28
    bic r2, r2, #61440
    mov r1, r1, lsl #28
    orr r1, r2, r1, lsr #16
    strh r1, [r0, r12]
    ldr r0, [r5, #0x10]
    add r1, r0, #2
    str r1, [r5, #0x10]
    ldrh r0, [r0, #2]
    mov r0, r0, lsl #28
    mov r0, r0, lsr #28
    cmp r0, #15
    bne ov000_021f662c_Lc4
    ldrsb r2, [r5, #3]
    cmp r2, #0
    ble ov000_021f662c_Lc4
    ldr r0, =0x02236ee4
    add r1, r1, #2
    str r1, [r0, #0x10]
    sub r1, r2, #1
    strb r1, [r0, #0x3]
    mov r0, #0
    ldmia sp!, {r3, r4, r5, pc}
ov000_021f662c_Lc4:
    add r4, r4, #1
    cmp r4, #2
    blt ov000_021f662c_L3c
    mov r0, #0
    ldmia sp!, {r3, r4, r5, pc}
}
