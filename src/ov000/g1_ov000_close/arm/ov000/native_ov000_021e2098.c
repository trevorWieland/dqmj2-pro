/* ov000 row 0x021e2098: 180 bytes.
 *
 * What it does: 43 instructions; 3 call(s) to 0x021d8c80, 0x021d8c80, 0x021d8c80; loops (back edge at +0x24); returns through pop {r3, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xac -> constant 0x022322c4 (image word 0x022322c4)
 *   pool +0xb0 -> native_data_0222ebec (image word 0x0222ebec)
 *   branch +0x14 -> +0x2c
 *   branch +0x28 -> +0xa4
 *   branch +0x34 -> +0xa4
 *   branch +0x3c -> +0x70
 *   branch +0x6c -> +0xa4
 *   branch +0x74 -> +0xa4
 *   test +0x10 tst r1, #2
 *   test +0x30 tst r0, #2
 *   test +0x38 tst r1, #64
 *   test +0x54 cmp r1, #2
 *   test +0x70 tst r1, #128
 *   test +0x8c cmp r1, #0
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e2098; the literal pool and
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

extern u8 native_data_0222ebec[];
extern void native_fn_021d8c80(void);


asm u32 native_ov000_021e2098 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r0, =0x022322c4
    ldr r0, [r0, #0x4]
    ldrh r1, [r0, #2]
    tst r1, #2
    beq ov000_021e2098_L2c
    ldr r1, =native_data_0222ebec
    mov r0, #1
    strb r0, [r1]
    bl native_fn_021d8c80
    b ov000_021e2098_La4
ov000_021e2098_L2c:
    ldrh r0, [r0]
    tst r0, #2
    beq ov000_021e2098_La4
    tst r1, #64
    beq ov000_021e2098_L70
    ldr r0, =native_data_0222ebec
    ldrsb r1, [r0]
    add r1, r1, #1
    strb r1, [r0]
    ldrsb r1, [r0]
    cmp r1, #2
    movgt r1, #2
    strgtb r1, [r0]
    ldr r0, =native_data_0222ebec
    ldrsb r0, [r0]
    bl native_fn_021d8c80
    b ov000_021e2098_La4
ov000_021e2098_L70:
    tst r1, #128
    beq ov000_021e2098_La4
    ldr r0, =native_data_0222ebec
    ldrsb r1, [r0]
    sub r1, r1, #1
    strb r1, [r0]
    ldrsb r1, [r0]
    cmp r1, #0
    movlt r1, #0
    strltb r1, [r0]
    ldr r0, =native_data_0222ebec
    ldrsb r0, [r0]
    bl native_fn_021d8c80
ov000_021e2098_La4:
    mov r0, #0
    ldmia sp!, {r3, pc}
}
