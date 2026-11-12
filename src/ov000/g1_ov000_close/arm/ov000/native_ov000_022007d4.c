/* ov000 row 0x022007d4: 260 bytes.
 *
 * What it does: 64 instructions; 11 call(s) to 0x02062aa0, 0x02215d94, 0x02210f84, +8 more; loops (back edge at +0x10); returns through pop {r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x100 -> constant 0x02237778 (image word 0x02237778)
 *   branch +0x4c -> +0x5c
 *   branch +0x58 -> +0x64
 *   test +0x48 cmp r4, r6
 *   1 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022007d4; the literal pool and
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
extern void native_fn_02215d94(void);
extern void native_fn_02210f84(void);
extern void native_fn_0221742c(void);
extern void native_fn_02049ad0(void);
extern void native_fn_02049ffc(void);
extern void native_fn_02049f4c(void);
extern void native_fn_020602ec(void);
extern void native_fn_0204a288(void);
extern void native_fn_02065818(void);


asm u32 native_ov000_022007d4 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, lr}
    sub sp, sp, #20
    mov r7, r0
    mov r4, r1
    bl native_fn_02062aa0
    ldr r1, =0x02237778
    add r3, sp, #16
    mov r2, #0
    ldr r1, [r1, #0x8]
    mov r6, r0
    and r0, r1, #255
    strh r2, [r3]
    strh r2, [r3, #2]
    bl native_fn_02215d94
    mov r1, r0
    mov r0, r7
    bl native_fn_02210f84
    mov r5, r0
    cmp r4, r6
    bge ov000_022007d4_L5c
    mov r0, #7
    bl native_fn_0221742c
    b ov000_022007d4_L64
ov000_022007d4_L5c:
    mov r0, #8
    bl native_fn_0221742c
ov000_022007d4_L64:
    mov r6, r0
    mov r0, #1
    bl native_fn_02049ad0
    mov r4, r0
    ldr r0, [r4]
    ldr r0, [r0, #0x4]
    bl native_fn_02049ffc
    mov r0, r4
    bl native_fn_02049f4c
    mov r0, #24
    strh r0, [sp, #16]
    mov r0, #0
    str r0, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    ldrsh r1, [r7, #24]
    ldrsh r3, [sp, #16]
    ldr r0, [r4]
    mov r2, r7
    bl native_fn_020602ec
    mov r0, #144
    strh r0, [sp, #16]
    ldrsh r2, [r7, #38]
    mov r1, #4
    mov r0, #0
    stmia sp, {r2, r5}
    str r1, [sp, #0x8]
    str r0, [sp, #0xc]
    mov r0, #1
    add r1, sp, #16
    mov r2, r0
    mov r3, r0
    bl native_fn_0204a288
    mov r1, #3
    mov r0, r6
    mov r2, r1
    bl native_fn_02065818
    add sp, sp, #20
    ldmia sp!, {r4, r5, r6, r7, pc}
}
