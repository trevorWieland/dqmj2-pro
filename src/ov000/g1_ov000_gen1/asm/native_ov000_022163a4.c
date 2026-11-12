/* ov000 row 0x022163a4: 88 bytes.
 *
 * What it does: 22 instructions, 5 call(s), 2 load(s), 0 store(s), 2 branch(es).
 *
 * Body: the measured instruction stream transcribed from
 * extract/arm9_overlays/ov000.bin at 0x022163a4; every literal pool
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

extern void native_fn_02049ad0(void);
extern void native_fn_022162c0(void);
extern void native_fn_022172dc(void);


asm u32 native_ov000_022163a4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r4, r0
    ldrh r0, [r4, #0xc]
    mov r5, #0
    cmp r0, #0
    ble ov000_022163a4_L044
ov000_022163a4_L018:
    add r0, r5, #5
    mov r0, r0, lsl #0x18
    mov r0, r0, asr #0x18
    bl native_fn_02049ad0
    bl native_fn_022162c0
    add r0, r5, #1
    mov r0, r0, lsl #0x18
    ldrh r1, [r4, #0xc]
    mov r5, r0, asr #0x18
    cmp r1, r0, asr #24
    bgt ov000_022163a4_L018
ov000_022163a4_L044:
    mov r0, #4
    bl native_fn_02049ad0
    bl native_fn_022162c0
    bl native_fn_022172dc
    ldmia sp!, {r3, r4, r5, pc}
}
