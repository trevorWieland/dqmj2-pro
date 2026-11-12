/* ov001 row 0x021f9350: 200 bytes.
 *
 * What it does: 49 instructions; 4 call(s) to 0x0205e5d8, 0x0205e5d8, 0x0205e5d8, +1 more; loops (back edge at +0x68); returns through pop {r3, r4, r5, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 4 calls (49 instructions, 4 calls, 7 branches, 4 back edges, 1 literal slot).
 *
 *   pool +0xc4 -> native_data_0222e004 (image word 0x0222e004)
 *   branch +0x5c -> +0x70
 *   branch +0x6c -> +0xb8
 *   branch +0x74 -> +0x88
 *   branch +0x84 -> +0xb8
 *   branch +0x8c -> +0xa0
 *   branch +0x9c -> +0xb8
 *   branch +0xa8 -> +0xb8
 *   test +0x0c cmp r0, #0
 *   test +0x70 cmp r0, #1
 *   test +0x88 cmp r0, #3
 *   test +0xa0 cmp r0, #2
 *   0 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f9350; the literal pool and
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

extern u8 native_data_0222e004[];
extern void native_fn_0205e5d8(void);


asm u32 native_ov001_021f9350 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    sub sp, sp, #16
    ldr r2, =native_data_0222e004
    cmp r0, #0
    ldrh r3, [r2, #2]
    mov r4, #1
    add r1, sp, #2
    strh r3, [sp, #2]
    ldrh r12, [r2, #8]
    ldrh r3, [r2, #10]
    add r5, sp, #8
    add lr, sp, #0
    strh r12, [sp, #8]
    strh r3, [sp, #10]
    ldrh r3, [r2, #12]
    add r12, sp, #4
    strh r3, [sp, #12]
    ldrh r3, [r2]
    strh r3, [sp]
    ldrh r3, [r2, #4]
    ldrh r2, [r2, #6]
    strh r3, [sp, #4]
    strh r2, [sp, #6]
    bne ov001_021f9350_L70
    mov r0, r5
    mov r1, #6
    bl native_fn_0205e5d8
    b ov001_021f9350_Lb8
ov001_021f9350_L70:
    cmp r0, #1
    bne ov001_021f9350_L88
    mov r0, lr
    mov r1, #2
    bl native_fn_0205e5d8
    b ov001_021f9350_Lb8
ov001_021f9350_L88:
    cmp r0, #3
    bne ov001_021f9350_La0
    mov r0, r12
    mov r1, #4
    bl native_fn_0205e5d8
    b ov001_021f9350_Lb8
ov001_021f9350_La0:
    cmp r0, #2
    movne r4, #0
    bne ov001_021f9350_Lb8
    mov r0, r1
    mov r1, #2
    bl native_fn_0205e5d8
ov001_021f9350_Lb8:
    mov r0, r4
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, pc}
}
