/* ov000 row 0x02206de0: 316 bytes.
 *
 * What it does: 76 instructions; 18 call(s) to 0x0202abd8, 0x0203d30c, 0x0203d320, +15 more; loops (back edge at +0x14); returns through pop {r3, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x130 -> constant 0x00007fff (image word 0x00007fff)
 *   pool +0x134 -> constant 0x0400000a (image word 0x0400000a)
 *   pool +0x138 -> constant 0x022382c4 (image word 0x022382c4)
 *   0 block transfer(s), 10 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02206de0; the literal pool and
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

extern void native_fn_0202abd8(void);
extern void native_fn_0203d30c(void);
extern void native_fn_0203d320(void);
extern void native_fn_0203d334(void);
extern void native_fn_0203cb2c(void);
extern void native_fn_020033e8(void);
extern void native_fn_020035c0(void);
extern void native_fn_02002e5c(void);
extern void native_fn_020481b8(void);
extern void native_fn_02048308(void);
extern void native_fn_02002c98(void);
extern void native_fn_02008c58(void);
extern void native_fn_02041560(void);
extern void native_fn_020414b0(void);
extern void native_fn_02002c50(void);
extern void native_fn_0205fd80(void);
extern void native_fn_02041898(void);


asm u32 native_ov000_02206de0 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r2, =0x00007fff
    mov r0, #3
    mov r1, #65536
    strh r2, [sp]
    bl native_fn_0202abd8
    bl native_fn_0203d30c
    bl native_fn_0203d320
    bl native_fn_0203d334
    bl native_fn_0203cb2c
    mov r0, #11
    bl native_fn_020033e8
    mov r0, #16
    bl native_fn_020035c0
    mov r0, #96
    bl native_fn_02002e5c
    add r0, sp, #0
    mov r1, #0
    mov r2, #2
    bl native_fn_020481b8
    bl native_fn_02048308
    mov r0, #1
    mov r1, #0
    mov r2, r0
    bl native_fn_02002c98
    ldr r12, =0x0400000a
    mov r0, #0
    ldrh r3, [r12]
    mov r1, #100663296
    mov r2, #524288
    and r3, r3, #67
    orr r3, r3, #3328
    strh r3, [r12]
    ldrh r3, [r12, #2]
    and r3, r3, #67
    orr r3, r3, #3584
    strh r3, [r12, #2]
    ldrh r3, [r12, #4]
    and r3, r3, #67
    orr r3, r3, #3840
    strh r3, [r12, #4]
    bl native_fn_02008c58
    mov r1, #67108864
    ldr r2, [r1]
    mov r0, #0
    bic r2, r2, #7936
    orr r2, r2, #3840
    str r2, [r1]
    ldrh r2, [r1, #14]
    bic r2, r2, #3
    strh r2, [r1, #14]
    ldrh r2, [r1, #10]
    bic r2, r2, #3
    orr r2, r2, #1
    strh r2, [r1, #10]
    ldrh r2, [r1, #12]
    bic r2, r2, #3
    orr r2, r2, #2
    strh r2, [r1, #12]
    ldrh r2, [r1, #8]
    bic r2, r2, #3
    orr r2, r2, #3
    strh r2, [r1, #8]
    bl native_fn_02041560
    mov r0, #63
    bl native_fn_020414b0
    bl native_fn_02002c50
    mov r0, #0
    bl native_fn_0205fd80
    mov r0, #3
    bl native_fn_02041898
    bl native_fn_02002c50
    ldr r0, =0x022382c4
    mov r1, #0
    strb r1, [r0, #0x2]
    ldmia sp!, {r3, pc}
}
