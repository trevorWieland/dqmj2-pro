/* ov000 row 0x021f8b40: 120 bytes.
 *
 * What it does: 28 instructions; 3 call(s) to 0x0204b85c, 0x0203d350, 0x021f8bb8; loops (back edge at +0x44); returns through pop {r3, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x70 -> native_data_0222b9c0 (image word 0x0222b9c0)
 *   pool +0x74 -> constant 0x02236f2c (image word 0x02236f2c)
 *   0 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f8b40; the literal pool and
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
extern void native_fn_0203d350(void);
extern void native_fn_021f8bb8(void);


asm u32 native_ov000_021f8b40 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    sub sp, sp, #16
    ldr r0, =native_data_0222b9c0
    mov r2, #2
    ldrh r3, [r0, #6]
    ldrh r0, [r0, #4]
    add r1, sp, #12
    strh r3, [sp, #14]
    strh r0, [sp, #12]
    str r2, [sp]
    mov r2, #19
    str r2, [sp, #0x4]
    mov r12, #4
    ldr r0, =0x02236f2c
    mov r2, #5
    mov r3, #1
    str r12, [sp, #0x8]
    bl native_fn_0204b85c
    bl native_fn_0203d350
    ldr r1, =0x02236f2c
    mov r2, #0
    str r0, [r1, #0x2c]
    strh r2, [r1, #38]
    mov r0, #1
    strb r0, [r1, #0x24]
    bl native_fn_021f8bb8
    add sp, sp, #16
    ldmia sp!, {r3, pc}
}
