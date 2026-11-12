/* ov000 row 0x021fdf44: 84 bytes.
 *
 * What it does: 21 instructions, 2 call(s), 4 load(s), 0 store(s).
 *
 * Body: the measured instruction stream transcribed from
 * extract/arm9_overlays/ov000.bin at 0x021fdf44; every literal pool
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

extern void native_fn_0204b138(void);


asm u32 native_ov000_021fdf44 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    movs r4, r0
    ldmeqia sp!, {r4, pc}
    ldr r0, [r4, #4]
    mov r1, #0
    cmp r0, #0
    movgt r2, #1
    movle r2, #0
    add r0, r4, #0xa8
    bl native_fn_0204b138
    ldrh r1, [r4, #0xc]
    ldr r2, [r4, #4]
    ldrh r0, [r4, #0xe]
    add r1, r2, r1
    cmp r1, r0
    movlt r2, #1
    movge r2, #0
    add r0, r4, #0xa8
    mov r1, #1
    bl native_fn_0204b138
    ldmia sp!, {r4, pc}
}
