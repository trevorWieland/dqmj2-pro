/* ov000 row 0x021ff478: 84 bytes.
 *
 * What it does: 20 instructions, 5 call(s), 2 load(s), 0 store(s).
 *
 * Body: the measured instruction stream transcribed from
 * extract/arm9_overlays/ov000.bin at 0x021ff478; every literal pool
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

extern u8 native_data_0222f490[];
extern void native_fn_0202a498(void);
extern void native_fn_0203cc2c(void);
extern void native_fn_0204518c(void);
extern void native_fn_0204820c(void);
extern void native_fn_02048308(void);


asm u32 native_ov000_021ff478 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    sub sp, sp, #8
    ldr r0, =native_data_0222f490
    mov r1, #2
    bl native_fn_0203cc2c
    mov r4, r0
    add r0, sp, #0
    mov r1, r4
    mov r2, #0
    bl native_fn_0204518c
    ldr r0, [sp]
    mov r1, #0xa0
    mov r2, #0x20
    bl native_fn_0204820c
    bl native_fn_02048308
    mov r1, r4
    mov r0, #2
    bl native_fn_0202a498
    add sp, sp, #8
    ldmia sp!, {r4, pc}
}
