/* ov006 row 0x021f5a4c: 88 bytes.
 *
 * What it does: 26 instructions; 6 call(s) to 0x021f5aa4, 0x021f2ad4, 0x021f26f0, +3 more; loops (back edge at +0x08); returns through pop {r4, pc}; 6 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x40 -> constant 0x0221c09c (image word 0x0221c09c)
 *   pool +0x44 -> native_data_0220b54a (image word 0x0220b54a)
 *   pool +0x48 -> native_data_0220b548 (image word 0x0220b548)
 *   pool +0x4c -> native_data_0220b54c (image word 0x0220b54c)
 *   pool +0x50 -> native_data_0220b546 (image word 0x0220b546)
 *   pool +0x54 -> native_fn_021f5b3c+1 (image word 0x021f5b3d)
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f5a4c; the literal pool and
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

extern void native_fn_021f5aa4(void);
extern void native_fn_021f2ad4(void);
extern void native_fn_021f26f0(void);
extern void native_fn_021ffdf4(void);
extern u8 native_data_0220b54a[];
extern u8 native_data_0220b548[];
extern u8 native_data_0220b54c[];
extern u8 native_data_0220b546[];
extern void native_fn_021f29bc(void);
extern void native_fn_021f5b3c(void);
extern void native_fn_021f52cc(void);


asm u32 native_ov006_021f5a4c (register u32 a0)
{
    push {r4, lr}
    bl native_fn_021f5aa4
    mov r0, #0x0
    bl native_fn_021f2ad4
    mov r0, #0x2e
    add r1, r0, #0x0
    sub r1, #0x2f
    mov r2, #0x0
    bl native_fn_021f26f0
    mov r0, #0x4
    bl native_fn_021ffdf4
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
    ldr r0, =native_fn_021f5b3c+1
    bl native_fn_021f52cc
    pop {r4, pc}
}
