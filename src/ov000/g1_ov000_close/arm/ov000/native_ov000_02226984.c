/* ov000 row 0x02226984: 372 bytes.
 *
 * What it does: 91 instructions; 19 call(s) to 0x0202a634, 0x0206c0b0, 0x0206c0e0, +16 more; loops (back edge at +0x1c); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x16c -> constant 0x022468b8 (image word 0x022468b8)
 *   pool +0x170 -> native_data_0222feb4 (image word 0x0222feb4)
 *   branch +0x2c -> +0x68
 *   branch +0x38 -> +0x60
 *   branch +0x44 -> +0x60
 *   branch +0x50 -> +0x60
 *   branch +0x5c -> +0x68
 *   branch +0x7c -> +0x138
 *   branch +0x8c -> +0x130
 *   branch +0x98 -> +0x130
 *   branch +0xb4 -> +0x128
 *   branch +0xc0 -> +0xd0
 *   branch +0xcc -> +0xd8
 *   branch +0xd4 -> +0x13c
 *   branch +0xec -> +0x13c
 *   branch +0x124 -> +0x13c
 *   branch +0x12c -> +0x13c
 *   branch +0x134 -> +0x13c
 *   branch +0x140 -> +0x164
 *   test +0x28 cmp r1, #3
 *   test +0x34 cmp r0, #0
 *   test +0x40 cmp r0, #0
 *   test +0x4c cmp r0, #0
 *   test +0x58 cmp r0, #0
 *   test +0x74 tst r0, #4
 *   test +0x88 cmp r0, #0
 *   test +0x94 cmp r0, #3
 *   test +0xb0 cmp r0, #3
 *   test +0xbc cmp r0, #0
 *   test +0xc8 cmp r0, #0
 *   test +0xe4 cmp r0, #0
 *   test +0x13c cmp r9, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02226984; the literal pool and
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

extern u8 native_data_0222feb4[];
extern void native_fn_0202a634(void);
extern void native_fn_0206c0b0(void);
extern void native_fn_0206c0e0(void);
extern void native_fn_020c17b0(void);
extern void native_fn_020c15f8(void);
extern void native_fn_02049ae4(void);
extern void native_fn_020c8fdc(void);
extern void native_fn_020c8ee4(void);
extern void native_fn_0206c130(void);
extern void native_fn_020c1830(void);
extern void native_fn_020c1708(void);
extern void native_fn_0206be2c(void);
extern void native_fn_0206bf34(void);
extern void native_fn_02062a10(void);
extern void native_fn_0206dcd0(void);
extern void native_fn_01ffb388(void);
extern void native_fn_02068f60(void);
extern void native_fn_020caf9c(void);
extern void native_fn_01ffb2c8(void);


asm u32 native_ov000_02226984 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    ldr r0, =0x022468b8
    ldr r6, =native_data_0222feb4
    ldrsb r0, [r0, #24]
    mov r5, #0
    mov r9, #1
    add r4, r0, r0, lsl #2
    bl native_fn_0202a634
    ldrsb r1, [r6, r4]
    mov r4, r0
    cmp r1, #3
    bne ov000_02226984_L68
    bl native_fn_0206c0b0
    cmp r0, #0
    bne ov000_02226984_L60
    bl native_fn_0206c0e0
    cmp r0, #0
    bne ov000_02226984_L60
    bl native_fn_020c17b0
    cmp r0, #0
    bne ov000_02226984_L60
    bl native_fn_020c15f8
    cmp r0, #0
    beq ov000_02226984_L68
ov000_02226984_L60:
    mov r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
ov000_02226984_L68:
    ldrh r0, [r4, #2]
    mov r6, #16
    mov r7, #8
    tst r0, #4
    mov r8, #0
    beq ov000_02226984_L138
    bl native_fn_02049ae4
    ldr r0, [r0, #0x4]
    cmp r0, #0
    bne ov000_02226984_L130
    bl native_fn_020c8fdc
    cmp r0, #3
    bne ov000_02226984_L130
    bl native_fn_020c8ee4
    ldr r1, =0x022468b8
    mov r4, r0
    ldrsb r0, [r1, #24]
    mov r6, #5
    cmp r0, #3
    bne ov000_02226984_L128
    bl native_fn_0206c130
    cmp r0, #0
    bne ov000_02226984_Ld0
    bl native_fn_020c1830
    cmp r0, #0
    bne ov000_02226984_Ld8
ov000_02226984_Ld0:
    mov r9, #0
    b ov000_02226984_L13c
ov000_02226984_Ld8:
    mov r0, r4
    mov r7, #6
    bl native_fn_020c1708
    cmp r0, #0
    moveq r9, r8
    beq ov000_02226984_L13c
    ldr r0, [r4]
    add r0, r0, #26
    mov r0, r0, lsl #16
    mov r8, r0, lsr #16
    bl native_fn_0206be2c
    bl native_fn_0206bf34
    bl native_fn_02062a10
    bl native_fn_0206dcd0
    mov r0, #1
    bl native_fn_01ffb388
    mov r0, #0
    bl native_fn_02068f60
    bl native_fn_020caf9c
    b ov000_02226984_L13c
ov000_02226984_L128:
    mov r9, r8
    b ov000_02226984_L13c
ov000_02226984_L130:
    mov r9, #0
    b ov000_02226984_L13c
ov000_02226984_L138:
    mov r9, r8
ov000_02226984_L13c:
    cmp r9, #0
    beq ov000_02226984_L164
    mov r4, #1
    mov r0, r6
    mov r1, r7
    mov r2, r8
    mov r3, #0
    str r4, [sp]
    bl native_fn_01ffb2c8
    mov r5, r4
ov000_02226984_L164:
    mov r0, r5
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
