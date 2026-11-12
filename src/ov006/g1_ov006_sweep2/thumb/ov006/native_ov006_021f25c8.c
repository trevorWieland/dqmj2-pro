/* ov006 row 0x021f25c8: 60 bytes.
 *
 * What it does: Writes one block of 1 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x34 -> constant 0x0221c008 (image word 0x0221c008)
 *   pool +0x38 -> native_fn_021f2604+1 (image word 0x021f2605)
 *   branch +0x24 -> +0x2e
 *   test +0x22 cmp r0, #0xc0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f25c8; the literal pool and
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

extern void native_fn_02202f98(void);
extern void native_fn_021f2404(void);
extern void native_fn_021f2604(void);
extern void native_fn_02204970(void);


asm u32 native_ov006_021f25c8 (register u32 a0)
{
    push {r4, lr}
    sub sp, #0x8
    add r4, r0, #0x0
    ldr r0, =0x0221c008
    mov r1, #0x0
    ldr r0, [r0, #0]
    add r2, sp, #0x4
    ldr r0, [r0, #0x8]
    add r3, sp, #0x0
    bl native_fn_02202f98
    ldr r0, [sp]
    add r0, r0, #0x4
    str r0, [sp]
    bl native_fn_021f2404
    ldr r0, [sp]
    cmp r0, #0xc0
    blt ov006_021f25c8_L2e
    ldr r1, =native_fn_021f2604+1
    add r0, r4, #0x0
    bl native_fn_02204970
ov006_021f25c8_L2e:
    add sp, #0x8
    pop {r4, pc}
    mov r8, r8
}
