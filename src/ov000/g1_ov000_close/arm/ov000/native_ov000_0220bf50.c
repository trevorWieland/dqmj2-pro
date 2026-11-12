/* ov000 row 0x0220bf50: 532 bytes.
 *
 * What it does: 131 instructions; 33 call(s) to 0x0203d294, 0x0220a2a4, 0x02042c2c, +30 more; loops (back edge at +0x18); returns through pop {r3, r4, r5, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x20c -> constant 0x43340000 (image word 0x43340000)
 *   pool +0x210 -> constant 0x45800000 (image word 0x45800000)
 *   branch +0x10 -> +0x44
 *   branch +0x48 -> +0x15c
 *   branch +0x9c -> +0xb4
 *   branch +0xa4 -> +0xbc
 *   branch +0xb0 -> +0xc0
 *   branch +0xb8 -> +0xc0
 *   branch +0xf4 -> +0x124
 *   branch +0x120 -> +0x148
 *   branch +0x1c4 -> +0x1e4
 *   branch +0x1e0 -> +0x1f8
 *   test +0x0c cmp r1, #0
 *   test +0x44 cmp r1, #10
 *   test +0x70 cmp r0, #0
 *   test +0x98 cmp r0, #0
 *   test +0xa0 cmp r0, #1
 *   test +0xa8 cmp r0, #2
 *   test +0x15c cmp r1, #20
 *   test +0x198 cmp r0, #0
 *   test +0x1bc cmp r0, #0
 *   0 block transfer(s), 11 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0220bf50; the literal pool and
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

extern void native_fn_0203d294(void);
extern void native_fn_0220a2a4(void);
extern void native_fn_02042c2c(void);
extern void native_fn_02028158(void);
extern void native_fn_020c58c0(void);
extern void native_fn_02044cdc(void);
extern void native_fn_02025a28(void);
extern void native_fn_02025578(void);
extern void native_fn_0202537c(void);
extern void native_fn_02025ab8(void);
extern void native_fn_02024e0c(void);
extern void native_fn_02025ca4(void);
extern void native_fn_020259b4(void);
extern void native_fn_02042104(void);


asm u32 native_ov000_0220bf50 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    ldrb r1, [r5, #0x279]
    cmp r1, #0
    bne ov000_0220bf50_L44
    mov r0, #30
    bl native_fn_0203d294
    add r4, r0, #30
    add r3, r5, #512
    mov r0, r5
    mov r1, #1
    mov r2, #0
    strh r4, [r3, #122]
    bl native_fn_0220a2a4
    mov r0, #10
    strb r0, [r5, #0x279]
    ldmia sp!, {r3, r4, r5, pc}
ov000_0220bf50_L44:
    cmp r1, #10
    bne ov000_0220bf50_L15c
    bl native_fn_02042c2c
    ldr r1, [r5, #0x27c]
    add r0, r0, r1
    bl native_fn_02028158
    add r0, r5, #512
    ldrsh r1, [r0, #122]
    sub r1, r1, #1
    strh r1, [r0, #122]
    ldrsh r0, [r0, #122]
    cmp r0, #0
    ldmgtia sp!, {r3, r4, r5, pc}
    mov r0, #20
    bl native_fn_0203d294
    add r1, r0, #60
    add r0, r5, #512
    strh r1, [r0, #122]
    ldrsh r0, [r0, #118]
    bl native_fn_020c58c0
    bl native_fn_02044cdc
    cmp r0, #0
    beq ov000_0220bf50_Lb4
    cmp r0, #1
    beq ov000_0220bf50_Lbc
    cmp r0, #2
    moveq r4, #8
    b ov000_0220bf50_Lc0
ov000_0220bf50_Lb4:
    mov r4, #1
    b ov000_0220bf50_Lc0
ov000_0220bf50_Lbc:
    mov r4, #4
ov000_0220bf50_Lc0:
    add r0, r5, #512
    ldrsh r1, [r0, #122]
    smulbb r1, r1, r4
    strh r1, [r0, #122]
    ldrsh r4, [r0, #122]
    mov r0, r4
    bl native_fn_02025a28
    mov r1, r0
    ldr r0, =0x43340000
    bl native_fn_02025578
    mov r1, #0
    bl native_fn_0202537c
    mov r0, r4
    bls ov000_0220bf50_L124
    bl native_fn_02025a28
    mov r1, r0
    ldr r0, =0x43340000
    bl native_fn_02025578
    mov r1, r0
    ldr r0, =0x45800000
    bl native_fn_02025ab8
    mov r1, r0
    mov r0, #1056964608
    bl native_fn_02024e0c
    b ov000_0220bf50_L148
ov000_0220bf50_L124:
    bl native_fn_02025a28
    mov r1, r0
    ldr r0, =0x43340000
    bl native_fn_02025578
    mov r1, r0
    ldr r0, =0x45800000
    bl native_fn_02025ab8
    mov r1, #1056964608
    bl native_fn_02025ca4
ov000_0220bf50_L148:
    bl native_fn_020259b4
    str r0, [r5, #0x27c]
    mov r0, #20
    strb r0, [r5, #0x279]
    ldmia sp!, {r3, r4, r5, pc}
ov000_0220bf50_L15c:
    cmp r1, #20
    ldmneia sp!, {r3, r4, r5, pc}
    bl native_fn_02042c2c
    ldr r1, [r5, #0x27c]
    add r0, r0, r1
    bl native_fn_02028158
    ldr r1, [r5, #0x27c]
    mov r0, r5
    mov r2, #0
    bl native_fn_02042104
    add r0, r5, #512
    ldrsh r1, [r0, #122]
    sub r1, r1, #1
    strh r1, [r0, #122]
    ldrsh r0, [r0, #122]
    cmp r0, #0
    ldmgtia sp!, {r3, r4, r5, pc}
    mov r0, #30
    bl native_fn_0203d294
    add r2, r0, #90
    add r1, r5, #512
    mov r0, #10
    strh r2, [r1, #122]
    bl native_fn_0203d294
    cmp r0, #0
    mov r0, #10
    ble ov000_0220bf50_L1e4
    bl native_fn_0203d294
    mov r0, r0, lsl #12
    bl native_fn_02025a28
    mov r1, r0
    mov r0, #1056964608
    bl native_fn_02024e0c
    b ov000_0220bf50_L1f8
ov000_0220bf50_L1e4:
    bl native_fn_0203d294
    mov r0, r0, lsl #12
    bl native_fn_02025a28
    mov r1, #1056964608
    bl native_fn_02025ca4
ov000_0220bf50_L1f8:
    bl native_fn_020259b4
    str r0, [r5, #0x27c]
    mov r0, #10
    strb r0, [r5, #0x279]
    ldmia sp!, {r3, r4, r5, pc}
}
