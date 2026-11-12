/* ov000 row 0x02221bc0: 244 bytes.
 *
 * What it does: 60 instructions; 13 call(s) to 0x02062a10, 0x02048f5c, 0x02048f6c, +10 more; loops (back edge at +0x10); returns through pop {r4, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xf0 -> constant 0x02246438 (image word 0x02246438)
 *   branch +0x20 -> +0xd8
 *   0 block transfer(s), 11 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02221bc0; the literal pool and
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

extern void native_fn_02062a10(void);
extern void native_fn_02048f5c(void);
extern void native_fn_02048f6c(void);
extern void native_fn_02048f1c(void);
extern void native_fn_02048f2c(void);
extern void native_fn_02048f3c(void);
extern void native_fn_02045680(void);
extern void native_fn_0207e97c(void);
extern void native_fn_020418b0(void);
extern void native_fn_0207e720(void);


asm u32 native_ov000_02221bc0 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    sub sp, sp, #16
    ldr r0, =0x02246438
    ldr r0, [r0, #0xc]
    bl native_fn_02062a10
    movs r4, r0
    ldreq r0, =0x02246438
    moveq r1, #7
    beq ov000_02221bc0_Ld8
    mov r0, #1
    bl native_fn_02048f5c
    ldr r1, =0x02246438
    strb r0, [r1, #0x2]
    mov r0, #1
    bl native_fn_02048f6c
    ldr r1, =0x02246438
    strb r0, [r1, #0x1]
    mov r0, #1
    mov r1, r0
    bl native_fn_02048f1c
    mov r0, #0
    mov r1, #1
    bl native_fn_02048f2c
    mov r0, #2
    mov r1, #1
    bl native_fn_02048f3c
    mov r0, #0
    bl native_fn_02045680
    mov r0, #1
    bl native_fn_02045680
    mov r0, #2
    bl native_fn_02045680
    mov r0, #3
    bl native_fn_02045680
    bl native_fn_0207e97c
    mov r0, #2
    bl native_fn_020418b0
    mov r0, #1
    strb r0, [sp]
    ldrsh r0, [r4, #24]
    mov r2, #0
    mov r1, #16
    strh r0, [sp, #2]
    ldrb r3, [r4, #0x1a]
    add r0, sp, #0
    strb r3, [sp, #0x4]
    ldrb r3, [r4, #0x1b]
    strb r3, [sp, #0x5]
    strb r1, [sp, #0xc]
    str r2, [sp, #0x8]
    strb r2, [sp, #0xd]
    bl native_fn_0207e720
    ldr r0, =0x02246438
    mov r1, #2
ov000_02221bc0_Ld8:
    str r1, [r0, #0x18]
    ldr r1, =0x02246438
    mov r0, #0
    strb r0, [r1, #0x4]
    add sp, sp, #16
    ldmia sp!, {r4, pc}
}
