/* ov001 row 0x021ff774: 504 bytes.
 *
 * What it does: 124 instructions; 14 call(s) to 0x02202360, 0x02048f6c, 0x02045dc4, +11 more; loops (back edge at +0x6c); returns through pop {r4, r5, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 14 calls (124 instructions, 14 calls, 13 branches, 7 back edges, 2 literal slots).
 *
 *   pool +0x1f0 -> constant 0x02239c10 (image word 0x02239c10)
 *   pool +0x1f4 -> native_data_0222e044 (image word 0x0222e044)
 *   branch +0x4c -> +0x174
 *   branch +0x50 -> +0x174
 *   branch +0x54 -> +0x68
 *   branch +0x58 -> +0xdc
 *   branch +0x5c -> +0x174
 *   branch +0x60 -> +0xdc
 *   branch +0x64 -> +0xdc
 *   branch +0xac -> +0xc4
 *   branch +0xd8 -> +0x198
 *   branch +0x120 -> +0x13c
 *   branch +0x138 -> +0x164
 *   branch +0x148 -> +0x164
 *   branch +0x170 -> +0x198
 *   test +0x40 cmp r0, #5
 *   test +0xa0 cmp r0, #3
 *   test +0x11c cmp r0, #2
 *   test +0x13c cmp r0, #4
 *   0 block transfer(s), 19 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021ff774; the literal pool and
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

extern void ov001_table_f0_entry_02202360(void);
extern u8 native_data_0222e044[];
extern void native_fn_02048f6c(void);
extern void native_fn_02045dc4(void);
extern void native_fn_02026144(void);
extern void native_fn_02202b30(void);
extern void ov001_side_slot_record_021db438(void);
extern void native_fn_02204590(void);
extern void native_fn_022023dc(void);
extern void native_fn_022023c4(void);
extern void native_fn_022044c8(void);
extern void native_fn_02204558(void);


asm u32 native_ov001_021ff774 (register u32 a0)
{
    stmdb sp!, {r4, r5, lr}
    sub sp, sp, #12
    ldr r0, =0x02239c10
    ldrsb r0, [r0, #12]
    bl ov001_table_f0_entry_02202360
    mov r4, r0
    ldr r1, =native_data_0222e044
    ldrh r3, [r4, #12]
    ldrh r2, [r1, #12]
    ldr r0, =0x02239c10
    ldrh r1, [r1, #10]
    ldrsb r0, [r0, #12]
    mov r3, r3, lsl #1
    add r3, r3, #2
    strh r1, [sp, #8]
    strh r2, [sp, #10]
    cmp r0, #5
    and r5, r3, #255
    addls pc, pc, r0, lsl #2
    b ov001_021ff774_L174
    b ov001_021ff774_L174
    b ov001_021ff774_L68
    b ov001_021ff774_Ldc
    b ov001_021ff774_L174
    b ov001_021ff774_Ldc
    b ov001_021ff774_Ldc
ov001_021ff774_L68:
    mov r0, #1
    bl native_fn_02048f6c
    mov r1, r0
    mov r2, #21
    str r2, [sp]
    mov r0, #1
    mov r3, r0
    mov r2, #11
    str r5, [sp, #0x4]
    bl native_fn_02045dc4
    ldr r0, =0x02239c10
    ldrsb r0, [r0, #12]
    strb r0, [r4, #0x10]
    ldrb r0, [r4, #0x13]
    cmp r0, #3
    movne r0, #0
    strne r0, [r4]
    bne ov001_021ff774_Lc4
    ldrh r5, [r4, #12]
    ldr r0, [r4]
    mov r1, r5
    bl native_fn_02026144
    mul r0, r5, r0
ov001_021ff774_Lc4:
    str r0, [r4, #0x4]
    ldr r0, =0x02239c10
    mov r1, #1
    strb r1, [r0, #0x9]
    bl native_fn_02202b30
    b ov001_021ff774_L198
ov001_021ff774_Ldc:
    mov r1, #0
    mov r0, #1
    str r1, [r4, #0x4]
    bl native_fn_02048f6c
    mov r1, r0
    mov r2, #21
    mov r0, #1
    str r2, [sp]
    mov r3, r0
    mov r2, #11
    str r5, [sp, #0x4]
    bl native_fn_02045dc4
    ldr r0, =0x02239c10
    ldrsb r1, [r0, #12]
    strb r1, [r4, #0x10]
    ldrsb r0, [r0, #12]
    cmp r0, #2
    bne ov001_021ff774_L13c
    ldrsb r1, [r4, #8]
    mov r0, #0
    bl ov001_side_slot_record_021db438
    ldrb r0, [r0, #0x1fe]
    str r0, [r4]
    b ov001_021ff774_L164
ov001_021ff774_L13c:
    cmp r0, #4
    movne r0, #0
    strne r0, [r4]
    bne ov001_021ff774_L164
    ldrh r5, [r4, #12]
    ldr r0, [r4]
    mov r1, r5
    bl native_fn_02026144
    mul r0, r5, r0
    str r0, [r4, #0x4]
ov001_021ff774_L164:
    ldr r0, =0x02239c10
    mov r1, #1
    strb r1, [r0, #0x9]
    b ov001_021ff774_L198
ov001_021ff774_L174:
    add r0, r4, #24
    mov r1, #125
    bl native_fn_02204590
    ldr r0, =0x02239c10
    mov r1, #3
    strb r1, [r0, #0xa]
    add sp, sp, #12
    mov r0, #0
    ldmia sp!, {r4, r5, pc}
ov001_021ff774_L198:
    mov r0, #64
    bl native_fn_022023dc
    mov r0, #133
    bl native_fn_022023c4
    ldr r0, =0x02239c10
    add r2, sp, #8
    ldrsb r1, [r0, #12]
    add r0, r4, #24
    mov r3, #152
    bl native_fn_022044c8
    ldr r2, [r4]
    ldr r1, [r4, #0x4]
    add r0, r4, #24
    sub r1, r2, r1
    bl native_fn_02204558
    ldr r1, =0x02239c10
    mov r0, #5
    strb r0, [r1, #0xa]
    mov r0, #0
    str r0, [r1, #0x10]
    add sp, sp, #12
    ldmia sp!, {r4, r5, pc}
}
