/* ov000 row 0x02210628: 296 bytes.
 *
 * What it does: 74 instructions; 10 call(s) to 0x021e07b8, 0x021e07b8, 0x021e07b8, +7 more; loops (back edge at +0x34); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x20 -> +0x104
 *   branch +0x2c -> +0x104
 *   branch +0xf4 -> +0x100
 *   back edge +0x120 -> +0x10
 *   test +0x1c cmp r1, r4
 *   test +0x28 cmp r0, #0
 *   test +0xf0 cmp r0, r4
 *   test +0x110 cmp r0, #0
 *   test +0x11c cmp r8, #3
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02210628; the literal pool and
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


asm u32 native_ov000_02210628 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r10, r0
    mov r8, #0
    mvn r4, #0
ov000_02210628_L10:
    add r9, r10, r8
    add r0, r9, #512
    ldrsb r1, [r0, #104]
    cmp r1, r4
    beq ov000_02210628_L104
    ldrsb r0, [r0, #110]
    cmp r0, #0
    bne ov000_02210628_L104
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
    mov r11, r0
    mov r0, #0
    bl ov000_saved_world_position_get_021e07b8
    str r0, [sp]
    mov r0, #0
    bl ov000_saved_world_position_get_021e07b8
    ldr r2, [r7, #0x8]
    ldr r1, [r6, #0x8]
    ldr r6, [r5]
    ldr r5, [r11]
    ldr r3, [sp]
    ldr r11, [r10, #0x78]
    ldr r7, [r10, #0x70]
    sub r2, r11, r2
    sub r11, r11, r1
    sub r1, r7, r5
    ldr r3, [r3, #0x4]
    ldr r5, [r10, #0x74]
    ldr r0, [r0, #0x4]
    sub r3, r5, r3
    sub r0, r5, r0
    smull r0, r5, r3, r0
    sub r6, r7, r6
    smlal r0, r5, r6, r1
    smlal r0, r5, r2, r11
    mov r0, r0, lsr #12
    orr r0, r0, r5, lsl #20
    bl native_fn_0200236c
    mov r0, r0, asr #12
    rsbs r5, r0, #135
    add r0, r9, #512
    ldrsb r0, [r0, #104]
    movmi r5, #0
    bl native_fn_021e7b9c
    add r1, r9, #512
    strb r0, [r9, #0x26b]
    ldrsb r0, [r1, #107]
    cmp r0, r4
    beq ov000_02210628_L100
    mov r1, r5
    bl native_fn_021e7bbc
ov000_02210628_L100:
    strb r4, [r9, #0x268]
ov000_02210628_L104:
    add r0, r9, #512
    ldrsb r0, [r0, #110]
    add r8, r8, #1
    cmp r0, #0
    subge r0, r0, #1
    strgeb r0, [r9, #0x26e]
    cmp r8, #3
    blt ov000_02210628_L10
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
