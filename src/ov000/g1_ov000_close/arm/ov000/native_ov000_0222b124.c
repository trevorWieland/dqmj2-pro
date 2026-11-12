/* ov000 row 0x0222b124: 92 bytes.
 *
 * What it does: 22 instructions; 3 call(s) to 0x0222b0c8, 0x0222b06c, 0x0205f9e4; loops (back edge at +0x30); returns through pop {r3, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x58 -> constant 0x022476f0 (image word 0x022476f0)
 *   test +0x10 cmp r2, #0
 *   test +0x20 cmp r1, r0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0222b124; the literal pool and
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

extern void native_fn_0222b0c8(void);
extern void native_fn_0222b06c(void);
extern void native_fn_0205f9e4(void);


asm u32 native_ov000_0222b124 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldrh r1, [r0, #12]
    ldr r2, [r0, #0x4]
    ldrh r0, [r0, #14]
    cmp r2, #0
    movne r3, #1
    add r1, r2, r1
    moveq r3, #0
    cmp r1, r0
    movlt r1, #1
    movge r1, #0
    mov r0, r3
    bl native_fn_0222b0c8
    mov r0, #200
    mov r2, r0
    mov r1, #40
    mov r3, #128
    bl native_fn_0222b06c
    ldr r0, =0x022476f0
    ldr r0, [r0, #0xc]
    bl native_fn_0205f9e4
    ldmia sp!, {r3, pc}
}
