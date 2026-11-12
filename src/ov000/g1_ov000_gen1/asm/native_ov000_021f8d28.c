/* ov000 row 0x021f8d28: 92 bytes.
 *
 * What it does: 21 instructions, 2 call(s), 4 load(s), 5 store(s).
 *
 * Body: the measured instruction stream transcribed from
 * extract/arm9_overlays/ov000.bin at 0x021f8d28; every literal pool
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

extern u8 native_data_0222b9c0[];
extern u8 native_data_02236fbc[];
extern void native_fn_0204b85c(void);
extern void native_fn_021f8d84(void);


asm u32 native_ov000_021f8d28 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    sub sp, sp, #0x10
    ldr r0, =native_data_0222b9c0
    mov r2, #2
    ldrh r3, [r0, #0xa]
    ldrh r0, [r0, #8]
    add r1, sp, #0xc
    strh r3, [sp, #0xe]
    strh r0, [sp, #0xc]
    str r2, [sp]
    mov r2, #0x24
    str r2, [sp, #4]
    mov ip, #7
    ldr r0, =native_data_02236fbc
    mov r2, #6
    mov r3, #1
    str ip, [sp, #8]
    bl native_fn_0204b85c
    bl native_fn_021f8d84
    add sp, sp, #0x10
    ldmia sp!, {r3, pc}
}
