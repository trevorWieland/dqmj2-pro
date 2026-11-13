/* ov000 row 0x021fe600: 200 bytes.
 *
 * What it does: 48 instructions; 8 call(s) to 0x02215698, 0x022159b8, 0x0204b4f4, +5 more; loops (back edge at +0x44); returns through pop {r4, r5, r6, r7, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xc0 -> native_data_0222f460 (image word 0x0222f460)
 *   pool +0xc4 -> constant 0x022373b4 (image word 0x022373b4)
 *   back edge +0xb4 -> +0x74
 *   test +0xac cmp r7, #6
 *   0 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021fe600; the literal pool and
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
extern u8 native_data_0222f460[];
extern void native_fn_022159b8(void);
extern void native_fn_0204b4f4(void);
extern void native_fn_0204b61c(void);
extern void native_fn_0205f998(void);
extern void native_fn_0221799c(void);
extern void native_fn_0205fa4c(void);


asm u32 native_ov000_021fe600 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, lr}
    sub sp, sp, #12
    bl ov000_display_context_02215698
    mov r5, r0
    ldr r0, =native_data_0222f460
    mov r1, #4
    bl native_fn_022159b8
    mov r0, #0
    strh r0, [sp, #8]
    strh r0, [sp, #10]
    mov r3, #2
    add r1, sp, #8
    str r3, [sp]
    mov r4, #36
    add r0, r5, #16
    mov r2, #224
    str r4, [sp, #0x4]
    bl native_fn_0204b4f4
    add r0, r5, #16
    mov r1, #0
    bl native_fn_0204b61c
    mov r1, #8
    mov r0, #40
    mov r7, #0
    ldr r4, =0x022373b4
    strh r1, [sp, #8]
    strh r0, [sp, #10]
    add r6, sp, #8
    mov r5, r7
ov000_021fe600_L74:
    mov r0, r4
    bl native_fn_0205f998
    mov r0, r4
    mov r1, r6
    bl native_fn_0221799c
    ldrsh r2, [sp, #10]
    mov r0, r4
    mov r1, r5
    add r2, r2, #16
    strh r2, [sp, #10]
    bl native_fn_0205fa4c
    add r0, r7, #1
    mov r0, r0, lsl #24
    mov r7, r0, asr #24
    cmp r7, #6
    add r4, r4, #72
    blt ov000_021fe600_L74
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, pc}
}
