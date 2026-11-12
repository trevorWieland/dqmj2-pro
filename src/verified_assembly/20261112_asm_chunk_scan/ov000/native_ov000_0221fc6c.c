/* ov000 row 0x0221fc6c: 116 bytes.
 *
 * What it does: Moves 4-register chunks between two pointers with writeback block moves (one load, one store).
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x68 -> constant 0x022463b0 (image word 0x022463b0)
 *   pool +0x6c -> constant 0x022463f6 (image word 0x022463f6)
 *   pool +0x70 -> constant 0x022463e2 (image word 0x022463e2)
 *   back edge +0x4c -> +0x40
 *   1 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0221fc6c; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02008e0c(void);
extern void native_fn_02221118(void);
extern void native_fn_0221cab0(void);


asm u32 native_ov000_0221fc6c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    ldr r1, =0x022463b0
    mov r4, r0
    ldr r0, [r1, #0xc]
    ldr r1, =0x022463f6
    mov r2, #20
    mla r1, r0, r2, r1
    ldr r0, =0x022463e2
    bl native_fn_02008e0c
    ldr r1, =0x022463b0
    mov r0, #132
    ldr r3, [r1, #0x1c]
    ldr r2, [r1, #0xc]
    ldr r5, [r1, #0x24]
    mla r14, r2, r0, r3
    mov r12, #8
ov000_0221fc6c_L40:
    ldmia r5!, {r0, r1, r2, r3}
    stmia lr!, {r0, r1, r2, r3}
    subs r12, r12, #1
    bne ov000_0221fc6c_L40
    ldr r1, [r5]
    mov r0, r4
    str r1, [lr]
    bl native_fn_02221118
    bl native_fn_0221cab0
    ldmia sp!, {r3, r4, r5, pc}
}
