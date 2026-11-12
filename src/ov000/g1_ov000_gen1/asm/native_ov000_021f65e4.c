/* ov000 row 0x021f65e4: 52 bytes.
 *
 * What it does: 13 instructions, 1 call(s), 0 load(s), 4 store(s).
 *
 * Body: the measured instruction stream transcribed from
 * extract/arm9_overlays/ov000.bin at 0x021f65e4; every literal pool
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

extern void native_fn_0204a9d4(void);


asm u32 native_ov000_021f65e4 (register u32 a0)
{
    stmdb sp!, {lr}
    sub sp, sp, #0xc
    mov r3, r1
    add r1, sp, #8
    mov ip, #0
    strh ip, [r1]
    strh ip, [r1, #2]
    str r2, [sp]
    mov r2, #1
    str ip, [sp, #4]
    bl native_fn_0204a9d4
    add sp, sp, #0xc
    ldmia sp!, {pc}
}
