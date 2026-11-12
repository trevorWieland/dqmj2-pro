/* ov001 row 0x021fd7c4: 104 bytes.
 *
 * What it does: 26 instructions; 2 call(s) to 0x021fe4ac, 0x021fe4ac; no back edge
 *
 * Decoded shape: block fill (26 instructions, 2 calls, 1 branch, 0 back edges, 0 literal slots).
 *
 *   branch +0x1c -> +0x44
 *   test +0x10 cmp r3, #0
 *   4 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021fd7c4; the literal pool and
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

extern void native_fn_021fe4ac(void);


asm u32 native_ov001_021fd7c4 (register u32 a0)
{
    stmdb sp!, {lr}
    sub sp, sp, #20
    stmia sp, {r1, r2}
    mov r1, #2
    cmp r3, #0
    str r1, [sp, #0x8]
    mov r12, #1
    beq ov001_021fd7c4_L44
    str r12, [sp, #0xc]
    mov r3, r0
    mov r0, #22
    mov r1, #8
    mov r2, #24
    str r12, [sp, #0x10]
    bl native_fn_021fe4ac
    add sp, sp, #20
    ldmia sp!, {pc}
ov001_021fd7c4_L44:
    str r12, [sp, #0xc]
    mov r3, r0
    mov r0, #22
    mov r1, #0
    mov r2, #127
    str r12, [sp, #0x10]
    bl native_fn_021fe4ac
    add sp, sp, #20
    ldmia sp!, {pc}
}
