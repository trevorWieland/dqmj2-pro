/* ov001 row 0x02215ac8: 628 bytes.
 *
 * What it does: 155 instructions; 33 call(s) to 0x021f1354, 0x021f1414, 0x021f1438, +30 more; loops (back edge at +0x24); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 33 calls (155 instructions, 33 calls, 15 branches, 32 back edges, 2 literal slots).
 *
 *   pool +0x26c -> constant 0x02242ba0 (image word 0x02242ba0)
 *   pool +0x270 -> constant 0x02242bb4 (image word 0x02242bb4)
 *   branch +0x10 -> +0xb4
 *   branch +0x7c -> +0x98
 *   back edge +0xa0 -> +0x64
 *   branch +0xb0 -> +0x264
 *   branch +0xb8 -> +0xdc
 *   branch +0xd8 -> +0x264
 *   branch +0xe0 -> +0x110
 *   branch +0xf8 -> +0x264
 *   branch +0x10c -> +0x264
 *   branch +0x114 -> +0x1f8
 *   branch +0x120 -> +0x264
 *   back edge +0x188 -> +0x164
 *   branch +0x1bc -> +0x1d4
 *   back edge +0x1dc -> +0x1a0
 *   branch +0x1f4 -> +0x264
 *   branch +0x1fc -> +0x22c
 *   branch +0x214 -> +0x264
 *   branch +0x228 -> +0x264
 *   branch +0x230 -> +0x264
 *   test +0x0c cmp r1, #0
 *   test +0x78 cmp r0, #0
 *   test +0x9c cmp r9, #3
 *   test +0xb4 cmp r1, #5
 *   test +0xdc cmp r1, #10
 *   test +0xf4 cmp r1, #45
 *   test +0x110 cmp r1, #30
 *   test +0x11c cmp r0, #0
 *   test +0x184 cmp r0, #0
 *   test +0x1b4 cmp r0, #0
 *   test +0x1b8 cmpne r7, r8
 *   test +0x1d8 cmp r8, #3
 *   test +0x1f8 cmp r1, #40
 *   test +0x210 cmp r1, #30
 *   test +0x22c cmp r1, #100
 *   0 block transfer(s), 11 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02215ac8; the literal pool and
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
extern void native_fn_021f1414(void);
extern void ov001_select_mode_id_021f1438(void);
extern void native_fn_021d7f54(void);
extern void native_fn_0202ac08(void);
extern void native_fn_021eea10(void);
extern void ov001_side_slot_record_021db438(void);
extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_0205c904(void);
extern void ov001_effect_resource_create_021eec7c(void);
extern void native_fn_02041898(void);
extern void ov001_clear_state_flag4_021f14a4(void);
extern void native_fn_021f14e4(void);
extern void native_fn_0205f210(void);
extern void native_fn_0205e7a8(void);
extern void native_fn_0203d294(void);
extern void native_fn_021fb214(void);
extern void native_fn_022025a4(void);
extern void native_fn_021eeb70(void);
extern void native_fn_0202ac4c(void);
extern void native_fn_0203d0d8(void);


asm u32 native_ov001_02215ac8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    ldr r0, =0x02242ba0
    ldrb r1, [r0, #0x1]
    cmp r1, #0
    bne ov001_02215ac8_Lb4
    mov r0, #1
    mov r3, r0
    mov r1, #0
    mov r2, #25
    bl ov001_begin_state_transition_021f1354
    mov r0, #1
    bl native_fn_021f1414
    bl ov001_select_mode_id_021f1438
    mov r0, #1
    bl native_fn_021d7f54
    ldr r0, =0x02242bb4
    bl native_fn_0202ac08
    mov r0, #63
    mov r1, #0
    bl native_fn_021eea10
    mov r6, #63
    mov r4, #1
    mov r9, #0
    mov r5, r6
    mov r8, r4
ov001_02215ac8_L64:
    mov r0, r8
    mov r1, r9
    bl ov001_side_slot_record_021db438
    mov r7, r0
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_02215ac8_L98
    mov r0, r6
    bl native_fn_0205c904
    mov r0, r5
    mov r1, r7
    mov r2, r4
    bl ov001_effect_resource_create_021eec7c
ov001_02215ac8_L98:
    add r9, r9, #1
    cmp r9, #3
    blt ov001_02215ac8_L64
    ldr r0, =0x02242ba0
    mov r1, #5
    strb r1, [r0, #0x1]
    b ov001_02215ac8_L264
ov001_02215ac8_Lb4:
    cmp r1, #5
    bne ov001_02215ac8_Ldc
    mov r0, #0
    bl native_fn_02041898
    ldr r0, =0x02242ba0
    mov r1, #10
    strb r1, [r0, #0x1]
    mov r1, #0
    strb r1, [r0]
    b ov001_02215ac8_L264
ov001_02215ac8_Ldc:
    cmp r1, #10
    bne ov001_02215ac8_L110
    ldrb r1, [r0]
    add r2, r1, #1
    and r1, r2, #255
    strb r2, [r0]
    cmp r1, #45
    blo ov001_02215ac8_L264
    bl ov001_clear_state_flag4_021f14a4
    ldr r0, =0x02242ba0
    mov r1, #30
    strb r1, [r0, #0x1]
    b ov001_02215ac8_L264
ov001_02215ac8_L110:
    cmp r1, #30
    bne ov001_02215ac8_L1f8
    bl native_fn_021f14e4
    cmp r0, #0
    bne ov001_02215ac8_L264
    mov r0, #1
    mov r3, r0
    mov r1, #0
    mov r2, #32
    bl ov001_begin_state_transition_021f1354
    mov r0, #0
    bl native_fn_021f1414
    bl ov001_select_mode_id_021f1438
    mov r0, #1
    mov r1, #0
    bl native_fn_0205f210
    mvn r0, #0
    mov r1, #58
    bl native_fn_0205e7a8
    mov r6, #3
    mov r5, #1
ov001_02215ac8_L164:
    mov r0, r6
    bl native_fn_0203d294
    mov r7, r0
    mov r0, r5
    mov r1, r7
    bl ov001_side_slot_record_021db438
    mov r4, r0
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_02215ac8_L164
    mov r0, r4
    bl native_fn_021fb214
    mov r4, #1
    mov r8, #0
    mov r6, r4
ov001_02215ac8_L1a0:
    mov r0, r6
    mov r1, r8
    bl ov001_side_slot_record_021db438
    mov r5, r0
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    cmpne r7, r8
    beq ov001_02215ac8_L1d4
    mov r0, r4
    mov r1, r8
    mov r2, r4
    strb r4, [r5, #0x325]
    bl native_fn_022025a4
ov001_02215ac8_L1d4:
    add r8, r8, #1
    cmp r8, #3
    blt ov001_02215ac8_L1a0
    ldr r0, =0x02242ba0
    mov r1, #40
    strb r1, [r0, #0x1]
    mov r1, #0
    strb r1, [r0]
    b ov001_02215ac8_L264
ov001_02215ac8_L1f8:
    cmp r1, #40
    bne ov001_02215ac8_L22c
    ldrb r1, [r0]
    add r2, r1, #1
    and r1, r2, #255
    strb r2, [r0]
    cmp r1, #30
    blo ov001_02215ac8_L264
    bl ov001_clear_state_flag4_021f14a4
    ldr r0, =0x02242ba0
    mov r1, #100
    strb r1, [r0, #0x1]
    b ov001_02215ac8_L264
ov001_02215ac8_L22c:
    cmp r1, #100
    bne ov001_02215ac8_L264
    mov r0, #63
    bl native_fn_021eeb70
    ldr r0, =0x02242bb4
    bl native_fn_0202ac4c
    mov r0, #3
    mov r1, #1
    bl native_fn_0203d0d8
    ldr r0, =0x02242ba0
    mov r1, #3
    str r1, [r0, #0x8]
    mov r0, #1
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
ov001_02215ac8_L264:
    mov r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
