/* ov006 row 0x021f218c: 144 bytes.
 *
 * What it does: Writes one block of 1 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x74 -> native_data3_0221c004 (image word 0x0221c004)
 *   pool +0x78 -> constant 0xfffff3ff (image word 0xfffff3ff)
 *   pool +0x7c -> constant 0xffff0fff (image word 0xffff0fff)
 *   pool +0x80 -> native_data_0220b0b8 (image word 0x0220b0b8)
 *   pool +0x84 -> constant 0xfe00ff00 (image word 0xfe00ff00)
 *   pool +0x88 -> constant 0x00e6008b (image word 0x00e6008b)
 *   pool +0x8c -> native_fn_021f2244+1 (image word 0x021f2245)
 *   0 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f218c; the literal pool and
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

extern void ov006_clear_buffer_02203c08(void);
extern u8 native_data3_0221c004[];
extern void native_fn_0220303c(void);
extern u8 native_data_0220b0b8[];
extern void native_fn_021f2244(void);
extern void native_fn_0220490c(void);


asm u32 native_ov006_021f218c (register u32 a0)
{
    push {r3, r4, r5, lr}
    add r4, r0, #0x0
    mov r0, #0xc
    mov r1, #0x4
    bl ov006_clear_buffer_02203c08
    ldr r1, =native_data3_0221c004
    str r0, [r1, #0]
    strb r4, [r0, #0x8]
    mov r0, #0x0
    mov r1, #0x47
    bl native_fn_0220303c
    ldr r1, =native_data3_0221c004
    ldr r3, =0xfffff3ff
    ldr r2, [r1, #0]
    str r0, [r2, #0x4]
    ldr r0, [r1, #0]
    ldr r0, [r0, #0x4]
    ldrh r2, [r0, #0x4]
    add r5, r2, #0x0
    mov r2, #0x1
    and r5, r3
    lsl r2, r2, #0xa
    orr r2, r5
    strh r2, [r0, #0x4]
    ldr r0, [r1, #0]
    ldr r0, [r0, #0x4]
    ldr r2, [r0, #0]
    and r2, r3
    str r2, [r0, #0]
    ldrh r3, [r0, #0x4]
    ldr r2, =0xffff0fff
    and r3, r2
    ldr r2, =native_data_0220b0b8
    ldrb r2, [r2, r4]
    lsl r2, r2, #0xc
    orr r2, r3
    strh r2, [r0, #0x4]
    ldr r0, [r1, #0]
    mov r3, #0x78
    ldr r2, [r0, #0x4]
    ldr r0, =0xfe00ff00
    ldr r1, [r2, #0]
    and r1, r0
    ldr r0, =0x00e6008b
    orr r0, r1
    str r0, [r2, #0]
    ldr r1, =native_fn_021f2244+1
    mov r0, #0x1
    mov r2, #0x0
    bl native_fn_0220490c
    ldr r1, =native_data3_0221c004
    ldr r1, [r1, #0]
    str r0, [r1, #0]
    pop {r3, r4, r5, pc}
    mov r8, r8
}
