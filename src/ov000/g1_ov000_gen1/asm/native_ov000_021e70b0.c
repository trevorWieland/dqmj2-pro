/* ov000 row 0x021e70b0: 88 bytes.
 *
 * What it does: 22 instructions, 4 call(s), 3 load(s), 0 store(s).
 *
 * Body: the measured instruction stream transcribed from
 * extract/arm9_overlays/ov000.bin at 0x021e70b0; every literal pool
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

extern void native_fn_02028484(void);
extern void native_fn_0202859c(void);
extern void native_fn_021e63a4(void);
extern void native_fn_021e6db8(void);


asm u32 native_ov000_021e70b0 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, lr}
    sub sp, sp, #0xc
    mov r7, r1
    mov r6, r2
    mov r5, r3
    bl native_fn_021e63a4
    mov r4, r0
    add r0, sp, #0
    mov r1, r7
    mov r2, r6
    mov r3, r5
    bl native_fn_021e6db8
    ldr r1, [sp]
    ldr r2, [sp, #4]
    ldr r3, [sp, #8]
    mov r0, r4
    bl native_fn_02028484
    mov r0, r4
    mov r1, #0
    bl native_fn_0202859c
    add sp, sp, #0xc
    ldmia sp!, {r4, r5, r6, r7, pc}
}
