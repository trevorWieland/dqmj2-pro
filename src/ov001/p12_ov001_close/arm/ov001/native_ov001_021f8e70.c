/* ov001 row 0x021f8e70: 360 bytes.
 *
 * What it does: 88 instructions; 17 call(s) to 0x021d7e80, 0x0202ac08, 0x021eea10, +14 more; loops (back edge at +0x18); returns through pop {r3, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 17 calls (88 instructions, 17 calls, 9 branches, 16 back edges, 2 literal slots).
 *
 *   pool +0x160 -> constant 0x0223989c (image word 0x0223989c)
 *   pool +0x164 -> constant 0x0223992c (image word 0x0223992c)
 *   branch +0x10 -> +0xa4
 *   branch +0xa0 -> +0x158
 *   branch +0xa8 -> +0xf8
 *   branch +0xb8 -> +0x158
 *   branch +0xf4 -> +0x158
 *   branch +0xfc -> +0x128
 *   branch +0x114 -> +0x158
 *   branch +0x124 -> +0x158
 *   branch +0x12c -> +0x158
 *   test +0x0c cmp r1, #0
 *   test +0x7c cmp r0, #0
 *   test +0xa4 cmp r1, #10
 *   test +0xb4 cmp r0, #0
 *   test +0xf8 cmp r1, #20
 *   test +0x110 cmp r0, #0
 *   test +0x128 cmp r1, #100
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f8e70; the literal pool and
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

extern void native_fn_021d7e80(void);
extern void native_fn_0202ac08(void);
extern void native_fn_021eea10(void);
extern void native_fn_0205c904(void);
extern void native_fn_0205d790(void);
extern void ov001_effect_resource_create_021eec7c(void);
extern void ov001_begin_state_transition_021f1354(void);
extern void native_fn_021f1414(void);
extern void ov001_select_mode_id_021f1438(void);
extern void native_fn_0205d6f4(void);
extern void native_fn_021db788(void);
extern void native_fn_022024d4(void);
extern void ov001_clear_state_flag4_021f14a4(void);
extern void native_fn_021f2230(void);
extern void native_fn_021eeb70(void);
extern void native_fn_0202ac4c(void);
extern void native_fn_021f8e10(void);


asm u32 native_ov001_021f8e70 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r0, =0x0223989c
    ldrsb r1, [r0, #57]
    cmp r1, #0
    bne ov001_021f8e70_La4
    ldr r0, [r0, #0x84]
    bl native_fn_021d7e80
    ldr r0, =0x0223992c
    bl native_fn_0202ac08
    mov r0, #125
    mov r1, #0
    bl native_fn_021eea10
    mov r0, #125
    bl native_fn_0205c904
    mov r0, #125
    bl native_fn_0205d790
    ldr r1, =0x0223989c
    mov r2, r0
    ldr r1, [r1, #0x84]
    mov r0, #125
    bl ov001_effect_resource_create_021eec7c
    ldr r2, =0x0223989c
    mov r1, #3
    str r0, [r2, #0x58]
    mov r0, #5
    mov r2, #59
    mov r3, #1
    bl ov001_begin_state_transition_021f1354
    ldr r0, =0x0223989c
    ldr r0, [r0, #0x84]
    ldrb r0, [r0, #0x31e]
    cmp r0, #0
    moveq r0, #1
    movne r0, #0
    and r0, r0, #255
    bl native_fn_021f1414
    bl ov001_select_mode_id_021f1438
    ldr r0, =0x0223989c
    mov r1, #10
    strb r1, [r0, #0x39]
    b ov001_021f8e70_L158
ov001_021f8e70_La4:
    cmp r1, #10
    bne ov001_021f8e70_Lf8
    ldr r0, [r0, #0x58]
    bl native_fn_0205d6f4
    cmp r0, #0
    bne ov001_021f8e70_L158
    ldr r0, =0x0223989c
    mov r1, #0
    ldr r0, [r0, #0x84]
    bl native_fn_021db788
    ldr r0, =0x0223989c
    mov r2, #1
    ldr r1, [r0, #0x84]
    ldrb r0, [r1, #0x31e]
    ldrb r1, [r1, #0x31f]
    bl native_fn_022024d4
    bl ov001_clear_state_flag4_021f14a4
    ldr r0, =0x0223989c
    mov r1, #20
    strb r1, [r0, #0x39]
    b ov001_021f8e70_L158
ov001_021f8e70_Lf8:
    cmp r1, #20
    bne ov001_021f8e70_L128
    ldr r0, [r0, #0x84]
    mov r1, #0
    ldrb r2, [r0, #0x31e]
    bl native_fn_021f2230
    cmp r0, #0
    beq ov001_021f8e70_L158
    ldr r0, =0x0223989c
    mov r1, #100
    strb r1, [r0, #0x39]
    b ov001_021f8e70_L158
ov001_021f8e70_L128:
    cmp r1, #100
    bne ov001_021f8e70_L158
    mov r0, #125
    bl native_fn_021eeb70
    ldr r0, =0x0223992c
    bl native_fn_0202ac4c
    bl native_fn_021f8e10
    ldr r0, =0x0223989c
    mov r1, #27
    strb r1, [r0, #0x1b]
    mov r1, #0
    strb r1, [r0, #0x39]
ov001_021f8e70_L158:
    mov r0, #0
    ldmia sp!, {r3, pc}
}
