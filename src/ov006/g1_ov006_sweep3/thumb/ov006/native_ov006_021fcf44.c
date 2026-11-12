/* ov006 row 0x021fcf44: 92 bytes.
 *
 * What it does: 36 instructions; 4 call(s) to 0x02202dc0, 0x02202ff0, 0x02202eb0, +1 more; no back edge; returns through pop {r3, r4, r5, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x50 -> constant 0x0221c10c (image word 0x0221c10c)
 *   pool +0x54 -> native_data_0220b82a (image word 0x0220b82a)
 *   pool +0x58 -> native_data_0220b82c (image word 0x0220b82c)
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fcf44; the literal pool and
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

extern void native_fn_02202dc0(void);
extern void native_fn_02202ff0(void);
extern u8 native_data_0220b82a[];
extern u8 native_data_0220b82c[];
extern void native_fn_02202eb0(void);
extern void native_fn_02202f54(void);


asm u32 native_ov006_021fcf44 (register u32 a0)
{
    push {r3, r4, r5, lr}
    ldr r0, =0x0221c10c
    ldrb r1, [r0, #0]
    ldr r0, [r0, #0x4]
    sub r5, r1, #0x4
    lsl r4, r5, #0x2
    add r0, r0, r4
    ldr r0, [r0, #0x10]
    mov r1, #0x0
    bl native_fn_02202dc0
    add r2, r0, #0x0
    mov r0, #0x0
    mov r1, #0x32
    bl native_fn_02202ff0
    add r0, r5, #0x3
    lsl r3, r0, #0x2
    ldr r0, =0x0221c10c
    ldr r2, =native_data_0220b82a
    ldr r0, [r0, #0x4]
    mov r1, #0x0
    add r0, r0, r4
    ldr r5, =native_data_0220b82c
    ldrh r2, [r2, r3]
    ldrh r3, [r5, r3]
    ldr r0, [r0, #0x10]
    mvn r1, r1
    bl native_fn_02202eb0
    ldr r0, =0x0221c10c
    mov r1, #0x0
    ldr r0, [r0, #0x4]
    mvn r1, r1
    add r0, r0, r4
    ldr r0, [r0, #0x10]
    mov r2, #0x3
    bl native_fn_02202f54
    pop {r3, r4, r5, pc}
}
