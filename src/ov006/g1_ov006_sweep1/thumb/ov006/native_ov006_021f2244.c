/* ov006 row 0x021f2244: 140 bytes.
 *
 * What it does: Writes one block of 1 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x74 -> native_data4_0221c004 (image word 0x0221c004)
 *   pool +0x78 -> constant 0xfffff3ff (image word 0xfffff3ff)
 *   pool +0x7c -> native_data_0220b0b8 (image word 0x0220b0b8)
 *   pool +0x80 -> constant 0xffff0fff (image word 0xffff0fff)
 *   pool +0x84 -> constant 0xfe00ff00 (image word 0xfe00ff00)
 *   pool +0x88 -> constant 0x00e6008b (image word 0x00e6008b)
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f2244; the literal pool and
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

extern u8 native_data4_0221c004[];
extern void native_fn_020024bc(void);
extern void native_fn_02002480(void);
extern void native_fn_02202ff0(void);
extern u8 native_data_0220b0b8[];


asm u32 native_ov006_021f2244 (register u32 a0)
{
    push {r4, lr}
    ldr r0, =native_data4_0221c004
    mov r1, #0x28
    ldr r0, [r0, #0]
    ldrb r0, [r0, #0x9]
    add r0, r0, #0x1
    blx native_fn_020024bc
    ldr r1, =native_data4_0221c004
    ldr r2, [r1, #0]
    strb r0, [r2, #0x9]
    ldr r0, [r1, #0]
    mov r1, #0x5
    ldrb r0, [r0, #0x9]
    blx native_fn_02002480
    add r1, r0, #0x0
    ldr r2, =native_data4_0221c004
    add r1, #0x47
    ldr r2, [r2, #0]
    mov r0, #0x0
    ldr r2, [r2, #0x4]
    bl native_fn_02202ff0
    ldr r3, =native_data4_0221c004
    ldr r2, =0xfffff3ff
    ldr r0, [r3, #0]
    ldr r4, [r0, #0x4]
    ldrh r0, [r4, #0x4]
    add r1, r0, #0x0
    mov r0, #0x1
    and r1, r2
    lsl r0, r0, #0xa
    orr r0, r1
    strh r0, [r4, #0x4]
    ldr r4, [r3, #0]
    ldr r0, =native_data_0220b0b8
    ldrb r1, [r4, #0x8]
    ldrb r1, [r0, r1]
    ldr r0, [r4, #0x4]
    ldr r4, [r0, #0]
    lsl r1, r1, #0xc
    and r2, r4
    str r2, [r0, #0]
    ldrh r4, [r0, #0x4]
    ldr r2, =0xffff0fff
    and r2, r4
    orr r1, r2
    strh r1, [r0, #0x4]
    ldr r0, [r3, #0]
    ldr r2, [r0, #0x4]
    ldr r0, =0xfe00ff00
    ldr r1, [r2, #0]
    and r1, r0
    ldr r0, =0x00e6008b
    orr r0, r1
    str r0, [r2, #0]
    pop {r4, pc}
}
