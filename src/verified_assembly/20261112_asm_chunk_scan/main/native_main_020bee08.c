/* main row 0x020bee08: 320 bytes.
 *
 * What it does: Copies a 5-register block to an optional destination under a condition in one predicated move.
 *
 * Decoded shape: predicated block copy.
 *
 *   pool +0x130 -> constant 0xfff003ff (image word 0xfff003ff)
 *   pool +0x134 -> constant 0xc00fffff (image word 0xc00fffff)
 *   pool +0x138 -> constant 0x00002710 (image word 0x00002710)
 *   pool +0x13c -> constant 0x88888889 (image word 0x88888889)
 *   test +0x108 cmp r0, #1000
 *   11 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020bee08; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02063f6c(void);
extern void native_fn_0206442c(void);
extern void native_fn_02063f48(void);
extern void native_fn_02064454(void);
extern void native_fn_02063aa4(void);
extern void native_fn_02008e0c(void);
extern void native_fn_0206434c(void);
extern void native_fn_020643b0(void);
extern void native_fn_02026144(void);
extern void native_fn_020633bc(void);


asm u32 native_main_020bee08 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    bl native_fn_02063f6c
    mov r4, r0
    bl native_fn_0206442c
    ldrh r0, [r0]
    strh r0, [r5, #22]
    bl native_fn_02063f48
    add r1, r0, #6400
    mov r2, #1024
    ldrh r3, [r1, #64]
    rsb r2, r2, #0
    ldr r0, [r5, #0x2c]
    and r3, r3, r2, lsr #22
    and r12, r0, r2
    orr r3, r12, r3
    str r3, [r5, #0x2c]
    ldrh r1, [r1, #66]
    ldr r0, =0xfff003ff
    and r3, r3, r0
    mov r1, r1, lsl #22
    orr r1, r3, r1, lsr #12
    str r1, [r5, #0x2c]
    ldr r1, [r4, #0x44]
    add r0, r0, #1048576
    ldr r3, [r5, #0x30]
    and r0, r1, r0
    and r1, r3, r2
    orr r0, r1, r0
    str r0, [r5, #0x30]
    bl native_fn_02064454
    ldr r2, [r5, #0x2c]
    ldr r1, =0xc00fffff
    mov r0, r0, lsl #22
    and r1, r2, r1
    orr r0, r1, r0, lsr #2
    str r0, [r5, #0x2c]
    bl native_fn_02063f48
    add r0, r0, #8192
    ldr r0, [r0, #0x294]
    str r0, [r5, #0x28]
    bl native_fn_02063f48
    add r0, r0, #8192
    ldr r0, [r0, #0x298]
    str r0, [r5, #0x1c]
    bl native_fn_02063f48
    add r0, r0, #8192
    ldr r0, [r0, #0x29c]
    str r0, [r5, #0x20]
    bl native_fn_02063f48
    add r0, r0, #8192
    ldr r0, [r0, #0x2a0]
    str r0, [r5, #0x24]
    bl native_fn_02063aa4
    mov r1, r5
    mov r2, #20
    bl native_fn_02008e0c
    bl native_fn_0206434c
    mov r4, r0
    bl native_fn_020643b0
    mov r1, r0
    mov r0, #1000
    mul r0, r4, r0
    bl native_fn_02026144
    mov r0, r0, lsl #16
    mov r0, r0, lsr #16
    cmp r0, #1000
    ldrhi r0, =0x00002710
    strh r0, [r5, #20]
    bl native_fn_020633bc
    ldr r1, [r0]
    ldr r0, =0x88888889
    umull r0, r2, r1, r0
    mov r2, r2, lsr #4
    str r2, [r5, #0x18]
    ldmia sp!, {r3, r4, r5, pc}
}
