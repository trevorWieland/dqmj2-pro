/* ov000 row 0x022104e8: 320 bytes.
 *
 * What it does: 79 instructions; 11 call(s) to 0x021e07b8, 0x021e07b8, 0x021e07b8, +8 more; loops (back edge at +0x14); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x13c -> constant 0x022385b8 (image word 0x022385b8)
 *   branch +0xc8 -> +0xd4
 *   branch +0xec -> +0xfc
 *   branch +0xf8 -> +0x12c
 *   back edge +0x134 -> +0xdc
 *   test +0xc4 cmp r0, r1
 *   test +0xe8 cmp r0, r6
 *   test +0xf4 cmp r0, #0
 *   test +0x130 cmp r5, #3
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022104e8; the literal pool and
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

extern void ov000_saved_world_position_get_021e07b8(void);
extern void native_fn_0200236c(void);
extern void native_fn_021e7b9c(void);
extern void native_fn_021e7bbc(void);
extern void native_fn_0205f2d8(void);


asm u32 native_ov000_022104e8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r10, r0
    mov r0, #0
    mov r11, r1
    mov r9, r2
    bl ov000_saved_world_position_get_021e07b8
    mov r8, r0
    mov r0, #0
    bl ov000_saved_world_position_get_021e07b8
    mov r7, r0
    mov r0, #0
    bl ov000_saved_world_position_get_021e07b8
    mov r6, r0
    mov r0, #0
    bl ov000_saved_world_position_get_021e07b8
    mov r5, r0
    mov r0, #0
    bl ov000_saved_world_position_get_021e07b8
    mov r4, r0
    mov r0, #0
    bl ov000_saved_world_position_get_021e07b8
    ldr r2, [r8, #0x8]
    ldr r1, [r7, #0x8]
    ldr r8, [r10, #0x78]
    ldr r6, [r6]
    sub r3, r8, r2
    ldr r5, [r5]
    ldr r7, [r10, #0x70]
    sub r2, r8, r1
    sub r1, r7, r6
    sub r6, r7, r5
    ldr r4, [r4, #0x4]
    ldr r5, [r10, #0x74]
    ldr r0, [r0, #0x4]
    sub r4, r5, r4
    sub r0, r5, r0
    smull r0, r5, r4, r0
    smlal r0, r5, r1, r6
    smlal r0, r5, r3, r2
    mov r0, r0, lsr #12
    orr r0, r0, r5, lsl #20
    bl native_fn_0200236c
    mov r4, r0
    mov r0, r4, asr #12
    rsbs r5, r0, #135
    mov r0, r11
    movmi r5, #0
    bl native_fn_021e7b9c
    mvn r1, #0
    cmp r0, r1
    beq ov000_022104e8_Ld4
    mov r1, r5
    bl native_fn_021e7bbc
ov000_022104e8_Ld4:
    mov r5, #0
    mvn r6, #0
ov000_022104e8_Ldc:
    add r0, r10, r5
    add r0, r0, #512
    ldrsb r0, [r0, #107]
    cmp r0, r6
    beq ov000_022104e8_Lfc
    bl native_fn_0205f2d8
    cmp r0, #0
    bne ov000_022104e8_L12c
ov000_022104e8_Lfc:
    ldr r0, =0x022385b8
    add r1, r10, r5
    ldr r0, [r0, #0x8]
    smull r2, r0, r4, r0
    adds r2, r2, #2048
    adc r0, r0, #0
    mov r2, r2, lsr #12
    orr r2, r2, r0, lsl #20
    mov r0, r2, asr #12
    strb r0, [r1, #0x26e]
    strb r9, [r1, #0x268]
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov000_022104e8_L12c:
    add r5, r5, #1
    cmp r5, #3
    blt ov000_022104e8_Ldc
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
