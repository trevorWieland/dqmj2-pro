/* ov006 row 0x021ddc38: 348 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x14c -> constant 0x04001000 (image word 0x04001000)
 *   pool +0x150 -> constant 0xffcfffef (image word 0xffcfffef)
 *   pool +0x154 -> constant 0x0220f500 (image word 0x0220f500)
 *   pool +0x158 -> constant 0x04001008 (image word 0x04001008)
 *   back edge +0x5c -> +0x50
 *   test +0x58 cmp r2, #4
 *   0 block transfer(s), 12 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ddc38; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity proves the instruction stream, not the meaning of the fields, blocks and callee contracts it touches.
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
extern void native_fn_02045738(void);
extern void native_fn_02045338(void);
extern void native_fn_02046150(void);


asm u32 native_ov006_021ddc38 (register u32 a0)
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
    ldr r0, =0x0220f500
    mov r2, #0
    mov r1, #32
ov006_021ddc38_L50:
    str r1, [r0, r2, lsl #2]
    add r2, r2, #1
    cmp r2, #4
    blt ov006_021ddc38_L50
    ldr r3, =0x04001008
    mov r0, #0
    ldrh r12, [r3]
    mov r1, #102760448
    mov r2, #131072
    and r12, r12, #67
    orr r12, r12, #284
    strh r12, [r3]
    ldrh r12, [r3, #2]
    and r12, r12, #67
    orr r12, r12, #20
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
    bl native_fn_02045738
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
    mov r1, #0
    mov r2, #2
    bl native_fn_02046150
    mov r0, #2
    mov r1, r0
    mov r2, r0
    bl native_fn_02046150
    ldr r1, =0x04001000
    ldr r0, [r1]
    bic r0, r0, #7936
    orr r0, r0, #7936
    str r0, [r1]
    ldmia sp!, {r3, pc}
}
