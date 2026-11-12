/* ov006 row 0x021fcdb4: 76 bytes.
 *
 * What it does: 26 instructions; 2 call(s) to 0x021f29bc, 0x021f2948; loops (back edge at +0x1c); returns through pop {r4, pc}; 5 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x38 -> constant 0x0221c10c (image word 0x0221c10c)
 *   pool +0x3c -> native_data_0220b87a (image word 0x0220b87a)
 *   pool +0x40 -> native_data_0220b87e (image word 0x0220b87e)
 *   pool +0x44 -> native_data_0220b87c (image word 0x0220b87c)
 *   pool +0x48 -> native_data_0220b880 (image word 0x0220b880)
 *   branch +0x08 -> +0x22
 *   test +0x06 cmp r0, #0x4
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fcdb4; the literal pool and
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

extern u8 native_data_0220b87a[];
extern u8 native_data_0220b87e[];
extern u8 native_data_0220b87c[];
extern u8 native_data_0220b880[];
extern void native_fn_021f29bc(void);
extern void native_fn_021f2948(void);


asm u32 native_ov006_021fcdb4 (register u32 a0)
{
    push {r4, lr}
    ldr r0, =0x0221c10c
    ldrb r0, [r0, #0]
    cmp r0, #0x4
    bhs ov006_021fcdb4_L22
    lsl r3, r0, #0x3
    ldr r0, =native_data_0220b87a
    ldr r1, =native_data_0220b87e
    ldr r2, =native_data_0220b87c
    ldr r4, =native_data_0220b880
    ldrh r0, [r0, r3]
    ldrh r1, [r1, r3]
    ldrh r2, [r2, r3]
    ldrh r3, [r4, r3]
    bl native_fn_021f29bc
    pop {r4, pc}
ov006_021fcdb4_L22:
    ldr r1, =native_data_0220b87a
    lsl r4, r0, #0x3
    ldr r2, =native_data_0220b87e
    ldr r3, =native_data_0220b87c
    ldrh r1, [r1, r4]
    ldrh r2, [r2, r4]
    ldrh r3, [r3, r4]
    mov r0, #0x0
    bl native_fn_021f2948
    pop {r4, pc}
}
