/* ov006 row 0x021f3de4: 88 bytes.
 *
 * What it does: 33 instructions; 4 call(s) to 0x02202dc0, 0x021f37f0, 0x021f3e28, +1 more; loops (back edge at +0x32); returns through pop {r4, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x48 -> constant 0x0221c05c (image word 0x0221c05c)
 *   pool +0x4c -> constant 0x01ff0000 (image word 0x01ff0000)
 *   pool +0x50 -> constant 0x0000011d (image word 0x0000011d)
 *   pool +0x54 -> native_fn_021f3e3c+1 (image word 0x021f3e3d)
 *   branch +0x3a -> +0x44
 *   test +0x38 cmp r0, #0xc0
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f3de4; the literal pool and
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
extern void native_fn_021f37f0(void);
extern void native_fn_021f3e3c(void);
extern void native_fn_02204970(void);


asm u32 native_ov006_021f3de4 (register u32 a0)
{
    push {r4, lr}
    sub sp, #0x8
    add r4, r0, #0x0
    ldr r0, =0x0221c05c
    mov r1, #0x0
    ldr r0, [r0, #0]
    add r0, #0xfc
    ldr r0, [r0, #0]
    bl native_fn_02202dc0
    ldr r1, [r0, #0]
    ldr r0, =0x01ff0000
    and r0, r1
    lsr r0, r0, #0x10
    str r0, [sp, #0x4]
    lsl r0, r1, #0x18
    lsr r2, r0, #0x18
    ldr r0, =0x0221c05c
    str r2, [sp]
    ldr r1, [r0, #0]
    ldr r0, =0x0000011d
    add r2, #0xc
    ldrb r0, [r1, r0]
    str r2, [sp]
    mov r1, #0x4
    bl native_fn_021f37f0
    ldr r0, [sp]
    cmp r0, #0xc0
    blt ov006_021f3de4_L44
    ldr r1, =native_fn_021f3e3c+1
    add r0, r4, #0x0
    bl native_fn_02204970
ov006_021f3de4_L44:
    add sp, #0x8
    pop {r4, pc}
}
