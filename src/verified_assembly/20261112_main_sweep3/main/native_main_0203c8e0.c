/* main row 0x0203c8e0: 40 bytes.
 *
 * What it does: calls 1 helper; 3 loads, 1 store; 1 local pool word (0x04000540); returns through a restored pc
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   pool +0x24 -> constant 0x04000540 (image word 0x04000540)
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x0203c8e0; the literal pool and
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

extern void native_fn_0202e300(void);


asm u32 native_main_0203c8e0 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r4, r0
    bl native_fn_0202e300
    ldr r2, [r4, #0xc]
    ldr r1, [r4, #8]
    ldr r0, =0x04000540
    orr r1, r1, r2, lsl #1
    str r1, [r0]
    ldmia sp!, {r4, pc}
}
