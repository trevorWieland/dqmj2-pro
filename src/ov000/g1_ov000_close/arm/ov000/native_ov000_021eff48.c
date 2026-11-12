/* ov000 row 0x021eff48: 164 bytes.
 *
 * What it does: 41 instructions; 3 call(s) to 0x0204a1d0, 0x0204a574, 0x0204a1d0; loops (back edge at +0x3c); returns through pop {r4, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   0 block transfer(s), 12 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021eff48; the literal pool and
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

extern void native_fn_0204a1d0(void);
extern void native_fn_0204a574(void);


asm u32 native_ov000_021eff48 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    sub sp, sp, #16
    mov r4, r0
    mul r3, r1, r4
    mov r2, #0
    add r1, sp, #12
    sub r0, r2, #16
    strh r2, [r1]
    strh r2, [r1, #2]
    strh r0, [sp, #12]
    mov r0, #6
    str r0, [sp]
    mov r2, #1
    mov r0, #19
    str r2, [sp, #0x4]
    bl native_fn_0204a1d0
    mov r0, #16
    strh r0, [sp, #12]
    mov r0, #8
    str r0, [sp]
    mov r12, #1
    str r12, [sp, #0x4]
    add r1, sp, #12
    mov r0, #18
    mov r2, #9
    mov r3, #2
    str r12, [sp, #0x8]
    bl native_fn_0204a574
    mvn r0, #7
    strh r0, [sp, #12]
    mov r0, #2
    str r0, [sp]
    mov r2, #0
    str r2, [sp, #0x4]
    add r1, sp, #12
    mov r3, r4
    mov r0, #18
    mov r2, #1
    bl native_fn_0204a1d0
    add sp, sp, #16
    ldmia sp!, {r4, pc}
}
