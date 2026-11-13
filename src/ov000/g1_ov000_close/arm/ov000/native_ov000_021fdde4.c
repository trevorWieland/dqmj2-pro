/* ov000 row 0x021fdde4: 172 bytes.
 *
 * What it does: 41 instructions; 6 call(s) to 0x02215698, 0x022159b8, 0x0204b4f4, +3 more; loops (back edge at +0x44); returns through pop {r3, r4, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xa4 -> native_data_0222f434 (image word 0x0222f434)
 *   pool +0xa8 -> constant 0x022372a8 (image word 0x022372a8)
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021fdde4; the literal pool and
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

extern void ov000_display_context_02215698(void);
extern u8 native_data_0222f434[];
extern void native_fn_022159b8(void);
extern void native_fn_0204b4f4(void);
extern void native_fn_0204b61c(void);
extern void native_fn_02215094(void);


asm u32 native_ov000_021fdde4 (register u32 a0)
{
    stmdb sp!, {r3, r4, lr}
    sub sp, sp, #12
    bl ov000_display_context_02215698
    mov r4, r0
    ldr r0, =native_data_0222f434
    mov r1, #4
    bl native_fn_022159b8
    mov r0, #0
    strh r0, [sp, #8]
    strh r0, [sp, #10]
    mov r3, #2
    add r1, sp, #8
    str r3, [sp]
    mov r12, #36
    add r0, r4, #16
    mov r2, #216
    str r12, [sp, #0x4]
    bl native_fn_0204b4f4
    add r0, r4, #16
    mov r1, #0
    bl native_fn_0204b61c
    mov r0, #136
    str r0, [sp]
    ldr r0, =0x022372a8
    mov r1, #240
    ldr r0, [r0, #0xc]
    mov r2, #48
    add r0, r0, #180
    mov r3, r1
    bl native_fn_02215094
    mov r0, #152
    str r0, [sp]
    ldr r0, =0x022372a8
    mov r1, #240
    ldr r0, [r0, #0xc]
    mov r2, #64
    add r0, r0, #420
    mov r3, r1
    bl native_fn_02215094
    add sp, sp, #12
    ldmia sp!, {r3, r4, pc}
}
