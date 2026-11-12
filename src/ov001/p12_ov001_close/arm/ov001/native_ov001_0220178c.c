/* ov001 row 0x0220178c: 348 bytes.
 *
 * What it does: 82 instructions; 17 call(s) to 0x02049ae4, 0x02202360, 0x022021fc, +14 more; loops (back edge at +0x04); returns through pop {r3, r4, r5, pc}; 5 literal slot(s) in the extent
 *
 * Decoded shape: loop with 17 calls (82 instructions, 17 calls, 7 branches, 10 back edges, 5 literal slots).
 *
 *   pool +0x148 -> constant 0x02239c10 (image word 0x02239c10)
 *   pool +0x14c -> native_data_0222ed34 (image word 0x0222ed34)
 *   pool +0x150 -> constant 0x04001040 (image word 0x04001040)
 *   pool +0x154 -> constant 0x0000e0f0 (image word 0x0000e0f0)
 *   pool +0x158 -> constant 0x00006070 (image word 0x00006070)
 *   branch +0x30 -> +0x40
 *   branch +0x44 -> +0x78
 *   branch +0x54 -> +0x64
 *   branch +0x11c -> +0x138
 *   test +0x1c cmp r0, #8
 *   test +0x2c cmp r0, #0
 *   test +0x38 cmp r0, #1
 *   test +0x40 cmp r5, #0
 *   test +0x50 cmp r0, #5
 *   test +0x118 cmp r0, #0
 *   0 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0220178c; the literal pool and
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

extern void native_fn_02049ae4(void);
extern void ov001_table_f0_entry_02202360(void);
extern void native_fn_022021fc(void);
extern void native_fn_0204458c(void);
extern void native_fn_021ff238(void);
extern void native_fn_021e13a8(void);
extern void native_fn_021fd82c(void);
extern void native_fn_021fe3d0(void);
extern void native_fn_02086b14(void);
extern u8 native_data_0222ed34[];
extern void native_fn_02206888(void);
extern void native_fn_021fea80(void);
extern void native_fn_022032b0(void);
extern void native_fn_02203070(void);
extern void native_fn_02204590(void);
extern void native_fn_0220451c(void);


asm u32 native_ov001_0220178c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    bl native_fn_02049ae4
    mov r0, #0
    bl ov001_table_f0_entry_02202360
    ldr r1, =0x02239c10
    mov r4, r0
    ldrsb r0, [r1, #4]
    cmp r0, #8
    ldmneia sp!, {r3, r4, r5, pc}
    mov r5, #0
    bl native_fn_022021fc
    cmp r0, #0
    bne ov001_0220178c_L40
    bl native_fn_0204458c
    cmp r0, #1
    moveq r5, #1
ov001_0220178c_L40:
    cmp r5, #0
    bne ov001_0220178c_L78
    ldr r0, =0x02239c10
    ldrsb r0, [r0, #13]
    cmp r0, #5
    beq ov001_0220178c_L64
    mov r0, #1
    bl native_fn_021ff238
    ldmia sp!, {r3, r4, r5, pc}
ov001_0220178c_L64:
    mov r0, #4
    bl native_fn_021e13a8
    mov r0, #1
    bl native_fn_021ff238
    ldmia sp!, {r3, r4, r5, pc}
ov001_0220178c_L78:
    bl native_fn_02049ae4
    mov r5, r0
    bl native_fn_021fd82c
    mov r0, #1
    mov r1, r0
    mov r2, #12
    bl native_fn_021fe3d0
    ldr r2, [r5, #0x4]
    mov r1, #10
    ldr r0, [r2, #0x18]
    orr r0, r0, #2
    str r0, [r2, #0x18]
    ldr r0, [r5, #0x4]
    bl native_fn_02086b14
    ldr r0, =native_data_0222ed34
    mov r1, #1
    ldrsb r0, [r0, #3]
    bl native_fn_02206888
    ldr r2, =0x04001040
    ldr r1, =0x0000e0f0
    ldr r0, =0x00006070
    strh r1, [r2]
    strh r0, [r2, #4]
    ldrh r0, [r2, #8]
    sub r1, r2, #64
    bic r0, r0, #63
    orr r0, r0, #31
    strh r0, [r2, #8]
    ldrh r0, [r2, #10]
    bic r0, r0, #63
    orr r0, r0, #63
    strh r0, [r2, #10]
    ldr r0, [r1]
    bic r0, r0, #57344
    orr r0, r0, #8192
    str r0, [r1]
    bl native_fn_021fea80
    bl native_fn_022032b0
    bl native_fn_02203070
    ldr r0, [r4, #0x34]
    cmp r0, #0
    beq ov001_0220178c_L138
    add r0, r4, #24
    mov r1, #125
    bl native_fn_02204590
    ldr r1, [r4]
    add r0, r4, #24
    bl native_fn_0220451c
ov001_0220178c_L138:
    ldr r0, =0x02239c10
    mov r1, #10
    strb r1, [r0, #0xa]
    ldmia sp!, {r3, r4, r5, pc}
}
