/* ov000 row 0x0220a4b4: 48 bytes.
 *
 * What it does: 12 instructions, 1 call(s), 1 branch(es).
 *
 * Body: the measured instruction stream transcribed from
 * extract/arm9_overlays/ov000.bin at 0x0220a4b4; every literal pool
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

extern void native_fn_0220a358(void);


asm u32 native_ov000_0220a4b4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, #0
    mov r4, r5
ov000_0220a4b4_L00c:
    mov r0, r4
    bl native_fn_0220a358
    cmp r0, #0
    add r4, r4, #1
    addne r5, r5, #1
    cmp r4, #0x30
    blt ov000_0220a4b4_L00c
    mov r0, r5
    ldmia sp!, {r3, r4, r5, pc}
}
