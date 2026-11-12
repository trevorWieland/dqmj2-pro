/* ov000 row 0x021eb720: 88 bytes.
 *
 * What it does: 21 instructions, 2 call(s), 2 load(s), 1 store(s), 4 branch(es).
 *
 * Body: the measured instruction stream transcribed from
 * extract/arm9_overlays/ov000.bin at 0x021eb720; every literal pool
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

extern u8 native_data_02236980[];
extern void native_fn_0205e7a8(void);


asm u32 native_ov000_021eb720 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    ldr r2, =native_data_02236980
    ldrsb r4, [r2, #0x20]
    cmp r4, #0
    beq ov000_021eb720_L024
    cmp r4, #1
    cmpne r4, #2
    beq ov000_021eb720_L03c
    b ov000_021eb720_L04c
ov000_021eb720_L024:
    mov r3, #6
    sub r0, r3, #7
    mov r1, #0x53
    strb r3, [r2, #0x100]
    bl native_fn_0205e7a8
    b ov000_021eb720_L04c
ov000_021eb720_L03c:
    mvn r0, #0
    mov r1, #0x53
    bl native_fn_0205e7a8
    mov r4, #0
ov000_021eb720_L04c:
    mov r0, r4
    ldmia sp!, {r4, pc}
}
