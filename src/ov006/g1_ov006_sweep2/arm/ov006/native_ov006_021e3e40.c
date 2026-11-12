/* ov006 row 0x021e3e40: 100 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x60 -> constant 0x02218d20 (image word 0x02218d20)
 *   branch +0x10 -> +0x48
 *   branch +0x1c -> +0x48
 *   branch +0x2c -> +0x38
 *   test +0x0c cmp r0, #10
 *   test +0x18 cmp r0, #4
 *   test +0x28 cmp r0, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e3e40; the literal pool and
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

extern void native_fn_020273f0(void);
extern void native_fn_0202a32c(void);
extern void native_fn_0202a164(void);
extern void native_fn_020c1898(void);
extern void ov006_forward_four_args_021e3cd8(void);


asm u32 native_ov006_021e3e40 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r0, =0x02218d20
    ldr r0, [r0]
    cmp r0, #10
    ble ov006_021e3e40_L48
    bl native_fn_020273f0
    cmp r0, #4
    beq ov006_021e3e40_L48
    mov r0, #7
    bl native_fn_0202a32c
    cmp r0, #0
    beq ov006_021e3e40_L38
    mov r0, #7
    bl native_fn_0202a164
ov006_021e3e40_L38:
    mov r0, #1
    bl native_fn_020c1898
    mov r0, #7
    ldmia sp!, {r3, pc}
ov006_021e3e40_L48:
    ldr r0, =0x02218d20
    ldr r1, [r0]
    add r1, r1, #1
    str r1, [r0]
    bl ov006_forward_four_args_021e3cd8
    ldmia sp!, {r3, pc}
}
