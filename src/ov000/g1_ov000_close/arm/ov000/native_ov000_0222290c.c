/* ov000 row 0x0222290c: 260 bytes.
 *
 * What it does: 63 instructions; 6 call(s) to 0x0203cb2c, 0x02002e5c, 0x020030ec, +3 more; loops (back edge at +0x04); returns through pop {r3, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xfc -> constant 0x04000008 (image word 0x04000008)
 *   pool +0x100 -> constant 0x0400000a (image word 0x0400000a)
 *   0 block transfer(s), 11 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0222290c; the literal pool and
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

extern void native_fn_0203cb2c(void);
extern void native_fn_02002e5c(void);
extern void native_fn_020030ec(void);
extern void native_fn_02002c98(void);
extern void native_fn_02008c58(void);
extern void native_fn_020414b0(void);


asm u32 native_ov000_0222290c (register u32 a0)
{
    stmdb sp!, {r3, lr}
    bl native_fn_0203cb2c
    mov r0, #9
    bl native_fn_02002e5c
    mov r0, #2
    bl native_fn_020030ec
    mov r0, #1
    mov r1, #3
    mov r2, #0
    bl native_fn_02002c98
    ldr r3, =0x04000008
    mov r0, #0
    ldrh r12, [r3]
    mov r1, #100663296
    mov r2, #524288
    and r12, r12, #67
    orr r12, r12, #792
    strh r12, [r3]
    ldrh r12, [r3, #2]
    and r12, r12, #67
    orr r12, r12, #264
    strh r12, [r3, #2]
    ldrh r12, [r3, #4]
    and r12, r12, #67
    orr r12, r12, #528
    strh r12, [r3, #4]
    ldrh r12, [r3, #6]
    and r12, r12, #67
    orr r12, r12, #132
    orr r12, r12, #18432
    strh r12, [r3, #6]
    bl native_fn_02008c58
    mov r2, #67108864
    ldr r1, [r2]
    mov r0, #40
    bic r1, r1, #7936
    orr r1, r1, #3840
    str r1, [r2]
    bl native_fn_020414b0
    ldr r12, =0x0400000a
    mov r0, #0
    ldrh r2, [r12]
    sub r3, r12, #2
    mov r1, #67108864
    bic r2, r2, #3
    strh r2, [r12]
    ldrh r2, [r12, #4]
    bic r2, r2, #3
    orr r2, r2, #3
    strh r2, [r12, #4]
    ldrh r2, [r12, #2]
    bic r2, r2, #3
    orr r2, r2, #2
    strh r2, [r12, #2]
    ldrh r2, [r3]
    bic r2, r2, #3
    orr r2, r2, #1
    strh r2, [r3]
    str r0, [r12, #0x12]
    ldr r0, [r1]
    bic r0, r0, #57344
    str r0, [r1]
    ldmia sp!, {r3, pc}
}
