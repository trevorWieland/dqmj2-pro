/* ov000 row 0x02212720: 76 bytes.
 *
 * Decoded shape: 1 call, no loop.
 *
 *   call +0x1c -> native_fn_02211104
 *   test +0x20 cmp r0, #0
 *   1 store instruction(s)
 *
 * Why transcribed rather than written as C: by-value block copy spills one word less (72 vs 76 B)
 * Recorded in docs/authoring/2026-11-11-ov000-pass2.md.
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02212720; the literal pool and
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

extern void native_fn_02211104(void);


asm u32 native_ov000_02212720 (register u32 a0)
{
    stmdb sp!, {r0, r1, r2, r3}
    stmdb sp!, {r4, lr}
    mov r0, r0, lsl #0x10
    mov r1, r1, lsl #0x10
    mov r0, r0, asr #0x10
    mov r1, r1, asr #0x10
    mov r4, #0
    bl native_fn_02211104
    cmp r0, #0
    beq ov000_02212720_L3c
    add r1, sp, #0x10
    add r3, r0, #0x90
    ldmia r1, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    mov r4, #1
ov000_02212720_L3c:
    mov r0, r4
    ldmia sp!, {r4, lr}
    add sp, sp, #0x10
    bx lr
}
