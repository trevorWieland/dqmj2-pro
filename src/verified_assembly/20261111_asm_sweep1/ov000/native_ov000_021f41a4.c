/* ov000 row 0x021f41a4: 52 bytes.
 *
 * Decoded shape: 1 call, no loop.
 *
 *   pool +0x30 -> native_data_02236ed8 (image word 0x02236ed8)
 *   call +0x24 -> native_fn_02042c1c
 *   test +0x18 cmp r2, #0
 *   memory +0x0c ldr r3, [r3, #4]
 *   memory +0x14 ldrb r2, [r0, #0x278]
 *
 * Why transcribed rather than written as C: same `mla` register choice (48 vs 52 B)
 * Recorded in docs/authoring/2026-11-11-ov000-pass2.md.
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f41a4; the literal pool and
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

extern u8 native_data_02236ed8[];
extern void native_fn_02042c1c(void);


asm u32 native_ov000_021f41a4 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    ldr r3, =native_data_02236ed8
    mov r2, #0x27c
    ldr r3, [r3, #4]
    mla r0, r2, r0, r3
    ldrb r2, [r0, #0x278]
    cmp r2, #0
    moveq r4, #0
    beq ov000_021f41a4_L28
    bl native_fn_02042c1c
ov000_021f41a4_L28:
    mov r0, r4
    ldmia sp!, {r4, pc}
}
