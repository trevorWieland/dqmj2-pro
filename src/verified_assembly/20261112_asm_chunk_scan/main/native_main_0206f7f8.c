/* main row 0x0206f7f8: 832 bytes.
 *
 * What it does: Moves 2-register chunks between two pointers with writeback block moves (one load, 2 stores).
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x330 -> constant 0x021c5004 (image word 0x021c5004)
 *   pool +0x334 -> constant 0x021c4f60 (image word 0x021c4f60)
 *   pool +0x338 -> native_fn_02070134 (image word 0x02070134)
 *   pool +0x33c -> native_fn_020701cc (image word 0x020701cc)
 *   branch +0x24 -> +0x314
 *   branch +0x28 -> +0x3c
 *   branch +0x2c -> +0x98
 *   branch +0x30 -> +0xc4
 *   branch +0x34 -> +0x2ac
 *   branch +0x38 -> +0x278
 *   branch +0x58 -> +0x7c
 *   branch +0x78 -> +0x98
 *   branch +0xd0 -> +0x154
 *   back edge +0x128 -> +0xf8
 *   branch +0x160 -> +0x270
 *   branch +0x170 -> +0x270
 *   branch +0x184 -> +0x270
 *   branch +0x190 -> +0x1e4
 *   back edge +0x258 -> +0x24c
 *   branch +0x274 -> +0x314
 *   branch +0x288 -> +0x314
 *   branch +0x2a8 -> +0x314
 *   branch +0x2bc -> +0x310
 *   test +0x1c cmp r0, #4
 *   test +0x54 cmp r0, #0
 *   test +0xcc cmp r0, #0
 *   test +0x124 cmp r6, #8
 *   test +0x15c cmp r0, #0
 *   test +0x16c cmp r0, #42
 *   test +0x18c cmp r0, #0
 *   test +0x31c cmp r0, #42
 *   25 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x0206f7f8; the literal pool and
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

extern void native_fn_02061944(void);
extern void native_fn_0206df40(void);
extern void native_fn_02004140(void);
extern void native_fn_02008d78(void);
extern void native_fn_020040ec(void);
extern void native_fn_0206fc8c(void);
extern void native_fn_0206fbf8(void);
extern void native_fn_0206de44(void);
extern void native_fn_02062328(void);
extern void native_fn_02062144(void);
extern void native_fn_0206e11c(void);
extern void native_fn_0206e214(void);
extern void native_fn_0206e148(void);
extern void native_fn_02061dcc(void);
extern void native_fn_02049f4c(void);
extern void native_fn_0206ff40(void);
extern void native_fn_02045dec(void);
extern void native_fn_02070134(void);
extern void native_fn_020701cc(void);
extern void native_fn_0205fc10(void);
extern void native_fn_0205fd0c(void);
extern void native_fn_0206f79c(void);
extern void native_fn_020620b4(void);
extern void native_fn_02062358(void);
extern void native_fn_02045dc4(void);


asm u32 native_main_0206f7f8 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    sub sp, sp, #16
    bl native_fn_02061944
    mov r4, r0
    add r0, r4, #512
    ldrsb r0, [r0, #106]
    mov r5, #0
    cmp r0, #4
    addls pc, pc, r0, lsl #2
    b main_0206f7f8_L314
    b main_0206f7f8_L3c
    b main_0206f7f8_L98
    b main_0206f7f8_Lc4
    b main_0206f7f8_L2ac
    b main_0206f7f8_L278
main_0206f7f8_L3c:
    mov r0, #1
    strb r0, [r4, #0x26a]
    ldr r1, [r4, #0x25c]
    ldr r0, =0x021c5004
    str r1, [r0, #0xe0]
    bl native_fn_0206df40
    cmp r0, #0
    bne main_0206f7f8_L7c
    bl native_fn_02004140
    ldr r2, =0x021c5004
    mov r1, r5
    ldr r3, [r2, #0xe0]
    mov r2, #2400
    add r0, r0, r3
    bl native_fn_02008d78
    b main_0206f7f8_L98
main_0206f7f8_L7c:
    bl native_fn_020040ec
    ldr r2, =0x021c5004
    mov r1, r5
    ldr r3, [r2, #0xe0]
    mov r2, #2400
    add r0, r0, r3
    bl native_fn_02008d78
main_0206f7f8_L98:
    bl native_fn_0206fc8c
    bl native_fn_0206fbf8
    mov r1, #2
    mov r0, #1
    strb r1, [r4, #0x26a]
    bl native_fn_0206de44
    ldr r0, =0x021c4f60
    mov r1, #1
    str r1, [r0, #0xc]
    mov r1, #0
    str r1, [r0, #0x10]
main_0206f7f8_Lc4:
    ldr r0, =0x021c4f60
    ldrsb r0, [r0, #44]
    cmp r0, #0
    beq main_0206f7f8_L154
    bl native_fn_02062328
    add r0, r4, #512
    ldrsb r0, [r0, #111]
    mov r1, #0
    bl native_fn_02062144
    bl native_fn_0206e11c
    bl native_fn_0206e214
    bl native_fn_0206e148
    mov r6, #0
main_0206f7f8_Lf8:
    add r0, r6, #6
    mov r0, r0, lsl #24
    mov r7, r0, asr #24
    mov r0, r7
    bl native_fn_02061dcc
    bl native_fn_02049f4c
    mov r0, r7
    bl native_fn_0206ff40
    add r0, r6, #1
    mov r0, r0, lsl #24
    mov r6, r0, asr #24
    cmp r6, #8
    blt main_0206f7f8_Lf8
    mov r0, #0
    bl native_fn_0206de44
    ldr r1, =0x021c4f60
    mov r2, #1
    str r2, [r1, #0xc]
    ldr r0, =0x021c5004
    str r2, [r1, #0x10]
    ldrsb r1, [r0, #209]
    orr r1, r1, #8
    strb r1, [r0, #0xd1]
main_0206f7f8_L154:
    ldr r1, =0x021c4f60
    ldr r0, [r1, #0xc]
    cmp r0, #0
    beq main_0206f7f8_L270
    add r0, r4, #512
    ldrsb r0, [r0, #108]
    cmp r0, #42
    bne main_0206f7f8_L270
    ldr r0, =0x021c5004
    ldrsb r0, [r0, #209]
    mov r0, r0, lsl #31
    movs r0, r0, asr #31
    bne main_0206f7f8_L270
    ldr r0, [r1, #0x10]
    cmp r0, #0
    beq main_0206f7f8_L1e4
    mov r0, #5
    str r0, [sp]
    mov r6, #15
    mov r0, #0
    mov r1, #1
    mov r2, #26
    mov r3, #8
    str r6, [sp, #0x4]
    bl native_fn_02045dec
    mov r0, #5
    str r0, [sp]
    mov r0, #0
    mov r1, #2
    mov r2, #26
    mov r3, #8
    str r6, [sp, #0x4]
    bl native_fn_02045dec
    ldr r0, =0x021c4f60
    mov r1, #0
    str r1, [r0, #0x10]
main_0206f7f8_L1e4:
    ldr r0, =0x021c5004
    mov r3, #0
    strb r3, [r0, #0xd0]
    ldrsb r1, [r0, #209]
    mov r7, #18
    mov lr, #8192
    bic r1, r1, #1
    orr r1, r1, #1
    strb r1, [r0, #0xd1]
    ldrsb r2, [r0, #209]
    mov r12, #2
    ldr r1, =native_fn_02070134
    bic r2, r2, #2
    strb r2, [r0, #0xd1]
    ldrsb r8, [r0, #209]
    ldr r2, =native_fn_020701cc
    mov r6, #1
    bic r8, r8, #8
    strb r8, [r0, #0xd1]
    stmia sp, {r7, lr}
    str r12, [sp, #0x8]
    str r6, [sp, #0xc]
    bl native_fn_0205fc10
    ldr lr, =0x021c5004
    mov r6, r0
    mov r12, #13
main_0206f7f8_L24c:
    ldmia r6!, {r0, r1, r2, r3}
    stmia lr!, {r0, r1, r2, r3}
    subs r12, r12, #1
    bne main_0206f7f8_L24c
    ldr r0, =0x021c5004
    bl native_fn_0205fd0c
    ldr r0, =0x021c4f60
    mov r1, #0
    str r1, [r0, #0xc]
main_0206f7f8_L270:
    bl native_fn_0206f79c
    b main_0206f7f8_L314
main_0206f7f8_L278:
    ldr r0, =0x021c5004
    ldrsb r0, [r0, #209]
    mov r0, r0, lsl #31
    movs r0, r0, asr #31
    bne main_0206f7f8_L314
    ldr r0, =0x021c4f60
    ldrsb r0, [r0, #1]
    bl native_fn_020620b4
    ldr r0, =0x021c4f60
    ldrsb r0, [r0]
    bl native_fn_02062358
    mov r5, #1
    b main_0206f7f8_L314
main_0206f7f8_L2ac:
    ldr r0, =0x021c5004
    ldrsb r0, [r0, #209]
    mov r0, r0, lsl #31
    movs r0, r0, asr #31
    bne main_0206f7f8_L310
    mov r1, #5
    str r1, [sp]
    mov r12, #15
    mov r0, r5
    mov r1, #1
    mov r2, #26
    mov r3, #8
    str r12, [sp, #0x4]
    bl native_fn_02045dc4
    mov r0, #5
    str r0, [sp]
    mov r12, #15
    mov r0, r5
    mov r1, #2
    mov r2, #26
    mov r3, #8
    str r12, [sp, #0x4]
    bl native_fn_02045dc4
    mov r0, #2
    strb r0, [r4, #0x26a]
main_0206f7f8_L310:
    bl native_fn_0206f79c
main_0206f7f8_L314:
    add r0, r4, #512
    ldrsb r0, [r0, #108]
    cmp r0, #42
    movne r5, #1
    mov r0, r5
    add sp, sp, #16
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
