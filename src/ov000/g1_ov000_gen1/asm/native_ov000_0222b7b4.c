/* ov000 row 0x0222b7b4: 44 bytes.
 *
 * What it does: 11 instructions, 2 call(s), 1 load(s), 0 store(s).
 *
 * Body: the measured instruction stream transcribed from
 * extract/arm9_overlays/ov000.bin at 0x0222b7b4; every literal pool
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

extern void native_fn_02044454(void);
extern void native_fn_0205bd60(void);


asm u32 native_ov000_0222b7b4 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    bl native_fn_0205bd60
    ldrsb r1, [r0, #0x11]
    mov r0, #0
    orr r0, r0, #0x60
    orr r0, r0, #0x6000000
    cmp r1, #0
    orreq r0, r0, #2
    orreq r0, r0, #0x2000
    bl native_fn_02044454
    ldmia sp!, {r3, pc}
}
