/* ov001 row 0x021eea10: 168 bytes.
 *
 * What it does: 40 instructions; 3 call(s) to 0x021eea28, 0x021eea58, 0x0205c668; loops (back edge at +0x34); returns through pop {r3, r4, r5, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 3 calls (40 instructions, 3 calls, 5 branches, 3 back edges, 2 literal slots).
 *
 *   pool +0xa0 -> constant 0x02238e58 (image word 0x02238e58)
 *   pool +0xa4 -> constant 0x02238e5c (image word 0x02238e5c)
 *   branch +0x28 -> +0x38
 *   back edge +0x34 -> +0x18
 *   branch +0x3c -> +0x84
 *   branch +0x50 -> +0x60
 *   back edge +0x5c -> +0x48
 *   branch +0x64 -> +0x80
 *   branch +0x7c -> +0x84
 *   test +0x1c cmp r5, r2
 *   test +0x30 cmp r12, #32
 *   test +0x38 cmp lr, #0
 *   test +0x4c cmp r0, #0
 *   test +0x58 cmp r4, #32
 *   test +0x60 cmp r4, #32
 *   test +0x70 cmp r0, #0
 *   test +0x84 cmp r0, #0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021eea10; the literal pool and
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

extern void native_fn_0205c668(void);


asm u32 native_ov001_021eea10 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov lr, #0
    mov r5, r0
    ldr r3, =0x02238e58
    mov r12, lr
    mov r0, #1
ov001_021eea10_L18:
    ldr r2, [r3, r12, lsl #3]
    cmp r5, r2
    moveq r4, r12
    moveq lr, #1
    beq ov001_021eea10_L38
    add r12, r12, #1
    cmp r12, #32
    blt ov001_021eea10_L18
ov001_021eea10_L38:
    cmp lr, #0
    bne ov001_021eea10_L84
    ldr r2, =0x02238e58
    mov r4, #0
ov001_021eea10_L48:
    ldr r0, [r2, r4, lsl #3]
    cmp r0, #0
    beq ov001_021eea10_L60
    add r4, r4, #1
    cmp r4, #32
    blt ov001_021eea10_L48
ov001_021eea10_L60:
    cmp r4, #32
    bge ov001_021eea10_L80
    mov r0, r5
    bl native_fn_0205c668
    cmp r0, #0
    ldrne r1, =0x02238e58
    strne r5, [r1, r4, lsl #3]
    b ov001_021eea10_L84
ov001_021eea10_L80:
    mov r0, #0
ov001_021eea10_L84:
    cmp r0, #0
    ldmeqia sp!, {r3, r4, r5, pc}
    ldr r2, =0x02238e5c
    ldrb r1, [r2, r4, lsl #3]
    add r1, r1, #1
    strb r1, [r2, r4, lsl #3]
    ldmia sp!, {r3, r4, r5, pc}
}
