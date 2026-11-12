/* ov006 row 0x021ffdf4: 52 bytes.
 *
 * What it does: Writes one block of 2 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x28 -> native_data_0220e248 (image word 0x0220e248)
 *   pool +0x2c -> constant 0x0221c150 (image word 0x0221c150)
 *   pool +0x30 -> native_fn_021ffe28+1 (image word 0x021ffe29)
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ffdf4; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 10 of 52 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_0220e248[];
extern void native_fn_021f2798(void);
extern void native_fn_02202a80(void);
extern void native_fn_021ffe28(void);
extern void native_fn_0220490c(void);


asm u32 native_ov006_021ffdf4 (register u32 a0)
{
    push {r3, lr}
    lsl r1, r0, #0x2
    ldr r0, =native_data_0220e248
    ldr r0, [r0, r1]
    bl native_fn_021f2798
    mov r1, #0x0
    mov r2, #0x4
    bl native_fn_02202a80
    ldr r1, =0x0221c150
    mov r2, #0x0
    str r0, [r1, #0]
    ldr r1, =native_fn_021ffe28+1
    mov r0, #0x1
    mov r3, #0x78
    bl native_fn_0220490c
    pop {r3, pc}
    mov r8, r8
}
