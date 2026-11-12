/* ov000 row 0x0220a0d0: 80 bytes.
 *
 * Decoded shape: 1 call, no loop.
 *
 *   call +0x0c -> ov000_saved_world_position_get_021e07b8
 *   memory +0x10 ldr r2, [r4, #0x74]
 *   memory +0x14 ldr r1, [r0, #4]
 *   memory +0x18 ldr ip, [r4, #0x70]
 *   memory +0x20 ldr r3, [r0]
 *   memory +0x30 ldr r3, [r4, #0x78]
 *   memory +0x34 ldr r0, [r0, #8]
 *
 * Why transcribed rather than written as C: 64-bit distance accumulates one instruction short (76 vs 80 B)
 * Recorded in docs/authoring/2026-11-11-ov000-pass2.md.
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0220a0d0; the literal pool and
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

extern void ov000_saved_world_position_get_021e07b8(void);


asm u32 native_ov000_0220a0d0 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r4, r0
    mov r0, #0
    bl ov000_saved_world_position_get_021e07b8
    ldr r2, [r4, #0x74]
    ldr r1, [r0, #4]
    ldr ip, [r4, #0x70]
    sub lr, r2, r1
    ldr r3, [r0]
    smull r1, r2, lr, lr
    sub r3, ip, r3
    smlal r1, r2, r3, r3
    ldr r3, [r4, #0x78]
    ldr r0, [r0, #8]
    sub r0, r3, r0
    smlal r1, r2, r0, r0
    mov r0, r1, lsr #0xc
    mov r1, r2, asr #0xc
    orr r0, r0, r2, lsl #20
    ldmia sp!, {r4, pc}
}
