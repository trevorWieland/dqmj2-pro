/* main row 0x0208522c: 56 bytes.
 *
 * What it does: calls 1 helper; 3 loads, 0 stores; 2 local pool words (0x021c96b0, 0x00001810); returns through a restored pc
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   pool +0x30 -> constant 0x021c96b0 (image word 0x021c96b0)
 *   pool +0x34 -> constant 0x00001810 (image word 0x00001810)
 *   test +0x20 cmp r1, #2
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x0208522c; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the field meanings and the callee contracts are not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02085478(void);


asm u32 native_main_0208522c (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r12, =0x021c96b0
    ldr r2, =0x00001810
    mov r3, #0xb0
    mla r2, r0, r2, r12
    mla r0, r1, r3, r2
    ldr r1, [r0, #0x18]
    and r1, r1, #2
    cmp r1, #2
    ldmneia sp!, {r3, pc}
    bl native_fn_02085478
    ldmia sp!, {r3, pc}
}
