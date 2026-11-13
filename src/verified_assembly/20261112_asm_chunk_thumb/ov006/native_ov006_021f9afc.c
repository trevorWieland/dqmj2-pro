/* ov006 row 0x021f9afc: 60 bytes.
 *
 * What it does: Writes one block of 4 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x34 -> constant 0x0221c0e4 (image word 0x0221c0e4)
 *   pool +0x38 -> native_fn_021f9b38+1 (image word 0x021f9b39)
 *   branch +0x12 -> +0x1a
 *   branch +0x16 -> +0x22
 *   branch +0x20 -> +0x28
 *   test +0x10 cmp r0, #0x0
 *   test +0x14 cmp r0, #0x1
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f9afc; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 14 of 60 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02200574(void);
extern void native_fn_021ff6d4(void);
extern void native_fn_02200548(void);
extern void native_fn_021f9b38(void);
extern void ov006_main_loop_set_callback_021f52cc(void);


asm u32 native_ov006_021f9afc (register u32 a0)
{
    push {r3, lr}
    bl native_fn_02200574
    ldr r1, =0x0221c0e4
    ldr r2, [r1, #0]
    strb r0, [r2, #0x15]
    ldr r0, [r1, #0]
    ldrb r0, [r0, #0x15]
    cmp r0, #0x0
    beq ov006_021f9afc_L1a
    cmp r0, #0x1
    beq ov006_021f9afc_L22
    pop {r3, pc}
ov006_021f9afc_L1a:
    mov r0, #0x7
    bl native_fn_021ff6d4
    b ov006_021f9afc_L28
ov006_021f9afc_L22:
    mov r0, #0xe
    bl native_fn_021ff6d4
ov006_021f9afc_L28:
    bl native_fn_02200548
    ldr r0, =native_fn_021f9b38+1
    bl ov006_main_loop_set_callback_021f52cc
    pop {r3, pc}
}
