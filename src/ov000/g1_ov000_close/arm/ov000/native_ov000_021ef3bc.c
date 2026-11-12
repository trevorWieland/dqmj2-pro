/* ov000 row 0x021ef3bc: 184 bytes.
 *
 * What it does: 45 instructions; 5 call(s) to 0x021ef328, 0x021ef2cc, 0x021ef328, +2 more; loops (back edge at +0x34); returns through pop {r3, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xb4 -> constant 0x02236bd0 (image word 0x02236bd0)
 *   branch +0x18 -> +0x60
 *   branch +0x5c -> +0xa4
 *   test +0x14 cmp r12, #2
 *   test +0x1c cmp r3, r2
 *   test +0x28 cmp r3, r1
 *   test +0x6c cmp r2, #0
 *   test +0x7c cmp r1, r0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021ef3bc; the literal pool and
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

extern void native_fn_021ef328(void);
extern void native_fn_021ef2cc(void);
extern void native_fn_0205f9e4(void);


asm u32 native_ov000_021ef3bc (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r12, =0x02236bd0
    ldr r12, [r12, #0xc]
    ldr r12, [r12, #0x7c]
    and r12, r12, #2
    cmp r12, #2
    bne ov000_021ef3bc_L60
    cmp r3, r2
    movne r0, #1
    moveq r0, #0
    cmp r3, r1
    movne r1, #1
    moveq r1, #0
    bl native_fn_021ef328
    ldr r1, =0x02236bd0
    mov r0, #232
    ldr r1, [r1, #0xc]
    mov r2, r0
    ldr r1, [r1, #0x70]
    add r3, r1, #8
    and r1, r1, #255
    and r3, r3, #255
    bl native_fn_021ef2cc
    b ov000_021ef3bc_La4
ov000_021ef3bc_L60:
    ldrh r1, [r0, #12]
    ldr r2, [r0, #0x4]
    ldrh r0, [r0, #14]
    cmp r2, #0
    movne r3, #1
    add r1, r2, r1
    moveq r3, #0
    cmp r1, r0
    movlt r1, #1
    movge r1, #0
    mov r0, r3
    bl native_fn_021ef328
    mov r0, #240
    mov r2, r0
    mov r1, #64
    mov r3, #152
    bl native_fn_021ef2cc
ov000_021ef3bc_La4:
    ldr r0, =0x02236bd0
    ldr r0, [r0, #0x10]
    bl native_fn_0205f9e4
    ldmia sp!, {r3, pc}
}
