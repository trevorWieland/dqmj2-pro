/* ov000 row 0x02215984: 52 bytes.
 *
 * What it does: 13 instructions, 2 call(s), 5 load(s), 2 store(s).
 *
 * Body: the measured instruction stream transcribed from
 * extract/arm9_overlays/ov000.bin at 0x02215984; every literal pool
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

extern void native_fn_02048a60(void);
extern void native_fn_0205f98c(void);


asm u32 native_ov000_02215984 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    ldrh r3, [r1]
    ldrh r2, [r1, #2]
    mov r4, r0
    mov r1, #0
    strh r3, [r4, #0x48]
    strh r2, [r4, #0x4a]
    ldr r0, [r4, #0x1c]
    bl native_fn_0205f98c
    ldrsh r1, [r4, #0x48]
    ldrsh r2, [r4, #0x4a]
    bl native_fn_02048a60
    ldmia sp!, {r4, pc}
}
