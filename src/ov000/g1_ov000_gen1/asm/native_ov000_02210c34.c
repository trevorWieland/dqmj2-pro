/* ov000 row 0x02210c34: 88 bytes.
 *
 * What it does: 21 instructions, 1 call(s), 2 load(s), 0 store(s), 3 branch(es).
 *
 * Body: the measured instruction stream transcribed from
 * extract/arm9_overlays/ov000.bin at 0x02210c34; every literal pool
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

extern void native_fn_020430b4(void);


asm u32 native_ov000_02210c34 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    ldr r0, =0x000001aa
    sub r1, r5, #0x32
    cmp r1, r0
    mvn r4, #0
    bhi ov000_02210c34_L04c
    mov r0, #0x34
    bl native_fn_020430b4
    mov r2, #0
ov000_02210c34_L028:
    ldrsh r1, [r0, #2]
    cmp r1, r5
    moveq r0, r2, lsl #0x10
    moveq r4, r0, asr #0x10
    beq ov000_02210c34_L04c
    add r2, r2, #1
    cmp r2, #0x200
    add r0, r0, #0xe
    blt ov000_02210c34_L028
ov000_02210c34_L04c:
    mov r0, r4
    ldmia sp!, {r3, r4, r5, pc}
}
