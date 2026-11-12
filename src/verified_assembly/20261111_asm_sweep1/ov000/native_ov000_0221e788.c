/* ov000 row 0x0221e788: 96 bytes.
 *
 * Decoded shape: 1 call, no loop.
 *
 *   pool +0x58 -> native_data_02246348 (image word 0x02246348)
 *   pool +0x58 -> native_data_02246348 (image word 0x02246348)
 *   pool +0x58 -> native_data_02246348 (image word 0x02246348)
 *   pool +0x5c -> native_data_02101ae8 (image word 0x02101ae8)
 *   call +0x1c -> native_fn_02048a60
 *   test +0x04 cmp r0, #0
 *   memory +0x14 ldr r0, [r0, #0x28]
 *   memory +0x24 ldr r1, [r0, #0x28]
 *   memory +0x28 ldr r0, [r1, #0x7c]
 *   memory +0x38 ldr r1, [r0, #0x28]
 *   memory +0x3c ldr r0, [r1, #0x7c]
 *   memory +0x44 str r0, [r1, #0x7c]
 *   memory +0x50 str r1, [r0, #0xc84]
 *   2 store instruction(s)
 *
 * Why transcribed rather than written as C: enable branch re-reads the object once more (92 vs 96 B)
 * Recorded in docs/authoring/2026-11-11-ov000-pass2.md.
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0221e788; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the meaning of the fields, blocks and callee contracts
 * the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_02101ae8[];
extern u8 native_data_02246348[];
extern void native_fn_02048a60(void);


asm u32 native_ov000_0221e788 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    cmp r0, #0
    beq ov000_0221e788_L34
    ldr r0, =native_data_02246348
    mov r1, #0xa0
    ldr r0, [r0, #0x28]
    mov r2, #0x18
    bl native_fn_02048a60
    ldr r0, =native_data_02246348
    ldr r1, [r0, #0x28]
    ldr r0, [r1, #0x7c]
    orr r0, r0, #2
    b ov000_0221e788_L44
ov000_0221e788_L34:
    ldr r0, =native_data_02246348
    ldr r1, [r0, #0x28]
    ldr r0, [r1, #0x7c]
    bic r0, r0, #2
ov000_0221e788_L44:
    str r0, [r1, #0x7c]
    ldr r0, =native_data_02101ae8
    mov r1, #1
    str r1, [r0, #0xc84]
    ldmia sp!, {r3, pc}
}
