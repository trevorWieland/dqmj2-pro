/* ov006 row 0x021fdac0: 72 bytes.
 *
 * What it does: 26 instructions; 5 call(s) to 0x021fdaf8, 0x021f530c, 0x021f5334, +2 more; loops (back edge at +0x14); returns through pop {r3, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x3c -> constant 0x0221c124 (image word 0x0221c124)
 *   pool +0x40 -> native_fn_021f57f4+1 (image word 0x021f57f5)
 *   pool +0x44 -> native_fn_021fda18+1 (image word 0x021fda19)
 *   branch +0x0e -> +0x38
 *   branch +0x1e -> +0x32
 *   branch +0x22 -> +0x32
 *   branch +0x28 -> +0x32
 *   test +0x0c cmp r0, #0xb4
 *   test +0x1c cmp r0, #0x0
 *   test +0x20 cmp r0, #0x1
 *   test +0x26 cmp r0, #0x0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fdac0; the literal pool and
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

extern void native_fn_021f530c(void);
extern void native_fn_021f5334(void);
extern void native_fn_021f57f4(void);
extern void ov006_main_loop_set_callback_021f52cc(void);
extern void native_fn_021fda18(void);


asm u32 native_ov006_021fdac0 (register u32 a0)
{
    push {r3, lr}
    ldr r0, =0x0221c124
    ldrb r1, [r0, #0]
    add r1, r1, #0x1
    strb r1, [r0, #0]
    ldrb r0, [r0, #0]
    cmp r0, #0xb4
    blo ov006_021fdac0_L38
    mov r0, #0x0
    add r1, sp, #0x0
    bl native_fn_021f530c
    bl native_fn_021f5334
    cmp r0, #0x0
    beq ov006_021fdac0_L32
    cmp r0, #0x1
    bne ov006_021fdac0_L32
    ldr r0, [sp]
    cmp r0, #0x0
    beq ov006_021fdac0_L32
    ldr r0, =native_fn_021f57f4+1
    bl ov006_main_loop_set_callback_021f52cc
    pop {r3, pc}
ov006_021fdac0_L32:
    ldr r0, =native_fn_021fda18+1
    bl ov006_main_loop_set_callback_021f52cc
ov006_021fdac0_L38:
    pop {r3, pc}
    mov r8, r8
}
