/* ov000 row 0x021f95c8: 76 bytes.
 *
 * What it does: 19 instructions, 2 call(s), 2 load(s), 0 store(s), 2 branch(es).
 *
 * Body: the measured instruction stream transcribed from
 * extract/arm9_overlays/ov000.bin at 0x021f95c8; every literal pool
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

extern void native_fn_021f9614(void);
extern void ov000_display_context_02215698(void);


asm u32 native_ov000_021f95c8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    mov r7, r0
    bl ov000_display_context_02215698
    mov r4, r0
    mov r6, #0x7f
    mov r5, #0
ov000_021f95c8_L018:
    add r0, r4, r5
    ldrb r0, [r0, #0x484]
    bl native_fn_021f9614
    cmp r7, r0
    addeq r0, r4, r5
    ldreqb r6, [r0, #0x484]
    beq ov000_021f95c8_L044
    add r0, r5, #1
    and r5, r0, #0xff
    cmp r5, #0xc
    blo ov000_021f95c8_L018
ov000_021f95c8_L044:
    mov r0, r6
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
