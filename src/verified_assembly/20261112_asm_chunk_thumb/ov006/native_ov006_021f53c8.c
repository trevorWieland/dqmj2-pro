/* ov006 row 0x021f53c8: 52 bytes.
 *
 * What it does: Writes one block of 3 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x30 -> constant 0x0221c08c (image word 0x0221c08c)
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f53c8; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 13 of 52 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02203114(void);
extern void native_fn_02202a80(void);


asm u32 native_ov006_021f53c8 (register u32 a0)
{
    push {r3, r4, r5, lr}
    add r5, r0, #0x0
    ldr r0, =0x0221c08c
    ldr r0, [r0, #0]
    ldr r0, [r0, #0x60]
    bl native_fn_02203114
    add r4, r0, #0x0
    add r0, r5, #0x0
    add r1, sp, #0x0
    mov r2, #0x4
    bl native_fn_02202a80
    str r0, [r4, #0x8]
    add r0, #0x20
    add r1, r0, #0x0
    add r1, #0x10
    str r1, [r4, #0]
    ldr r1, [r0, #0x4]
    add r0, r0, r1
    add r0, #0x8
    str r0, [r4, #0x4]
    add r0, r4, #0x0
    pop {r3, r4, r5, pc}
}
