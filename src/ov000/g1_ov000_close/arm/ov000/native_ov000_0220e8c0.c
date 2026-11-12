/* ov000 row 0x0220e8c0: 472 bytes.
 *
 * What it does: 118 instructions; 19 call(s) to 0x0220a2a4, 0x021e07b8, 0x021e07b8, +16 more; loops (back edge at +0x1c); returns through pop {r3, r4, r5, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x10 -> +0x90
 *   branch +0x8c -> +0x1d0
 *   branch +0x94 -> +0xf8
 *   branch +0xb4 -> +0xc0
 *   branch +0xbc -> +0xc8
 *   branch +0xd8 -> +0x1d0
 *   branch +0xf4 -> +0x1d0
 *   branch +0xfc -> +0x154
 *   branch +0x120 -> +0x1d0
 *   branch +0x150 -> +0x1d0
 *   branch +0x158 -> +0x18c
 *   branch +0x188 -> +0x1d0
 *   branch +0x190 -> +0x1d0
 *   branch +0x1b0 -> +0x1d0
 *   test +0x0c cmp r1, #0
 *   test +0x90 cmp r1, #10
 *   test +0xd4 cmp r0, #8192
 *   test +0xf8 cmp r1, #20
 *   test +0x11c cmp r1, #4096
 *   test +0x154 cmp r1, #30
 *   test +0x17c cmp r0, #0
 *   test +0x18c cmp r1, #40
 *   test +0x1ac cmp r1, r0
 *   0 block transfer(s), 9 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0220e8c0; the literal pool and
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

extern void native_fn_0220a2a4(void);
extern void ov000_saved_world_position_get_021e07b8(void);
extern void native_fn_020028d8(void);
extern void native_fn_0200235c(void);
extern void native_fn_0203d294(void);
extern void native_fn_02042c2c(void);
extern void native_fn_02042104(void);
extern void native_fn_020c56b4(void);
extern void native_fn_02042bfc(void);
extern void native_fn_021dc374(void);
extern void native_fn_02041f48(void);
extern void native_fn_02209c68(void);


asm u32 native_ov000_0220e8c0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r4, r0
    ldrb r1, [r4, #0x279]
    cmp r1, #0
    bne ov000_0220e8c0_L90
    mov r1, #0
    mov r2, r1
    bl native_fn_0220a2a4
    mov r0, #0
    bl ov000_saved_world_position_get_021e07b8
    ldr r2, [r0]
    ldr r1, [r4, #0x70]
    mov r0, #0
    sub r5, r2, r1
    bl ov000_saved_world_position_get_021e07b8
    mov r0, #0
    bl ov000_saved_world_position_get_021e07b8
    ldr r2, [r0, #0x8]
    ldr r1, [r4, #0x78]
    mov r0, r5
    sub r1, r2, r1
    bl native_fn_020028d8
    mov r1, #71
    str r0, [r4, #0x27c]
    bl native_fn_0200235c
    mov r5, r0
    mov r0, #11
    bl native_fn_0203d294
    sub r0, r0, #5
    add r0, r5, r0, lsl #12
    str r0, [r4, #0x27c]
    mov r0, #10
    strb r0, [r4, #0x279]
    mov r0, #1
    strb r0, [r4, #0x2c1]
    b ov000_0220e8c0_L1d0
ov000_0220e8c0_L90:
    cmp r1, #10
    bne ov000_0220e8c0_Lf8
    bl native_fn_02042c2c
    ldr r1, [r4, #0x27c]
    mov r5, r0
    subs r0, r5, r1
    mov r1, #8192
    mov r0, r4
    mov r2, #1
    bpl ov000_0220e8c0_Lc0
    bl native_fn_02042104
    b ov000_0220e8c0_Lc8
ov000_0220e8c0_Lc0:
    rsb r1, r1, #0
    bl native_fn_02042104
ov000_0220e8c0_Lc8:
    ldr r0, [r4, #0x27c]
    subs r0, r5, r0
    rsbmi r0, r0, #0
    cmp r0, #8192
    bgt ov000_0220e8c0_L1d0
    mov r0, r4
    mov r1, #1
    mov r2, #0
    bl native_fn_0220a2a4
    mov r0, #20
    strb r0, [r4, #0x279]
    b ov000_0220e8c0_L1d0
ov000_0220e8c0_Lf8:
    cmp r1, #20
    bne ov000_0220e8c0_L154
    ldr r1, [r4, #0x60]
    ldr r2, [r1, #0x8]
    ldr r1, [r1]
    ldrh r2, [r2, #4]
    mov r2, r2, lsl #12
    sub r2, r2, #1
    sub r1, r2, r1
    cmp r1, #4096
    bgt ov000_0220e8c0_L1d0
    mov r1, #2
    mov r2, #0
    bl native_fn_0220a2a4
    add r0, r4, #512
    ldrsh r0, [r0, #118]
    bl native_fn_020c56b4
    ldr r1, [r0, #0x14]
    mov r0, r4
    bl native_fn_02042bfc
    mov r0, #30
    strb r0, [r4, #0x279]
    b ov000_0220e8c0_L1d0
ov000_0220e8c0_L154:
    cmp r1, #30
    bne ov000_0220e8c0_L18c
    add r0, r4, #512
    ldrsh r0, [r0, #118]
    bl native_fn_020c56b4
    ldrb r3, [r0, #0xc]
    add r0, r4, #112
    add r1, r4, #528
    mov r2, #0
    bl native_fn_021dc374
    cmp r0, #0
    movne r0, #40
    strneb r0, [r4, #0x279]
    b ov000_0220e8c0_L1d0
ov000_0220e8c0_L18c:
    cmp r1, #40
    bne ov000_0220e8c0_L1d0
    mov r1, #0
    mov r3, r1
    mov r2, #4096
    bl native_fn_02041f48
    ldr r1, [r4, #0x74]
    ldr r0, [r4, #0x2ac]
    cmp r1, r0
    ble ov000_0220e8c0_L1d0
    mov r0, r4
    mov r1, #3
    bl native_fn_02209c68
    mov r0, #0
    strb r0, [r4, #0x2c1]
    mov r0, #2
    strb r0, [r4, #0x1e4]
ov000_0220e8c0_L1d0:
    mov r0, #0
    ldmia sp!, {r3, r4, r5, pc}
}
