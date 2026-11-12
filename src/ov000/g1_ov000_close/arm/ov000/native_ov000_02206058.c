/* ov000 row 0x02206058: 180 bytes.
 *
 * What it does: 44 instructions; 4 call(s) to 0x0205e434, 0x02041510, 0x0205f210, +1 more; loops (back edge at +0x08); returns through pop {r4, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xb0 -> constant 0x022381a8 (image word 0x022381a8)
 *   branch +0x3c -> +0xa8
 *   branch +0x44 -> +0x84
 *   branch +0x54 -> +0xa8
 *   branch +0x80 -> +0xa8
 *   branch +0x88 -> +0xa8
 *   test +0x0c cmp r0, #0
 *   test +0x28 cmp r1, #0
 *   test +0x40 cmp r1, #5
 *   test +0x50 cmp r1, r0
 *   test +0x84 cmp r1, #10
 *   test +0x90 cmp r0, #1
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02206058; the literal pool and
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

extern void native_fn_0205e434(void);
extern void native_fn_02041510(void);
extern void native_fn_0205f210(void);
extern void native_fn_02041800(void);


asm u32 native_ov000_02206058 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r4, #0
    bl native_fn_0205e434
    cmp r0, #0
    movne r1, r4
    ldrne r0, =0x022381a8
    movne r4, #1
    strne r1, [r0, #0x8]
    ldr r0, =0x022381a8
    ldr r1, [r0, #0x8]
    cmp r1, #0
    moveq r1, #1
    streq r1, [r0, #0x4]
    moveq r1, #5
    streq r1, [r0, #0x8]
    beq ov000_02206058_La8
    cmp r1, #5
    bne ov000_02206058_L84
    ldrsb r1, [r0]
    ldrsb r0, [r0, #1]
    cmp r1, r0
    beq ov000_02206058_La8
    mov r0, #1
    mov r1, #2
    mov r2, #10
    bl native_fn_02041510
    mov r0, #0
    mov r1, #7
    bl native_fn_0205f210
    ldr r0, =0x022381a8
    mov r1, #10
    str r1, [r0, #0x8]
    b ov000_02206058_La8
ov000_02206058_L84:
    cmp r1, #10
    bne ov000_02206058_La8
    bl native_fn_02041800
    cmp r0, #1
    ldrne r0, =0x022381a8
    movne r1, #0
    strne r1, [r0, #0x8]
    strne r1, [r0, #0x4]
    movne r4, #1
ov000_02206058_La8:
    mov r0, r4
    ldmia sp!, {r4, pc}
}
