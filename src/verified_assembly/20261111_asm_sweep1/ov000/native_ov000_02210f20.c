/* ov000 row 0x02210f20: 28 bytes.
 *
 * Decoded shape: 1 call, no loop.
 *
 *   pool +0x18 -> native_data_02238634 (image word 0x02238634)
 *   call +0x10 -> native_fn_02041f90
 *
 * Why transcribed rather than written as C: void tail call becomes `ldr ip`/`bx ip`; the image uses
 * `bl`/`pop`
 * Recorded in docs/authoring/2026-11-11-ov000-pass2.md.
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02210f20; the literal pool and
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

extern u8 native_data_02238634[];
extern void native_fn_02041f90(void);


asm u32 native_ov000_02210f20 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr ip, =native_data_02238634
    mov r3, #0x2c4
    mla r0, r3, r0, ip
    bl native_fn_02041f90
    ldmia sp!, {r3, pc}
}
