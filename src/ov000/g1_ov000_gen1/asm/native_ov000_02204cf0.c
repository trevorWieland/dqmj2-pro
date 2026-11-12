/* ov000 row 0x02204cf0: 56 bytes.
 *
 * What it does: 13 instructions, 2 call(s), 3 load(s), 1 store(s), 1 branch(es).
 *
 * Body: the measured instruction stream transcribed from
 * extract/arm9_overlays/ov000.bin at 0x02204cf0; every literal pool
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

extern u8 native_data_02238190[];
extern void native_fn_020622ec(void);
extern void native_fn_02204f10(void);


asm u32 native_ov000_02204cf0 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r0, =native_data_02238190
    ldrb r0, [r0, #1]
    cmp r0, #0
    bne ov000_02204cf0_L018
    bl native_fn_02204f10
ov000_02204cf0_L018:
    ldr r3, =native_data_02238190
    mov r2, #0
    mov r0, #6
    mov r1, #0xb
    strb r2, [r3, #1]
    bl native_fn_020622ec
    ldmia sp!, {r3, pc}
}
