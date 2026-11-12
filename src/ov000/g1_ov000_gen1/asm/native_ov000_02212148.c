/* ov000 row 0x02212148: 56 bytes.
 *
 * What it does: 13 instructions, 1 call(s), 2 load(s), 0 store(s), 2 branch(es).
 *
 * Body: the measured instruction stream transcribed from
 * extract/arm9_overlays/ov000.bin at 0x02212148; every literal pool
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

extern u8 native_data_0224157c[];
extern void native_fn_0221211c(void);


asm u32 native_ov000_02212148 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    ldr r5, =native_data_0224157c
    mov r4, #0
ov000_02212148_L00c:
    ldrsh r0, [r5]
    cmp r0, #0
    ble ov000_02212148_L01c
    bl native_fn_0221211c
ov000_02212148_L01c:
    add r4, r4, #1
    cmp r4, #0x18
    add r5, r5, #0x168
    blt ov000_02212148_L00c
    mov r0, #0
    ldmia sp!, {r3, r4, r5, pc}
}
