/* ov000 row 0x021ef474: 100 bytes.
 *
 * What it does: 23 instructions; 1 call(s) to 0x02048a60; loops (back edge at +0x20); returns through pop {r4, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x5c -> constant 0x02236c04 (image word 0x02236c04)
 *   pool +0x60 -> constant 0x02101ae8 (image word 0x02101ae8)
 *   branch +0x0c -> +0x38
 *   branch +0x34 -> +0x48
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021ef474; the literal pool and
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

extern void native_fn_02048a60(void);


asm u32 native_ov000_021ef474 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    movs r2, r1
    mov r4, r0
    beq ov000_021ef474_L38
    ldr r0, =0x02236c04
    ldrsh r1, [r2]
    ldrsh r2, [r2, #2]
    ldr r0, [r0, r4, lsl #2]
    bl native_fn_02048a60
    ldr r0, =0x02236c04
    ldr r1, [r0, r4, lsl #2]
    ldr r0, [r1, #0x7c]
    orr r0, r0, #2
    b ov000_021ef474_L48
ov000_021ef474_L38:
    ldr r0, =0x02236c04
    ldr r1, [r0, r4, lsl #2]
    ldr r0, [r1, #0x7c]
    bic r0, r0, #2
ov000_021ef474_L48:
    str r0, [r1, #0x7c]
    ldr r0, =0x02101ae8
    mov r1, #1
    str r1, [r0, #0xc84]
    ldmia sp!, {r4, pc}
}
