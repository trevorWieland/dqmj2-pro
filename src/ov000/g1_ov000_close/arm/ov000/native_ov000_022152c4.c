/* ov000 row 0x022152c4: 96 bytes.
 *
 * What it does: 24 instructions; 2 call(s) to 0x0204b85c, 0x0205f98c; loops (back edge at +0x38); returns through pop {r4, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022152c4; the literal pool and
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

extern void native_fn_0204b85c(void);
extern void native_fn_0205f98c(void);


asm u32 native_ov000_022152c4 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    sub sp, sp, #16
    strh r1, [sp, #12]
    strh r2, [sp, #14]
    mov r1, #2
    str r1, [sp]
    mov r1, #30
    str r1, [sp, #0x4]
    mov r2, #6
    str r2, [sp, #0x8]
    add r1, sp, #12
    mov r4, r0
    mov r2, #5
    mov r3, #1
    bl native_fn_0204b85c
    ldr r0, [r4, #0x1c]
    mov r1, #0
    bl native_fn_0205f98c
    ldr r1, [r0, #0x7c]
    orr r1, r1, #2
    str r1, [r0, #0x7c]
    mov r0, #0
    add sp, sp, #16
    ldmia sp!, {r4, pc}
}
