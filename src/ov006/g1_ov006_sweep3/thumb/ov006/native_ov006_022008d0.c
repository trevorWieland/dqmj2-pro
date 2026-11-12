/* ov006 row 0x022008d0: 128 bytes.
 *
 * What it does: 50 instructions; 4 call(s) to 0x02202dc0, 0x02202ff0, 0x02202eb0, +1 more; no back edge; returns through pop {r4, r5, r6, pc}; 5 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x6c -> constant 0x0221c15c (image word 0x0221c15c)
 *   pool +0x70 -> native_data_0220baa6 (image word 0x0220baa6)
 *   pool +0x74 -> native_data_0220ba92 (image word 0x0220ba92)
 *   pool +0x78 -> native_data_0220bb0e (image word 0x0220bb0e)
 *   pool +0x7c -> native_data_0220bb0c (image word 0x0220bb0c)
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x022008d0; the literal pool and
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
extern u8 native_data_0220baa6[];
extern void native_fn_02202ff0(void);
extern u8 native_data_0220ba92[];
extern u8 native_data_0220bb0e[];
extern u8 native_data_0220bb0c[];
extern void native_fn_02202eb0(void);
extern void native_fn_02202f54(void);


asm u32 native_ov006_022008d0 (register u32 a0)
{
    push {r4, r5, r6, lr}
    add r5, r0, #0x0
    ldr r0, =0x0221c15c
    lsl r4, r5, #0x2
    ldr r0, [r0, #0]
    mov r1, #0x0
    add r0, r0, r4
    ldr r0, [r0, #0x8]
    bl native_fn_02202dc0
    ldr r1, =0x0221c15c
    add r2, r0, #0x0
    ldr r1, [r1, #0]
    mov r0, #0x0
    ldrb r1, [r1, #0x1c]
    lsl r3, r1, #0x1
    ldr r1, =native_data_0220baa6
    add r1, r1, r3
    ldrb r1, [r5, r1]
    add r1, r1, #0x1
    bl native_fn_02202ff0
    ldr r0, =0x0221c15c
    ldr r2, =native_data_0220ba92
    ldr r1, [r0, #0]
    ldr r6, =native_data_0220bb0e
    ldrb r0, [r1, #0x1c]
    lsl r3, r0, #0x1
    add r2, r2, r3
    ldrb r2, [r5, r2]
    lsl r3, r0, #0x3
    add r0, r1, r4
    lsl r5, r2, #0x2
    ldr r2, =native_data_0220bb0c
    mov r1, #0x0
    add r2, r2, r3
    add r3, r6, r3
    ldrh r2, [r5, r2]
    ldrh r3, [r5, r3]
    ldr r0, [r0, #0x8]
    mvn r1, r1
    bl native_fn_02202eb0
    ldr r0, =0x0221c15c
    mov r1, #0x0
    ldr r0, [r0, #0]
    mvn r1, r1
    add r0, r0, r4
    ldr r0, [r0, #0x8]
    mov r2, #0x0
    bl native_fn_02202f54
    pop {r4, r5, r6, pc}
    mov r8, r8
}
