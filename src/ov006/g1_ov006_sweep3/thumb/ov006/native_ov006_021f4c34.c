/* ov006 row 0x021f4c34: 76 bytes.
 *
 * What it does: 29 instructions; 4 call(s) to 0x02202dc0, 0x021f4944, 0x021f4c6e, +1 more; loops (back edge at +0x28); returns through pop {r4, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x40 -> constant 0x0221c060 (image word 0x0221c060)
 *   pool +0x44 -> constant 0x01ff0000 (image word 0x01ff0000)
 *   pool +0x48 -> native_fn_021f4c80+1 (image word 0x021f4c81)
 *   branch +0x30 -> +0x3a
 *   test +0x2e cmp r0, #0xc0
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f4c34; the literal pool and
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
extern void native_fn_021f4944(void);
extern void native_fn_021f4c80(void);
extern void native_fn_02204970(void);


asm u32 native_ov006_021f4c34 (register u32 a0)
{
    push {r4, lr}
    sub sp, #0x8
    add r4, r0, #0x0
    ldr r0, =0x0221c060
    mov r1, #0x0
    ldr r0, [r0, #0]
    ldr r0, [r0, #0x40]
    bl native_fn_02202dc0
    ldr r1, [r0, #0]
    ldr r0, =0x01ff0000
    and r0, r1
    lsr r0, r0, #0x10
    str r0, [sp, #0x4]
    lsl r0, r1, #0x18
    lsr r1, r0, #0x18
    str r1, [sp]
    add r1, #0xc
    str r1, [sp]
    mov r0, #0x4
    bl native_fn_021f4944
    ldr r0, [sp]
    cmp r0, #0xc0
    blt ov006_021f4c34_L3a
    ldr r1, =native_fn_021f4c80+1
    add r0, r4, #0x0
    bl native_fn_02204970
ov006_021f4c34_L3a:
    add sp, #0x8
    pop {r4, pc}
    mov r8, r8
}
