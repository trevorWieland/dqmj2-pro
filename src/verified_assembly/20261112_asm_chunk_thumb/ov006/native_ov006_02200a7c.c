/* ov006 row 0x02200a7c: 44 bytes.
 *
 * What it does: Writes one block of 2 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x20 -> native_data2_0221c160 (image word 0x0221c160)
 *   pool +0x24 -> constant 0x0001b160 (image word 0x0001b160)
 *   pool +0x28 -> constant 0x0001b140 (image word 0x0001b140)
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02200a7c; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 9 of 44 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data2_0221c160[];
extern void native_fn_02201248(void);


asm u32 native_ov006_02200a7c (register u32 a0)
{
    push {r3, lr}
    ldr r1, =native_data2_0221c160
    str r0, [r1, #0]
    ldr r1, =0x0001b160
    add r0, r0, r1
    bl native_fn_02201248
    ldr r1, =native_data2_0221c160
    ldr r0, =0x0001b140
    ldr r2, [r1, #0]
    mov r3, #0x0
    str r3, [r2, r0]
    ldr r1, [r1, #0]
    add r0, r0, #0x4
    str r3, [r1, r0]
    pop {r3, pc}
}
