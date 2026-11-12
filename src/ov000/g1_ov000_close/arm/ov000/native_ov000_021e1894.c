/* ov000 row 0x021e1894: 928 bytes.
 *
 * What it does: 227 instructions; 33 call(s) to 0x021e0ff0, 0x021e1658, 0x021e0e2c, +30 more; loops (back edge at +0x10); returns through pop {r3, r4, r5, pc}; 5 literal slot(s) in the extent
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x38c -> constant 0x022322d4 (image word 0x022322d4)
 *   pool +0x390 -> constant 0x02232344 (image word 0x02232344)
 *   pool +0x394 -> constant 0x0223244c (image word 0x0223244c)
 *   pool +0x398 -> constant 0x02232458 (image word 0x02232458)
 *   pool +0x39c -> native_data_0222ebec (image word 0x0222ebec)
 *   branch +0x18 -> +0x378
 *   branch +0x28 -> +0x260
 *   branch +0x34 -> +0x250
 *   branch +0x4c -> +0x60
 *   branch +0x54 -> +0x60
 *   branch +0x74 -> +0xe0
 *   branch +0xfc -> +0x158
 *   branch +0x164 -> +0x224
 *   branch +0x17c -> +0x224
 *   branch +0x1ec -> +0x208
 *   branch +0x204 -> +0x21c
 *   branch +0x228 -> +0x234
 *   branch +0x24c -> +0x374
 *   branch +0x25c -> +0x374
 *   branch +0x27c -> +0x2e8
 *   branch +0x304 -> +0x360
 *   branch +0x364 -> +0x370
 *   test +0x14 cmp r0, #0
 *   test +0x24 cmp r1, #0
 *   test +0x30 cmp r0, #1
 *   test +0x38 cmp r4, #0
 *   test +0x48 cmp r0, #0
 *   test +0x50 cmp r4, #0
 *   test +0x70 cmp r0, #0
 *   test +0xf8 cmp r0, #0
 *   test +0x160 cmp r1, #6
 *   test +0x178 cmp r0, #0
 *   test +0x1e8 cmp r0, #0
 *   test +0x224 cmp r4, #0
 *   test +0x268 cmp r4, #0
 *   test +0x278 cmp r0, #0
 *   test +0x300 cmp r0, #0
 *   test +0x360 cmp r5, #0
 *   20 block transfer(s), 18 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e1894; the literal pool and
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

extern void native_fn_021e0ff0(void);
extern void native_fn_021e1658(void);
extern void native_fn_021e0e2c(void);
extern void native_fn_021e4388(void);
extern void native_fn_021e1c4c(void);
extern void native_fn_020404f0(void);
extern void native_fn_021e74e8(void);
extern void native_fn_021e7510(void);
extern void native_fn_021e44a8(void);
extern void native_fn_021e4a48(void);
extern u8 native_data_0222ebec[];
extern void native_fn_021d8c80(void);
extern void native_fn_021e339c(void);
extern void native_fn_021d84e8(void);
extern void native_fn_021e10d4(void);
extern void native_fn_021e176c(void);
extern void native_fn_021e1dfc(void);
extern void native_fn_021e182c(void);
extern void native_fn_02042be8(void);


asm u32 native_ov000_021e1894 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    sub sp, sp, #64
    mov r4, r0
    mov r5, #1
    bl native_fn_021e0ff0
    cmp r0, #0
    bne ov000_021e1894_L378
    ldr r0, =0x022322d4
    ldrb r1, [r0, #0x27e]
    cmp r1, #0
    beq ov000_021e1894_L260
    ldrb r0, [r0, #0x278]
    cmp r0, #1
    beq ov000_021e1894_L250
    cmp r4, #0
    moveq r4, r5
    movne r4, #0
    bl native_fn_021e1658
    cmp r0, #0
    beq ov000_021e1894_L60
    cmp r4, #0
    bne ov000_021e1894_L60
    bl native_fn_021e0e2c
    mov r4, r0
ov000_021e1894_L60:
    ldr r0, =0x02232344
    add r2, sp, #12
    mov r1, #0
    bl native_fn_021e4388
    cmp r0, #0
    beq ov000_021e1894_Le0
    mov r0, #0
    str r0, [sp]
    ldrsh r1, [sp, #58]
    mov r0, #2
    str r1, [sp, #0x4]
    ldrsh r1, [sp, #60]
    str r1, [sp, #0x8]
    ldrsb r1, [sp, #47]
    ldrsb r2, [sp, #51]
    ldrb r3, [sp, #0x35]
    bl native_fn_021e1c4c
    add r0, sp, #12
    ldr r3, =0x0223244c
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    add r0, sp, #24
    ldr r3, =0x02232458
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    mov r0, #11
    bl native_fn_020404f0
    ldrb r0, [sp, #0x37]
    bl native_fn_021e74e8
    add r0, sp, #12
    bl native_fn_021e7510
    mov r4, #1
ov000_021e1894_Le0:
    ldr r1, =0x022322d4
    ldr r0, =0x02232344
    ldr r2, [r1, #0x8c]
    add r3, sp, #12
    mov r1, #1
    bl native_fn_021e44a8
    cmp r0, #0
    beq ov000_021e1894_L158
    mov r0, #0
    str r0, [sp]
    ldrsh r1, [sp, #58]
    mov r0, #2
    str r1, [sp, #0x4]
    ldrsh r1, [sp, #60]
    str r1, [sp, #0x8]
    ldrsb r1, [sp, #47]
    ldrsb r2, [sp, #51]
    ldrb r3, [sp, #0x35]
    bl native_fn_021e1c4c
    add r0, sp, #12
    ldr r3, =0x0223244c
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    add r0, sp, #24
    ldr r3, =0x02232458
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    mov r0, #35
    bl native_fn_020404f0
    mov r4, #1
ov000_021e1894_L158:
    ldr r0, =0x022322d4
    ldrb r1, [r0, #0x278]
    cmp r1, #6
    beq ov000_021e1894_L224
    add r2, sp, #12
    mov r1, #2
    mov r3, #1
    bl native_fn_021e4a48
    cmp r0, #0
    beq ov000_021e1894_L224
    ldr r1, =native_data_0222ebec
    mov r0, #1
    strb r0, [r1]
    bl native_fn_021d8c80
    mov r0, #0
    str r0, [sp]
    ldrsh r1, [sp, #58]
    mov r0, #6
    str r1, [sp, #0x4]
    ldrsh r1, [sp, #60]
    str r1, [sp, #0x8]
    ldrsb r1, [sp, #47]
    ldrsb r2, [sp, #51]
    ldrb r3, [sp, #0x35]
    bl native_fn_021e1c4c
    add r0, sp, #12
    ldr r3, =0x0223244c
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    add r0, sp, #24
    ldr r3, =0x02232458
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    bl native_fn_021e339c
    ldrsb r0, [sp, #44]
    mov r1, #0
    cmp r0, #0
    bne ov000_021e1894_L208
    ldr r0, [sp, #0x1c]
    add r0, r0, #245760
    bl native_fn_021d84e8
    ldr r0, =0x022322d4
    mov r1, #8
    b ov000_021e1894_L21c
ov000_021e1894_L208:
    ldr r0, [sp, #0x1c]
    sub r0, r0, #245760
    bl native_fn_021d84e8
    ldr r0, =0x022322d4
    mov r1, #7
ov000_021e1894_L21c:
    strb r1, [r0, #0x1e0]
    mov r4, #1
ov000_021e1894_L224:
    cmp r4, #0
    bne ov000_021e1894_L234
    bl native_fn_021e10d4
    mov r4, r0
ov000_021e1894_L234:
    bl native_fn_021e176c
    ldr r0, =0x022322d4
    mov r5, r4
    ldrb r1, [r0, #0x161]
    add r1, r1, #1
    strb r1, [r0, #0x161]
    b ov000_021e1894_L374
ov000_021e1894_L250:
    bl native_fn_021e176c
    bl native_fn_021e1dfc
    mov r5, r4
    b ov000_021e1894_L374
ov000_021e1894_L260:
    ldr r0, =0x02232344
    add r2, sp, #12
    cmp r4, #0
    mov r1, #0
    movne r5, #0
    bl native_fn_021e4388
    cmp r0, #0
    beq ov000_021e1894_L2e8
    mov r0, #0
    str r0, [sp]
    ldrsh r1, [sp, #58]
    mov r0, #2
    str r1, [sp, #0x4]
    ldrsh r1, [sp, #60]
    str r1, [sp, #0x8]
    ldrsb r1, [sp, #47]
    ldrsb r2, [sp, #51]
    ldrb r3, [sp, #0x35]
    bl native_fn_021e1c4c
    add r0, sp, #12
    ldr r3, =0x0223244c
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    add r0, sp, #24
    ldr r3, =0x02232458
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    mov r0, #11
    bl native_fn_020404f0
    ldrb r0, [sp, #0x37]
    bl native_fn_021e74e8
    add r0, sp, #12
    bl native_fn_021e7510
    mov r5, #1
ov000_021e1894_L2e8:
    ldr r1, =0x022322d4
    ldr r0, =0x02232344
    ldr r2, [r1, #0x8c]
    add r3, sp, #12
    mov r1, #1
    bl native_fn_021e44a8
    cmp r0, #0
    beq ov000_021e1894_L360
    mov r0, #0
    str r0, [sp]
    ldrsh r1, [sp, #58]
    mov r0, #2
    str r1, [sp, #0x4]
    ldrsh r1, [sp, #60]
    str r1, [sp, #0x8]
    ldrsb r1, [sp, #47]
    ldrsb r2, [sp, #51]
    ldrb r3, [sp, #0x35]
    bl native_fn_021e1c4c
    add r0, sp, #12
    ldr r3, =0x0223244c
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    add r0, sp, #24
    ldr r3, =0x02232458
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    mov r0, #35
    bl native_fn_020404f0
    mov r5, #1
ov000_021e1894_L360:
    cmp r5, #0
    bne ov000_021e1894_L370
    bl native_fn_021e10d4
    mov r5, r0
ov000_021e1894_L370:
    bl native_fn_021e176c
ov000_021e1894_L374:
    bl native_fn_021e182c
ov000_021e1894_L378:
    ldr r0, =0x022322d4
    bl native_fn_02042be8
    mov r0, r5
    add sp, sp, #64
    ldmia sp!, {r3, r4, r5, pc}
}
