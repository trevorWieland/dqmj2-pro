/* ov006 row 0x0220267c: 44 bytes.
 *
 * What it does: 18 instructions; 2 call(s) to 0x022011d4, 0x022011b0; loops (back edge at +0x04); returns through pop {r4, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x28 -> constant 0x0221c16c (image word 0x0221c16c)
 *   branch +0x0a -> +0x10
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x0220267c; the literal pool and
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

extern void native_fn_022011d4(void);
extern void native_fn_022011b0(void);


asm u32 native_ov006_0220267c (register u32 a0)
{
    push {r4, lr}
    add r0, #0xa
    bl native_fn_022011d4
    add r4, r0, #0x0
    bne ov006_0220267c_L10
    mov r0, #0x0
    pop {r4, pc}
ov006_0220267c_L10:
    bl native_fn_022011b0
    ldr r1, =0x0221c16c
    ldr r2, [r1, #0]
    sub r1, r4, #0x1
    lsl r1, r1, #0x2
    add r2, r2, r1
    mov r1, #0xaa
    lsl r1, r1, #0x4
    str r0, [r2, r1]
    mov r0, #0x1
    pop {r4, pc}
}
