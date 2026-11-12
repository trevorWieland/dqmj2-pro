/* ov000 row 0x0221799c: 96 bytes.
 *
 * What it does: 24 instructions; 3 call(s) to 0x02048f6c, 0x0204b85c, 0x0203cfe0; loops (back edge at +0x14); returns through pop {r4, r5, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   test +0x48 cmp r0, #5
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0221799c; the literal pool and
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

extern void native_fn_02048f6c(void);
extern void native_fn_0204b85c(void);
extern void native_fn_0203cfe0(void);


asm u32 native_ov000_0221799c (register u32 a0)
{
    stmdb sp!, {r4, r5, lr}
    sub sp, sp, #12
    mov r5, r0
    mov r0, #1
    mov r4, r1
    bl native_fn_02048f6c
    str r0, [sp]
    mov r2, #40
    str r2, [sp, #0x4]
    mov r12, #8
    mov r0, r5
    mov r1, r4
    mov r2, #5
    mov r3, #1
    str r12, [sp, #0x8]
    bl native_fn_0204b85c
    bl native_fn_0203cfe0
    str r0, [r5, #0x2c]
    cmp r0, #5
    addeq r0, r0, #40
    movne r0, #40
    str r0, [r5, #0x30]
    add sp, sp, #12
    ldmia sp!, {r4, r5, pc}
}
