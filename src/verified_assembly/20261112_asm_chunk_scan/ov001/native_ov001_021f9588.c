/* ov001 row 0x021f9588: 128 bytes.
 *
 * What it does: Moves 4-register chunks between two pointers with writeback block moves (one load, one store).
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x70 -> constant 0x02239b40 (image word 0x02239b40)
 *   pool +0x74 -> native_fn_021f9528 (image word 0x021f9528)
 *   pool +0x78 -> native_fn_021f9558 (image word 0x021f9558)
 *   pool +0x7c -> constant 0x02239a14 (image word 0x02239a14)
 *   back edge +0x50 -> +0x44
 *   5 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f9588; the literal pool and
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

extern void native_fn_021f9528(void);
extern void native_fn_021f9558(void);
extern void native_fn_0205fc10(void);
extern void native_fn_0205fd0c(void);


asm u32 native_ov001_021f9588 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    sub sp, sp, #16
    mov r0, #18
    str r0, [sp]
    mov r0, #8192
    str r0, [sp, #0x4]
    mov r3, #2
    str r3, [sp, #0x8]
    mov r3, #0
    ldr r0, =0x02239b40
    ldr r1, =native_fn_021f9528
    ldr r2, =native_fn_021f9558
    str r3, [sp, #0xc]
    bl native_fn_0205fc10
    ldr lr, =0x02239b40
    mov r4, r0
    mov r12, #13
ov001_021f9588_L44:
    ldmia r4!, {r0, r1, r2, r3}
    stmia lr!, {r0, r1, r2, r3}
    subs r12, r12, #1
    bne ov001_021f9588_L44
    ldr r0, =0x02239b40
    bl native_fn_0205fd0c
    ldr r0, =0x02239a14
    mov r1, #0
    strb r1, [r0, #0xa]
    add sp, sp, #16
    ldmia sp!, {r4, pc}
}
