/* ov000 row 0x021f83e0: 56 bytes.
 *
 * What it does: 14 instructions, 3 call(s), 2 load(s), 1 store(s).
 *
 * Body: the measured instruction stream transcribed from
 * extract/arm9_overlays/ov000.bin at 0x021f83e0; every literal pool
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

extern void native_fn_0204ac5c(void);
extern void native_fn_020602dc(void);
extern void native_fn_0221742c(void);


asm u32 native_ov000_021f83e0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r0, r0, lsl #0x18
    mov r0, r0, asr #0x18
    mov r5, r1
    bl native_fn_0221742c
    mov r4, r0
    bl native_fn_020602dc
    ldr r1, [r4]
    mov r3, r5
    str r1, [sp]
    ldrb r2, [r4, #0xb]
    mov r1, #1
    bl native_fn_0204ac5c
    ldmia sp!, {r3, r4, r5, pc}
}
