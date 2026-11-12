/* ov006 row 0x021e4138: 104 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x10 -> +0x50
 *   branch +0x18 -> +0x28
 *   branch +0x20 -> +0x3c
 *   branch +0x24 -> +0x60
 *   branch +0x38 -> +0x60
 *   branch +0x4c -> +0x60
 *   test +0x0c cmp r0, r1
 *   test +0x14 cmp r0, #1
 *   test +0x1c cmp r0, #2
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e4138; the literal pool and
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
extern void native_fn_021e802c(void);
extern void native_fn_ov006_021e3f28(void);
extern void ov006_forward_four_args_021e3cd8(void);


asm u32 native_ov006_021e4138 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    bl ov006_active_state_value_021e65a4
    mvn r1, #0
    cmp r0, r1
    beq ov006_021e4138_L50
    cmp r0, #1
    beq ov006_021e4138_L28
    cmp r0, #2
    beq ov006_021e4138_L3c
    b ov006_021e4138_L60
ov006_021e4138_L28:
    mov r0, #0
    bl native_fn_021e802c
    mov r0, #7
    bl native_fn_ov006_021e3f28
    b ov006_021e4138_L60
ov006_021e4138_L3c:
    mov r0, #0
    bl native_fn_021e802c
    mov r0, #10
    bl native_fn_ov006_021e3f28
    b ov006_021e4138_L60
ov006_021e4138_L50:
    mov r0, #0
    bl native_fn_021e802c
    mov r0, #3
    bl native_fn_ov006_021e3f28
ov006_021e4138_L60:
    bl ov006_forward_four_args_021e3cd8
    ldmia sp!, {r3, pc}
}
