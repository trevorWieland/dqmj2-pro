/* ov000 row 0x021f8db4: 152 bytes.
 *
 * What it does: 36 instructions; 3 call(s) to 0x0204b85c, 0x0203cfe0, 0x021f8e6c; loops (back edge at +0x58); returns through pop {r3, r4, r5, r6, r7, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x90 -> native_data_0222b9c0 (image word 0x0222b9c0)
 *   pool +0x94 -> constant 0x02236f2c (image word 0x02236f2c)
 *   test +0x78 cmp r0, #5
 *   0 block transfer(s), 9 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f8db4; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity fixes the instruction stream, not the field, block and callee semantics behind the addresses and strides it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_0222b9c0[];
extern void native_fn_0204b85c(void);
extern void native_fn_0203cfe0(void);
extern void native_fn_021f8e6c(void);


asm u32 native_ov000_021f8db4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    sub sp, sp, #16
    ldr r3, =native_data_0222b9c0
    mov r7, r0
    ldrh r12, [r3, #2]
    ldrh r3, [r3]
    ldr r4, =0x02236f2c
    mov r0, #72
    mla r4, r7, r0, r4
    strh r3, [sp, #12]
    mov r5, r2
    mov r6, r1
    strh r12, [sp, #14]
    mov r3, #1
    str r3, [sp]
    mov r0, #38
    str r0, [sp, #0x4]
    mov r2, #7
    str r2, [sp, #0x8]
    add r1, sp, #12
    mov r0, r4
    mov r2, #4
    bl native_fn_0204b85c
    bl native_fn_0203cfe0
    str r0, [r4, #0x2c]
    str r6, [r4, #0x34]
    mov r0, r7
    strb r5, [r4, #0x23]
    bl native_fn_021f8e6c
    ldr r0, [r4, #0x2c]
    cmp r0, #5
    addeq r0, r0, #38
    movne r0, #38
    str r0, [r4, #0x30]
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
