/* ov006 row 0x021e52a0: 136 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x84 -> native_data2_02218d30 (image word 0x02218d30)
 *   test +0x48 cmp r1, #0
 *   test +0x50 cmpne r0, #0
 *   test +0x68 cmp r1, #0
 *   2 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e52a0; the literal pool and
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

extern void native_fn_02008c58(void);
extern void native_fn_02068a68(void);
extern void native_fn_02063aa4(void);
extern void native_fn_02008e0c(void);
extern void native_fn_02068a88(void);
extern void native_fn_021e802c(void);
extern u8 native_data2_02218d30[];
extern void native_fn_021e7e78(void);
extern void native_fn_ov006_021e3f28(void);
extern void ov006_forward_four_args_021e3cd8(void);


asm u32 native_ov006_021e52a0 (register u32 a0)
{
    stmdb sp!, {lr}
    sub sp, sp, #76
    add r1, sp, #0
    mov r0, #0
    mov r2, #76
    bl native_fn_02008c58
    add r0, sp, #0
    bl native_fn_02068a68
    bl native_fn_02063aa4
    add r1, sp, #0
    mov r2, #20
    bl native_fn_02008e0c
    add r0, sp, #0
    bl native_fn_02068a88
    mov r0, #0
    bl native_fn_021e802c
    ldr r0, =native_data2_02218d30
    ldr r1, [r0, #0x20]
    cmp r1, #0
    ldrne r0, [r0, #0x10]
    cmpne r0, #0
    movne r0, #1
    moveq r0, #0
    bl native_fn_021e7e78
    ldr r0, =native_data2_02218d30
    ldr r1, [r0, #0x20]
    cmp r1, #0
    movne r0, #64
    ldreq r0, [r0, #0x1c]
    bl native_fn_ov006_021e3f28
    bl ov006_forward_four_args_021e3cd8
    add sp, sp, #76
    ldmia sp!, {pc}
}
