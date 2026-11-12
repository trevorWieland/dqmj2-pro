/* ov006 row 0x02204974: 24 bytes.
 *
 * What it does: Writes one block of 4 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x10 -> constant 0x0221c1e8 (image word 0x0221c1e8)
 *   pool +0x14 -> native_fn_022030dc+1 (image word 0x022030dd)
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02204974; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 11 of 24 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_022030dc(void);


asm u32 native_ov006_02204974 (register u32 a0)
{
    ldr r2, =0x0221c1e8
    lsl r0, r0, #0x6
    ldr r2, [r2, #0]
    ldr r3, =native_fn_022030dc+1
    add r0, r2, r0
    ldr r0, [r0, #0x4]
    bx r3
    mov r8, r8
}
