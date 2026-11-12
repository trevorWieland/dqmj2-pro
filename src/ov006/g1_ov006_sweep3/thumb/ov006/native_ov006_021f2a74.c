/* ov006 row 0x021f2a74: 80 bytes.
 *
 * What it does: 25 instructions; 5 call(s) to 0x02203c08, 0x021f27d4, 0x021f5334, +2 more; loops (back edge at +0x12); returns through pop {r3, pc}; 5 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x3c -> constant 0x0221c054 (image word 0x0221c054)
 *   pool +0x40 -> native_data_0220d77c (image word 0x0220d77c)
 *   pool +0x44 -> constant 0x02004f18 (image word 0x02004f18)
 *   pool +0x48 -> native_data_0220d72c (image word 0x0220d72c)
 *   pool +0x4c -> constant 0x02004c18 (image word 0x02004c18)
 *   branch +0x1c -> +0x24
 *   branch +0x20 -> +0x30
 *   test +0x1a cmp r0, #0x0
 *   test +0x1e cmp r0, #0x1
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f2a74; the literal pool and
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

extern void ov006_clear_buffer_02203c08(void);
extern u8 native_data_0220d77c[];
extern void native_fn_021f27d4(void);
extern void native_fn_021f5334(void);
extern u8 native_data_0220d72c[];


asm u32 native_ov006_021f2a74 (register u32 a0)
{
    push {r3, lr}
    mov r0, #0xc0
    mov r1, #0x4
    bl ov006_clear_buffer_02203c08
    ldr r1, =0x0221c054
    str r0, [r1, #0]
    ldr r0, =native_data_0220d77c
    ldr r1, =0x02004f18
    bl native_fn_021f27d4
    bl native_fn_021f5334
    cmp r0, #0x0
    beq ov006_021f2a74_L24
    cmp r0, #0x1
    beq ov006_021f2a74_L30
    pop {r3, pc}
ov006_021f2a74_L24:
    ldr r0, =native_data_0220d72c
    ldr r1, =0x02004c18
    ldr r0, [r0, #0]
    bl native_fn_021f27d4
    pop {r3, pc}
ov006_021f2a74_L30:
    ldr r0, =native_data_0220d72c
    ldr r1, =0x02004c18
    ldr r0, [r0, #0x4]
    bl native_fn_021f27d4
    pop {r3, pc}
}
