/* ov006 row 0x021f99d0: 116 bytes.
 *
 * What it does: Writes 2 blocks of 4 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x60 -> native_data_0221c0e4 (image word 0x0221c0e4)
 *   pool +0x64 -> native_data_0220de48 (image word 0x0220de48)
 *   pool +0x68 -> constant 0x0200494c (image word 0x0200494c)
 *   pool +0x6c -> native_fn_021fa164+1 (image word 0x021fa165)
 *   pool +0x70 -> native_data_0221c0e4 (image word 0x0221c0e4)
 *   branch +0x3a -> +0x40
 *   test +0x38 cmp r0, #0x3
 *   1 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f99d0; the literal pool and
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

extern void native_fn_021f2774(void);
extern u8 native_data_0221c0e4[];
extern void native_fn_022043a4(void);
extern void native_fn_02203690(void);
extern u8 native_data_0220de48[];
extern void native_fn_021f27d4(void);
extern void native_fn_02203954(void);
extern void native_fn_021f530c(void);
extern void native_fn_021f52d8(void);
extern void native_fn_021f5300(void);
extern void native_fn_021fa164(void);
extern void ov006_main_loop_set_callback_021f52cc(void);
extern u8 native_data2_0221c0e4[];
extern void native_fn_02203c20(void);


asm u32 native_ov006_021f99d0 (register u32 a0)
{
    push {r3, lr}
    bl native_fn_021f2774
    ldr r0, =native_data_0221c0e4
    ldr r0, [r0, #0]
    ldr r0, [r0, #0x4]
    bl native_fn_022043a4
    mov r0, #0x0
    bl native_fn_02203690
    ldr r0, =native_data_0220de48
    ldr r1, =0x0200494c
    bl native_fn_021f27d4
    mov r0, #0x1
    add r1, r0, #0x0
    bl native_fn_02203954
    mov r0, #0x0
    mov r1, #0x15
    bl native_fn_02203954
    add r0, sp, #0x0
    mov r1, #0x0
    bl native_fn_021f530c
    ldr r0, [sp, #0]
    cmp r0, #0x3
    blt ov006_021f99d0_L40
    add r0, r0, #0x1
    str r0, [sp, #0]
ov006_021f99d0_L40:
    mov r0, #0x2
    mov r1, #0x1
    bl native_fn_021f52d8
    ldr r1, [sp, #0]
    mov r0, #0x0
    add r1, r1, #0x3
    bl native_fn_021f5300
    ldr r0, =native_fn_021fa164+1
    bl ov006_main_loop_set_callback_021f52cc
    ldr r0, =native_data2_0221c0e4
    bl native_fn_02203c20
    pop {r3, pc}
}
