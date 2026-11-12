/* ov000 row 0x021dfd80: 44 bytes.
 *
 * What it does: 10 instructions, 2 call(s), 1 load(s), 0 store(s).
 *
 * Body: the measured instruction stream transcribed from
 * extract/arm9_overlays/ov000.bin at 0x021dfd80; every literal pool
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

extern u8 native_data_0222ebd8[];
extern void native_fn_02042fec(void);
extern void native_fn_0207a9ec(void);


asm u32 native_ov000_021dfd80 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r4, #1
    ldr r0, =native_data_0222ebd8
    mov r1, r4
    bl native_fn_02042fec
    and r4, r0, #1
    mov r0, #1
    bl native_fn_0207a9ec
    and r0, r4, r0
    ldmia sp!, {r4, pc}
}
