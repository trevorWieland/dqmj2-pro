/* ov006 row 0x021ff000: 44 bytes.
 *
 * What it does: 17 instructions; 1 call(s) to 0x0200616c; loops (back edge at +0x1c); returns through pop {r3, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x24 -> constant 0x0221c148 (image word 0x0221c148)
 *   pool +0x28 -> native_data_0220e1bc (image word 0x0220e1bc)
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ff000; the literal pool and
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

extern u8 native_data_0220e1bc[];
extern void native_fn_0200616c(void);


asm u32 native_ov006_021ff000 (register u32 a0)
{
    push {r3, lr}
    sub sp, #0x8
    ldr r1, =0x0221c148
    ldr r2, [r1, #0]
    mov r1, #0x4f
    lsl r1, r1, #0x4
    add r3, r2, r1
    ldrb r1, [r3, #0x2]
    str r1, [sp]
    ldrb r1, [r3, #0x3]
    str r1, [sp, #0x4]
    ldrb r2, [r3, #0]
    ldrb r3, [r3, #0x1]
    ldr r1, =native_data_0220e1bc
    blx native_fn_0200616c
    add sp, #0x8
    pop {r3, pc}
}
