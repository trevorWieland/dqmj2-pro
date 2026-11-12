/* ov001 row 0x021fb960: 904 bytes.
 *
 * What it does: 223 instructions; 31 call(s) to 0x021fb8d4, 0x021f1354, 0x021f1414, +28 more; loops (back edge at +0x18); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: loop with 31 calls (223 instructions, 31 calls, 34 branches, 31 back edges, 3 literal slots).
 *
 *   pool +0x37c -> constant 0x02239a14 (image word 0x02239a14)
 *   pool +0x380 -> native_data_0222ed28 (image word 0x0222ed28)
 *   pool +0x384 -> constant 0x00000101 (image word 0x00000101)
 *   branch +0x14 -> +0x60
 *   branch +0x5c -> +0x370
 *   branch +0x64 -> +0x88
 *   branch +0x84 -> +0x370
 *   branch +0x8c -> +0xa4
 *   branch +0xa0 -> +0x370
 *   branch +0xa8 -> +0xc8
 *   branch +0xb4 -> +0x370
 *   branch +0xc4 -> +0x370
 *   branch +0xcc -> +0x100
 *   branch +0xdc -> +0xf0
 *   branch +0xec -> +0x370
 *   branch +0xfc -> +0x370
 *   branch +0x104 -> +0x19c
 *   branch +0x154 -> +0x170
 *   back edge +0x178 -> +0x13c
 *   branch +0x198 -> +0x370
 *   branch +0x1a0 -> +0x224
 *   branch +0x1d4 -> +0x208
 *   back edge +0x210 -> +0x1bc
 *   branch +0x220 -> +0x370
 *   branch +0x228 -> +0x24c
 *   branch +0x248 -> +0x370
 *   branch +0x250 -> +0x2a4
 *   branch +0x274 -> +0x288
 *   back edge +0x290 -> +0x25c
 *   branch +0x2a0 -> +0x370
 *   branch +0x2a8 -> +0x2e4
 *   branch +0x2e0 -> +0x370
 *   branch +0x2e8 -> +0x30c
 *   branch +0x308 -> +0x370
 *   branch +0x310 -> +0x328
 *   branch +0x324 -> +0x370
 *   branch +0x32c -> +0x34c
 *   branch +0x338 -> +0x370
 *   branch +0x348 -> +0x370
 *   branch +0x350 -> +0x370
 *   test +0x10 cmp r1, #0
 *   test +0x60 cmp r1, #10
 *   test +0x74 cmp r1, #60
 *   test +0x88 cmp r1, #20
 *   test +0xa4 cmp r1, #25
 *   test +0xb0 cmp r0, #0
 *   test +0xc8 cmp r1, #30
 *   test +0xd8 cmp r0, #128
 *   test +0x100 cmp r1, #40
 *   test +0x150 cmp r0, #0
 *   test +0x174 cmp r9, #3
 *   test +0x19c cmp r1, #41
 *   test +0x1d0 cmp r0, #0
 *   test +0x20c cmp r10, #3
 *   test +0x224 cmp r1, #42
 *   test +0x238 cmp r1, #30
 *   test +0x24c cmp r1, #45
 *   test +0x270 cmp r0, #0
 *   test +0x28c cmp r6, #3
 *   test +0x2a4 cmp r1, #50
 *   test +0x2e4 cmp r1, #60
 *   test +0x2f8 cmp r1, #60
 *   test +0x30c cmp r1, #70
 *   test +0x328 cmp r1, #75
 *   test +0x334 cmp r0, #0
 *   test +0x34c cmp r1, #100
 *   0 block transfer(s), 25 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021fb960; the literal pool and
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

extern void native_fn_021fb8d4(void);
extern void ov001_begin_state_transition_021f1354(void);
extern void native_fn_021f1414(void);
extern void ov001_select_mode_id_021f1438(void);
extern void native_fn_021f949c(void);
extern void ov001_clear_state_flag4_021f14a4(void);
extern void native_fn_021f14e4(void);
extern void native_fn_0203d294(void);
extern void ov001_side_slot_record_021db438(void);
extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_021dbf98(void);
extern u8 native_data_0222ed28[];
extern void native_fn_0205d790(void);
extern void ov001_effect_resource_create_021eec7c(void);
extern void native_fn_021ee91c(void);
extern void native_fn_021fb214(void);


asm u32 native_ov001_021fb960 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, lr}
    sub sp, sp, #4
    ldr r0, =0x02239a14
    ldrb r1, [r0, #0x1a]
    cmp r1, #0
    bne ov001_021fb960_L60
    bl native_fn_021fb8d4
    mov r0, #1
    mov r3, r0
    mov r1, #2
    mov r2, #4
    bl ov001_begin_state_transition_021f1354
    mov r0, #0
    bl native_fn_021f1414
    bl ov001_select_mode_id_021f1438
    mov r0, #228
    mov r1, #1
    bl native_fn_021f949c
    ldr r0, =0x02239a14
    mov r1, #0
    strb r1, [r0, #0x18]
    mov r1, #10
    strb r1, [r0, #0x1a]
    b ov001_021fb960_L370
ov001_021fb960_L60:
    cmp r1, #10
    bne ov001_021fb960_L88
    ldrb r1, [r0, #0x18]
    add r2, r1, #1
    and r1, r2, #255
    cmp r1, #60
    strb r2, [r0, #0x18]
    movhi r1, #20
    strhib r1, [r0, #0x1a]
    b ov001_021fb960_L370
ov001_021fb960_L88:
    cmp r1, #20
    bne ov001_021fb960_La4
    bl ov001_clear_state_flag4_021f14a4
    ldr r0, =0x02239a14
    mov r1, #25
    strb r1, [r0, #0x1a]
    b ov001_021fb960_L370
ov001_021fb960_La4:
    cmp r1, #25
    bne ov001_021fb960_Lc8
    bl native_fn_021f14e4
    cmp r0, #0
    bne ov001_021fb960_L370
    ldr r0, =0x02239a14
    mov r1, #30
    strb r1, [r0, #0x1a]
    b ov001_021fb960_L370
ov001_021fb960_Lc8:
    cmp r1, #30
    bne ov001_021fb960_L100
    mov r0, #256
    bl native_fn_0203d294
    cmp r0, #128
    bge ov001_021fb960_Lf0
    ldr r0, =0x02239a14
    mov r1, #40
    strb r1, [r0, #0x1a]
    b ov001_021fb960_L370
ov001_021fb960_Lf0:
    ldr r0, =0x02239a14
    mov r1, #50
    strb r1, [r0, #0x1a]
    b ov001_021fb960_L370
ov001_021fb960_L100:
    cmp r1, #40
    bne ov001_021fb960_L19c
    mov r0, #1
    mov r3, r0
    mov r1, #2
    mov r2, #7
    bl ov001_begin_state_transition_021f1354
    mov r0, #1
    bl native_fn_021f1414
    bl ov001_select_mode_id_021f1438
    mov r9, #0
    mov r4, #1
    mov r6, r9
    mov r5, #7
    mov r8, r4
ov001_021fb960_L13c:
    mov r0, r8
    mov r1, r9
    bl ov001_side_slot_record_021db438
    mov r7, r0
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_021fb960_L170
    mov r0, r7
    mov r1, r5
    mov r2, r4
    mov r3, r4
    str r6, [sp]
    bl native_fn_021dbf98
ov001_021fb960_L170:
    add r9, r9, #1
    cmp r9, #3
    blt ov001_021fb960_L13c
    ldr r1, =native_data_0222ed28
    mov r2, #0
    ldr r0, =0x02239a14
    strb r2, [r1]
    strb r2, [r0, #0x18]
    mov r1, #41
    strb r1, [r0, #0x1a]
    b ov001_021fb960_L370
ov001_021fb960_L19c:
    cmp r1, #41
    bne ov001_021fb960_L224
    mov r10, #0
    mov r5, #1
    ldr r4, =0x00000101
    mov r7, r10
    mov r6, #8
    mov r9, r5
ov001_021fb960_L1bc:
    mov r0, r9
    mov r1, r10
    bl ov001_side_slot_record_021db438
    mov r8, r0
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_021fb960_L208
    mov r0, r8
    mov r1, r6
    mov r2, r5
    mov r3, r7
    str r7, [sp]
    bl native_fn_021dbf98
    mov r0, r4
    bl native_fn_0205d790
    mov r2, r0
    mov r1, r8
    mov r0, r4
    bl ov001_effect_resource_create_021eec7c
ov001_021fb960_L208:
    add r10, r10, #1
    cmp r10, #3
    blt ov001_021fb960_L1bc
    ldr r0, =0x02239a14
    mov r1, #42
    strb r1, [r0, #0x1a]
    b ov001_021fb960_L370
ov001_021fb960_L224:
    cmp r1, #42
    bne ov001_021fb960_L24c
    ldrb r1, [r0, #0x18]
    add r2, r1, #1
    and r1, r2, #255
    cmp r1, #30
    strb r2, [r0, #0x18]
    movhs r1, #45
    strhsb r1, [r0, #0x1a]
    b ov001_021fb960_L370
ov001_021fb960_L24c:
    cmp r1, #45
    bne ov001_021fb960_L2a4
    mov r6, #0
    mov r5, #1
ov001_021fb960_L25c:
    mov r0, r5
    mov r1, r6
    bl ov001_side_slot_record_021db438
    mov r4, r0
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_021fb960_L288
    add r0, r4, #512
    ldrsb r1, [r0, #52]
    mov r0, r4
    bl native_fn_021ee91c
ov001_021fb960_L288:
    add r6, r6, #1
    cmp r6, #3
    blt ov001_021fb960_L25c
    ldr r0, =0x02239a14
    mov r1, #60
    strb r1, [r0, #0x1a]
    b ov001_021fb960_L370
ov001_021fb960_L2a4:
    cmp r1, #50
    bne ov001_021fb960_L2e4
    mov r0, #1
    mov r3, r0
    mov r1, #2
    mov r2, #6
    bl ov001_begin_state_transition_021f1354
    mov r0, #1
    bl native_fn_021f1414
    bl ov001_select_mode_id_021f1438
    ldr r0, =0x02239a14
    mov r1, #0
    strb r1, [r0, #0x18]
    mov r1, #60
    strb r1, [r0, #0x1a]
    b ov001_021fb960_L370
ov001_021fb960_L2e4:
    cmp r1, #60
    bne ov001_021fb960_L30c
    ldrb r1, [r0, #0x18]
    add r2, r1, #1
    and r1, r2, #255
    cmp r1, #60
    strb r2, [r0, #0x18]
    movhi r1, #70
    strhib r1, [r0, #0x1a]
    b ov001_021fb960_L370
ov001_021fb960_L30c:
    cmp r1, #70
    bne ov001_021fb960_L328
    bl ov001_clear_state_flag4_021f14a4
    ldr r0, =0x02239a14
    mov r1, #75
    strb r1, [r0, #0x1a]
    b ov001_021fb960_L370
ov001_021fb960_L328:
    cmp r1, #75
    bne ov001_021fb960_L34c
    bl native_fn_021f14e4
    cmp r0, #0
    bne ov001_021fb960_L370
    ldr r0, =0x02239a14
    mov r1, #100
    strb r1, [r0, #0x1a]
    b ov001_021fb960_L370
ov001_021fb960_L34c:
    cmp r1, #100
    bne ov001_021fb960_L370
    mov r0, #0
    bl native_fn_021fb214
    ldr r0, =0x02239a14
    mov r1, #0
    strb r1, [r0, #0x1a]
    mov r1, #15
    strb r1, [r0, #0xa]
ov001_021fb960_L370:
    mov r0, #0
    add sp, sp, #4
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, pc}
}
