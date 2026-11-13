/* ov006 row 0x021e4250: 104 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x64 -> constant 0x04000208 (image word 0x04000208)
 *   branch +0x10 -> +0x48
 *   branch +0x1c -> +0x5c
 *   branch +0x44 -> +0x5c
 *   test +0x0c cmp r0, r1
 *   test +0x18 cmp r0, r1
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e4250; the literal pool and
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

extern void ov006_active_state_value_021e65a4(void);
extern void native_fn_021e9420(void);
extern void native_fn_020bb2b0(void);
extern void native_fn_02008140(void);
extern void native_fn_021e802c(void);
extern void native_fn_021e7e28(void);
extern void native_fn_ov006_021e3f28(void);
extern void ov006_forward_four_args_021e3cd8(void);


asm u32 native_ov006_021e4250 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    bl ov006_active_state_value_021e65a4
    mvn r1, #3
    cmp r0, r1
    beq ov006_021e4250_L48
    add r1, r1, #1
    cmp r0, r1
    bne ov006_021e4250_L5c
    mov r0, #0
    bl native_fn_021e9420
    bl native_fn_020bb2b0
    ldr r2, =0x04000208
    mov r1, #1
    ldrh r0, [r2]
    mov r0, #0
    strh r1, [r2]
    bl native_fn_02008140
    b ov006_021e4250_L5c
ov006_021e4250_L48:
    mov r0, #4
    bl native_fn_021e802c
    bl native_fn_021e7e28
    mov r0, #3
    bl native_fn_ov006_021e3f28
ov006_021e4250_L5c:
    bl ov006_forward_four_args_021e3cd8
    ldmia sp!, {r3, pc}
}
