/* ov006 row 0x021fe4dc: 32 bytes.
 *
 * What it does: Writes 2 blocks of 3 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x18 -> native_data_0221c134 (image word 0x0221c134)
 *   pool +0x1c -> native_data2_0221c134 (image word 0x0221c134)
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fe4dc; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 13 of 32 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_0221c134[];
extern void native_fn_0220498c(void);
extern u8 native_data2_0221c134[];
extern void native_fn_02203c20(void);


asm u32 native_ov006_021fe4dc (register u32 a0)
{
    push {r3, lr}
    ldr r1, =native_data_0221c134
    mov r0, #0x1
    ldr r1, [r1, #0]
    ldr r1, [r1, #0]
    bl native_fn_0220498c
    ldr r0, =native_data2_0221c134
    bl native_fn_02203c20
    pop {r3, pc}
    mov r8, r8
}
