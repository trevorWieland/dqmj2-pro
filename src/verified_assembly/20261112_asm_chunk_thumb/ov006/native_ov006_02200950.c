/* ov006 row 0x02200950: 36 bytes.
 *
 * What it does: Writes one block of 4 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x1c -> constant 0x0221c15c (image word 0x0221c15c)
 *   pool +0x20 -> native_fn_02200974+1 (image word 0x02200975)
 *   branch +0x12 -> +0x1a
 *   test +0x10 cmp r1, #0x8
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02200950; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 14 of 36 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02200974(void);
extern void native_fn_02204970(void);


asm u32 native_ov006_02200950 (register u32 a0)
{
    push {r3, lr}
    ldr r1, =0x0221c15c
    ldr r3, [r1, #0]
    ldrb r2, [r3, #0x1d]
    add r2, r2, #0x1
    strb r2, [r3, #0x1d]
    ldr r1, [r1, #0]
    ldrb r1, [r1, #0x1d]
    cmp r1, #0x8
    blo ov006_02200950_L1a
    ldr r1, =native_fn_02200974+1
    bl native_fn_02204970
ov006_02200950_L1a:
    pop {r3, pc}
}
