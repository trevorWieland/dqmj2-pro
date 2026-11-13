/* ov001 row 0x021fae50: 412 bytes.
 *
 * What it does: 102 instructions; 8 call(s) to 0x021fad98, 0x02212adc, 0x021db438, +5 more; loops (back edge at +0x14); returns through pop {r4, r5, r6, r7, r8, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 8 calls (102 instructions, 8 calls, 16 branches, 7 back edges, 1 literal slot).
 *
 *   pool +0x198 -> constant 0x02239a14 (image word 0x02239a14)
 *   branch +0x10 -> +0x2c
 *   branch +0x38 -> +0x5c
 *   branch +0x48 -> +0x170
 *   branch +0x58 -> +0x170
 *   branch +0x60 -> +0x98
 *   branch +0x6c -> +0x84
 *   branch +0x80 -> +0x170
 *   branch +0x94 -> +0x170
 *   branch +0xa4 -> +0x170
 *   branch +0xb4 -> +0x170
 *   branch +0xbc -> +0x12c
 *   branch +0xe8 -> +0x110
 *   branch +0x100 -> +0x110
 *   back edge +0x118 -> +0xd0
 *   branch +0x128 -> +0x170
 *   branch +0x130 -> +0x170
 *   branch +0x17c -> +0x190
 *   test +0x0c cmp r0, #0
 *   test +0x34 cmp r0, #10
 *   test +0x44 cmp r0, #0
 *   test +0x5c cmp r0, #15
 *   test +0x68 cmp r0, #1000
 *   test +0x98 cmp r0, #20
 *   test +0xa8 cmp r0, #21
 *   test +0xb8 cmp r0, #30
 *   test +0xe4 cmp r0, #0
 *   test +0xfc cmp r0, #0
 *   test +0x114 cmp r8, #3
 *   test +0x12c cmp r0, #40
 *   test +0x164 cmp r1, #24
 *   test +0x178 cmp r1, #100
 *   0 block transfer(s), 15 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021fae50; the literal pool and
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

extern void native_fn_021fad98(void);
extern void native_fn_02212adc(void);
extern void ov001_side_slot_record_021db438(void);
extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_0205d718(void);
extern void native_fn_0205f210(void);
extern void native_fn_021d8cc8(void);


asm u32 native_ov001_021fae50 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    ldr r0, =0x02239a14
    ldrb r0, [r0, #0x12]
    cmp r0, #0
    bne ov001_021fae50_L2c
    bl native_fn_021fad98
    ldr r0, =0x02239a14
    mov r1, #0
    strb r1, [r0, #0x11]
    mov r1, #10
    strb r1, [r0, #0x12]
ov001_021fae50_L2c:
    ldr r1, =0x02239a14
    ldrb r0, [r1, #0x12]
    cmp r0, #10
    bne ov001_021fae50_L5c
    ldrsb r0, [r1, #16]
    bl native_fn_02212adc
    cmp r0, #0
    beq ov001_021fae50_L170
    ldr r0, =0x02239a14
    mov r1, #15
    strb r1, [r0, #0x12]
    b ov001_021fae50_L170
ov001_021fae50_L5c:
    cmp r0, #15
    bne ov001_021fae50_L98
    ldrsh r0, [r1, #38]
    cmp r0, #1000
    bge ov001_021fae50_L84
    mov r0, #20
    strb r0, [r1, #0x12]
    mov r0, #90
    strh r0, [r1, #40]
    b ov001_021fae50_L170
ov001_021fae50_L84:
    mov r0, #21
    strb r0, [r1, #0x12]
    mov r0, #15
    strh r0, [r1, #40]
    b ov001_021fae50_L170
ov001_021fae50_L98:
    cmp r0, #20
    moveq r0, #30
    streqb r0, [r1, #0x12]
    beq ov001_021fae50_L170
    cmp r0, #21
    moveq r0, #30
    streqb r0, [r1, #0x12]
    beq ov001_021fae50_L170
    cmp r0, #30
    bne ov001_021fae50_L12c
    mov r8, #0
    mov r5, r8
    mov r4, r8
    mov r7, r8
ov001_021fae50_Ld0:
    mov r0, r7
    mov r1, r8
    bl ov001_side_slot_record_021db438
    mov r6, r0
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_021fae50_L110
    add r0, r6, #768
    ldrsb r0, [r0, #88]
    bl native_fn_0205d718
    ldrb r0, [r6, #0x324]
    cmp r0, #0
    beq ov001_021fae50_L110
    mov r1, r5
    bl native_fn_0205f210
    strb r4, [r6, #0x324]
ov001_021fae50_L110:
    add r8, r8, #1
    cmp r8, #3
    blt ov001_021fae50_Ld0
    ldr r0, =0x02239a14
    mov r1, #40
    strb r1, [r0, #0x12]
    b ov001_021fae50_L170
ov001_021fae50_L12c:
    cmp r0, #40
    bne ov001_021fae50_L170
    ldrb r0, [r1, #0x11]
    add r3, r0, #1
    and r0, r3, #255
    add r2, r0, #7
    orr r0, r2, r2, lsl #5
    orr r0, r0, r2, lsl #10
    mov r0, r0, lsl #16
    mov r0, r0, lsr #16
    strb r3, [r1, #0x11]
    bl native_fn_021d8cc8
    ldr r0, =0x02239a14
    ldrb r1, [r0, #0x11]
    cmp r1, #24
    movhs r1, #100
    strhsb r1, [r0, #0x12]
ov001_021fae50_L170:
    ldr r0, =0x02239a14
    ldrb r1, [r0, #0x12]
    cmp r1, #100
    bne ov001_021fae50_L190
    mov r1, #0
    strb r1, [r0, #0x12]
    mov r1, #12
    strb r1, [r0, #0xa]
ov001_021fae50_L190:
    mov r0, #0
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
