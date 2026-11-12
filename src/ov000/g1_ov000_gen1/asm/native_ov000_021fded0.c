/* ov000 row 0x021fded0: 88 bytes.
 *
 * What it does: 22 instructions, 2 call(s), 3 load(s), 4 store(s).
 *
 * Body: the measured instruction stream transcribed from
 * extract/arm9_overlays/ov000.bin at 0x021fded0; every literal pool
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

extern void native_fn_0204b53c(void);
extern void native_fn_02215698(void);


asm u32 native_ov000_021fded0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    mov r4, r1
    bl native_fn_02215698
    mov r1, #0x28
    mov r2, #0x10
    cmp r4, #4
    strh r1, [sp, #2]
    cmpne r4, #5
    moveq r1, #0x40
    streqh r1, [sp, #2]
    strh r2, [sp]
    ldrsh ip, [sp, #2]
    ldr r3, [r5]
    ldr r2, [r5, #4]
    add r1, sp, #0
    sub r2, r3, r2
    add r2, ip, r2, lsl #4
    add r0, r0, #0x10
    strh r2, [sp, #2]
    bl native_fn_0204b53c
    ldmia sp!, {r3, r4, r5, pc}
}
