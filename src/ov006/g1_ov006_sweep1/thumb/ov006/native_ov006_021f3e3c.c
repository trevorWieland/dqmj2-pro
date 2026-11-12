/* ov006 row 0x021f3e3c: 80 bytes.
 *
 * What it does: Writes one block of 4 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x40 -> constant 0x0221c05c (image word 0x0221c05c)
 *   pool +0x44 -> constant 0x01ff0000 (image word 0x01ff0000)
 *   pool +0x48 -> constant 0x0000011d (image word 0x0000011d)
 *   pool +0x4c -> native_fn_021f3e8c+1 (image word 0x021f3e8d)
 *   branch +0x32 -> +0x3c
 *   test +0x30 cmp r0, #0xc0
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f3e3c; the literal pool and
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
extern void native_fn_021f3e8c(void);
extern void native_fn_02204970(void);


asm u32 native_ov006_021f3e3c (register u32 a0)
{
    push {r4, lr}
    sub sp, #0x8
    add r4, r0, #0x0
    ldr r0, =0x0221c05c
    ldr r0, [r0, #0]
    add r1, r0, #0x0
    add r1, #0xc0
    ldr r1, [r1, #0]
    ldr r2, [r1, #0]
    ldr r1, =0x01ff0000
    and r1, r2
    lsr r1, r1, #0x10
    str r1, [sp, #0x4]
    lsl r1, r2, #0x18
    lsr r2, r1, #0x18
    ldr r1, =0x0000011d
    str r2, [sp]
    ldrb r0, [r0, r1]
    add r2, #0xc
    str r2, [sp]
    mov r1, #0x3
    bl native_fn_021f37f0
    ldr r0, [sp]
    cmp r0, #0xc0
    blt ov006_021f3e3c_L3c
    ldr r1, =native_fn_021f3e8c+1
    add r0, r4, #0x0
    bl native_fn_02204970
ov006_021f3e3c_L3c:
    add sp, #0x8
    pop {r4, pc}
}
