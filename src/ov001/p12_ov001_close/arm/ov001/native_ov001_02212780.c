/* ov001 row 0x02212780: 148 bytes.
 *
 * What it does: 37 instructions; 2 call(s) to 0x021f1a44, 0x022122ac; loops (back edge at +0x0c); returns through pop {r3, r4, r5, pc}
 *
 * Decoded shape: loop with 2 calls (37 instructions, 2 calls, 4 branches, 2 back edges, 0 literal slots).
 *
 *   branch +0x1c -> +0x2c
 *   branch +0x24 -> +0x4c
 *   branch +0x28 -> +0x80
 *   branch +0x48 -> +0x80
 *   test +0x18 cmp r1, #0
 *   test +0x20 cmp r1, #1
 *   test +0x3c cmp r0, #0
 *   test +0x60 cmp r1, r0
 *   test +0x84 cmp r0, #0
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02212780; the literal pool and
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

extern void native_fn_021f1a44(void);
extern void native_fn_022122ac(void);


asm u32 native_ov001_02212780 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    ldrsb r0, [r5, #8]
    bl native_fn_021f1a44
    ldr r1, [r5, #0x10]
    mov r4, r0
    cmp r1, #0
    beq ov001_02212780_L2c
    cmp r1, #1
    beq ov001_02212780_L4c
    b ov001_02212780_L80
ov001_02212780_L2c:
    ldrsh r0, [r5, #38]
    sub r0, r0, #1
    strh r0, [r5, #38]
    ldrsh r0, [r5, #38]
    cmp r0, #0
    movle r0, #1
    strle r0, [r5, #0x10]
    b ov001_02212780_L80
ov001_02212780_L4c:
    ldr r1, [r5, #0x30]
    ldr r0, [r5, #0x34]
    add r1, r1, r0
    str r1, [r5, #0x30]
    ldr r0, [r5, #0x2c]
    cmp r1, r0
    strge r0, [r5, #0x30]
    movge r0, #2
    strge r0, [r5, #0x10]
    ldr r2, [r5, #0x30]
    mov r0, r5
    mov r1, #7
    bl native_fn_022122ac
ov001_02212780_L80:
    ldrb r0, [r4, #0x23]
    cmp r0, #0
    moveq r0, #1
    movne r0, #0
    ldmia sp!, {r3, r4, r5, pc}
}
