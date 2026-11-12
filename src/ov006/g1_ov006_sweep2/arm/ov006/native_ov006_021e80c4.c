/* ov006 row 0x021e80c4: 108 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x68 -> constant 0x2aaaaaab (image word 0x2aaaaaab)
 *   branch +0x0c -> +0x58
 *   branch +0x34 -> +0x58
 *   test +0x08 cmp r0, #0
 *   test +0x30 cmp r0, #0
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e80c4; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity proves the instruction stream, not the meaning of the fields, blocks and callee contracts it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_021e92cc(void);


asm u32 native_ov006_021e80c4 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r4, r1
    cmp r0, #0
    blt ov006_021e80c4_L58
    ldr r2, =0x2aaaaaab
    mov r3, #6
    smull r1, r12, r2, r0
    add r12, r12, r0, lsr #31
    smull r1, r2, r3, r12
    sub r12, r0, r1
    add r0, r12, #7
    bl native_fn_021e92cc
    cmp r0, #0
    beq ov006_021e80c4_L58
    ldrb r1, [r0, #0x1c]
    mov r1, r1, lsl #3
    strh r1, [r4]
    ldrb r1, [r0, #0x1d]
    mov r0, #1
    mov r1, r1, lsl #3
    strh r1, [r4, #2]
    ldmia sp!, {r4, pc}
ov006_021e80c4_L58:
    mov r0, #0
    strh r0, [r4]
    strh r0, [r4, #2]
    ldmia sp!, {r4, pc}
}
