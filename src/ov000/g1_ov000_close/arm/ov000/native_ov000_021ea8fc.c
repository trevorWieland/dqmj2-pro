/* ov000 row 0x021ea8fc: 100 bytes.
 *
 * What it does: 24 instructions; 2 call(s) to 0x02042b3c, 0x020446f8; loops (back edge at +0x34); 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x60 -> constant 0x02236950 (image word 0x02236950)
 *   branch +0x30 -> +0x38
 *   test +0x2c cmp r2, #0
 *   test +0x44 cmp r1, #0
 *   3 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021ea8fc; the literal pool and
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

extern void native_fn_02042b3c(void);
extern void native_fn_020446f8(void);


asm u32 native_ov000_021ea8fc (register u32 a0)
{
    stmdb sp!, {lr}
    sub sp, sp, #12
    ldr r0, =0x02236950
    add r1, sp, #0
    ldr r0, [r0, #0x18]
    mov r2, #0
    str r2, [r1]
    str r2, [r1, #0x4]
    str r2, [r1, #0x8]
    add r2, r0, #256
    ldrsh r2, [r2, #240]
    cmp r2, #0
    beq ov000_021ea8fc_L38
    bl native_fn_02042b3c
ov000_021ea8fc_L38:
    ldr r0, =0x02236950
    ldr r0, [r0, #0x20]
    ldr r1, [r0, #0x30]
    cmp r1, #0
    addeq sp, sp, #12
    ldmeqia sp!, {pc}
    mov r1, #1
    bl native_fn_020446f8
    add sp, sp, #12
    ldmia sp!, {pc}
}
