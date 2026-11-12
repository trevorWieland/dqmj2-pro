/* ov006 row 0x021f2370: 32 bytes.
 *
 * What it does: Writes one block of 1 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x14 -> constant 0x0221c008 (image word 0x0221c008)
 *   pool +0x18 -> native_fn_02204970+1 (image word 0x02204971)
 *   pool +0x1c -> native_fn_021f25c8+1 (image word 0x021f25c9)
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f2370; the literal pool and
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

extern void native_fn_02204970(void);
extern void native_fn_021f25c8(void);


asm u32 native_ov006_021f2370 (register u32 a0)
{
    ldr r0, =0x0221c008
    mov r2, #0x1
    ldr r1, [r0, #0]
    ldr r3, =native_fn_02204970+1
    strb r2, [r1, #0x19]
    ldr r0, [r0, #0]
    ldr r1, =native_fn_021f25c8+1
    ldr r0, [r0, #0xc]
    bx r3
    mov r8, r8
}
