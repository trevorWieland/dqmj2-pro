/* ov000 row 0x021d915c: 112 bytes.
 *
 * What it does: 28 instructions; 1 call(s) to 0x02002480; loops (back edge at +0x4c); returns through pop {r3, r4, r5, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x34 -> +0x44
 *   branch +0x40 -> +0x5c
 *   test +0x0c cmp r4, #0
 *   test +0x2c cmp r1, #0
 *   test +0x30 cmpne r0, #0
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021d915c; the literal pool and
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


asm u32 native_ov000_021d915c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    ldr r4, [r5, #0xb0]
    cmp r4, #0
    ldmeqia sp!, {r3, r4, r5, pc}
    ldr r1, [r5, #0x4]
    ldr r0, [r4, #0xc]
    ldr r1, [r1, #0x2c]
    and r0, r0, #2031616
    ldrb r1, [r1, #0x172]
    mov r0, r0, lsr #16
    cmp r1, #0
    cmpne r0, #0
    bne ov000_021d915c_L44
    ldr r0, [r4, #0xc]
    bic r0, r0, #2031616
    b ov000_021d915c_L5c
ov000_021d915c_L44:
    mul r0, r1, r0
    mov r1, #31
    bl native_fn_02002480
    ldr r1, [r4, #0xc]
    bic r1, r1, #2031616
    orr r0, r1, r0, lsl #16
ov000_021d915c_L5c:
    str r0, [r4, #0xc]
    mov r0, #0
    str r0, [r5, #0x1c]
    strb r0, [r5, #0x90]
    ldmia sp!, {r3, r4, r5, pc}
}
