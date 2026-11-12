/* main row 0x02071748: 992 bytes.
 *
 * What it does: Moves 4-register chunks between two pointers with writeback block moves (one load, one store).
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x3c8 -> constant 0x021c4f60 (image word 0x021c4f60)
 *   pool +0x3cc -> constant 0x021c50e8 (image word 0x021c50e8)
 *   pool +0x3d0 -> native_fn_02071d78 (image word 0x02071d78)
 *   pool +0x3d4 -> native_fn_02071fe4 (image word 0x02071fe4)
 *   pool +0x3d8 -> native_data_020de318 (image word 0x020de318)
 *   pool +0x3dc -> constant 0x021c4f62 (image word 0x021c4f62)
 *   branch +0x2c -> +0x390
 *   branch +0x30 -> +0x40
 *   branch +0x34 -> +0xa4
 *   branch +0x38 -> +0xe4
 *   branch +0x3c -> +0x30c
 *   branch +0x60 -> +0x84
 *   branch +0x80 -> +0x390
 *   branch +0xa0 -> +0x390
 *   back edge +0xd4 -> +0xbc
 *   branch +0xe0 -> +0x390
 *   branch +0xec -> +0x27c
 *   branch +0xfc -> +0x118
 *   branch +0x104 -> +0x118
 *   branch +0x13c -> +0x1d0
 *   branch +0x158 -> +0x220
 *   back edge +0x1c0 -> +0x1b4
 *   branch +0x1cc -> +0x220
 *   branch +0x1e4 -> +0x208
 *   back edge +0x21c -> +0x1dc
 *   back edge +0x258 -> +0x228
 *   branch +0x28c -> +0x2b0
 *   branch +0x298 -> +0x2b0
 *   branch +0x2ec -> +0x390
 *   branch +0x308 -> +0x390
 *   branch +0x31c -> +0x350
 *   branch +0x328 -> +0x390
 *   branch +0x34c -> +0x390
 *   branch +0x374 -> +0x390
 *   branch +0x39c -> +0x3bc
 *   branch +0x3b0 -> +0x3b8
 *   test +0x24 cmp r0, #3
 *   test +0x5c cmp r0, #0
 *   test +0xcc cmp r0, #7
 *   test +0xe8 cmp r0, #0
 *   test +0xf8 cmp r0, #0
 *   test +0x100 cmp r6, #0
 *   test +0x110 cmp r2, r0
 *   test +0x138 cmp r4, #0
 *   test +0x1e0 cmp r0, #0
 *   test +0x214 cmp r9, #7
 *   test +0x250 cmp r8, #5
 *   test +0x25c cmp r6, #0
 *   test +0x2cc cmp r0, #1
 *   test +0x2e8 cmp r1, r0
 *   test +0x370 cmp r0, #5
 *   test +0x398 cmp r0, #42
 *   20 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x02071748; the literal pool and
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
extern void native_fn_02071c9c(void);
extern void native_fn_0206df40(void);
extern void native_fn_02004140(void);
extern void native_fn_02008d78(void);
extern void native_fn_020040ec(void);
extern void native_fn_02071bc0(void);
extern void native_fn_0206de44(void);
extern void native_fn_02062328(void);
extern void native_fn_02062144(void);
extern void native_fn_0206e11c(void);
extern void native_fn_0206e214(void);
extern void native_fn_0206e148(void);
extern void native_fn_02071d78(void);
extern void native_fn_02071fe4(void);
extern void native_fn_0205fc10(void);
extern void native_fn_0205fd0c(void);
extern u8 native_data_020de318[];
extern void native_fn_0207211c(void);
extern void native_fn_02061dcc(void);
extern void native_fn_02049f4c(void);
extern void native_fn_020721b4(void);
extern void native_fn_0206de54(void);
extern void native_fn_0206238c(void);
extern void native_fn_020620b4(void);
extern void native_fn_02062358(void);
extern void native_fn_02071410(void);
extern void native_fn_020624b0(void);
extern void native_fn_02072030(void);


asm u32 native_main_02071748 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    sub sp, sp, #16
    bl native_fn_02061944
    mov r5, r0
    add r0, r5, #512
    ldrsb r0, [r0, #106]
    ldr r1, =0x021c4f60
    mov r7, #0
    ldr r6, [r1, #0x20]
    cmp r0, #3
    addls pc, pc, r0, lsl #2
    b main_02071748_L390
    b main_02071748_L40
    b main_02071748_La4
    b main_02071748_Le4
    b main_02071748_L30c
main_02071748_L40:
    bl native_fn_02071c9c
    mov r0, #1
    strb r0, [r5, #0x26a]
    ldr r1, [r5, #0x25c]
    ldr r0, =0x021c50e8
    str r1, [r0, #0xe0]
    bl native_fn_0206df40
    cmp r0, #0
    bne main_02071748_L84
    bl native_fn_02004140
    ldr r2, =0x021c50e8
    mov r1, r7
    ldr r3, [r2, #0xe0]
    mov r2, #4800
    add r0, r0, r3
    bl native_fn_02008d78
    b main_02071748_L390
main_02071748_L84:
    bl native_fn_020040ec
    ldr r2, =0x021c50e8
    mov r1, r7
    ldr r3, [r2, #0xe0]
    mov r2, #4800
    add r0, r0, r3
    bl native_fn_02008d78
    b main_02071748_L390
main_02071748_La4:
    bl native_fn_02071bc0
    mov r0, #2
    strb r0, [r5, #0x26a]
    ldr r2, =0x021c50e8
    mov r0, r7
    mov r1, r7
main_02071748_Lbc:
    add r0, r0, #1
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    strb r1, [r2, #0xd8]
    cmp r0, #7
    add r2, r2, #1
    blt main_02071748_Lbc
    mov r0, #1
    bl native_fn_0206de44
    b main_02071748_L390
main_02071748_Le4:
    ldrsb r0, [r1, #44]
    cmp r0, #0
    beq main_02071748_L27c
    ldrsb r0, [r1, #52]
    mov r4, #1
    cmp r0, #0
    bne main_02071748_L118
    cmp r6, #0
    beq main_02071748_L118
    ldr r2, [r6, #0x14]
    ldr r0, [r1, #0x30]
    cmp r2, r0
    moveq r4, r7
main_02071748_L118:
    bl native_fn_02062328
    add r0, r5, #512
    ldrsb r0, [r0, #111]
    mov r1, #0
    bl native_fn_02062144
    bl native_fn_0206e11c
    bl native_fn_0206e214
    bl native_fn_0206e148
    cmp r4, #0
    beq main_02071748_L1d0
    ldr r0, =0x021c50e8
    ldrsb r1, [r0, #209]
    mov r2, r1, lsl #31
    movs r2, r2, asr #31
    orrne r1, r1, #8
    strneb r1, [r0, #0xd1]
    bne main_02071748_L220
    bic r1, r1, #1
    mov r3, #0
    strb r3, [r0, #0xd0]
    orr r1, r1, #1
    strb r1, [r0, #0xd1]
    ldrsb r4, [r0, #209]
    mov r2, #18
    mov r1, #8192
    bic r4, r4, #2
    strb r4, [r0, #0xd1]
    str r2, [sp]
    str r1, [sp, #0x4]
    mov r4, #2
    str r4, [sp, #0x8]
    mov r4, #1
    ldr r1, =native_fn_02071d78
    ldr r2, =native_fn_02071fe4
    str r4, [sp, #0xc]
    bl native_fn_0205fc10
    ldr r8, =0x021c50e8
    mov r9, r0
    mov r4, #13
main_02071748_L1b4:
    ldmia r9!, {r0, r1, r2, r3}
    stmia r8!, {r0, r1, r2, r3}
    subs r4, r4, #1
    bne main_02071748_L1b4
    ldr r0, =0x021c50e8
    bl native_fn_0205fd0c
    b main_02071748_L220
main_02071748_L1d0:
    ldr r8, =0x021c50e8
    ldr r4, =native_data_020de318
    mov r9, #0
main_02071748_L1dc:
    ldrsb r0, [r8, #216]
    cmp r0, #0
    beq main_02071748_L208
    mov r1, r9, lsl #1
    add r2, r4, r9, lsl #1
    add r0, r9, #3
    mov r0, r0, lsl #24
    ldrsb r1, [r4, r1]
    ldrsb r2, [r2, #1]
    mov r0, r0, asr #24
    bl native_fn_0207211c
main_02071748_L208:
    add r0, r9, #1
    mov r0, r0, lsl #24
    mov r9, r0, asr #24
    cmp r9, #7
    add r8, r8, #1
    blt main_02071748_L1dc
main_02071748_L220:
    mov r4, #6
    mov r8, #0
main_02071748_L228:
    mov r0, r4
    bl native_fn_02061dcc
    bl native_fn_02049f4c
    mov r0, r4
    bl native_fn_020721b4
    add r0, r8, #1
    add r2, r4, #1
    mov r1, r0, lsl #24
    mov r0, r2, lsl #24
    mov r8, r1, asr #24
    cmp r8, #5
    mov r4, r0, asr #24
    blt main_02071748_L228
    cmp r6, #0
    ldrne r1, [r6, #0x14]
    ldrne r0, =0x021c4f60
    strne r1, [r0, #0x30]
    mov r0, #0
    bl native_fn_0206de54
    mov r0, #0
    bl native_fn_0206de44
main_02071748_L27c:
    ldr r0, =0x021c50e8
    ldrsb r1, [r0, #209]
    mov r2, r1, lsl #31
    movs r2, r2, asr #31
    beq main_02071748_L2b0
    mov r1, r1, lsl #29
    movs r1, r1, asr #31
    beq main_02071748_L2b0
    bl native_fn_0205fd0c
    ldr r0, =0x021c50e8
    ldrsb r1, [r0, #209]
    bic r1, r1, #4
    strb r1, [r0, #0xd1]
main_02071748_L2b0:
    ldr r0, =0x021c4f62
    mov r1, #1
    mov r2, #6
    bl native_fn_0206238c
    ldr r1, =0x021c4f60
    strb r0, [r1, #0x4]
    ldrsb r0, [r1, #4]
    cmp r0, #1
    movne r0, #0
    strneb r0, [r1, #0x4]
    ldr r1, =0x021c4f60
    add r0, r5, #512
    ldrsb r1, [r1, #2]
    ldrsb r0, [r0, #105]
    cmp r1, r0
    beq main_02071748_L390
    mov r1, #3
    ldr r0, =0x021c50e8
    strb r1, [r5, #0x26a]
    ldrsb r1, [r0, #209]
    bic r1, r1, #240
    strb r1, [r0, #0xd1]
    b main_02071748_L390
main_02071748_L30c:
    ldr r0, =0x021c50e8
    ldrsb r2, [r0, #209]
    mov r3, r2, lsl #31
    movs r3, r3, asr #31
    beq main_02071748_L350
    mov r1, r2, lsl #30
    movs r1, r1, asr #31
    bne main_02071748_L390
    bl native_fn_0205fd0c
    ldr r0, =0x021c50e8
    ldrsb r1, [r0, #209]
    bic r1, r1, #240
    strb r1, [r0, #0xd1]
    ldrsb r1, [r0, #209]
    bic r1, r1, #4
    strb r1, [r0, #0xd1]
    b main_02071748_L390
main_02071748_L350:
    ldrsb r0, [r1, #2]
    bl native_fn_020620b4
    ldr r0, =0x021c4f60
    ldrsb r0, [r0, #4]
    bl native_fn_02062358
    ldr r0, =0x021c4f60
    mov r7, #1
    ldrsb r0, [r0, #2]
    cmp r0, #5
    bne main_02071748_L390
    bl native_fn_02071410
    sub r0, r0, #1
    mov r0, r0, lsl #24
    mov r1, r0, asr #24
    mov r0, #5
    bl native_fn_020624b0
main_02071748_L390:
    add r0, r5, #512
    ldrsb r0, [r0, #108]
    cmp r0, #42
    beq main_02071748_L3bc
    ldr r0, =0x021c50e8
    ldrsb r0, [r0, #209]
    mov r0, r0, lsl #31
    movs r0, r0, asr #31
    beq main_02071748_L3b8
    bl native_fn_02072030
main_02071748_L3b8:
    mov r7, #1
main_02071748_L3bc:
    mov r0, r7
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
