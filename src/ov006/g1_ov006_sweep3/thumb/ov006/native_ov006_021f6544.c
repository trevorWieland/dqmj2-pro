/* ov006 row 0x021f6544: 144 bytes.
 *
 * What it does: 47 instructions; 7 call(s) to 0x021f65d4, 0x021f2ad4, 0x021ffdf4, +4 more; loops (back edge at +0x0e); returns through pop {r4, pc}; 9 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x6c -> constant 0x0221c0a8 (image word 0x0221c0a8)
 *   pool +0x70 -> constant 0xfe00ff00 (image word 0xfe00ff00)
 *   pool +0x74 -> native_data_0220b5c0 (image word 0x0220b5c0)
 *   pool +0x78 -> constant 0x00e00084 (image word 0x00e00084)
 *   pool +0x7c -> constant 0xfffff3ff (image word 0xfffff3ff)
 *   pool +0x80 -> native_data_0220b5be (image word 0x0220b5be)
 *   pool +0x84 -> native_data_0220b5bc (image word 0x0220b5bc)
 *   pool +0x88 -> native_data_0220b5ba (image word 0x0220b5ba)
 *   pool +0x8c -> native_fn_021f66d8+1 (image word 0x021f66d9)
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f6544; the literal pool and
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

extern void native_fn_021f65d4(void);
extern void native_fn_021f2ad4(void);
extern void native_fn_021ffdf4(void);
extern void native_fn_021f26f0(void);
extern void native_fn_0220303c(void);
extern u8 native_data_0220b5c0[];
extern u8 native_data_0220b5be[];
extern u8 native_data_0220b5bc[];
extern u8 native_data_0220b5ba[];
extern void native_fn_021f29bc(void);
extern void native_fn_021f66d8(void);
extern void native_fn_021f52cc(void);


asm u32 native_ov006_021f6544 (register u32 a0)
{
    push {r4, lr}
    ldr r0, =0x0221c0a8
    mov r1, #0x0
    strb r1, [r0, #0x1]
    bl native_fn_021f65d4
    mov r0, #0x10
    bl native_fn_021f2ad4
    mov r0, #0x3
    bl native_fn_021ffdf4
    mov r0, #0x39
    add r1, r0, #0x0
    sub r1, #0x3a
    mov r2, #0x0
    bl native_fn_021f26f0
    mov r0, #0x0
    mov r1, #0x5b
    bl native_fn_0220303c
    ldr r2, =0x0221c0a8
    ldr r1, =0xfe00ff00
    str r0, [r2, #0x8]
    ldr r3, [r0, #0]
    ldr r4, =native_data_0220b5c0
    and r3, r1
    ldr r1, =0x00e00084
    orr r1, r3
    str r1, [r0, #0]
    ldr r3, [r2, #0x8]
    ldr r0, =0xfffff3ff
    ldrh r1, [r3, #0x4]
    and r1, r0
    mov r0, #0x3
    lsl r0, r0, #0xa
    orr r0, r1
    strh r0, [r3, #0x4]
    ldrb r0, [r2, #0]
    ldr r1, =native_data_0220b5be
    ldr r2, =native_data_0220b5bc
    lsl r3, r0, #0x3
    ldr r0, =native_data_0220b5ba
    ldrh r1, [r1, r3]
    ldrh r0, [r0, r3]
    ldrh r2, [r2, r3]
    ldrh r3, [r4, r3]
    bl native_fn_021f29bc
    ldr r0, =native_fn_021f66d8+1
    bl native_fn_021f52cc
    pop {r4, pc}
}
