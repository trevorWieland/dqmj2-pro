/* ov001 row 0x02205d9c: 668 bytes.
 *
 * What it does: 167 instructions; 6 call(s) to 0x0205f98c, 0x02048a60, 0x02205ebc, +3 more; loops (back edge at +0x10); returns through pop {r3, r4, r5, pc}
 *
 * Decoded shape: loop with 6 calls (167 instructions, 6 calls, 32 branches, 4 back edges, 0 literal slots).
 *
 *   branch +0x24 -> +0x288
 *   branch +0x28 -> +0x3c
 *   branch +0x2c -> +0xe4
 *   branch +0x30 -> +0x130
 *   branch +0x34 -> +0x1bc
 *   branch +0x38 -> +0x218
 *   branch +0x54 -> +0x294
 *   branch +0x58 -> +0x294
 *   branch +0x5c -> +0x6c
 *   branch +0x60 -> +0x90
 *   branch +0x64 -> +0xac
 *   branch +0x68 -> +0xc8
 *   branch +0x8c -> +0x294
 *   branch +0xa8 -> +0x294
 *   branch +0xc4 -> +0x294
 *   branch +0xe0 -> +0x294
 *   branch +0xf0 -> +0x120
 *   branch +0x10c -> +0x294
 *   branch +0x11c -> +0x294
 *   branch +0x12c -> +0x294
 *   branch +0x140 -> +0x294
 *   branch +0x154 -> +0x190
 *   branch +0x168 -> +0x188
 *   branch +0x184 -> +0x294
 *   branch +0x1b8 -> +0x294
 *   branch +0x1c4 -> +0x204
 *   branch +0x1d8 -> +0x294
 *   branch +0x200 -> +0x294
 *   branch +0x214 -> +0x294
 *   branch +0x220 -> +0x274
 *   branch +0x234 -> +0x294
 *   branch +0x244 -> +0x25c
 *   branch +0x270 -> +0x294
 *   branch +0x284 -> +0x294
 *   test +0x1c cmp r1, #4
 *   test +0x4c cmp r1, #4
 *   test +0xec cmp r2, r1
 *   test +0x108 cmp r2, r0
 *   test +0x134 cmp r0, #0
 *   test +0x148 cmp r0, #0
 *   test +0x150 cmple r0, #0
 *   test +0x164 cmp r0, #0
 *   test +0x1c0 cmp r1, #0
 *   test +0x1cc cmp r0, #0
 *   test +0x1dc tst r1, #1
 *   test +0x21c cmp r1, #0
 *   test +0x228 cmp r0, #0
 *   test +0x238 tst r1, #1
 *   test +0x24c cmp r0, #0
 *   0 block transfer(s), 43 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02205d9c; the literal pool and
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

extern void native_fn_0205f98c(void);
extern void native_fn_02048a60(void);
extern void native_fn_02048a6c(void);


asm u32 native_ov001_02205d9c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    ldr r0, [r5, #0x1c]
    mov r1, #0
    bl native_fn_0205f98c
    ldr r1, [r5, #0x10]
    mov r4, r0
    cmp r1, #4
    addls pc, pc, r1, lsl #2
    b ov001_02205d9c_L288
    b ov001_02205d9c_L3c
    b ov001_02205d9c_Le4
    b ov001_02205d9c_L130
    b ov001_02205d9c_L1bc
    b ov001_02205d9c_L218
ov001_02205d9c_L3c:
    mov r2, #0
    strh r2, [r5, #24]
    strh r2, [r5, #26]
    ldr r1, [r5, #0x2c]
    cmp r1, #4
    addls pc, pc, r1, lsl #2
    b ov001_02205d9c_L294
    b ov001_02205d9c_L294
    b ov001_02205d9c_L6c
    b ov001_02205d9c_L90
    b ov001_02205d9c_Lac
    b ov001_02205d9c_Lc8
ov001_02205d9c_L6c:
    ldrsh r1, [r5, #20]
    sub r2, r2, #16
    bl native_fn_02048a60
    ldr r1, [r4, #0x7c]
    mov r0, #1
    orr r1, r1, #2
    str r1, [r4, #0x7c]
    str r0, [r5, #0x10]
    b ov001_02205d9c_L294
ov001_02205d9c_L90:
    mov r0, #1
    strb r0, [r5, #0x24]
    strh r2, [r5, #38]
    mov r0, #2
    str r0, [r5, #0x3c]
    str r0, [r5, #0x10]
    b ov001_02205d9c_L294
ov001_02205d9c_Lac:
    mov r0, #10
    strb r0, [r5, #0x24]
    mov r0, #1
    strh r0, [r5, #38]
    mov r0, #3
    str r0, [r5, #0x10]
    b ov001_02205d9c_L294
ov001_02205d9c_Lc8:
    mov r0, #2
    strb r0, [r5, #0x24]
    mov r0, #5
    strh r0, [r5, #38]
    mov r0, #4
    str r0, [r5, #0x10]
    b ov001_02205d9c_L294
ov001_02205d9c_Le4:
    ldrsh r2, [r5, #22]
    ldr r1, [r4, #0x70]
    cmp r2, r1
    ble ov001_02205d9c_L120
    mov r1, #0
    mov r2, #12
    bl native_fn_02048a6c
    ldrsh r2, [r5, #22]
    ldr r0, [r4, #0x70]
    cmp r2, r0
    bge ov001_02205d9c_L294
    ldrsh r1, [r5, #20]
    mov r0, r4
    bl native_fn_02048a60
    b ov001_02205d9c_L294
ov001_02205d9c_L120:
    mov r0, #0
    str r0, [r5, #0x2c]
    str r0, [r5, #0x10]
    b ov001_02205d9c_L294
ov001_02205d9c_L130:
    ldrsh r0, [r5, #38]
    cmp r0, #0
    subgt r0, r0, #1
    strgth r0, [r5, #38]
    bgt ov001_02205d9c_L294
    ldr r0, [r5, #0x3c]
    cmp r0, #0
    ldrlesh r0, [r5, #26]
    cmple r0, #0
    bgt ov001_02205d9c_L190
    mov r1, #0
    strh r1, [r5, #26]
    ldrsb r0, [r5, #36]
    cmp r0, #0
    ble ov001_02205d9c_L188
    sub r0, r0, #1
    strb r0, [r5, #0x24]
    mov r0, #6
    strh r0, [r5, #38]
    mov r0, #2
    str r0, [r5, #0x3c]
    b ov001_02205d9c_L294
ov001_02205d9c_L188:
    str r1, [r5, #0x2c]
    str r1, [r5, #0x10]
ov001_02205d9c_L190:
    ldrsh r1, [r5, #26]
    ldr r0, [r5, #0x3c]
    sub r0, r1, r0
    strh r0, [r5, #26]
    ldr r0, [r5, #0x3c]
    sub r0, r0, #1
    str r0, [r5, #0x3c]
    ldrsh r0, [r5, #38]
    add r0, r0, #2
    strh r0, [r5, #38]
    b ov001_02205d9c_L294
ov001_02205d9c_L1bc:
    ldrsb r1, [r5, #36]
    cmp r1, #0
    beq ov001_02205d9c_L204
    ldrsh r0, [r5, #38]
    cmp r0, #0
    subne r0, r0, #1
    strneh r0, [r5, #38]
    bne ov001_02205d9c_L294
    tst r1, #1
    movne r0, #1
    mvneq r0, #0
    strh r0, [r5, #24]
    ldrsb r1, [r5, #36]
    mov r0, #2
    sub r1, r1, #1
    strb r1, [r5, #0x24]
    strh r0, [r5, #38]
    b ov001_02205d9c_L294
ov001_02205d9c_L204:
    mov r0, #0
    str r0, [r5, #0x2c]
    str r0, [r5, #0x10]
    strh r0, [r5, #24]
    b ov001_02205d9c_L294
ov001_02205d9c_L218:
    ldrsb r1, [r5, #36]
    cmp r1, #0
    beq ov001_02205d9c_L274
    ldrsh r0, [r5, #38]
    cmp r0, #0
    subne r0, r0, #1
    strneh r0, [r5, #38]
    bne ov001_02205d9c_L294
    tst r1, #1
    movne r0, #0
    strneh r0, [r5, #24]
    bne ov001_02205d9c_L25c
    ldr r0, [r5, #0x30]
    cmp r0, #0
    moveq r0, #2
    mvnne r0, #1
    strh r0, [r5, #24]
ov001_02205d9c_L25c:
    ldrsb r1, [r5, #36]
    mov r0, #12
    sub r1, r1, #1
    strb r1, [r5, #0x24]
    strh r0, [r5, #38]
    b ov001_02205d9c_L294
ov001_02205d9c_L274:
    mov r0, #0
    strh r0, [r5, #24]
    str r0, [r5, #0x2c]
    str r0, [r5, #0x10]
    b ov001_02205d9c_L294
ov001_02205d9c_L288:
    mov r0, #0
    str r0, [r5, #0x2c]
    str r0, [r5, #0x10]
ov001_02205d9c_L294:
    mov r0, #0
    ldmia sp!, {r3, r4, r5, pc}
}
