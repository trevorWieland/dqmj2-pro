/* ov001 row 0x021ef398: 308 bytes.
 *
 * What it does: 75 instructions; 9 call(s) to 0x020449d4, 0x0207b02c, 0x0207b02c, +6 more; loops (back edge at +0x10); returns through pop {r3, r4, r5, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 9 calls (75 instructions, 9 calls, 8 branches, 9 back edges, 2 literal slots).
 *
 *   pool +0x12c -> constant 0x80000040 (image word 0x80000040)
 *   pool +0x130 -> constant 0x80000080 (image word 0x80000080)
 *   branch +0x28 -> +0x44
 *   branch +0x48 -> +0x64
 *   branch +0x68 -> +0x84
 *   branch +0x88 -> +0xa4
 *   branch +0xa8 -> +0xc4
 *   branch +0xc8 -> +0xe4
 *   branch +0xe8 -> +0x104
 *   branch +0x108 -> +0x124
 *   test +0x24 cmp r4, #1
 *   test +0x38 cmp r0, #0
 *   test +0x44 cmp r4, #2
 *   test +0x58 cmp r0, #0
 *   test +0x64 cmp r4, #3
 *   test +0x78 cmp r0, #0
 *   test +0x84 cmp r4, #5
 *   test +0x98 cmp r0, #0
 *   test +0xa4 cmp r4, #6
 *   test +0xb8 cmp r0, #0
 *   test +0xc4 cmp r4, #7
 *   test +0xd8 cmp r0, #0
 *   test +0xe4 cmp r4, #8
 *   test +0xf8 cmp r0, #0
 *   test +0x104 cmp r4, #4
 *   test +0x118 cmp r0, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021ef398; the literal pool and
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

extern void native_fn_020449d4(void);
extern void native_fn_0207b02c(void);


asm u32 native_ov001_021ef398 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    ldr r1, [r1, #0x1e8]
    mov r5, r0
    ldrsh r0, [r1, #42]
    bl native_fn_020449d4
    ldrh r0, [r0, #4]
    mov r0, r0, lsl #24
    mov r0, r0, lsr #28
    and r4, r0, #255
    cmp r4, #1
    bne ov001_021ef398_L44
    mov r0, r5
    mov r1, #-2147483647
    bl native_fn_0207b02c
    cmp r0, #0
    movne r0, #1
    ldmneia sp!, {r3, r4, r5, pc}
ov001_021ef398_L44:
    cmp r4, #2
    bne ov001_021ef398_L64
    mov r0, r5
    mov r1, #-2147483646
    bl native_fn_0207b02c
    cmp r0, #0
    movne r0, #1
    ldmneia sp!, {r3, r4, r5, pc}
ov001_021ef398_L64:
    cmp r4, #3
    bne ov001_021ef398_L84
    mov r0, r5
    mov r1, #-2147483644
    bl native_fn_0207b02c
    cmp r0, #0
    movne r0, #1
    ldmneia sp!, {r3, r4, r5, pc}
ov001_021ef398_L84:
    cmp r4, #5
    bne ov001_021ef398_La4
    mov r0, r5
    mov r1, #-2147483632
    bl native_fn_0207b02c
    cmp r0, #0
    movne r0, #1
    ldmneia sp!, {r3, r4, r5, pc}
ov001_021ef398_La4:
    cmp r4, #6
    bne ov001_021ef398_Lc4
    mov r0, r5
    mov r1, #-2147483616
    bl native_fn_0207b02c
    cmp r0, #0
    movne r0, #1
    ldmneia sp!, {r3, r4, r5, pc}
ov001_021ef398_Lc4:
    cmp r4, #7
    bne ov001_021ef398_Le4
    ldr r1, =0x80000040
    mov r0, r5
    bl native_fn_0207b02c
    cmp r0, #0
    movne r0, #1
    ldmneia sp!, {r3, r4, r5, pc}
ov001_021ef398_Le4:
    cmp r4, #8
    bne ov001_021ef398_L104
    ldr r1, =0x80000080
    mov r0, r5
    bl native_fn_0207b02c
    cmp r0, #0
    movne r0, #1
    ldmneia sp!, {r3, r4, r5, pc}
ov001_021ef398_L104:
    cmp r4, #4
    bne ov001_021ef398_L124
    mov r0, r5
    mov r1, #-2147483640
    bl native_fn_0207b02c
    cmp r0, #0
    movne r0, #1
    ldmneia sp!, {r3, r4, r5, pc}
ov001_021ef398_L124:
    mov r0, #0
    ldmia sp!, {r3, r4, r5, pc}
}
