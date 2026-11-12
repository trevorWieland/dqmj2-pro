/* ov006 row 0x021f39e8: 144 bytes.
 *
 * What it does: Writes one block of 4 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x7c -> constant 0x0221c05c (image word 0x0221c05c)
 *   pool +0x80 -> constant 0xfffff3ff (image word 0xfffff3ff)
 *   pool +0x84 -> constant 0xffff0fff (image word 0xffff0fff)
 *   pool +0x88 -> native_data_0220b154 (image word 0x0220b154)
 *   pool +0x8c -> native_data_0220b158 (image word 0x0220b158)
 *   branch +0x06 -> +0x7a
 *   branch +0x0a -> +0x30
 *   branch +0x36 -> +0x5e
 *   test +0x04 cmp r0, #0x0
 *   test +0x08 cmp r0, #0x2f
 *   test +0x34 cmp r2, #0x4
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f39e8; the literal pool and
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

extern u8 native_data_0220b154[];
extern u8 native_data_0220b158[];
extern void native_fn_02202e50(void);


asm u32 native_ov006_021f39e8 (register u32 a0)
{
    push {r4, lr}
    add r3, r1, #0x0
    cmp r0, #0x0
    blt ov006_021f39e8_L7a
    cmp r0, #0x2f
    bge ov006_021f39e8_L30
    ldr r1, =0x0221c05c
    lsl r0, r0, #0x2
    ldr r1, [r1, #0]
    add r0, r1, r0
    ldr r0, [r0, #0x30]
    ldr r1, =0xfffff3ff
    ldr r2, [r0, #0]
    and r1, r2
    str r1, [r0, #0]
    ldrh r2, [r0, #0x4]
    ldr r1, =0xffff0fff
    and r2, r1
    ldr r1, =native_data_0220b154
    ldrb r1, [r1, r3]
    lsl r1, r1, #0xc
    orr r1, r2
    strh r1, [r0, #0x4]
    pop {r4, pc}
ov006_021f39e8_L30:
    add r2, r0, #0x0
    sub r2, #0x2f
    cmp r2, #0x4
    bge ov006_021f39e8_L5e
    ldr r0, =0x0221c05c
    ldr r1, [r0, #0]
    lsl r0, r2, #0x2
    add r0, r1, r0
    add r0, #0xec
    ldr r0, [r0, #0]
    ldr r1, =0xfffff3ff
    ldr r2, [r0, #0]
    and r1, r2
    str r1, [r0, #0]
    ldrh r2, [r0, #0x4]
    ldr r1, =0xffff0fff
    and r2, r1
    ldr r1, =native_data_0220b154
    ldrb r1, [r1, r3]
    lsl r1, r1, #0xc
    orr r1, r2
    strh r1, [r0, #0x4]
    pop {r4, pc}
ov006_021f39e8_L5e:
    ldr r1, =0x0221c05c
    sub r0, #0x33
    ldr r1, [r1, #0]
    lsl r0, r0, #0x2
    add r0, r1, r0
    ldr r4, =native_data_0220b158
    add r0, #0xfc
    mov r1, #0x0
    ldrb r3, [r4, r3]
    ldr r0, [r0, #0]
    mvn r1, r1
    mov r2, #0x0
    bl native_fn_02202e50
ov006_021f39e8_L7a:
    pop {r4, pc}
}
