/* ov006 row 0x021fdbc8: 84 bytes.
 *
 * What it does: Moves 2-register chunks between two pointers with writeback block moves (one load, one store).
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x4c -> native_data_0220b98c (image word 0x0220b98c)
 *   pool +0x50 -> native_fn_021fdc1c+1 (image word 0x021fdc1d)
 *   branch +0x18 -> +0x48
 *   branch +0x22 -> +0x48
 *   test +0x16 cmp r0, #0x0
 *   test +0x20 cmp r0, #0x0
 *   2 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fdbc8; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 10 of 84 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_0220b98c[];
extern void native_fn_02203188(void);
extern void native_fn_021f530c(void);
extern void native_fn_02200344(void);
extern void native_fn_021fdc1c(void);
extern void ov006_main_loop_set_callback_021f52cc(void);


asm u32 native_ov006_021fdbc8 (register u32 a0)
{
    push {lr}
    sub sp, #0x14
    ldr r3, =native_data_0220b98c
    add r2, sp, #0x8
    ldmia r3!, {r0, r1}
    stmia r2!, {r0, r1}
    ldr r0, [r3, #0]
    str r0, [r2, #0]
    mov r0, #0x1
    bl native_fn_02203188
    cmp r0, #0x0
    bne ov006_021fdbc8_L48
    mov r0, #0x0
    bl native_fn_02203188
    cmp r0, #0x0
    bne ov006_021fdbc8_L48
    mov r0, #0x0
    add r1, sp, #0x4
    bl native_fn_021f530c
    mov r0, #0x0
    str r0, [sp]
    ldr r0, [sp, #0x4]
    lsl r1, r0, #0x2
    add r0, sp, #0x8
    ldr r0, [r0, r1]
    mov r1, #0x1
    add r2, r1, #0x0
    sub r3, r1, #0x2
    bl native_fn_02200344
    ldr r0, =native_fn_021fdc1c+1
    bl ov006_main_loop_set_callback_021f52cc
ov006_021fdbc8_L48:
    add sp, #0x14
    pop {pc}
}
