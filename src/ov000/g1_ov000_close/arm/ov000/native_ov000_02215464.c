/* ov000 row 0x02215464: 320 bytes.
 *
 * What it does: 79 instructions; 15 call(s) to 0x02004120, 0x02008c58, 0x02004174, +12 more; loops (back edge at +0x48); returns through pop {r3, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x13c -> constant 0x04001008 (image word 0x04001008)
 *   branch +0xa0 -> +0xd4
 *   test +0x9c cmp r0, #1
 *   0 block transfer(s), 9 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02215464; the literal pool and
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

extern void native_fn_02004120(void);
extern void native_fn_02008c58(void);
extern void native_fn_02004174(void);
extern void native_fn_020041e4(void);
extern void native_fn_0200427c(void);
extern void native_fn_02078968(void);
extern void native_fn_02045680(void);
extern void native_fn_02008d78(void);


asm u32 native_ov000_02215464 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r1, =0x04001008
    ldrh r0, [r1]
    and r0, r0, #67
    orr r0, r0, #284
    strh r0, [r1]
    ldrh r0, [r1, #2]
    and r0, r0, #67
    orr r0, r0, #20
    strh r0, [r1, #2]
    ldrh r0, [r1, #4]
    and r0, r0, #67
    orr r0, r0, #520
    strh r0, [r1, #4]
    ldrh r0, [r1, #6]
    and r0, r0, #67
    orr r0, r0, #772
    strh r0, [r1, #6]
    bl native_fn_02004120
    mov r1, r0
    mov r0, #0
    mov r2, #16384
    bl native_fn_02008c58
    bl native_fn_02004174
    mov r1, r0
    mov r0, #0
    mov r2, #32768
    bl native_fn_02008c58
    bl native_fn_020041e4
    mov r1, r0
    mov r0, #0
    mov r2, #32768
    bl native_fn_02008c58
    bl native_fn_0200427c
    mov r1, r0
    mov r0, #0
    mov r2, #32768
    bl native_fn_02008c58
    bl native_fn_02078968
    cmp r0, #1
    bne ov000_02215464_Ld4
    mov r0, #2
    bl native_fn_02045680
    bl native_fn_020041e4
    mov r1, #0
    mov r2, #49152
    bl native_fn_02008d78
    mov r0, #3
    bl native_fn_02045680
    bl native_fn_0200427c
    mov r1, #0
    mov r2, #16384
    bl native_fn_02008d78
ov000_02215464_Ld4:
    ldr r1, =0x04001008
    ldrh r0, [r1]
    sub r2, r1, #8
    bic r0, r0, #3
    strh r0, [r1]
    ldrh r0, [r1, #4]
    bic r0, r0, #3
    orr r0, r0, #1
    strh r0, [r1, #4]
    ldrh r0, [r1, #6]
    bic r0, r0, #3
    orr r0, r0, #2
    strh r0, [r1, #6]
    ldrh r0, [r1, #2]
    bic r0, r0, #3
    orr r0, r0, #3
    strh r0, [r1, #2]
    ldr r1, [r2]
    ldr r0, [r2]
    and r1, r1, #7936
    mov r3, r1, lsr #8
    bic r1, r0, #7936
    orr r0, r3, #1
    orr r0, r1, r0, lsl #8
    str r0, [r2]
    ldmia sp!, {r3, pc}
}
