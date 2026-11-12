/* ov000 row 0x021f7278: 88 bytes.
 *
 * What it does: 21 instructions, 3 call(s), 3 load(s), 1 store(s), 1 branch(es).
 *
 * Body: the measured instruction stream transcribed from
 * extract/arm9_overlays/ov000.bin at 0x021f7278; every literal pool
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

extern u8 native_data_0222b9a0[];
extern void native_fn_02061944(void);
extern void native_fn_020622ec(void);
extern void native_fn_02065d28(void);


asm u32 native_ov000_021f7278 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    bl native_fn_02061944
    mov r5, r0
    mov r0, #0
    mov r2, r0
    mov r1, #0xf
    bl native_fn_020622ec
    ldr r4, =native_data_0222b9a0
    mov r6, #0
ov000_021f7278_L024:
    mov r0, r6, lsl #1
    ldrsb r0, [r4, r0]
    bl native_fn_02065d28
    add r1, r6, #1
    ldr r2, [r5, #0x25c]
    mov r1, r1, lsl #0x18
    sub r0, r2, r0
    mov r6, r1, asr #0x18
    str r0, [r5, #0x25c]
    cmp r6, #0xf
    blt ov000_021f7278_L024
    ldmia sp!, {r4, r5, r6, pc}
}
