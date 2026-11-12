/* main row 0x0209073c: 32 bytes.
 *
 * What it does: Thumb variadic forwarder: calls 0x02090794 with r0 = 2, r1 = sp + 8, r2 = 0x021d162c and r3 = 0x10, then tail-branches to its own first argument.
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   pool +0x1c -> constant 0x021d162c (image word 0x021d162c)
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x0209073c; the literal pool and
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

extern void native_fn_02090794(void);


asm u32 native_main_0209073c (register u32 a0)
{
    push {r0, r1, r2, r3}
    push {r3, lr}
    ldr r2, =0x021d162c
    mov r0, #2
    add r1, sp, #8
    mov r3, #0x10
    bl native_fn_02090794
    ldr r0, =0x021d162c
    pop {r3}
    pop {r3}
    add sp, #0x10
    bx r3
    mov r8, r8
}
