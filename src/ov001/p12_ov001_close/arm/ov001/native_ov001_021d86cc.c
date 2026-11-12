/* ov001 row 0x021d86cc: 112 bytes.
 *
 * What it does: 26 instructions; 1 call(s) to 0x020046c8; loops (back edge at +0x58); returns through pop {r3, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 1 call (26 instructions, 1 call, 5 branches, 1 back edge, 2 literal slots).
 *
 *   pool +0x68 -> constant 0x04000060 (image word 0x04000060)
 *   pool +0x6c -> constant 0x0000cfdf (image word 0x0000cfdf)
 *   branch +0x10 -> +0x60
 *   branch +0x1c -> +0x38
 *   branch +0x34 -> +0x4c
 *   branch +0x54 -> +0x60
 *   test +0x0c cmp r1, #0
 *   test +0x18 cmp r1, #0
 *   test +0x50 cmp r1, #0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021d86cc; the literal pool and
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

extern void native_fn_020046c8(void);


asm u32 native_ov001_021d86cc (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldrb r1, [r0, #0x11]
    mov r12, #0
    cmp r1, #0
    beq ov001_021d86cc_L60
    ldrb r1, [r0, #0x10]
    cmp r1, #0
    beq ov001_021d86cc_L38
    ldr r2, =0x04000060
    ldrh r1, [r2]
    bic r1, r1, #12288
    orr r1, r1, #32
    strh r1, [r2]
    b ov001_021d86cc_L4c
ov001_021d86cc_L38:
    ldr r3, =0x04000060
    ldr r1, =0x0000cfdf
    ldrh r2, [r3]
    and r1, r2, r1
    strh r1, [r3]
ov001_021d86cc_L4c:
    ldrb r1, [r0, #0x10]
    cmp r1, #0
    beq ov001_021d86cc_L60
    bl native_fn_020046c8
    mov r12, #1
ov001_021d86cc_L60:
    mov r0, r12
    ldmia sp!, {r3, pc}
}
