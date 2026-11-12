/* ov000 row 0x021fef08: 212 bytes.
 *
 * What it does: 53 instructions; 9 call(s) to 0x02062aa0, 0x0221742c, 0x0221742c, +6 more; loops (back edge at +0x10); returns through pop {r3, r4, r5, r6, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x28 -> +0x38
 *   branch +0x34 -> +0x40
 *   test +0x24 cmp r4, r0
 *   0 block transfer(s), 10 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021fef08; the literal pool and
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

extern void native_fn_02062aa0(void);
extern void native_fn_0221742c(void);
extern void native_fn_02049ad0(void);
extern void native_fn_02049ffc(void);
extern void native_fn_02049f4c(void);
extern void native_fn_020602ec(void);
extern void native_fn_0204a724(void);
extern void native_fn_02065818(void);


asm u32 native_ov000_021fef08 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, lr}
    sub sp, sp, #20
    mov r5, r0
    mov r4, r1
    bl native_fn_02062aa0
    add r2, sp, #16
    mov r1, #0
    strh r1, [r2]
    strh r1, [r2, #2]
    cmp r4, r0
    bge ov000_021fef08_L38
    mov r0, #7
    bl native_fn_0221742c
    b ov000_021fef08_L40
ov000_021fef08_L38:
    mov r0, #8
    bl native_fn_0221742c
ov000_021fef08_L40:
    mov r4, r0
    mov r0, #1
    bl native_fn_02049ad0
    mov r6, r0
    ldr r0, [r6]
    ldr r0, [r0, #0x4]
    bl native_fn_02049ffc
    mov r0, r6
    bl native_fn_02049f4c
    mov r0, #24
    strh r0, [sp, #16]
    mov r0, #0
    str r0, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    ldrsh r1, [r5, #24]
    ldrsh r3, [sp, #16]
    ldr r0, [r6]
    mov r2, r5
    bl native_fn_020602ec
    mov r3, #0
    strh r3, [sp, #16]
    mov r0, #1
    str r0, [sp]
    ldrb r5, [r5, #0x32]
    add r1, sp, #16
    mov r2, #24
    str r5, [sp, #0x4]
    str r0, [sp, #0x8]
    str r3, [sp, #0xc]
    bl native_fn_0204a724
    mov r1, #3
    mov r0, r4
    mov r2, r1
    bl native_fn_02065818
    add sp, sp, #20
    ldmia sp!, {r3, r4, r5, r6, pc}
}
