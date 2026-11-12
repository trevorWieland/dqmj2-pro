/* ov001 row 0x022177e0: 304 bytes.
 *
 * What it does: 75 instructions; 11 call(s) to 0x021f1354, 0x021f1438, 0x022168ac, +8 more; loops (back edge at +0x44); returns through pop {r4, r5, r6, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 11 calls (75 instructions, 11 calls, 10 branches, 11 back edges, 1 literal slot).
 *
 *   pool +0x12c -> constant 0x02242bf4 (image word 0x02242bf4)
 *   branch +0x18 -> +0x9c
 *   branch +0x30 -> +0x58
 *   branch +0x98 -> +0x124
 *   branch +0xa0 -> +0x124
 *   branch +0xac -> +0xec
 *   branch +0xbc -> +0xec
 *   branch +0xcc -> +0xec
 *   branch +0xf0 -> +0x124
 *   branch +0x108 -> +0x118
 *   test +0x14 cmp r1, #0
 *   test +0x2c cmp r2, #0
 *   test +0x9c cmp r1, #30
 *   test +0xa8 tst r1, #4
 *   test +0xb8 cmp r0, #0
 *   test +0xc8 cmp r0, #0
 *   test +0xec cmp r4, #0
 *   test +0x104 tst r1, #255
 *   0 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022177e0; the literal pool and
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

extern void ov001_begin_state_transition_021f1354(void);
extern void ov001_select_mode_id_021f1438(void);
extern void native_fn_022168ac(void);
extern void native_fn_0205d790(void);
extern void ov001_effect_resource_create_021eec7c(void);
extern void native_fn_021f5c38(void);
extern void native_fn_021f5cc0(void);
extern void native_fn_0205d6f4(void);
extern void native_fn_021dc940(void);
extern void ov001_clear_state_flag4_021f14a4(void);
extern void native_fn_022168d0(void);


asm u32 native_ov001_022177e0 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r6, r0
    ldrb r1, [r6, #0x327]
    mov r4, #0
    mov r5, r4
    cmp r1, #0
    bne ov001_022177e0_L9c
    ldr r0, =0x02242bf4
    ldrb r2, [r0, #0x2]
    add r1, r2, #1
    strb r1, [r0, #0x2]
    cmp r2, #0
    bne ov001_022177e0_L58
    mov r1, r4
    mov r0, #11
    mov r2, #37
    mov r3, #1
    bl ov001_begin_state_transition_021f1354
    mov r0, #2
    bl ov001_select_mode_id_021f1438
    mov r0, #141
    bl native_fn_022168ac
ov001_022177e0_L58:
    mov r0, #141
    bl native_fn_0205d790
    mov r2, r0
    mov r1, r6
    mov r0, #141
    bl ov001_effect_resource_create_021eec7c
    str r0, [r6, #0x338]
    mov r3, #1
    mov r0, r6
    mov r1, r6
    mov r2, #55
    strb r3, [r6, #0x1ff]
    mov r3, #0
    bl native_fn_021f5c38
    mov r0, #30
    strb r0, [r6, #0x327]
    b ov001_022177e0_L124
ov001_022177e0_L9c:
    cmp r1, #30
    bne ov001_022177e0_L124
    ldr r1, [r6, #0x33c]
    tst r1, #4
    beq ov001_022177e0_Lec
    mov r1, #55
    bl native_fn_021f5cc0
    cmp r0, #0
    beq ov001_022177e0_Lec
    ldr r0, [r6, #0x338]
    bl native_fn_0205d6f4
    cmp r0, #0
    bne ov001_022177e0_Lec
    ldr r1, [r6, #0x33c]
    mov r0, r6
    bic r2, r1, #4
    mov r1, #39
    str r2, [r6, #0x33c]
    mov r4, #1
    bl native_fn_021dc940
ov001_022177e0_Lec:
    cmp r4, #0
    beq ov001_022177e0_L124
    ldr r0, =0x02242bf4
    ldrb r1, [r0, #0x2]
    sub r1, r1, #1
    strb r1, [r0, #0x2]
    tst r1, #255
    bne ov001_022177e0_L118
    bl ov001_clear_state_flag4_021f14a4
    mov r0, #141
    bl native_fn_022168d0
ov001_022177e0_L118:
    mov r0, #0
    strb r0, [r6, #0x327]
    mov r5, #1
ov001_022177e0_L124:
    mov r0, r5
    ldmia sp!, {r4, r5, r6, pc}
}
