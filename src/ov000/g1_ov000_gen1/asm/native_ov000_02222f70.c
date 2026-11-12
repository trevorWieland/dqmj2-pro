/* ov000 row 0x02222f70: 72 bytes.
 *
 * What it does: 17 instructions, 2 call(s), 3 load(s), 2 store(s), 2 branch(es).
 *
 * Body: the measured instruction stream transcribed from
 * extract/arm9_overlays/ov000.bin at 0x02222f70; every literal pool
 * word and branch target is read from the image, not guessed.
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

extern u8 native_data_0222fd1c[];
extern void native_fn_0201d444(void);
extern void native_fn_02223390(void);


asm u32 native_ov000_02222f70 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    sub sp, sp, #0x20
    ldr r1, =native_data_0222fd1c
    add r0, sp, #0
    bl native_fn_0201d444
    add r0, sp, #0
    bl native_fn_02223390
    mov r1, #0x4000000
    ldr r0, [r1]
    bic r0, r0, #0x1f00
    orr r0, r0, #0xf00
    str r0, [r1]
    ldr r0, [r1]
    bic r0, r0, #0xe000
    str r0, [r1]
    add sp, sp, #0x20
    ldmia sp!, {r3, pc}
}
