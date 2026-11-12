/* ov000 row 0x0221c4b0: 236 bytes.
 *
 * What it does: 58 instructions; 13 call(s) to 0x0221f39c, 0x020c4824, 0x0221f39c, +10 more; loops (back edge at +0x38); returns through pop {r4, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xe8 -> constant 0x022460d4 (image word 0x022460d4)
 *   branch +0x18 -> +0x28
 *   branch +0x20 -> +0x7c
 *   branch +0x24 -> +0xdc
 *   branch +0x78 -> +0xdc
 *   test +0x14 cmp r0, #8
 *   test +0x1c cmp r0, #10
 *   test +0x44 cmp r0, #6
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0221c4b0; the literal pool and
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

extern void native_fn_0221f39c(void);
extern void native_fn_020c4824(void);
extern void native_fn_02077860(void);
extern void native_fn_020c48d0(void);
extern void native_fn_020c48e8(void);
extern void native_fn_0221e7e8(void);
extern void native_fn_0206c238(void);
extern void native_fn_02068f60(void);


asm u32 native_ov000_0221c4b0 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    sub sp, sp, #16
    ldr r0, =0x022460d4
    mov r4, #0
    ldrsb r0, [r0, #16]
    cmp r0, #8
    beq ov000_0221c4b0_L28
    cmp r0, #10
    beq ov000_0221c4b0_L7c
    b ov000_0221c4b0_Ldc
ov000_0221c4b0_L28:
    bl native_fn_0221f39c
    mov r2, r0
    mov r0, #8
    mov r1, r4
    bl native_fn_020c4824
    bl native_fn_0221f39c
    bl native_fn_02077860
    cmp r0, #6
    movhi r0, #1
    movls r0, r4
    mov r0, r0, lsl #16
    mov r2, r0, lsr #16
    mov r0, #12
    mov r1, #0
    bl native_fn_020c48d0
    mov r0, #87
    bl native_fn_020c48e8
    mov r0, #0
    mov r4, #1
    bl native_fn_0221e7e8
    b ov000_0221c4b0_Ldc
ov000_0221c4b0_L7c:
    add r0, sp, #8
    str r0, [sp]
    add r12, sp, #12
    add r0, sp, #11
    add r1, sp, #10
    add r2, sp, #14
    add r3, sp, #9
    str r12, [sp, #0x4]
    bl native_fn_0206c238
    ldrb r0, [sp, #0xb]
    ldrb r1, [sp, #0xa]
    ldrh r2, [sp, #14]
    bl native_fn_020c4824
    ldrb r0, [sp, #0x9]
    ldrb r1, [sp, #0x8]
    ldrh r2, [sp, #12]
    bl native_fn_020c48d0
    mov r0, #87
    bl native_fn_020c48e8
    mov r0, r4
    mov r4, #1
    bl native_fn_0221e7e8
    mov r0, #0
    bl native_fn_02068f60
ov000_0221c4b0_Ldc:
    mov r0, r4
    add sp, sp, #16
    ldmia sp!, {r4, pc}
}
