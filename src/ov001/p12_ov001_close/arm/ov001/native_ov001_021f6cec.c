/* ov001 row 0x021f6cec: 420 bytes.
 *
 * What it does: 103 instructions; 12 call(s) to 0x021f69a0, 0x021f2120, 0x021f2120, +9 more; loops (back edge at +0x30); returns through pop {r3, r4, r5, r6, r7, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 12 calls (103 instructions, 12 calls, 11 branches, 10 back edges, 2 literal slots).
 *
 *   pool +0x19c -> constant 0x0223989c (image word 0x0223989c)
 *   pool +0x1a0 -> constant 0x022398f0 (image word 0x022398f0)
 *   branch +0x28 -> +0xe4
 *   branch +0x40 -> +0x70
 *   branch +0x9c -> +0xc0
 *   back edge +0xc8 -> +0x78
 *   branch +0xe0 -> +0x194
 *   branch +0xe8 -> +0x130
 *   branch +0x100 -> +0x194
 *   branch +0x12c -> +0x194
 *   branch +0x134 -> +0x160
 *   branch +0x14c -> +0x194
 *   branch +0x15c -> +0x194
 *   branch +0x164 -> +0x194
 *   branch +0x180 -> +0x194
 *   test +0x10 cmp r0, #0
 *   test +0x24 cmp r1, #0
 *   test +0x3c cmp r0, #0
 *   test +0x8c cmp r0, #0
 *   test +0x98 cmpne r0, #0
 *   test +0xc4 cmp r7, #3
 *   test +0xe4 cmp r1, #5
 *   test +0xfc cmp r1, #30
 *   test +0x118 cmp r0, #0
 *   test +0x130 cmp r1, #10
 *   test +0x148 cmp r0, #0
 *   test +0x160 cmp r1, #100
 *   test +0x174 cmp r1, #0
 *   0 block transfer(s), 13 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f6cec; the literal pool and
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

extern void native_fn_021f69a0(void);
extern void native_fn_021f2120(void);
extern void ov001_side_slot_record_021db438(void);
extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_0205d790(void);
extern void ov001_effect_resource_create_021eec7c(void);
extern void native_fn_0220f868(void);
extern void native_fn_021f2230(void);
extern void native_fn_021f4210(void);


asm u32 native_ov001_021f6cec (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    ldr r0, =0x0223989c
    ldr r0, [r0, #0x84]
    ldrb r0, [r0, #0x31e]
    cmp r0, #0
    ldr r0, =0x0223989c
    moveq r4, #1
    ldrb r1, [r0, #0x3c]
    movne r4, #0
    cmp r1, #0
    bne ov001_021f6cec_Le4
    ldr r0, =0x022398f0
    bl native_fn_021f69a0
    ldr r0, =0x0223989c
    ldrb r0, [r0, #0x10]
    cmp r0, #0
    beq ov001_021f6cec_L70
    mov r0, #0
    mov r1, #176
    bl native_fn_021f2120
    mov r0, #0
    mov r1, #249
    bl native_fn_021f2120
    ldr r0, =0x0223989c
    mov r1, #5
    strb r1, [r0, #0x3c]
    mov r1, #0
    strb r1, [r0, #0x3b]
ov001_021f6cec_L70:
    mov r7, #0
    mov r5, r7
ov001_021f6cec_L78:
    mov r0, r4
    mov r1, r7
    bl ov001_side_slot_record_021db438
    mov r6, r0
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    addne r0, r6, #768
    ldrneh r0, [r0, #76]
    cmpne r0, #0
    beq ov001_021f6cec_Lc0
    bl native_fn_0205d790
    add r1, r6, #768
    mov r2, r0
    ldrh r0, [r1, #76]
    mov r1, r6
    bl ov001_effect_resource_create_021eec7c
    add r0, r6, #768
    strh r5, [r0, #76]
ov001_021f6cec_Lc0:
    add r7, r7, #1
    cmp r7, #3
    blt ov001_021f6cec_L78
    ldr r0, =0x0223989c
    mov r1, #5
    strb r1, [r0, #0x3c]
    mov r1, #0
    strb r1, [r0, #0x3b]
    b ov001_021f6cec_L194
ov001_021f6cec_Le4:
    cmp r1, #5
    bne ov001_021f6cec_L130
    ldrb r1, [r0, #0x3b]
    add r2, r1, #1
    and r1, r2, #255
    strb r2, [r0, #0x3b]
    cmp r1, #30
    blo ov001_021f6cec_L194
    mov r0, r4
    bl native_fn_0220f868
    ldr r1, =0x0223989c
    strb r0, [r1, #0x3a]
    ldr r0, [r1, #0x54]
    cmp r0, #0
    movne r0, #10
    strneb r0, [r1, #0x3c]
    moveq r0, #100
    streqb r0, [r1, #0x3c]
    b ov001_021f6cec_L194
ov001_021f6cec_L130:
    cmp r1, #10
    bne ov001_021f6cec_L160
    ldrb r1, [r0, #0x3a]
    mov r2, r4
    mov r0, #0
    bl native_fn_021f2230
    cmp r0, #0
    beq ov001_021f6cec_L194
    ldr r0, =0x0223989c
    mov r1, #100
    strb r1, [r0, #0x3c]
    b ov001_021f6cec_L194
ov001_021f6cec_L160:
    cmp r1, #100
    bne ov001_021f6cec_L194
    mov r1, #0
    strb r1, [r0, #0x3c]
    ldrb r1, [r0, #0x10]
    cmp r1, #0
    moveq r1, #14
    streqb r1, [r0, #0x1b]
    beq ov001_021f6cec_L194
    bl native_fn_021f4210
    ldr r0, =0x0223989c
    mov r1, #3
    strb r1, [r0, #0x1b]
ov001_021f6cec_L194:
    mov r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
