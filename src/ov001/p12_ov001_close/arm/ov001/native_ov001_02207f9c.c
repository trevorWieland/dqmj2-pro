/* ov001 row 0x02207f9c: 380 bytes.
 *
 * What it does: 94 instructions; 18 call(s) to 0x0202a634, 0x02207938, 0x02208330, +15 more; loops (back edge at +0x04); returns through pop {r3, r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 18 calls (94 instructions, 18 calls, 18 branches, 12 back edges, 1 literal slot).
 *
 *   pool +0x178 -> constant 0x00000201 (image word 0x00000201)
 *   branch +0x28 -> +0x170
 *   branch +0x2c -> +0x48
 *   branch +0x30 -> +0x50
 *   branch +0x34 -> +0x88
 *   branch +0x38 -> +0x98
 *   branch +0x3c -> +0xec
 *   branch +0x40 -> +0xf4
 *   branch +0x44 -> +0x120
 *   branch +0x4c -> +0x170
 *   branch +0x84 -> +0x170
 *   branch +0x94 -> +0x170
 *   branch +0xa0 -> +0xb0
 *   branch +0xac -> +0xd8
 *   branch +0xd4 -> +0x170
 *   branch +0xe8 -> +0x170
 *   branch +0xf0 -> +0x170
 *   branch +0xfc -> +0x170
 *   branch +0x11c -> +0x170
 *   test +0x1c cmp r0, #6
 *   test +0x54 cmp r0, #2
 *   test +0x74 cmp r0, #0
 *   test +0x9c cmp r0, #0
 *   test +0xa8 tst r1, #2
 *   test +0xdc tst r1, r0
 *   test +0xf8 cmp r0, #1
 *   test +0x124 cmp r0, #1
 *   test +0x14c cmp r0, #0
 *   test +0x154 cmpne r0, #0
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02207f9c; the literal pool and
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

extern void native_fn_0202a634(void);
extern void native_fn_02207938(void);
extern void native_fn_02208330(void);
extern void native_fn_02208214(void);
extern void native_fn_022082a0(void);
extern void native_fn_02208408(void);
extern void native_fn_02208358(void);
extern void native_fn_02203418(void);
extern void native_fn_02041538(void);
extern void native_fn_021f949c(void);
extern void native_fn_02207db8(void);
extern void native_fn_02041814(void);
extern void native_fn_02045680(void);
extern void native_fn_02208210(void);
extern void native_fn_02202374(void);
extern void native_fn_0206d914(void);
extern void native_fn_021fefb0(void);


asm u32 native_ov001_02207f9c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    bl native_fn_0202a634
    mov r7, r0
    bl native_fn_02207938
    mov r4, r0
    ldr r0, [r4, #0x1c]
    ldr r5, [r4, #0x538]
    cmp r0, #6
    mov r6, #0
    addls pc, pc, r0, lsl #2
    b ov001_02207f9c_L170
    b ov001_02207f9c_L48
    b ov001_02207f9c_L50
    b ov001_02207f9c_L88
    b ov001_02207f9c_L98
    b ov001_02207f9c_Lec
    b ov001_02207f9c_Lf4
    b ov001_02207f9c_L120
ov001_02207f9c_L48:
    bl native_fn_02208330
    b ov001_02207f9c_L170
ov001_02207f9c_L50:
    ldr r0, [r4, #0x20]
    cmp r0, #2
    moveq r0, #1
    movne r0, r6
    bl native_fn_02208214
    bl native_fn_022082a0
    ldr r0, [r4, #0x20]
    bl native_fn_02208408
    ldr r0, [r4, #0x20]
    cmp r0, #0
    movne r0, #3
    moveq r0, #2
    str r0, [r4, #0x1c]
    b ov001_02207f9c_L170
ov001_02207f9c_L88:
    bl native_fn_02208358
    mov r0, #3
    str r0, [r4, #0x1c]
    b ov001_02207f9c_L170
ov001_02207f9c_L98:
    bl native_fn_02203418
    cmp r0, #0
    bne ov001_02207f9c_Lb0
    ldrh r1, [r7, #2]
    tst r1, #2
    beq ov001_02207f9c_Ld8
ov001_02207f9c_Lb0:
    mov r0, #1
    mov r1, #2
    mov r2, #10
    bl native_fn_02041538
    mov r0, #83
    mov r1, #1
    bl native_fn_021f949c
    mov r0, #5
    str r0, [r4, #0x1c]
    b ov001_02207f9c_L170
ov001_02207f9c_Ld8:
    ldr r0, =0x00000201
    tst r1, r0
    movne r0, #4
    strne r0, [r4, #0x1c]
    b ov001_02207f9c_L170
ov001_02207f9c_Lec:
    bl native_fn_02207db8
    b ov001_02207f9c_L170
ov001_02207f9c_Lf4:
    bl native_fn_02041814
    cmp r0, #1
    beq ov001_02207f9c_L170
    mov r0, #2
    bl native_fn_02045680
    mov r0, #1
    bl native_fn_02045680
    bl native_fn_02208210
    mov r0, #6
    str r0, [r4, #0x1c]
    b ov001_02207f9c_L170
ov001_02207f9c_L120:
    ldr r0, [r4, #0x24]
    cmp r0, #1
    moveq r6, #127
    movne r6, #6
    bl native_fn_02202374
    ldrsb r1, [r5, #12]
    and r2, r6, #255
    bl native_fn_0206d914
    ldr r1, [r4, #0x10]
    mov r2, #0
    ldrb r0, [r1, #0x31c]
    cmp r0, #0
    ldrneb r0, [r1, #0x1ff]
    cmpne r0, #0
    add r0, r1, #768
    ldrsb r0, [r0, #30]
    ldrsb r1, [r5, #12]
    movne r2, #1
    bl native_fn_021fefb0
    mov r6, #1
ov001_02207f9c_L170:
    mov r0, r6
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
