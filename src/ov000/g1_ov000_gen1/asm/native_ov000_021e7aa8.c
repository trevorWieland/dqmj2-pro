/* ov000 row 0x021e7aa8: 68 bytes.
 *
 * What it does: 16 instructions, 3 call(s), 2 load(s), 0 store(s), 2 branch(es).
 *
 * Body: the measured instruction stream transcribed from
 * extract/arm9_overlays/ov000.bin at 0x021e7aa8; every literal pool
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

extern u8 native_data_0222ed70[];
extern void native_fn_0205e73c(void);
extern void native_fn_021e7aa0(void);


asm u32 native_ov000_021e7aa8 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r5, #1
    mov r6, #0
    bl native_fn_021e7aa0
    cmp r0, #0
    bls ov000_021e7aa8_L038
    ldr r4, =native_data_0222ed70
ov000_021e7aa8_L01c:
    ldr r0, [r4, r6, lsl #2]
    bl native_fn_0205e73c
    add r6, r6, #1
    and r5, r5, r0
    bl native_fn_021e7aa0
    cmp r6, r0
    blo ov000_021e7aa8_L01c
ov000_021e7aa8_L038:
    mov r0, r5
    ldmia sp!, {r4, r5, r6, pc}
}
