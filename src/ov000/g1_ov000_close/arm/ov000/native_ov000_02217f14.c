/* ov000 row 0x02217f14: 100 bytes.
 *
 * What it does: 24 instructions; 3 call(s) to 0x02049ad0, 0x02049f4c, 0x0204a574; loops (back edge at +0x2c); returns through pop {r3, r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x60 -> native_data_0222df18 (image word 0x0222df18)
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02217f14; the literal pool and
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

extern u8 native_data_0222df18[];
extern void native_fn_02049ad0(void);
extern void native_fn_02049f4c(void);
extern void native_fn_0204a574(void);


asm u32 native_ov000_02217f14 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    sub sp, sp, #16
    ldr r12, =native_data_0222df18
    mov r4, r3
    ldrh r3, [r12, #10]
    ldrh r12, [r12, #8]
    mov r7, r0
    strh r3, [sp, #14]
    strh r12, [sp, #12]
    mov r6, r1
    mov r5, r2
    bl native_fn_02049ad0
    bl native_fn_02049f4c
    str r4, [sp]
    mov r1, #1
    str r1, [sp, #0x4]
    str r1, [sp, #0x8]
    mov r0, r7
    mov r2, r6
    mov r3, r5
    add r1, sp, #12
    bl native_fn_0204a574
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
