/* main row 0x0202e66c: 48 bytes.
 *
 * What it does: calls 1 helper; 4 loads, 1 store; 1 local pool word (0x020edf90); 2 branches, 2 backward; returns through a restored pc
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   pool +0x2c -> constant 0x020edf90 (image word 0x020edf90)
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x0202e66c; the literal pool and
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

extern void native_fn_0202e434(void);


asm u32 native_main_0202e66c (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r1, =0x020edf90
    mov r2, #0x3e
    ldr r0, [r1], #4
    bl native_fn_0202e434
    ldr r0, =0x020edf90
    ldr r1, [r0, #0xfc]
    bic r1, r1, #1
    bic r1, r1, #2
    str r1, [r0, #0xfc]
    ldmia sp!, {r3, pc}
}
