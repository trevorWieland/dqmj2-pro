/* main row 0x02084830: 44 bytes.
 *
 * What it does: calls 1 helper; 1 load, 0 stores; returns through a restored pc
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   test +0x0c cmp r4, #0x10
 *   test +0x20 tst r1, r0, lsl r4
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x02084830; the literal pool and
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

extern void native_fn_0208481c(void);


asm u32 native_main_02084830 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    movs r4, r1
    movmi r4, #0
    cmp r4, #0x10
    movge r4, #0xf
    bl native_fn_0208481c
    ldrh r1, [r0]
    mov r0, #1
    tst r1, r0, lsl r4
    moveq r0, #0
    ldmia sp!, {r4, pc}
}
