/* ov001 row 0x02217c10: 344 bytes.
 *
 * What it does: 85 instructions; 13 call(s) to 0x02048034, 0x021f1354, 0x021f1414, +10 more; loops (back edge at +0x24); returns through pop {r4, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 13 calls (85 instructions, 13 calls, 3 branches, 13 back edges, 1 literal slot).
 *
 *   pool +0x154 -> constant 0x02242c40 (image word 0x02242c40)
 *   branch +0x10 -> +0xe4
 *   branch +0xf0 -> +0x110
 *   branch +0x11c -> +0x14c
 *   test +0x0c cmp r1, #0
 *   test +0xec cmp r1, #10
 *   test +0x100 cmp r1, #30
 *   test +0x118 cmp r0, #100
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02217c10; the literal pool and
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

extern void native_fn_02048034(void);
extern void ov001_begin_state_transition_021f1354(void);
extern void native_fn_021f1414(void);
extern void ov001_select_mode_id_021f1438(void);
extern void native_fn_02217b20(void);
extern void native_fn_021d9494(void);
extern void ov001_record_field_1f2_021dbd30(void);
extern void native_fn_0207b244(void);
extern void native_fn_021db834(void);
extern void native_fn_02202528(void);
extern void native_fn_022024d4(void);
extern void ov001_clear_state_flag4_021f14a4(void);
extern void native_fn_02202568(void);


asm u32 native_ov001_02217c10 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    ldr r0, =0x02242c40
    ldrb r1, [r0, #0x3]
    cmp r1, #0
    bne ov001_02217c10_Le4
    ldr r0, [r0, #0x8]
    mov r1, #0
    ldr r0, [r0, #0x1e8]
    add r0, r0, #178
    bl native_fn_02048034
    ldr r1, =0x02242c40
    mov r0, #7
    ldrh r2, [r1, #4]
    mov r1, #0
    mov r3, #1
    bl ov001_begin_state_transition_021f1354
    ldr r0, =0x02242c40
    ldr r0, [r0, #0x8]
    ldrb r0, [r0, #0x31e]
    bl native_fn_021f1414
    bl ov001_select_mode_id_021f1438
    bl native_fn_02217b20
    ldr r0, =0x02242c40
    mov r1, #0
    ldr r0, [r0, #0x8]
    mov r2, r1
    bl native_fn_021d9494
    ldr r0, =0x02242c40
    ldr r4, [r0, #0x8]
    mov r0, r4
    bl ov001_record_field_1f2_021dbd30
    ldr r2, [r4, #0x1e8]
    mov r1, r0
    add r2, r2, #70
    ldr r0, =0x02242c40
    ldrh r0, [r0, #4]
    bl native_fn_0207b244
    mov r1, r0
    ldr r0, =0x02242c40
    ldr r0, [r0, #0x8]
    bl native_fn_021db834
    ldr r0, =0x02242c40
    ldr r1, [r0, #0x8]
    ldrb r0, [r1, #0x31e]
    ldrb r1, [r1, #0x31f]
    bl native_fn_02202528
    ldr r0, =0x02242c40
    mov r2, #0
    ldr r1, [r0, #0x8]
    ldrb r0, [r1, #0x31e]
    ldrb r1, [r1, #0x31f]
    bl native_fn_022024d4
    mov r2, #0
    ldr r0, =0x02242c40
    mov r1, #10
    strb r2, [r0, #0x2]
    strb r1, [r0, #0x3]
ov001_02217c10_Le4:
    ldr r0, =0x02242c40
    ldrb r1, [r0, #0x3]
    cmp r1, #10
    bne ov001_02217c10_L110
    ldrb r1, [r0, #0x2]
    add r2, r1, #1
    and r1, r2, #255
    cmp r1, #30
    strb r2, [r0, #0x2]
    movhi r1, #100
    strhib r1, [r0, #0x3]
ov001_02217c10_L110:
    ldr r0, =0x02242c40
    ldrb r0, [r0, #0x3]
    cmp r0, #100
    bne ov001_02217c10_L14c
    bl ov001_clear_state_flag4_021f14a4
    ldr r0, =0x02242c40
    ldr r1, [r0, #0x8]
    ldrb r0, [r1, #0x31e]
    ldrb r1, [r1, #0x31f]
    bl native_fn_02202568
    ldr r0, =0x02242c40
    mov r1, #0
    strb r1, [r0, #0x3]
    mov r1, #3
    strb r1, [r0]
ov001_02217c10_L14c:
    mov r0, #0
    ldmia sp!, {r4, pc}
}
