/* ov001 row 0x021ebecc: 368 bytes.
 *
 * What it does: 91 instructions; 10 call(s) to 0x0203d294, 0x021f949c, 0x021e9884, +7 more; loops (back edge at +0x24); returns through pop {r3, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 10 calls (91 instructions, 10 calls, 6 branches, 4 back edges, 1 literal slot).
 *
 *   pool +0x16c -> constant 0x02238d7c (image word 0x02238d7c)
 *   branch +0x10 -> +0xec
 *   branch +0x1c -> +0x60
 *   branch +0xa0 -> +0xe0
 *   branch +0xf8 -> +0x130
 *   branch +0x13c -> +0x164
 *   branch +0x150 -> +0x158
 *   test +0x0c cmp r1, #0
 *   test +0x18 cmp r0, #0
 *   test +0x28 cmp r0, #0
 *   test +0x50 cmp r0, #0
 *   test +0x9c cmp r0, #0
 *   test +0xf4 cmp r1, #10
 *   test +0x124 cmp r0, r2, asr #12
 *   test +0x138 cmp r1, #100
 *   test +0x14c cmp r0, #0
 *   0 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021ebecc; the literal pool and
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
extern void native_fn_021f949c(void);
extern void native_fn_021e9884(void);
extern void native_fn_021d9494(void);
extern void native_fn_021f1354(void);
extern void native_fn_021f1438(void);
extern void native_fn_02202528(void);
extern void native_fn_021d9534(void);
extern void native_fn_021f14e4(void);
extern void native_fn_021f14a4(void);


asm u32 native_ov001_021ebecc (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r0, =0x02238d7c
    ldrb r1, [r0, #0x7]
    cmp r1, #0
    bne ov001_021ebecc_Lec
    ldrb r0, [r0, #0xa]
    cmp r0, #0
    bne ov001_021ebecc_L60
    mov r0, #3
    bl native_fn_0203d294
    cmp r0, #0
    ldrne r0, =0x02238d7c
    movne r1, #2
    ldreq r0, =0x02238d7c
    moveq r1, #1
    strb r1, [r0, #0xa]
    ldr r0, =0x02238d7c
    mov r1, #1
    ldr r0, [r0, #0x60]
    ldrb r0, [r0, #0x31e]
    cmp r0, #0
    moveq r0, #221
    movne r0, #224
    bl native_fn_021f949c
ov001_021ebecc_L60:
    ldr r0, =0x02238d7c
    ldrb r0, [r0, #0xa]
    bl native_fn_021e9884
    ldr r0, =0x02238d7c
    mov r1, #1
    ldr r0, [r0, #0x60]
    mov r2, #0
    bl native_fn_021d9494
    ldr r2, =0x02238d7c
    ldr r0, [r2, #0x60]
    ldr r0, [r0, #0x60]
    ldr r0, [r0]
    mov r0, r0, asr #12
    strh r0, [r2, #46]
    ldrsh r0, [r2, #46]
    cmp r0, #0
    bne ov001_021ebecc_Le0
    ldrb r0, [r2, #0x19]
    mov r3, #1
    strb r0, [r2, #0x1f]
    ldrb r0, [r2, #0x1a]
    ldrb r1, [r2, #0x17]
    ldrh r2, [r2, #56]
    bl native_fn_021f1354
    ldr r0, =0x02238d7c
    ldrb r0, [r0, #0x29]
    bl native_fn_021f1438
    ldr r0, =0x02238d7c
    ldr r1, [r0, #0x60]
    ldrb r0, [r1, #0x31e]
    ldrb r1, [r1, #0x31f]
    bl native_fn_02202528
ov001_021ebecc_Le0:
    ldr r0, =0x02238d7c
    mov r1, #10
    strb r1, [r0, #0x7]
ov001_021ebecc_Lec:
    ldr r0, =0x02238d7c
    ldrb r1, [r0, #0x7]
    cmp r1, #10
    bne ov001_021ebecc_L130
    ldrsh r3, [r0, #46]
    ldr r0, [r0, #0x60]
    mvn r1, #0
    mov r2, #1
    bl native_fn_021d9534
    ldr r1, =0x02238d7c
    sub r0, r0, #5
    ldr r2, [r1, #0x60]
    ldr r2, [r2, #0x60]
    ldr r2, [r2]
    cmp r0, r2, asr #12
    moveq r0, #100
    streqb r0, [r1, #0x7]
ov001_021ebecc_L130:
    ldr r0, =0x02238d7c
    ldrb r1, [r0, #0x7]
    cmp r1, #100
    bne ov001_021ebecc_L164
    mov r1, #0
    strb r1, [r0, #0x7]
    bl native_fn_021f14e4
    cmp r0, #0
    beq ov001_021ebecc_L158
    bl native_fn_021f14a4
ov001_021ebecc_L158:
    ldr r0, =0x02238d7c
    mov r1, #8
    strb r1, [r0, #0x13]
ov001_021ebecc_L164:
    mov r0, #0
    ldmia sp!, {r3, pc}
}
