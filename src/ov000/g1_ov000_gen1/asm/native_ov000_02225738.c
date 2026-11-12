/* ov000 row 0x02225738: 80 bytes.
 *
 * What it does: 20 instructions, 5 call(s), 1 branch(es).
 *
 * Body: the measured instruction stream transcribed from
 * extract/arm9_overlays/ov000.bin at 0x02225738; every literal pool
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

extern void native_fn_020642cc(void);
extern void native_fn_020c4928(void);
extern void native_fn_020c5f48(void);
extern void native_fn_02223c14(void);
extern void native_fn_022273a8(void);


asm u32 native_ov000_02225738 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r0, #0
    bl native_fn_022273a8
    mov r4, #0
ov000_02225738_L010:
    mov r0, r4
    bl native_fn_02223c14
    mov r1, r0
    and r0, r4, #0xff
    bl native_fn_020c4928
    add r0, r4, #1
    mov r0, r0, lsl #0x18
    mov r4, r0, asr #0x18
    cmp r4, #4
    blt ov000_02225738_L010
    mov r0, #0x28
    bl native_fn_020642cc
    mov r0, #6
    bl native_fn_020c5f48
    mov r0, #0
    ldmia sp!, {r4, pc}
}
