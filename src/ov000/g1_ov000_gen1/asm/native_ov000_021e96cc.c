/* ov000 row 0x021e96cc: 64 bytes.
 *
 * What it does: 16 instructions, 3 call(s), 2 branch(es).
 *
 * Body: the measured instruction stream transcribed from
 * extract/arm9_overlays/ov000.bin at 0x021e96cc; every literal pool
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

extern void native_fn_0205cba4(void);
extern void native_fn_0205cea4(void);
extern void native_fn_021f3cd0(void);


asm u32 native_ov000_021e96cc (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    mov r7, r1
    mov r6, r2
    mov r5, r3
    bl native_fn_021f3cd0
    movs r1, r0
    beq ov000_021e96cc_L038
    mov r0, r7
    mov r2, r6
    bl native_fn_0205cba4
    movs r4, r0
    bmi ov000_021e96cc_L038
    mov r1, r5
    bl native_fn_0205cea4
ov000_021e96cc_L038:
    mov r0, r4
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
