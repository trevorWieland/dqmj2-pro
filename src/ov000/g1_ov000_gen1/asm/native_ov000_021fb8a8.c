/* ov000 row 0x021fb8a8: 80 bytes.
 *
 * What it does: 20 instructions, 3 call(s), 1 load(s), 0 store(s), 2 branch(es).
 *
 * Body: the measured instruction stream transcribed from
 * extract/arm9_overlays/ov000.bin at 0x021fb8a8; every literal pool
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

extern void native_fn_02062aa0(void);
extern void native_fn_02062ad0(void);
extern void native_fn_021fb97c(void);


asm u32 native_ov000_021fb8a8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    bl native_fn_02062aa0
    mov r4, r0
    bl native_fn_02062ad0
    add r0, r4, r0
    ands r5, r0, #0xff
    mov r4, #0
    beq ov000_021fb8a8_L048
ov000_021fb8a8_L020:
    mov r0, r4
    bl native_fn_021fb97c
    ldrb r0, [r0, #0x33]
    cmp r0, #0
    movne r0, r4
    ldmneia sp!, {r3, r4, r5, pc}
    add r0, r4, #1
    and r4, r0, #0xff
    cmp r4, r5
    blo ov000_021fb8a8_L020
ov000_021fb8a8_L048:
    mov r0, #0xff
    ldmia sp!, {r3, r4, r5, pc}
}
