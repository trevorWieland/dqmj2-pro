/* ov006 row 0x021fd62c: 52 bytes.
 *
 * What it does: Writes one block of 2 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x2c -> native_data_0220b8bc (image word 0x0220b8bc)
 *   pool +0x30 -> constant 0x0221c114 (image word 0x0221c114)
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fd62c; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 10 of 52 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_0220b8bc[];
extern void native_fn_021fe580(void);


asm u32 native_ov006_021fd62c (register u32 a0)
{
    push {r3, lr}
    ldr r2, =native_data_0220b8bc
    add r1, sp, #0x0
    ldrb r3, [r2, #0]
    add r0, sp, #0x0
    strb r3, [r1, #0]
    ldrb r3, [r2, #0x1]
    strb r3, [r1, #0x1]
    ldrb r3, [r2, #0x2]
    ldrb r2, [r2, #0x3]
    strb r3, [r1, #0x2]
    strb r2, [r1, #0x3]
    ldr r2, =0x0221c114
    mov r1, #0x1
    ldrsb r1, [r2, r1]
    ldrb r1, [r0, r1]
    ldr r0, [r2, #0x4]
    add r2, r1, #0x0
    bl native_fn_021fe580
    pop {r3, pc}
    mov r8, r8
}
