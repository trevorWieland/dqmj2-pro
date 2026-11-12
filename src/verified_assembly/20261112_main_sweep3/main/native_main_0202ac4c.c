/* main row 0x0202ac4c: 68 bytes.
 *
 * What it does: Skeleton sibling of 0x0202ac08 with its own callee pair (0x0203c00c, 0x0203bcd8): the same pooled gate byte, the same null fallback and the same argument + 0x28, returning 1.
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   pool +0x3c -> constant 0x020edf20 (image word 0x020edf20)
 *   pool +0x40 -> constant 0x020edf44 (image word 0x020edf44)
 *   test +0x14 cmp r1, #1
 *   test +0x1c cmp r4, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x0202ac4c; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the table, the record layout and the callee contract are not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_0203c00c(void);
extern void native_fn_0203bcd8(void);


asm u32 native_main_0202ac4c (register u32 a0)
{
    stmdb sp!, {r4, lr}
    ldr r1, =0x020edf20
    mov r4, r0
    ldrb r1, [r1]
    mov r0, #0
    cmp r1, #1
    ldmneia sp!, {r4, pc}
    cmp r4, #0
    ldreq r4, =0x020edf44
    mov r0, r4
    bl native_fn_0203c00c
    add r0, r4, #0x28
    bl native_fn_0203bcd8
    mov r0, #1
    ldmia sp!, {r4, pc}
}
