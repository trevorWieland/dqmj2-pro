/* ov006 row 0x021f5d80: 76 bytes.
 *
 * What it does: 26 instructions; 2 call(s) to 0x021ff6d4, 0x021f29bc; loops (back edge at +0x30); returns through pop {r4, pc}; 5 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x38 -> constant 0x0221c09c (image word 0x0221c09c)
 *   pool +0x3c -> native_data_0220b54a (image word 0x0220b54a)
 *   pool +0x40 -> native_data_0220b548 (image word 0x0220b548)
 *   pool +0x44 -> native_data_0220b54c (image word 0x0220b54c)
 *   pool +0x48 -> native_data_0220b546 (image word 0x0220b546)
 *   branch +0x04 -> +0x34
 *   branch +0x08 -> +0x34
 *   test +0x02 cmp r0, #0x1
 *   test +0x06 cmp r0, #0x3
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f5d80; the literal pool and
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

extern void native_fn_021ff6d4(void);
extern u8 native_data_0220b54a[];
extern u8 native_data_0220b548[];
extern u8 native_data_0220b54c[];
extern u8 native_data_0220b546[];
extern void native_fn_021f29bc(void);


asm u32 native_ov006_021f5d80 (register u32 a0)
{
    push {r4, lr}
    cmp r0, #0x1
    beq ov006_021f5d80_L34
    cmp r0, #0x3
    beq ov006_021f5d80_L34
    ldr r1, =0x0221c09c
    mov r0, #0x1
    ldrb r2, [r1, #0]
    eor r0, r2
    strb r0, [r1, #0]
    mov r0, #0x8
    bl native_fn_021ff6d4
    ldr r0, =0x0221c09c
    ldr r1, =native_data_0220b54a
    ldrb r0, [r0, #0]
    ldr r2, =native_data_0220b548
    ldr r4, =native_data_0220b54c
    lsl r3, r0, #0x3
    ldr r0, =native_data_0220b546
    ldrh r1, [r1, r3]
    ldrh r0, [r0, r3]
    ldrh r2, [r2, r3]
    ldrh r3, [r4, r3]
    bl native_fn_021f29bc
ov006_021f5d80_L34:
    pop {r4, pc}
    mov r8, r8
}
