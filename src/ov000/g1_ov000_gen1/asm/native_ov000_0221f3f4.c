/* ov000 row 0x0221f3f4: 80 bytes.
 *
 * What it does: 16 instructions, 2 call(s), 4 load(s), 2 store(s).
 *
 * Body: the measured instruction stream transcribed from
 * extract/arm9_overlays/ov000.bin at 0x0221f3f4; every literal pool
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

extern u8 native_data_020db214[];
extern u8 native_data_020db218[];
extern u8 native_data_0222fb60[];
extern u8 native_data_022463a0[];
extern void native_fn_0205d9e8(void);
extern void native_fn_0205db90(void);


asm u32 native_ov000_0221f3f4 (register u32 a0)
{
    stmdb sp!, {lr}
    sub sp, sp, #0x24
    ldr r1, =native_data_0222fb60
    add r0, sp, #4
    mvn r2, #0
    bl native_fn_0205db90
    mov r0, #1
    ldr r2, =native_data_020db218
    ldr r3, =native_data_020db214
    add r1, sp, #4
    str r0, [sp]
    bl native_fn_0205d9e8
    ldr r1, =native_data_022463a0
    str r0, [r1, #8]
    add sp, sp, #0x24
    ldmia sp!, {pc}
}
