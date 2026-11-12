/* ov006 row 0x02203338: 180 bytes.
 *
 * What it does: 75 instructions; 9 call(s) to 0x02203c08, 0x022030a4, 0x021f5328, +6 more; loops (back edge at +0x18); returns through pop {r3, r4, r5, r6, r7, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0xa4 -> constant 0x0221c184 (image word 0x0221c184)
 *   pool +0xa8 -> native_data_0220e8dc (image word 0x0220e8dc)
 *   pool +0xac -> constant 0x00000674 (image word 0x00000674)
 *   pool +0xb0 -> native_data_0220e8e4 (image word 0x0220e8e4)
 *   branch +0x2c -> +0x68
 *   back edge +0x64 -> +0x36
 *   back edge +0x9e -> +0x70
 *   test +0x2a cmp r0, #0x6
 *   test +0x62 cmp r7, #0x2
 *   test +0x9c cmp r7, #0x2
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02203338; the literal pool and
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
extern void native_fn_022030a4(void);
extern void native_fn_021f5328(void);
extern u8 native_data_0220e8dc[];
extern void native_fn_02202a80(void);
extern void native_fn_02036928(void);
extern u8 native_data_0220e8e4[];


asm u32 native_ov006_02203338 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    mov r0, #0x1a
    lsl r0, r0, #0x6
    mov r1, #0x4
    bl ov006_clear_buffer_02203c08
    add r1, r0, #0x0
    ldr r0, =0x0221c184
    mov r2, #0x30
    str r1, [r0, #0]
    mov r0, #0x20
    add r1, #0x10
    bl native_fn_022030a4
    ldr r1, =0x0221c184
    ldr r2, [r1, #0]
    mov r1, #0x67
    lsl r1, r1, #0x4
    str r0, [r2, r1]
    bl native_fn_021f5328
    cmp r0, #0x6
    bne ov006_02203338_L68
    mov r7, #0x0
    ldr r4, =native_data_0220e8dc
    add r5, r7, #0x0
    add r6, r7, #0x0
ov006_02203338_L36:
    ldr r0, [r4, #0]
    mov r1, #0x0
    mov r2, #0x4
    bl native_fn_02202a80
    ldr r1, =0x0221c184
    ldr r1, [r1, #0]
    add r2, r1, r5
    ldr r1, =0x00000674
    str r0, [r2, r1]
    ldr r0, =0x0221c184
    ldr r1, [r0, #0]
    add r0, r1, r6
    add r2, r1, r5
    ldr r1, =0x00000674
    ldr r1, [r2, r1]
    blx native_fn_02036928
    add r7, r7, #0x1
    add r4, r4, #0x4
    add r5, r5, #0x4
    add r6, #0x8
    cmp r7, #0x2
    blt ov006_02203338_L36
    pop {r3, r4, r5, r6, r7, pc}
ov006_02203338_L68:
    mov r7, #0x0
    ldr r4, =native_data_0220e8e4
    add r5, r7, #0x0
    add r6, r7, #0x0
ov006_02203338_L70:
    ldr r0, [r4, #0]
    mov r1, #0x0
    mov r2, #0x4
    bl native_fn_02202a80
    ldr r1, =0x0221c184
    ldr r1, [r1, #0]
    add r2, r1, r5
    ldr r1, =0x00000674
    str r0, [r2, r1]
    ldr r0, =0x0221c184
    ldr r1, [r0, #0]
    add r0, r1, r6
    add r2, r1, r5
    ldr r1, =0x00000674
    ldr r1, [r2, r1]
    blx native_fn_02036928
    add r7, r7, #0x1
    add r4, r4, #0x4
    add r5, r5, #0x4
    add r6, #0x8
    cmp r7, #0x2
    blt ov006_02203338_L70
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
}
