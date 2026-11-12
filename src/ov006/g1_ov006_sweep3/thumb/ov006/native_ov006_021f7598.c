/* ov006 row 0x021f7598: 76 bytes.
 *
 * What it does: 26 instructions; 8 call(s) to 0x021f75e4, 0x021f75e8, 0x02200574, +5 more; loops (back edge at +0x34); returns through pop {r3, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x44 -> constant 0x0221c0c4 (image word 0x0221c0c4)
 *   pool +0x48 -> native_fn_021f75ec+1 (image word 0x021f75ed)
 *   branch +0x10 -> +0x18
 *   branch +0x14 -> +0x26
 *   branch +0x24 -> +0x32
 *   test +0x0e cmp r0, #0x0
 *   test +0x12 cmp r0, #0x1
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f7598; the literal pool and
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

extern void native_fn_021f75e4(void);
extern void native_fn_021f75e8(void);
extern void native_fn_02200574(void);
extern void native_fn_021ff6d4(void);
extern void native_fn_021f5538(void);
extern void native_fn_02200548(void);
extern void native_fn_021f75ec(void);
extern void ov006_main_loop_set_callback_021f52cc(void);


asm u32 native_ov006_021f7598 (register u32 a0)
{
    push {r3, lr}
    bl native_fn_021f75e4
    bl native_fn_021f75e8
    bl native_fn_02200574
    cmp r0, #0x0
    beq ov006_021f7598_L18
    cmp r0, #0x1
    beq ov006_021f7598_L26
    pop {r3, pc}
ov006_021f7598_L18:
    ldr r0, =0x0221c0c4
    mov r1, #0x0
    strb r1, [r0, #0x1]
    mov r0, #0x7
    bl native_fn_021ff6d4
    b ov006_021f7598_L32
ov006_021f7598_L26:
    ldr r0, =0x0221c0c4
    mov r1, #0x1
    strb r1, [r0, #0x1]
    mov r0, #0xe
    bl native_fn_021ff6d4
ov006_021f7598_L32:
    mov r0, #0x0
    bl native_fn_021f5538
    bl native_fn_02200548
    ldr r0, =native_fn_021f75ec+1
    bl ov006_main_loop_set_callback_021f52cc
    pop {r3, pc}
}
