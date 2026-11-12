/* ov000 row 0x021ebf34: 104 bytes.
 *
 * What it does: 26 instructions; 2 call(s) to 0x021ebdf0, 0x021ebeec; loops (back edge at +0x40); returns through pop {r3, r4, r5, r6, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021ebf34; the literal pool and
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

extern void native_fn_021ebdf0(void);
extern void native_fn_021ebeec(void);


asm u32 native_ov000_021ebf34 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, lr}
    sub sp, sp, #20
    mov r3, #1
    str r3, [sp]
    mov r12, #30
    mov r6, r0
    mov r4, r2
    str r12, [sp, #0x4]
    mov r0, #2
    str r0, [sp, #0x8]
    str r3, [sp, #0xc]
    mov r0, #0
    mov r5, r1
    mov r1, r0
    mov r2, #127
    str r3, [sp, #0x10]
    bl native_fn_021ebdf0
    mov r12, #8
    mov r1, r6
    mov r2, r5
    mov r3, r4
    mov r0, #0
    str r12, [sp]
    bl native_fn_021ebeec
    add sp, sp, #20
    ldmia sp!, {r3, r4, r5, r6, pc}
}
