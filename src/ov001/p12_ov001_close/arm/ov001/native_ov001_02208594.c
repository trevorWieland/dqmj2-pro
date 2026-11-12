/* ov001 row 0x02208594: 116 bytes.
 *
 * What it does: 29 instructions; 1 call(s) to 0x0204a574; loops (back edge at +0x68); returns through pop {r3, pc}
 *
 * Decoded shape: loop with 1 call (29 instructions, 1 call, 4 branches, 1 back edge, 0 literal slots).
 *
 *   branch +0x1c -> +0x38
 *   branch +0x24 -> +0x44
 *   branch +0x34 -> +0x4c
 *   branch +0x40 -> +0x4c
 *   test +0x18 cmp r0, #0
 *   test +0x20 cmp r0, #1
 *   test +0x28 cmp r0, #2
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02208594; the literal pool and
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

extern void native_fn_0204a574(void);


asm u32 native_ov001_02208594 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    sub sp, sp, #16
    add r2, sp, #12
    mov r1, #0
    strh r1, [r2]
    strh r1, [r2, #2]
    cmp r0, #0
    beq ov001_02208594_L38
    cmp r0, #1
    beq ov001_02208594_L44
    cmp r0, #2
    moveq r0, r1
    moveq r3, #3
    b ov001_02208594_L4c
ov001_02208594_L38:
    mov r0, r1
    mov r3, #1
    b ov001_02208594_L4c
ov001_02208594_L44:
    mov r3, r1
    mov r0, #1
ov001_02208594_L4c:
    str r0, [sp]
    mov r12, #1
    str r12, [sp, #0x4]
    add r1, sp, #12
    mov r0, #25
    mov r2, #5
    str r12, [sp, #0x8]
    bl native_fn_0204a574
    add sp, sp, #16
    ldmia sp!, {r3, pc}
}
