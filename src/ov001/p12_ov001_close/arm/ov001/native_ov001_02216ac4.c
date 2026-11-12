/* ov001 row 0x02216ac4: 372 bytes.
 *
 * What it does: 91 instructions; 14 call(s) to 0x021f1354, 0x021f1438, 0x022168ac, +11 more; loops (back edge at +0x38); returns through pop {r4, r5, r6, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 14 calls (91 instructions, 14 calls, 12 branches, 12 back edges, 2 literal slots).
 *
 *   pool +0x16c -> constant 0x02242bf4 (image word 0x02242bf4)
 *   pool +0x170 -> constant 0x00000117 (image word 0x00000117)
 *   branch +0x1c -> +0x84
 *   branch +0x24 -> +0x44
 *   branch +0x80 -> +0x164
 *   branch +0x88 -> +0xb4
 *   branch +0xa0 -> +0x164
 *   branch +0xb0 -> +0x164
 *   branch +0xb8 -> +0x11c
 *   branch +0xc4 -> +0x164
 *   branch +0xd8 -> +0xec
 *   branch +0x118 -> +0x164
 *   branch +0x120 -> +0x14c
 *   branch +0x138 -> +0x164
 *   branch +0x148 -> +0x164
 *   branch +0x150 -> +0x164
 *   test +0x18 cmp r0, #0
 *   test +0x20 cmp r4, #0
 *   test +0x84 cmp r0, #10
 *   test +0x9c cmp r0, #40
 *   test +0xb4 cmp r0, #20
 *   test +0xc0 cmp r0, #0
 *   test +0xd0 cmp r4, #0
 *   test +0x11c cmp r0, #30
 *   test +0x134 cmp r0, #30
 *   test +0x14c cmp r0, #40
 *   0 block transfer(s), 10 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02216ac4; the literal pool and
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
extern void native_fn_021d7e80(void);
extern void ov001_clear_state_flag4_021f14a4(void);
extern void native_fn_021f14e4(void);
extern void native_fn_022168d0(void);


asm u32 native_ov001_02216ac4 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    ldr r3, =0x02242bf4
    mov r6, r0
    ldrsb r0, [r3, #1]
    mov r5, r1
    mov r4, r2
    cmp r0, #0
    bne ov001_02216ac4_L84
    cmp r4, #0
    bne ov001_02216ac4_L44
    mov r2, r5
    mov r0, #11
    mov r1, #0
    mov r3, #1
    bl ov001_begin_state_transition_021f1354
    mov r0, #2
    bl ov001_select_mode_id_021f1438
ov001_02216ac4_L44:
    ldr r0, =0x00000117
    bl native_fn_022168ac
    ldr r0, =0x00000117
    bl native_fn_0205d790
    mov r2, r0
    ldr r0, =0x00000117
    mov r1, r6
    bl ov001_effect_resource_create_021eec7c
    mov r0, r6
    bl native_fn_021d7e80
    ldr r0, =0x02242bf4
    mov r1, #10
    strb r1, [r0, #0x1]
    mov r1, #0
    strb r1, [r0]
    b ov001_02216ac4_L164
ov001_02216ac4_L84:
    cmp r0, #10
    bne ov001_02216ac4_Lb4
    ldrsb r0, [r3]
    add r0, r0, #1
    strb r0, [r3]
    ldrsb r0, [r3]
    cmp r0, #40
    blt ov001_02216ac4_L164
    mov r0, #20
    strb r0, [r3, #0x1]
    bl ov001_clear_state_flag4_021f14a4
    b ov001_02216ac4_L164
ov001_02216ac4_Lb4:
    cmp r0, #20
    bne ov001_02216ac4_L11c
    bl native_fn_021f14e4
    cmp r0, #0
    bne ov001_02216ac4_L164
    ldr r0, =0x00000117
    bl native_fn_022168d0
    cmp r4, #0
    mov r1, #0
    bne ov001_02216ac4_Lec
    ldr r0, =0x02242bf4
    strb r1, [r0, #0x1]
    mov r0, #1
    ldmia sp!, {r4, r5, r6, pc}
ov001_02216ac4_Lec:
    mov r2, r5
    mov r0, #11
    mov r3, #1
    bl ov001_begin_state_transition_021f1354
    mov r0, #2
    bl ov001_select_mode_id_021f1438
    ldr r0, =0x02242bf4
    mov r1, #30
    strb r1, [r0, #0x1]
    mov r1, #0
    strb r1, [r0]
    b ov001_02216ac4_L164
ov001_02216ac4_L11c:
    cmp r0, #30
    bne ov001_02216ac4_L14c
    ldrsb r0, [r3]
    add r0, r0, #1
    strb r0, [r3]
    ldrsb r0, [r3]
    cmp r0, #30
    blt ov001_02216ac4_L164
    mov r0, #40
    strb r0, [r3, #0x1]
    bl ov001_clear_state_flag4_021f14a4
    b ov001_02216ac4_L164
ov001_02216ac4_L14c:
    cmp r0, #40
    bne ov001_02216ac4_L164
    mov r0, #0
    strb r0, [r3, #0x1]
    mov r0, #1
    ldmia sp!, {r4, r5, r6, pc}
ov001_02216ac4_L164:
    mov r0, #0
    ldmia sp!, {r4, r5, r6, pc}
}
