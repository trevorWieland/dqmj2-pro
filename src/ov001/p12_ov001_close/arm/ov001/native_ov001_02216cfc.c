/* ov001 row 0x02216cfc: 1016 bytes.
 *
 * What it does: 252 instructions; 36 call(s) to 0x02216da0, 0x02216da0, 0x021f1294, +33 more; loops (back edge at +0xbc); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 36 calls (252 instructions, 36 calls, 54 branches, 31 back edges, 2 literal slots).
 *
 *   pool +0x3f0 -> constant 0x02242bf4 (image word 0x02242bf4)
 *   pool +0x3f4 -> constant 0x02242bfb (image word 0x02242bfb)
 *   branch +0x14 -> +0x60
 *   branch +0x1c -> +0x44
 *   branch +0x20 -> +0x58
 *   branch +0x28 -> +0xa4
 *   branch +0x30 -> +0xa4
 *   branch +0x34 -> +0x50
 *   branch +0x3c -> +0x58
 *   branch +0x40 -> +0xa4
 *   branch +0x48 -> +0x58
 *   branch +0x4c -> +0xa4
 *   branch +0x54 -> +0xa4
 *   branch +0x5c -> +0xa4
 *   branch +0x64 -> +0x8c
 *   branch +0x68 -> +0xa0
 *   branch +0x70 -> +0xa4
 *   branch +0x78 -> +0xa4
 *   branch +0x7c -> +0x98
 *   branch +0x84 -> +0xa0
 *   branch +0x88 -> +0xa4
 *   branch +0x90 -> +0xa0
 *   branch +0x94 -> +0xa4
 *   branch +0x9c -> +0xa4
 *   branch +0xb0 -> +0x154
 *   branch +0xf4 -> +0x108
 *   branch +0x104 -> +0x3e8
 *   branch +0x114 -> +0x134
 *   branch +0x150 -> +0x3e8
 *   branch +0x158 -> +0x184
 *   branch +0x170 -> +0x3e8
 *   branch +0x180 -> +0x3e8
 *   branch +0x188 -> +0x2d0
 *   branch +0x198 -> +0x1a0
 *   branch +0x1ac -> +0x1c0
 *   branch +0x1e8 -> +0x2a0
 *   branch +0x1f0 -> +0x204
 *   branch +0x208 -> +0x230
 *   branch +0x20c -> +0x284
 *   branch +0x214 -> +0x2a0
 *   branch +0x21c -> +0x2a0
 *   branch +0x220 -> +0x238
 *   branch +0x228 -> +0x254
 *   branch +0x22c -> +0x2a0
 *   branch +0x234 -> +0x2a0
 *   branch +0x250 -> +0x2a0
 *   branch +0x260 -> +0x2a0
 *   branch +0x280 -> +0x2a0
 *   back edge +0x2ac -> +0x1dc
 *   branch +0x2cc -> +0x3e8
 *   branch +0x2d4 -> +0x2f8
 *   branch +0x2f4 -> +0x3e8
 *   branch +0x2fc -> +0x35c
 *   branch +0x320 -> +0x334
 *   back edge +0x340 -> +0x314
 *   branch +0x358 -> +0x3e8
 *   branch +0x360 -> +0x384
 *   branch +0x380 -> +0x3e8
 *   branch +0x388 -> +0x3b4
 *   branch +0x3a0 -> +0x3e8
 *   branch +0x3b0 -> +0x3e8
 *   branch +0x3b8 -> +0x3e8
 *   branch +0x3c8 -> +0x3d0
 *   test +0x10 cmp r0, #0
 *   test +0x18 cmp r10, #50
 *   test +0x24 cmp r10, #43
 *   test +0x2c cmp r10, #42
 *   test +0x38 cmp r10, #43
 *   test +0x44 cmp r10, #57
 *   test +0x60 cmp r10, #50
 *   test +0x6c cmp r10, #43
 *   test +0x74 cmp r10, #42
 *   test +0x80 cmp r10, #43
 *   test +0x8c cmp r10, #57
 *   test +0xac cmp r1, #0
 *   test +0xf0 cmp r0, #0
 *   test +0x154 cmp r1, #10
 *   test +0x16c cmp r1, #40
 *   test +0x184 cmp r1, #20
 *   test +0x194 cmp r0, #0
 *   test +0x1e4 cmp r0, #0
 *   test +0x1ec cmp r9, #0
 *   test +0x204 cmp r10, #50
 *   test +0x210 cmp r10, #43
 *   test +0x218 cmp r10, #42
 *   test +0x224 cmp r10, #43
 *   test +0x230 cmp r10, #57
 *   test +0x25c cmp r0, #0
 *   test +0x2a8 cmp r7, #3
 *   test +0x2d0 cmp r1, #30
 *   test +0x2e8 cmp r1, #30
 *   test +0x2f8 cmp r1, #40
 *   test +0x31c cmp r0, #0
 *   test +0x338 cmp r5, #3
 *   test +0x35c cmp r1, #50
 *   test +0x374 cmp r1, #30
 *   test +0x384 cmp r1, #80
 *   test +0x39c cmp r0, #0
 *   test +0x3b4 cmp r1, #100
 *   test +0x3c4 cmp r0, #0
 *   0 block transfer(s), 18 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02216cfc; the literal pool and
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

extern void native_fn_021f1294(void);
extern void ov001_begin_state_transition_021f1354(void);
extern void ov001_select_mode_id_021f1438(void);
extern void native_fn_0220f9a4(void);
extern void native_fn_02216c38(void);
extern void native_fn_022168ac(void);
extern void native_fn_0205d790(void);
extern void ov001_effect_resource_create_021eec7c(void);
extern void native_fn_021d7e80(void);
extern void ov001_clear_state_flag4_021f14a4(void);
extern void native_fn_022168d0(void);
extern void native_fn_02216cac(void);
extern void ov001_side_slot_record_021db438(void);
extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_021dbf98(void);
extern void native_fn_021d7f54(void);
extern void native_fn_021ee91c(void);
extern void native_fn_02216ac4(void);
extern void native_fn_021f1324(void);


asm u32 native_ov001_02216cfc (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r4, r0
    ldrb r0, [r4, #0x31e]
    mov r10, r1
    cmp r0, #0
    bne ov001_02216cfc_L60
    cmp r10, #50
    bgt ov001_02216cfc_L44
    bge ov001_02216cfc_L58
    cmp r10, #43
    bgt ov001_02216cfc_La4
    cmp r10, #42
    blt ov001_02216cfc_La4
    beq ov001_02216cfc_L50
    cmp r10, #43
    beq ov001_02216cfc_L58
    b ov001_02216cfc_La4
ov001_02216cfc_L44:
    cmp r10, #57
    beq ov001_02216cfc_L58
    b ov001_02216cfc_La4
ov001_02216cfc_L50:
    mov r6, #0
    b ov001_02216cfc_La4
ov001_02216cfc_L58:
    mov r6, #1
    b ov001_02216cfc_La4
ov001_02216cfc_L60:
    cmp r10, #50
    bgt ov001_02216cfc_L8c
    bge ov001_02216cfc_La0
    cmp r10, #43
    bgt ov001_02216cfc_La4
    cmp r10, #42
    blt ov001_02216cfc_La4
    beq ov001_02216cfc_L98
    cmp r10, #43
    beq ov001_02216cfc_La0
    b ov001_02216cfc_La4
ov001_02216cfc_L8c:
    cmp r10, #57
    beq ov001_02216cfc_La0
    b ov001_02216cfc_La4
ov001_02216cfc_L98:
    mov r6, #1
    b ov001_02216cfc_La4
ov001_02216cfc_La0:
    mov r6, #0
ov001_02216cfc_La4:
    ldr r0, =0x02242bf4
    ldrb r1, [r0, #0x6]
    cmp r1, #0
    bne ov001_02216cfc_L154
    mov r0, #16
    mov r1, #2
    bl native_fn_021f1294
    mov r2, r10
    mov r0, #11
    mov r1, #0
    mov r3, #1
    bl ov001_begin_state_transition_021f1354
    mov r0, #2
    bl ov001_select_mode_id_021f1438
    ldr r0, [r4, #0x1e8]
    ldr r2, =0x02242bfb
    add r0, r0, #70
    mov r1, #0
    bl native_fn_0220f9a4
    cmp r0, #0
    beq ov001_02216cfc_L108
    ldr r0, =0x02242bf4
    mov r1, #80
    strb r1, [r0, #0x6]
    b ov001_02216cfc_L3e8
ov001_02216cfc_L108:
    mov r0, r10
    bl native_fn_02216c38
    movs r5, r0
    beq ov001_02216cfc_L134
    bl native_fn_022168ac
    mov r0, r5
    bl native_fn_0205d790
    mov r2, r0
    mov r0, r5
    mov r1, r4
    bl ov001_effect_resource_create_021eec7c
ov001_02216cfc_L134:
    mov r0, r4
    bl native_fn_021d7e80
    ldr r0, =0x02242bf4
    mov r1, #10
    strb r1, [r0, #0x6]
    mov r1, #0
    strb r1, [r0]
    b ov001_02216cfc_L3e8
ov001_02216cfc_L154:
    cmp r1, #10
    bne ov001_02216cfc_L184
    ldrsb r1, [r0]
    add r1, r1, #1
    strb r1, [r0]
    ldrsb r1, [r0]
    cmp r1, #40
    blt ov001_02216cfc_L3e8
    mov r1, #20
    strb r1, [r0, #0x6]
    bl ov001_clear_state_flag4_021f14a4
    b ov001_02216cfc_L3e8
ov001_02216cfc_L184:
    cmp r1, #20
    bne ov001_02216cfc_L2d0
    mov r0, r10
    bl native_fn_02216c38
    cmp r0, #0
    beq ov001_02216cfc_L1a0
    bl native_fn_022168d0
ov001_02216cfc_L1a0:
    mov r0, r10
    bl native_fn_02216cac
    movs r9, r0
    beq ov001_02216cfc_L1c0
    bl native_fn_022168ac
    mov r0, r9
    bl native_fn_0205d790
    mov r5, r0
ov001_02216cfc_L1c0:
    mov r0, r6
    mov r1, #0
    bl ov001_side_slot_record_021db438
    mov r7, #0
    mov r8, r0
    mvn r4, #0
    mov r11, r7
ov001_02216cfc_L1dc:
    mov r0, r8
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_02216cfc_L2a0
    cmp r9, #0
    beq ov001_02216cfc_L204
    mov r0, r9
    mov r1, r8
    mov r2, r5
    bl ov001_effect_resource_create_021eec7c
ov001_02216cfc_L204:
    cmp r10, #50
    bgt ov001_02216cfc_L230
    bge ov001_02216cfc_L284
    cmp r10, #43
    bgt ov001_02216cfc_L2a0
    cmp r10, #42
    blt ov001_02216cfc_L2a0
    beq ov001_02216cfc_L238
    cmp r10, #43
    beq ov001_02216cfc_L254
    b ov001_02216cfc_L2a0
ov001_02216cfc_L230:
    cmp r10, #57
    bne ov001_02216cfc_L2a0
ov001_02216cfc_L238:
    mov r0, r8
    mov r1, #8
    mov r2, #1
    mov r3, r4
    str r11, [sp]
    bl native_fn_021dbf98
    b ov001_02216cfc_L2a0
ov001_02216cfc_L254:
    add r0, r8, #512
    ldrsb r0, [r0, #52]
    cmp r0, #0
    ble ov001_02216cfc_L2a0
    rsb r2, r0, #0
    mov r0, #0
    str r0, [sp]
    mov r0, r8
    mov r1, #8
    mov r3, r4
    bl native_fn_021dbf98
    b ov001_02216cfc_L2a0
ov001_02216cfc_L284:
    mov r0, #0
    str r0, [sp]
    mov r0, r8
    mov r1, #8
    mov r2, r4
    mov r3, r4
    bl native_fn_021dbf98
ov001_02216cfc_L2a0:
    add r8, r8, #1088
    add r7, r7, #1
    cmp r7, #3
    blt ov001_02216cfc_L1dc
    mov r0, r6
    bl native_fn_021d7f54
    ldr r0, =0x02242bf4
    mov r1, #30
    strb r1, [r0, #0x6]
    mov r1, #0
    strb r1, [r0]
    b ov001_02216cfc_L3e8
ov001_02216cfc_L2d0:
    cmp r1, #30
    bne ov001_02216cfc_L2f8
    ldrsb r1, [r0]
    add r1, r1, #1
    strb r1, [r0]
    ldrsb r1, [r0]
    cmp r1, #30
    movge r1, #40
    strgeb r1, [r0, #0x6]
    b ov001_02216cfc_L3e8
ov001_02216cfc_L2f8:
    cmp r1, #40
    bne ov001_02216cfc_L35c
    mov r0, r6
    mov r1, #0
    bl ov001_side_slot_record_021db438
    mov r4, r0
    mov r5, #0
ov001_02216cfc_L314:
    mov r0, r4
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_02216cfc_L334
    add r0, r4, #512
    ldrsb r1, [r0, #52]
    mov r0, r4
    bl native_fn_021ee91c
ov001_02216cfc_L334:
    add r5, r5, #1
    cmp r5, #3
    add r4, r4, #1088
    blt ov001_02216cfc_L314
    ldr r0, =0x02242bf4
    mov r1, #50
    strb r1, [r0, #0x6]
    mov r1, #0
    strb r1, [r0]
    b ov001_02216cfc_L3e8
ov001_02216cfc_L35c:
    cmp r1, #50
    bne ov001_02216cfc_L384
    ldrsb r1, [r0]
    add r1, r1, #1
    strb r1, [r0]
    ldrsb r1, [r0]
    cmp r1, #30
    movge r1, #100
    strgeb r1, [r0, #0x6]
    b ov001_02216cfc_L3e8
ov001_02216cfc_L384:
    cmp r1, #80
    bne ov001_02216cfc_L3b4
    ldrb r1, [r0, #0x7]
    mov r0, r4
    mov r2, #1
    bl native_fn_02216ac4
    cmp r0, #0
    beq ov001_02216cfc_L3e8
    ldr r0, =0x02242bf4
    mov r1, #100
    strb r1, [r0, #0x6]
    b ov001_02216cfc_L3e8
ov001_02216cfc_L3b4:
    cmp r1, #100
    bne ov001_02216cfc_L3e8
    mov r0, r10
    bl native_fn_02216cac
    cmp r0, #0
    beq ov001_02216cfc_L3d0
    bl native_fn_022168d0
ov001_02216cfc_L3d0:
    ldr r0, =0x02242bf4
    mov r1, #0
    strb r1, [r0, #0x6]
    bl native_fn_021f1324
    mov r0, #1
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov001_02216cfc_L3e8:
    mov r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
