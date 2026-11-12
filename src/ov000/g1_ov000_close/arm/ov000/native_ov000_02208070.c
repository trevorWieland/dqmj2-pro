/* ov000 row 0x02208070: 228 bytes.
 *
 * What it does: 56 instructions; 8 call(s) to 0x0207e318, 0x02208938, 0x02206d58, +5 more; loops (back edge at +0x24); returns through pop {r3, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xe0 -> constant 0x022383e8 (image word 0x022383e8)
 *   branch +0x14 -> +0x20
 *   branch +0x1c -> +0x9c
 *   branch +0x34 -> +0x8c
 *   test +0x10 cmp r0, #0
 *   test +0x18 cmp r0, #1
 *   test +0x28 cmp r0, #0
 *   0 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02208070; the literal pool and
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

extern void native_fn_0207e318(void);
extern void native_fn_02208938(void);
extern void native_fn_02206d58(void);
extern void native_fn_020414c8(void);
extern void native_fn_0220895c(void);
extern void native_fn_0205e7a8(void);
extern void native_fn_02041538(void);
extern void native_fn_02207bc0(void);


asm u32 native_ov000_02208070 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    sub sp, sp, #8
    ldr r0, =0x022383e8
    ldr r0, [r0]
    cmp r0, #0
    beq ov000_02208070_L20
    cmp r0, #1
    b ov000_02208070_L9c
ov000_02208070_L20:
    mov r0, #2
    bl native_fn_0207e318
    cmp r0, #0
    ldreq r0, =0x022383e8
    moveq r1, #4
    beq ov000_02208070_L8c
    mov r0, #0
    bl native_fn_02208938
    mov r0, #0
    str r0, [sp]
    mov r12, #82
    mov r0, #5
    mov r1, #6
    mov r2, #30
    mov r3, #1
    str r12, [sp, #0x4]
    bl native_fn_02206d58
    mov r0, #46
    bl native_fn_020414c8
    mov r0, #1
    bl native_fn_0220895c
    ldr r0, =0x022383e8
    mov r1, #0
    strb r1, [r0, #0x118]
    mov r1, #4
    strb r1, [r0, #0xf1]
    mov r1, #3
ov000_02208070_L8c:
    strb r1, [r0, #0xf0]
    add sp, sp, #8
    mov r0, #1
    ldmia sp!, {r3, pc}
ov000_02208070_L9c:
    mvn r0, #0
    mov r1, #83
    bl native_fn_0205e7a8
    mov r0, #1
    mov r1, #2
    mov r2, #10
    bl native_fn_02041538
    ldr r0, =0x022383e8
    mov r1, #1
    strb r1, [r0, #0xf1]
    bl native_fn_02207bc0
    ldr r0, =0x022383e8
    mov r1, #11
    strb r1, [r0, #0xf0]
    mov r0, #1
    add sp, sp, #8
    ldmia sp!, {r3, pc}
}
