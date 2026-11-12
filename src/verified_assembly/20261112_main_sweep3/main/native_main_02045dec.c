/* main row 0x02045dec: 40 bytes.
 *
 * What it does: Twin of 0x02045dc4 with 1 instead of 0 in the block's third word: builds the same three-word argument block and calls 0x02045c90.
 *
 * Decoded shape: block fill.
 *
 *   1 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x02045dec; the literal pool and
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

extern void native_fn_02045c90(void);


asm u32 native_main_02045dec (register u32 a0)
{
    stmdb sp!, {r3, r4, lr}
    sub sp, sp, #0xc
    ldrb r4, [sp, #0x18]
    ldrb lr, [sp, #0x1c]
    mov r12, #1
    stmia sp, {r4, lr}
    str r12, [sp, #8]
    bl native_fn_02045c90
    add sp, sp, #0xc
    ldmia sp!, {r3, r4, pc}
}
