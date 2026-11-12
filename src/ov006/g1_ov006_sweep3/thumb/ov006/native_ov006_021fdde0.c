/* ov006 row 0x021fdde0: 32 bytes.
 *
 * What it does: 11 instructions; 2 call(s) to 0x021fddf6, 0x021f52cc; loops (back edge at +0x12); returns through pop {r3, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x18 -> constant 0x0221c128 (image word 0x0221c128)
 *   pool +0x1c -> native_fn_021fdd6c+1 (image word 0x021fdd6d)
 *   branch +0x0e -> +0x16
 *   test +0x0c cmp r0, #0x78
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fdde0; the literal pool and
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

extern void native_fn_021fdd6c(void);
extern void native_fn_021f52cc(void);


asm u32 native_ov006_021fdde0 (register u32 a0)
{
    push {r3, lr}
    ldr r0, =0x0221c128
    ldrb r1, [r0, #0]
    add r1, r1, #0x1
    strb r1, [r0, #0]
    ldrb r0, [r0, #0]
    cmp r0, #0x78
    blo ov006_021fdde0_L16
    ldr r0, =native_fn_021fdd6c+1
    bl native_fn_021f52cc
ov006_021fdde0_L16:
    pop {r3, pc}
}
