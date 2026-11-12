/* ov006 row 0x022043a4: 60 bytes.
 *
 * What it does: Writes one block of 4 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x30 -> constant 0xc1fffcff (image word 0xc1fffcff)
 *   pool +0x34 -> constant 0x0221c1ac (image word 0x0221c1ac)
 *   pool +0x38 -> native_fn_022030dc+1 (image word 0x022030dd)
 *   branch +0x1c -> +0x20
 *   test +0x1a cmp r1, r2
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x022043a4; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 16 of 60 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_022030dc(void);


asm u32 native_ov006_022043a4 (register u32 a0)
{
    add r1, r0, #0x0
    ldr r3, [r1, #0]
    ldr r2, =0xc1fffcff
    mov r0, #0x0
    and r3, r2
    mov r2, #0x2
    lsl r2, r2, #0x8
    orr r3, r2
    str r3, [r1, #0]
    ldr r3, =0x0221c1ac
    lsl r2, r2, #0x1
    ldr r3, [r3, #0]
    add r2, r3, r2
    cmp r1, r2
    blo ov006_022043a4_L20
    mov r0, #0x1
ov006_022043a4_L20:
    lsl r0, r0, #0x2
    add r2, r3, r0
    mov r0, #0x2
    lsl r0, r0, #0xa
    ldr r3, =native_fn_022030dc+1
    ldr r0, [r2, r0]
    bx r3
    mov r8, r8
}
