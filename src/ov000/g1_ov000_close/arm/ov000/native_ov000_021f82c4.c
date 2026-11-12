/* ov000 row 0x021f82c4: 212 bytes.
 *
 * What it does: 50 instructions; 9 call(s) to 0x02215698, 0x021f8418, 0x0201d444, +6 more; loops (back edge at +0x30); returns through pop {r3, r4, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xc8 -> native_data_0222f39c (image word 0x0222f39c)
 *   pool +0xcc -> constant 0x02236f14 (image word 0x02236f14)
 *   pool +0xd0 -> native_data_0222f3b0 (image word 0x0222f3b0)
 *   back edge +0x30 -> +0x18
 *   branch +0x54 -> +0x6c
 *   test +0x50 cmp r0, #0
 *   0 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f82c4; the literal pool and
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
extern void native_fn_021f8418(void);
extern u8 native_data_0222f39c[];
extern void native_fn_0201d444(void);
extern void native_fn_0202a8e0(void);
extern void native_fn_0203cc2c(void);
extern u8 native_data_0222f3b0[];
extern void native_fn_020451c4(void);
extern void native_fn_0202a37c(void);
extern void native_fn_02008e0c(void);
extern void native_fn_0204532c(void);


asm u32 native_ov000_021f82c4 (register u32 a0)
{
    stmdb sp!, {r3, r4, lr}
    sub sp, sp, #36
    bl native_fn_02215698
    add r2, sp, #4
    mov r1, #8
    mov r0, #0
ov000_021f82c4_L18:
    strb r0, [r2]
    strb r0, [r2, #0x1]
    strb r0, [r2, #0x2]
    strb r0, [r2, #0x3]
    add r2, r2, #4
    subs r1, r1, #1
    bne ov000_021f82c4_L18
    bl native_fn_021f8418
    ldr r1, =native_data_0222f39c
    add r0, sp, #4
    bl native_fn_0201d444
    add r0, sp, #4
    bl native_fn_0202a8e0
    str r0, [sp]
    cmp r0, #0
    beq ov000_021f82c4_L6c
    add r0, sp, #4
    mov r1, #2
    bl native_fn_0203cc2c
    ldr r1, =0x02236f14
    str r0, [r1, #0xc]
ov000_021f82c4_L6c:
    mov r1, #0
    str r1, [sp]
    ldr r0, =native_data_0222f3b0
    add r3, sp, #0
    mov r1, #17
    mov r2, #1
    bl native_fn_020451c4
    mov r4, r0
    ldr r1, [sp]
    mov r0, #2
    mov r2, #4
    bl native_fn_0202a37c
    mov r1, r0
    ldr r2, =0x02236f14
    mov r0, r4
    str r1, [r2, #0x10]
    ldr r2, [sp]
    bl native_fn_02008e0c
    mov r1, r4
    mov r0, #1
    bl native_fn_0204532c
    add sp, sp, #36
    ldmia sp!, {r3, r4, pc}
}
