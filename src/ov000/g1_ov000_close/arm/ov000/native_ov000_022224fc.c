/* ov000 row 0x022224fc: 660 bytes.
 *
 * What it does: 163 instructions; 15 call(s) to 0x02008d78, 0x02068de0, 0x02068de0, +12 more; loops (back edge at +0x20); returns through pop {r4, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x28c -> constant 0x02246560 (image word 0x02246560)
 *   pool +0x290 -> constant 0x02246568 (image word 0x02246568)
 *   0 block transfer(s), 46 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022224fc; the literal pool and
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

extern void native_fn_02008d78(void);
extern void native_fn_02068de0(void);
extern void native_fn_02068f70(void);
extern void native_fn_02049ad0(void);
extern void native_fn_02049be4(void);
extern void native_fn_02049f4c(void);
extern void native_fn_0204a04c(void);
extern void native_fn_02085270(void);
extern void native_fn_02217500(void);
extern void native_fn_022179fc(void);
extern void native_fn_02217ac8(void);
extern void native_fn_02045ed0(void);
extern void native_fn_022174f4(void);


asm u32 native_ov000_022224fc (register u32 a0)
{
    stmdb sp!, {r4, lr}
    sub sp, sp, #32
    ldr r3, =0x02246560
    mov r1, #0
    str r1, [r3, #0x4]
    ldr r0, =0x02246568
    mov r2, #10
    strb r1, [r3]
    bl native_fn_02008d78
    mov r0, #0
    mov r2, #1
    str r2, [sp]
    mov r1, #4
    str r1, [sp, #0x4]
    ldr r1, =0x02246560
    str r2, [sp, #0x8]
    ldr r4, [r1, #0x4]
    mov r1, r0
    mov r2, r0
    mov r3, #127
    str r4, [sp, #0xc]
    bl native_fn_02068de0
    ldr r1, =0x02246560
    ldr r4, =0x02246568
    ldr r3, [r1, #0x4]
    mov r2, #0
    add r0, r3, r0
    str r0, [r1, #0x4]
    ldrb lr, [r1]
    mov r0, #1
    mov r3, #9
    add r12, lr, #1
    strb r12, [r1]
    strb r2, [r4, lr]
    str r3, [sp]
    mov r3, #4
    str r3, [sp, #0x4]
    str r0, [sp, #0x8]
    ldr r4, [r1, #0x4]
    mov r1, r0
    mov r3, #127
    str r4, [sp, #0xc]
    bl native_fn_02068de0
    ldr r1, =0x02246560
    ldr r3, =0x02246568
    ldr r2, [r1, #0x4]
    mov r4, #1
    add r0, r2, r0
    str r0, [r1, #0x4]
    ldrb lr, [r1]
    mov r2, #17
    mov r0, #4
    add r12, lr, #1
    strb r12, [r1]
    strb r4, [r3, lr]
    str r2, [sp]
    str r0, [sp, #0x4]
    mov r0, #2
    str r0, [sp, #0x8]
    ldr r2, [r1, #0x4]
    mov r1, r0
    str r2, [sp, #0xc]
    mov r2, #0
    mov r3, #127
    bl native_fn_02068de0
    ldr r1, =0x02246560
    ldr r2, [r1, #0x4]
    add r0, r2, r0
    str r0, [r1, #0x4]
    ldrb r3, [r1]
    add r0, r3, #1
    strb r0, [r1]
    ldr r0, =0x02246568
    mov r2, #2
    strb r2, [r0, r3]
    mov r0, #12
    str r0, [sp]
    mov r0, #21
    str r0, [sp, #0x4]
    ldr r0, [r1, #0x4]
    mov r1, #0
    str r0, [sp, #0x8]
    mov r0, #9
    str r0, [sp, #0xc]
    str r1, [sp, #0x10]
    mov r0, #20
    str r0, [sp, #0x14]
    mov r0, #24
    str r0, [sp, #0x18]
    mov r3, r4
    mov r2, r1
    mov r0, #3
    str r3, [sp, #0x1c]
    bl native_fn_02068f70
    ldr r1, =0x02246560
    ldr r2, =0x02246568
    ldr r4, [r1, #0x4]
    mov r3, #3
    add r0, r4, r0
    str r0, [r1, #0x4]
    ldrb r12, [r1]
    mov r0, #4
    add r4, r12, #1
    strb r4, [r1]
    strb r3, [r2, r12]
    bl native_fn_02049ad0
    mov r2, #0
    str r2, [sp]
    mov r1, #1
    str r1, [sp, #0x4]
    mov r3, #16
    str r3, [sp, #0x8]
    mov r4, #2
    str r4, [sp, #0xc]
    ldr r3, =0x02246560
    mov r4, r0
    ldr r3, [r3, #0x4]
    str r3, [sp, #0x10]
    str r1, [sp, #0x14]
    str r1, [sp, #0x18]
    mov r3, #127
    bl native_fn_02049be4
    ldr r0, [r4]
    ldr r1, =0x02246560
    ldr r12, [r0, #0x4]
    ldr r2, =0x02246568
    ldr r0, [r12, #0x18]
    mov r3, #4
    orr r0, r0, #2
    str r0, [r12, #0x18]
    ldr r12, [r1, #0x4]
    mov r0, r4
    add r12, r12, #32
    str r12, [r1, #0x4]
    ldrb lr, [r1]
    add r12, lr, #1
    strb r12, [r1]
    strb r3, [r2, lr]
    ldr r1, [r4]
    ldr r4, [r1, #0x4]
    bl native_fn_02049f4c
    mov r0, r4
    mov r1, #9
    mov r2, #0
    mov r3, #13
    bl native_fn_0204a04c
    add r0, r4, #60
    mov r1, #16
    mov r2, #0
    bl native_fn_02085270
    ldr r0, =0x02246560
    ldr r0, [r0, #0x4]
    bl native_fn_02217500
    bl native_fn_022179fc
    mov r0, #1
    bl native_fn_02217ac8
    mov r0, #3
    bl native_fn_02045ed0
    bl native_fn_022174f4
    ldr r1, =0x02246560
    str r0, [r1, #0x4]
    add sp, sp, #32
    ldmia sp!, {r4, pc}
}
