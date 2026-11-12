/* ov000 row 0x02202568: 200 bytes.
 *
 * What it does: 48 instructions; 8 call(s) to 0x02215698, 0x022159b8, 0x0204b4f4, +5 more; loops (back edge at +0x44); returns through pop {r4, r5, r6, r7, r8, r9, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xc0 -> native_data_0222f530 (image word 0x0222f530)
 *   pool +0xc4 -> constant 0x02237f90 (image word 0x02237f90)
 *   back edge +0xb4 -> +0x78
 *   test +0xb0 cmp r6, #4
 *   0 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02202568; the literal pool and
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

extern void native_fn_02215698(void);
extern u8 native_data_0222f530[];
extern void native_fn_022159b8(void);
extern void native_fn_0204b4f4(void);
extern void native_fn_0204b61c(void);
extern void native_fn_0205f998(void);
extern void native_fn_0221799c(void);
extern void native_fn_0205fa4c(void);


asm u32 native_ov000_02202568 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, lr}
    sub sp, sp, #12
    bl native_fn_02215698
    mov r5, r0
    ldr r0, =native_data_0222f530
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
    mov r2, #216
    str r4, [sp, #0x4]
    bl native_fn_0204b4f4
    add r0, r5, #16
    mov r1, #0
    bl native_fn_0204b61c
    mov r1, #8
    mov r0, #40
    mov r6, #0
    ldr r5, =0x02237f90
    strh r1, [sp, #8]
    strh r0, [sp, #10]
    add r4, sp, #8
    mov r8, r6
    mov r7, #72
ov000_02202568_L78:
    mul r9, r6, r7
    add r0, r5, r9
    bl native_fn_0205f998
    mov r1, r4
    add r0, r5, r9
    bl native_fn_0221799c
    ldrsh r2, [sp, #10]
    mov r1, r8
    add r0, r5, r9
    add r2, r2, #16
    strh r2, [sp, #10]
    bl native_fn_0205fa4c
    add r0, r6, #1
    and r6, r0, #255
    cmp r6, #4
    blo ov000_02202568_L78
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, r8, r9, pc}
}
