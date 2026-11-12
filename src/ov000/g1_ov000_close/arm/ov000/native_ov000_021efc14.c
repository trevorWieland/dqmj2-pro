/* ov000 row 0x021efc14: 140 bytes.
 *
 * What it does: 35 instructions; 3 call(s) to 0x02048094, 0x0204a724, 0x0204a644; loops (back edge at +0x20)
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x1c -> +0x5c
 *   test +0x18 cmp r0, #0
 *   3 block transfer(s), 9 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021efc14; the literal pool and
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

extern void native_fn_02048094(void);
extern void native_fn_0204a724(void);
extern void native_fn_0204a644(void);


asm u32 native_ov000_021efc14 (register u32 a0)
{
    stmdb sp!, {lr}
    sub sp, sp, #20
    add r2, sp, #16
    mov r1, #0
    strh r1, [r2]
    strh r1, [r2, #2]
    cmp r0, #0
    beq ov000_021efc14_L5c
    bl native_fn_02048094
    mov r0, #2
    str r0, [sp]
    mov r0, #67
    str r0, [sp, #0x4]
    mov r12, #1
    str r12, [sp, #0x8]
    add r1, sp, #16
    mov r0, #17
    mov r2, #8
    mov r3, #5
    str r12, [sp, #0xc]
    bl native_fn_0204a724
    add sp, sp, #20
    ldmia sp!, {pc}
ov000_021efc14_L5c:
    mov r0, #74
    str r0, [sp]
    mov r12, #1
    str r12, [sp, #0x4]
    mov r1, r2
    mov r0, #17
    mov r2, #5
    mov r3, #2
    str r12, [sp, #0x8]
    bl native_fn_0204a644
    add sp, sp, #20
    ldmia sp!, {pc}
}
