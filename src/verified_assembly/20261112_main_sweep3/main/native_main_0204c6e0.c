/* main row 0x0204c6e0: 60 bytes.
 *
 * What it does: Stores -1 at the first pooled word, clears the pooled byte and the word at +4, then calls the fill primitive 0x02008d78 with 0x40.
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   pool +0x30 -> native_data_020ddb4c (image word 0x020ddb4c)
 *   pool +0x34 -> constant 0x02102d78 (image word 0x02102d78)
 *   pool +0x38 -> constant 0x02102d80 (image word 0x02102d80)
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x0204c6e0; the literal pool and
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

extern u8 native_data_020ddb4c[];
extern void native_fn_02008d78(void);


asm u32 native_main_0204c6e0 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r2, =native_data_020ddb4c
    mvn r12, #0
    ldr r3, =0x02102d78
    mov r1, #0
    ldr r0, =0x02102d80
    str r12, [r2]
    str r1, [r3, #4]
    mov r2, #0x40
    strb r1, [r3]
    bl native_fn_02008d78
    ldmia sp!, {r3, pc}
}
