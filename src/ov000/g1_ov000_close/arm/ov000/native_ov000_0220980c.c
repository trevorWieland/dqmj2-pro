/* ov000 row 0x0220980c: 116 bytes.
 *
 * What it does: 26 instructions; 4 call(s) to 0x02215a14, 0x022159b8, 0x0204b85c, +1 more; loops (back edge at +0x50); returns through pop {r3, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x68 -> native_data_0222bacc (image word 0x0222bacc)
 *   pool +0x6c -> native_data_0222f7f8 (image word 0x0222f7f8)
 *   pool +0x70 -> constant 0x02238570 (image word 0x02238570)
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0220980c; the literal pool and
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

extern u8 native_data_0222bacc[];
extern void native_fn_02215a14(void);
extern u8 native_data_0222f7f8[];
extern void native_fn_022159b8(void);
extern void native_fn_0204b85c(void);
extern void native_fn_0205fa4c(void);


asm u32 native_ov000_0220980c (register u32 a0)
{
    stmdb sp!, {r3, lr}
    sub sp, sp, #16
    ldr r0, =native_data_0222bacc
    ldrh r1, [r0, #2]
    ldrh r0, [r0]
    strh r1, [sp, #14]
    strh r0, [sp, #12]
    bl native_fn_02215a14
    ldr r0, =native_data_0222f7f8
    mov r1, #4
    bl native_fn_022159b8
    mov r12, #0
    str r12, [sp]
    mov r0, #51
    str r0, [sp, #0x4]
    ldr r0, =0x02238570
    add r1, sp, #12
    mov r2, #8
    mov r3, #1
    str r12, [sp, #0x8]
    bl native_fn_0204b85c
    ldr r0, =0x02238570
    mov r1, #0
    bl native_fn_0205fa4c
    add sp, sp, #16
    ldmia sp!, {r3, pc}
}
