/* ov006 row 0x021f913c: 184 bytes.
 *
 * What it does: Writes 2 blocks of 3 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x9c -> native_data_0221c0e0 (image word 0x0221c0e0)
 *   pool +0xa0 -> native_data_0220ddd0 (image word 0x0220ddd0)
 *   pool +0xa4 -> constant 0x0200494c (image word 0x0200494c)
 *   pool +0xa8 -> native_fn_021fa164+1 (image word 0x021fa165)
 *   pool +0xac -> native_fn_021f7ef8+1 (image word 0x021f7ef9)
 *   pool +0xb0 -> native_fn_021fdb08+1 (image word 0x021fdb09)
 *   pool +0xb4 -> native_data_0221c0e0 (image word 0x0221c0e0)
 *   branch +0x3c -> +0x56
 *   branch +0x54 -> +0x90
 *   branch +0x60 -> +0x7a
 *   branch +0x78 -> +0x90
 *   test +0x3a cmp r0, #0x0
 *   test +0x5e cmp r0, #0x0
 *   0 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f913c; the literal pool and
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
extern u8 native_data2_0221c0e0[];
extern void native_fn_022043a4(void);
extern void native_fn_02203690(void);
extern u8 native_data_0220ddd0[];
extern void native_fn_021f27d4(void);
extern void native_fn_02203954(void);
extern void native_fn_021f530c(void);
extern void native_fn_021f52d8(void);
extern void native_fn_021f5300(void);
extern void native_fn_021fa164(void);
extern void ov006_main_loop_set_callback_021f52cc(void);
extern void native_fn_021f7ef8(void);
extern void native_fn_021fdb08(void);
extern u8 native_data3_0221c0e0[];
extern void native_fn_02203c20(void);


asm u32 native_ov006_021f913c (register u32 a0)
{
    push {r3, lr}
    sub sp, #0x8
    bl native_fn_021f2774
    ldr r0, =native_data2_0221c0e0
    ldr r0, [r0, #0]
    ldr r0, [r0, #0x4]
    bl native_fn_022043a4
    mov r0, #0x0
    bl native_fn_02203690
    ldr r0, =native_data_0220ddd0
    ldr r1, =0x0200494c
    bl native_fn_021f27d4
    mov r0, #0x1
    add r1, r0, #0x0
    bl native_fn_02203954
    mov r0, #0x0
    mov r1, #0x15
    bl native_fn_02203954
    add r0, sp, #0x4
    add r1, sp, #0x0
    bl native_fn_021f530c
    ldr r0, [sp, #0]
    cmp r0, #0x0
    bne ov006_021f913c_L56
    mov r0, #0x2
    mov r1, #0x1
    bl native_fn_021f52d8
    ldr r1, [sp, #0x4]
    mov r0, #0x0
    bl native_fn_021f5300
    ldr r0, =native_fn_021fa164+1
    bl ov006_main_loop_set_callback_021f52cc
    b ov006_021f913c_L90
ov006_021f913c_L56:
    ldr r0, =native_data2_0221c0e0
    ldr r0, [r0, #0]
    add r0, #0x2a
    ldrb r0, [r0, #0]
    cmp r0, #0x0
    bne ov006_021f913c_L7a
    mov r0, #0x0
    mov r1, #0x1
    bl native_fn_021f52d8
    mov r0, #0x1
    mov r1, #0x0
    bl native_fn_021f5300
    ldr r0, =native_fn_021f7ef8+1
    bl ov006_main_loop_set_callback_021f52cc
    b ov006_021f913c_L90
ov006_021f913c_L7a:
    mov r0, #0x0
    add r1, r0, #0x0
    bl native_fn_021f52d8
    mov r0, #0x0
    mov r1, #0x1
    bl native_fn_021f5300
    ldr r0, =native_fn_021fdb08+1
    bl ov006_main_loop_set_callback_021f52cc
ov006_021f913c_L90:
    ldr r0, =native_data3_0221c0e0
    bl native_fn_02203c20
    add sp, #0x8
    pop {r3, pc}
    mov r8, r8
}
