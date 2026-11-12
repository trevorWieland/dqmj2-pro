/* ov000 row 0x02223748: 328 bytes.
 *
 * What it does: 79 instructions; 14 call(s) to 0x02002d00, 0x020038a8, 0x02003950, +11 more; loops (back edge at +0x08); returns through pop {r3, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x13c -> constant 0x04001000 (image word 0x04001000)
 *   pool +0x140 -> constant 0xffcfffef (image word 0xffcfffef)
 *   pool +0x144 -> constant 0x04001008 (image word 0x04001008)
 *   0 block transfer(s), 10 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02223748; the literal pool and
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

extern void native_fn_02002d00(void);
extern void native_fn_020038a8(void);
extern void native_fn_02003950(void);
extern void native_fn_020039c0(void);
extern void native_fn_02003a40(void);
extern void native_fn_02008c58(void);
extern void native_fn_02045680(void);
extern void native_fn_02045338(void);
extern void native_fn_020489f0(void);
extern void native_fn_02046150(void);


asm u32 native_ov000_02223748 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    mov r0, #0
    bl native_fn_02002d00
    ldr r3, =0x04001000
    ldr r1, =0xffcfffef
    ldr r2, [r3]
    mov r0, #4
    and r1, r2, r1
    orr r1, r1, #16
    str r1, [r3]
    bl native_fn_020038a8
    mov r0, #256
    bl native_fn_02003950
    mov r0, #0
    bl native_fn_020039c0
    mov r0, #0
    bl native_fn_02003a40
    ldr r3, =0x04001008
    mov r0, #0
    ldrh r12, [r3]
    mov r1, #102760448
    mov r2, #131072
    and r12, r12, #67
    orr r12, r12, #280
    strh r12, [r3]
    ldrh r12, [r3, #2]
    and r12, r12, #67
    orr r12, r12, #16
    strh r12, [r3, #2]
    ldrh r12, [r3, #4]
    and r12, r12, #67
    orr r12, r12, #520
    strh r12, [r3, #4]
    ldrh r12, [r3, #6]
    and r12, r12, #67
    orr r12, r12, #772
    strh r12, [r3, #6]
    bl native_fn_02008c58
    mov r0, #1
    bl native_fn_02045680
    mov r0, #2
    bl native_fn_02045680
    mov r0, #4
    bl native_fn_02045680
    mov r0, #8
    bl native_fn_02045680
    ldr r2, =0x04001008
    ldrh r0, [r2]
    sub r1, r2, #8
    bic r0, r0, #3
    strh r0, [r2]
    ldrh r0, [r2, #4]
    bic r0, r0, #3
    orr r0, r0, #1
    strh r0, [r2, #4]
    ldrh r0, [r2, #6]
    bic r0, r0, #3
    orr r0, r0, #2
    strh r0, [r2, #6]
    ldrh r0, [r2, #2]
    bic r0, r0, #3
    orr r0, r0, #3
    strh r0, [r2, #2]
    ldr r0, [r1]
    bic r0, r0, #7936
    orr r0, r0, #7936
    str r0, [r1]
    bl native_fn_02045338
    mov r0, #1
    bl native_fn_020489f0
    mov r0, #1
    mov r1, #0
    mov r2, #2
    bl native_fn_02046150
    mov r0, #2
    mov r1, r0
    mov r2, r0
    bl native_fn_02046150
    ldmia sp!, {r3, pc}
}
