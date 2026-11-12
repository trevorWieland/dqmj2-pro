/* ov000 row 0x021e1cc0: 316 bytes.
 *
 * What it does: 77 instructions; 16 call(s) to 0x021e0d78, 0x021e1cfc, 0x021e7b9c, +13 more; loops (back edge at +0x24); returns through pop {r4, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x134 -> constant 0x022322d4 (image word 0x022322d4)
 *   pool +0x138 -> constant 0x022324d4 (image word 0x022324d4)
 *   branch +0x14 -> +0x68
 *   branch +0x34 -> +0x3c
 *   branch +0x48 -> +0x54
 *   branch +0x7c -> +0x8c
 *   branch +0x9c -> +0xd0
 *   branch +0xdc -> +0xf4
 *   branch +0xf0 -> +0x108
 *   branch +0xf8 -> +0x108
 *   test +0x10 cmp r1, #0
 *   test +0x30 cmp r0, #0
 *   test +0x44 cmp r1, #0
 *   test +0x78 cmp r0, #3
 *   test +0x98 cmp r1, #0
 *   test +0xd8 cmp r1, #1
 *   test +0xf4 cmp r1, #2
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e1cc0; the literal pool and
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

extern void native_fn_021e0d78(void);
extern void native_fn_021e7b9c(void);
extern void native_fn_0205f35c(void);
extern void native_fn_02028158(void);
extern void native_fn_02042c2c(void);
extern void native_fn_02041f90(void);
extern void native_fn_021d84e8(void);
extern void native_fn_021e1658(void);


asm u32 native_ov000_021e1cc0 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    ldr r0, =0x022322d4
    add r0, r0, #512
    ldrsb r1, [r0, #125]
    cmp r1, #0
    bne ov000_021e1cc0_L68
    ldrsb r0, [r0, #122]
    mov r1, #0
    mov r2, r1
    bl native_fn_021e0d78
    ldr r0, =0x022324d4
    ldrsh r0, [r0, #128]
    cmp r0, #0
    ble ov000_021e1cc0_L3c
    bl native_fn_021e7b9c
ov000_021e1cc0_L3c:
    ldr r0, =0x022324d4
    ldrsh r1, [r0, #130]
    cmp r1, #0
    ble ov000_021e1cc0_L54
    mvn r0, #0
    bl native_fn_0205f35c
ov000_021e1cc0_L54:
    ldr r1, =0x022322d4
    add r0, r1, #512
    ldrsb r0, [r0, #125]
    add r0, r0, #1
    strb r0, [r1, #0x27d]
ov000_021e1cc0_L68:
    ldr r1, =0x022322d4
    add r0, r1, #512
    ldrsb r0, [r0, #123]
    ldr r4, [r1, #0x188]
    cmp r0, #3
    bne ov000_021e1cc0_L8c
    add r0, r4, #737280
    bl native_fn_02028158
    mov r4, r0
ov000_021e1cc0_L8c:
    ldr r0, =0x022322d4
    add r1, r0, #512
    ldrsb r1, [r1, #123]
    cmp r1, #0
    beq ov000_021e1cc0_Ld0
    bl native_fn_02042c2c
    sub r0, r4, r0
    bl native_fn_02028158
    mov r4, r0
    ldr r0, =0x022322d4
    bl native_fn_02042c2c
    add r0, r4, r0
    bl native_fn_02028158
    mov r1, r0
    ldr r0, =0x022322d4
    mov r2, #1
    bl native_fn_02041f90
ov000_021e1cc0_Ld0:
    ldr r0, =0x022322d4
    ldrb r1, [r0, #0x27c]
    cmp r1, #1
    bne ov000_021e1cc0_Lf4
    bl native_fn_02042c2c
    add r0, r0, #737280
    mov r1, #0
    bl native_fn_021d84e8
    b ov000_021e1cc0_L108
ov000_021e1cc0_Lf4:
    cmp r1, #2
    bne ov000_021e1cc0_L108
    bl native_fn_02042c2c
    mov r1, #0
    bl native_fn_021d84e8
ov000_021e1cc0_L108:
    bl native_fn_021e1658
    ldr r0, =0x022322d4
    ldr r0, [r0, #0x60]
    ldr r1, [r0, #0x8]
    ldr r0, [r0]
    ldrh r1, [r1, #4]
    mov r1, r1, lsl #12
    sub r1, r1, #1
    sub r0, r1, r0
    mov r0, r0, asr #12
    ldmia sp!, {r4, pc}
}
