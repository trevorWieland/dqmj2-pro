/* ov006 row 0x02202a48: 40 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x24 -> native_fn_02202a70+1 (image word 0x02202a71)
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02202a48; the literal pool and
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

extern void native_fn_02202a70(void);
extern void native_fn_0201109c(void);


asm u32 native_ov006_02202a48 (register u32 a0)
{
    push {r4, r5, lr}
    sub sp, #0xc
    add r5, r0, #0x0
    ldr r0, =native_fn_02202a70+1
    add r4, r1, #0x0
    str r0, [sp]
    str r5, [sp, #0x4]
    mov r0, #0x1
    str r0, [sp, #0x8]
    ldr r1, [r5, #0x28]
    sub r0, r0, #0x2
    add r1, r2, r1
    add r2, r4, #0x0
    blx native_fn_0201109c
    mov r0, #0x6
    add sp, #0xc
    pop {r4, r5, pc}
}
