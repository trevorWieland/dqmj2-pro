/* ov006 row 0x021d85d4: 672 bytes.
 *
 * What it does: 167 instructions; 41 call(s) to 0x02063eec, 0x020642dc, 0x02067bd4, +38 more; loops (back edge at +0x04); returns through pop {r4, r5, r6, r7, r8, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x29c -> constant 0x0220f2f4 (image word 0x0220f2f4)
 *   branch +0x20 -> +0x38
 *   branch +0x28 -> +0x160
 *   branch +0x30 -> +0x290
 *   branch +0x34 -> +0x188
 *   branch +0x5c -> +0x128
 *   branch +0x124 -> +0x290
 *   branch +0x15c -> +0x290
 *   branch +0x184 -> +0x290
 *   branch +0x198 -> +0x1c0
 *   branch +0x1bc -> +0x288
 *   branch +0x1fc -> +0x268
 *   branch +0x228 -> +0x258
 *   back edge +0x264 -> +0x208
 *   test +0x1c cmp r0, #34
 *   test +0x24 cmp r0, #35
 *   test +0x2c cmp r0, #36
 *   test +0x58 cmp r0, #0
 *   test +0x194 cmp r0, #0
 *   test +0x1f8 cmp r0, #0
 *   test +0x224 cmp r1, #0
 *   test +0x260 cmp r5, r0
 *   0 block transfer(s), 14 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021d85d4; the literal pool and
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

extern void native_fn_02063eec(void);
extern void native_fn_020642dc(void);
extern void native_fn_02067bd4(void);
extern void native_fn_02048034(void);
extern void native_fn_020653d0(void);
extern void native_fn_021de228(void);
extern void native_fn_02067ab8(void);
extern void native_fn_02067b48(void);
extern void native_fn_021ded5c(void);
extern void native_fn_021def28(void);
extern void native_fn_021d85b8(void);
extern void native_fn_021da15c(void);
extern void native_fn_02067ad0(void);
extern void native_fn_02067ac8(void);
extern void native_fn_021df974(void);
extern void native_fn_021dff30(void);
extern void native_fn_02063ee0(void);
extern void native_fn_02067b58(void);
extern void native_fn_02008d78(void);
extern void native_fn_02062aa0(void);
extern void native_fn_02067af4(void);
extern void native_fn_02062a50(void);
extern void native_fn_02008e0c(void);
extern void native_fn_02067e54(void);
extern void native_fn_020642cc(void);


asm u32 native_ov006_021d85d4 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    bl native_fn_02063eec
    ldr r1, =0x0220f2f4
    mov r2, #0
    str r0, [r1, #0x4]
    str r2, [r1, #0x10]
    bl native_fn_020642dc
    cmp r0, #34
    beq ov006_021d85d4_L38
    cmp r0, #35
    beq ov006_021d85d4_L160
    cmp r0, #36
    beq ov006_021d85d4_L290
    b ov006_021d85d4_L188
ov006_021d85d4_L38:
    ldr r0, =0x0220f2f4
    ldr r0, [r0, #0x4]
    ldrb r0, [r0]
    bl native_fn_02067bd4
    add r0, r0, #20
    mov r1, #0
    bl native_fn_02048034
    bl native_fn_020653d0
    cmp r0, #0
    bne ov006_021d85d4_L128
    ldr r1, =0x0220f2f4
    mov r0, #48
    ldr r4, [r1, #0x4]
    mov r3, #1
    ldrb r2, [r4]
    mla r0, r2, r0, r4
    str r3, [r0, #0x34]
    ldr r0, [r1, #0x4]
    ldrb r0, [r0]
    bl native_fn_021de228
    ldr r1, =0x0220f2f4
    ldr r2, [r1, #0x4]
    ldrh r1, [r2, #6]
    add r0, r1, r0
    strh r0, [r2, #6]
    bl native_fn_02067ab8
    ldr r1, =0x0220f2f4
    ldr r2, [r1, #0x4]
    ldrh r1, [r2, #4]
    add r0, r1, r0
    strh r0, [r2, #4]
    bl native_fn_02067b48
    ldr r1, =0x0220f2f4
    ldr r3, [r1, #0x4]
    ldr r2, [r3, #0x8]
    add r0, r2, r0
    str r0, [r3, #0x8]
    ldr r4, [r1, #0x4]
    ldrb r0, [r4]
    bl native_fn_021de228
    ldrb r3, [r4]
    mov r1, #48
    ldr r2, =0x0220f2f4
    mla r1, r3, r1, r4
    strh r0, [r1, #62]
    ldr r4, [r2, #0x4]
    bl native_fn_02067ab8
    ldrb r3, [r4]
    mov r2, #48
    mov r1, #4
    mla r2, r3, r2, r4
    strh r0, [r2, #60]
    mov r0, #15
    mov r2, #92
    bl native_fn_021ded5c
    mov r0, #1
    bl native_fn_021def28
    mov r0, #22
    bl native_fn_021d85b8
    b ov006_021d85d4_L290
ov006_021d85d4_L128:
    ldr r0, =0x0220f2f4
    mov r2, #48
    ldr r3, [r0, #0x4]
    mov r5, #0
    ldrb r4, [r3]
    mov r0, #15
    mov r1, #4
    mla r3, r4, r2, r3
    mov r2, #93
    str r5, [r3, #0x34]
    bl native_fn_021ded5c
    mov r0, #23
    bl native_fn_021d85b8
    b ov006_021d85d4_L290
ov006_021d85d4_L160:
    bl native_fn_021da15c
    mov r0, #15
    mov r1, #4
    mov r2, #148
    bl native_fn_021ded5c
    mov r0, #1
    bl native_fn_021def28
    mov r0, #31
    bl native_fn_021d85b8
    b ov006_021d85d4_L290
ov006_021d85d4_L188:
    ldr r0, =0x0220f2f4
    ldr r0, [r0, #0x4]
    ldrb r0, [r0]
    cmp r0, #0
    beq ov006_021d85d4_L1c0
    bl native_fn_02067ad0
    mov r4, r0
    bl native_fn_02067ac8
    mov r3, r0
    mov r2, r4
    mov r0, #1
    mov r1, #2
    bl native_fn_021df974
    b ov006_021d85d4_L288
ov006_021d85d4_L1c0:
    bl native_fn_021dff30
    bl native_fn_02063ee0
    mov r4, r0
    bl native_fn_02067b58
    ldr r0, [r0, #0x24]
    str r0, [r4]
    bl native_fn_02067ac8
    mov r4, r0
    bl native_fn_02067ad0
    mov r2, r4
    mov r1, #0
    bl native_fn_02008d78
    mov r5, #0
    bl native_fn_02062aa0
    cmp r0, #0
    ble ov006_021d85d4_L268
    mov r7, #132
    mov r6, r5
ov006_021d85d4_L208:
    mov r0, r5
    bl native_fn_02067af4
    mov r4, r0
    mov r0, r5
    bl native_fn_02062a50
    mov r8, r0
    ldr r1, [r8, #0x14]
    cmp r1, #0
    beq ov006_021d85d4_L258
    mov r1, r4
    mov r2, r7
    bl native_fn_02008e0c
    mov r0, r8
    bl native_fn_02067e54
    strh r0, [r4, #62]
    strb r6, [r4, #0x31]
    ldrsh r0, [r4, #32]
    strh r0, [r4, #36]
    ldrsh r0, [r4, #34]
    strh r0, [r4, #38]
ov006_021d85d4_L258:
    add r5, r5, #1
    bl native_fn_02062aa0
    cmp r5, r0
    blt ov006_021d85d4_L208
ov006_021d85d4_L268:
    bl native_fn_02067ad0
    mov r4, r0
    bl native_fn_02067ac8
    mov r3, r0
    mov r0, #2
    mov r1, r0
    mov r2, r4
    bl native_fn_021df974
ov006_021d85d4_L288:
    mov r0, #0
    bl native_fn_021d85b8
ov006_021d85d4_L290:
    mov r0, #0
    bl native_fn_020642cc
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
