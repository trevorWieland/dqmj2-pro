/* ov000 row 0x02214068: 88 bytes.
 *
 * Decoded shape: 1 call, no loop.
 *
 *   call +0x4c -> native_fn_02065e44
 *   test +0x08 cmp r0, #0
 *   memory +0x18 ldrsh lr, [r0, #0x18]
 *   memory +0x1c ldrb r3, [r0, #0x1a]
 *   memory +0x48 str ip, [sp, #8]
 *   2 store instruction(s)
 *
 * Why transcribed rather than written as C: null-record branch orders the three stack words differently
 * (58-byte diff)
 * Recorded in docs/authoring/2026-11-11-ov000-pass2.md.
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02214068; the literal pool and
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

extern void native_fn_02065e44(void);


asm u32 native_ov000_02214068 (register u32 a0)
{
    stmdb sp!, {r4, r5, lr}
    sub sp, sp, #0xc
    cmp r0, #0
    beq ov000_02214068_L24
    add r4, r0, #0x20
    add r5, r0, #0x40
    ldrsh lr, [r0, #0x18]
    ldrb r3, [r0, #0x1a]
    b ov000_02214068_L34
ov000_02214068_L24:
    mov r4, #0
    mov r5, r4
    mov lr, r4
    mov r3, r4
ov000_02214068_L34:
    stmia sp, {r1, r2}
    mov ip, #0
    mov r0, r4
    mov r1, r5
    mov r2, lr
    str ip, [sp, #8]
    bl native_fn_02065e44
    add sp, sp, #0xc
    ldmia sp!, {r4, r5, pc}
}
