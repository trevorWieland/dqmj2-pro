/* ov000 row 0x021e0cf8: 128 bytes.
 *
 * What it does: 29 instructions; 2 call(s) to 0x021e0d14, 0x021e0d64; no back edge; returns through bx lr; 3 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x74 -> native_fn_021e0c08 (image word 0x021e0c08)
 *   pool +0x78 -> native_fn_021e0c58 (image word 0x021e0c58)
 *   pool +0x7c -> native_fn_021e0c98 (image word 0x021e0c98)
 *   branch +0x04 -> +0x38
 *   branch +0x0c -> +0x1c
 *   branch +0x14 -> +0x5c
 *   branch +0x18 -> +0x6c
 *   branch +0x20 -> +0x6c
 *   branch +0x28 -> +0x6c
 *   branch +0x30 -> +0x54
 *   branch +0x34 -> +0x6c
 *   branch +0x3c -> +0x48
 *   branch +0x40 -> +0x64
 *   branch +0x44 -> +0x6c
 *   branch +0x4c -> +0x64
 *   branch +0x50 -> +0x6c
 *   test +0x00 cmp r0, #13
 *   test +0x08 cmp r0, #10
 *   test +0x10 cmpne r0, #13
 *   test +0x1c cmp r0, #7
 *   test +0x24 cmp r0, #3
 *   test +0x2c cmpne r0, #7
 *   test +0x38 cmp r0, #31
 *   test +0x48 cmp r0, #34
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e0cf8; the literal pool and
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

extern void native_fn_021e0c08(void);
extern void native_fn_021e0c58(void);
extern void native_fn_021e0c98(void);


asm u32 native_ov000_021e0cf8 (register u32 a0)
{
    cmp r0, #13
    bgt ov000_021e0cf8_L38
    cmp r0, #10
    blt ov000_021e0cf8_L1c
    cmpne r0, #13
    beq ov000_021e0cf8_L5c
    b ov000_021e0cf8_L6c
ov000_021e0cf8_L1c:
    cmp r0, #7
    bgt ov000_021e0cf8_L6c
    cmp r0, #3
    blt ov000_021e0cf8_L6c
    cmpne r0, #7
    beq ov000_021e0cf8_L54
    b ov000_021e0cf8_L6c
ov000_021e0cf8_L38:
    cmp r0, #31
    bgt ov000_021e0cf8_L48
    beq ov000_021e0cf8_L64
    b ov000_021e0cf8_L6c
ov000_021e0cf8_L48:
    cmp r0, #34
    beq ov000_021e0cf8_L64
    b ov000_021e0cf8_L6c
ov000_021e0cf8_L54:
    ldr r0, =native_fn_021e0c08
    bx lr
ov000_021e0cf8_L5c:
    ldr r0, =native_fn_021e0c58
    bx lr
ov000_021e0cf8_L64:
    ldr r0, =native_fn_021e0c98
    bx lr
ov000_021e0cf8_L6c:
    mov r0, #0
    bx lr
}
