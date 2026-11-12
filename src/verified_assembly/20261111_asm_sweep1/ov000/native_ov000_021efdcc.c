/* ov000 row 0x021efdcc: 80 bytes.
 *
 * Decoded shape: 1 call, no loop.
 *
 *   pool +0x4c -> native_fn_0222b910 (image word 0x0222b910)
 *   call +0x40 -> native_fn_0204a644
 *   memory +0x10 ldrh r3, [r0, #6]
 *   memory +0x14 ldrh r0, [r0, #4]
 *   memory +0x1c strh r3, [sp, #0xe]
 *   memory +0x20 strh r0, [sp, #0xc]
 *   memory +0x24 str r2, [sp]
 *   memory +0x28 str ip, [sp, #4]
 *   memory +0x3c str ip, [sp, #8]
 *   5 store instruction(s)
 *
 * Why transcribed rather than written as C: same two-`str` versus `stm` family (76 vs 80 B)
 * Recorded in docs/authoring/2026-11-11-ov000-pass2.md.
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021efdcc; the literal pool and
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

extern void native_fn_0204a644(void);
extern void native_fn_0222b910(void);


asm u32 native_ov000_021efdcc (register u32 a0)
{
    stmdb sp!, {r3, lr}
    sub sp, sp, #0x10
    ldr r0, =native_fn_0222b910
    mov r2, #3
    ldrh r3, [r0, #6]
    ldrh r0, [r0, #4]
    mov ip, #1
    strh r3, [sp, #0xe]
    strh r0, [sp, #0xc]
    str r2, [sp]
    str ip, [sp, #4]
    add r1, sp, #0xc
    mov r0, #0xf
    mov r2, #5
    mov r3, #2
    str ip, [sp, #8]
    bl native_fn_0204a644
    add sp, sp, #0x10
    ldmia sp!, {r3, pc}
}
