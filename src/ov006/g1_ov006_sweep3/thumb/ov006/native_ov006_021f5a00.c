/* ov006 row 0x021f5a00: 76 bytes.
 *
 * What it does: 27 instructions; 7 call(s) to 0x02203188, 0x02203188, 0x021f5334, +4 more; loops (back edge at +0x16); returns through pop {r3, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: block load.
 *
 *   pool +0x44 -> native_fn_021f5a4c+1 (image word 0x021f5a4d)
 *   pool +0x48 -> native_fn_021fc870+1 (image word 0x021fc871)
 *   branch +0x0a -> +0x42
 *   branch +0x14 -> +0x42
 *   branch +0x1c -> +0x24
 *   branch +0x20 -> +0x34
 *   test +0x08 cmp r0, #0x0
 *   test +0x12 cmp r0, #0x0
 *   test +0x1a cmp r0, #0x0
 *   test +0x1e cmp r0, #0x1
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f5a00; the literal pool and
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

extern void native_fn_02203188(void);
extern void native_fn_021f5334(void);
extern void native_fn_021f52d8(void);
extern void native_fn_021f5a4c(void);
extern void ov006_main_loop_set_callback_021f52cc(void);
extern void native_fn_021fc870(void);


asm u32 native_ov006_021f5a00 (register u32 a0)
{
    push {r3, lr}
    mov r0, #0x1
    bl native_fn_02203188
    cmp r0, #0x0
    bne ov006_021f5a00_L42
    mov r0, #0x0
    bl native_fn_02203188
    cmp r0, #0x0
    bne ov006_021f5a00_L42
    bl native_fn_021f5334
    cmp r0, #0x0
    beq ov006_021f5a00_L24
    cmp r0, #0x1
    beq ov006_021f5a00_L34
    pop {r3, pc}
ov006_021f5a00_L24:
    mov r0, #0x0
    mov r1, #0x1
    bl native_fn_021f52d8
    ldr r0, =native_fn_021f5a4c+1
    bl ov006_main_loop_set_callback_021f52cc
    pop {r3, pc}
ov006_021f5a00_L34:
    mov r0, #0x1
    add r1, r0, #0x0
    bl native_fn_021f52d8
    ldr r0, =native_fn_021fc870+1
    bl ov006_main_loop_set_callback_021f52cc
ov006_021f5a00_L42:
    pop {r3, pc}
}
