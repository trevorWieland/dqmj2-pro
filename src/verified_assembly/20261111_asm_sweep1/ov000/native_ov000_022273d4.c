/* ov000 row 0x022273d4: 52 bytes.
 *
 * Decoded shape: 1 call, no loop.
 *
 *   pool +0x2c -> native_data_02246c84 (image word 0x02246c84)
 *   pool +0x30 -> native_data_02246cb4 (image word 0x02246cb5)
 *   call +0x18 -> native_fn_02008e0c
 *   memory +0x24 strb r1, [r0, r4]
 *   1 store instruction(s)
 *
 * Why transcribed rather than written as C: row base literal materialised in `r2` instead of `r3` (2-byte
 * diff)
 * Recorded in docs/authoring/2026-11-11-ov000-pass2.md.
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022273d4; the literal pool and
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

extern u8 native_data_02246c84[];
extern void native_fn_02008e0c(void);


asm u32 native_ov000_022273d4 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r2, #0x84
    mul r4, r0, r2
    ldr r3, =native_data_02246c84
    mov r0, r1
    add r1, r3, r4
    bl native_fn_02008e0c
    ldr r0, =0x02246cb5
    mov r1, #0
    strb r1, [r0, r4]
    ldmia sp!, {r4, pc}
}
