/* ov006 row 0x021f2fc8: 104 bytes.
 *
 * What it does: Writes one block of 4 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x58 -> constant 0x0221c05c (image word 0x0221c05c)
 *   pool +0x5c -> constant 0x01ff0000 (image word 0x01ff0000)
 *   pool +0x60 -> constant 0x0000011d (image word 0x0000011d)
 *   pool +0x64 -> native_fn_021f3030+1 (image word 0x021f3031)
 *   branch +0x24 -> +0x32
 *   test +0x20 cmp r2, #0x67
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f2fc8; the literal pool and
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

extern void native_fn_021f37f0(void);
extern void native_fn_021f3030(void);
extern void native_fn_02204970(void);


asm u32 native_ov006_021f2fc8 (register u32 a0)
{
    push {r4, lr}
    sub sp, #0x8
    add r4, r0, #0x0
    ldr r0, =0x0221c05c
    ldr r0, [r0, #0]
    ldr r1, [r0, #0x60]
    ldr r2, [r1, #0]
    ldr r1, =0x01ff0000
    and r1, r2
    lsr r1, r1, #0x10
    str r1, [sp, #0x4]
    lsl r1, r2, #0x18
    lsr r2, r1, #0x18
    str r2, [sp]
    sub r2, #0xc
    str r2, [sp]
    cmp r2, #0x67
    ldr r1, =0x0000011d
    ble ov006_021f2fc8_L32
    ldrb r0, [r0, r1]
    mov r1, #0x1
    bl native_fn_021f37f0
    add sp, #0x8
    pop {r4, pc}
ov006_021f2fc8_L32:
    ldrb r0, [r0, r1]
    mov r1, #0x1
    mov r2, #0x67
    bl native_fn_021f37f0
    ldr r0, =0x0221c05c
    mov r2, #0xc0
    ldr r1, [r0, #0]
    ldr r0, =0x0000011d
    ldrb r0, [r1, r0]
    mov r1, #0x2
    bl native_fn_021f37f0
    ldr r1, =native_fn_021f3030+1
    add r0, r4, #0x0
    bl native_fn_02204970
    add sp, #0x8
    pop {r4, pc}
}
