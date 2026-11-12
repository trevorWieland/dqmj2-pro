/* ov001 row 0x0221157c: 324 bytes.
 *
 * What it does: 80 instructions; 15 call(s) to 0x022068a0, 0x022117e4, 0x021f1a44, +12 more; loops (back edge at +0x0c); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 15 calls (80 instructions, 15 calls, 2 branches, 12 back edges, 1 literal slot).
 *
 *   pool +0x140 -> constant 0x0223e120 (image word 0x0223e120)
 *   back edge +0x50 -> +0x3c
 *   branch +0x78 -> +0xfc
 *   branch +0x88 -> +0xfc
 *   back edge +0x114 -> +0x6c
 *   test +0x48 cmp r0, #3
 *   test +0x74 cmp r0, #0
 *   test +0x84 cmp r0, #0
 *   test +0x108 cmp r6, #3
 *   0 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221157c; the literal pool and
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

extern void native_fn_022068a0(void);
extern void native_fn_022117e4(void);
extern void native_fn_021f1a44(void);
extern void ov001_side_slot_record_021db438(void);
extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_021dbd24(void);
extern void native_fn_0220723c(void);
extern void native_fn_0206d250(void);
extern void native_fn_02212818(void);
extern void native_fn_02204b5c(void);
extern void native_fn_02204250(void);
extern void native_fn_02211860(void);


asm u32 native_ov001_0221157c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r7, r0
    str r1, [sp]
    bl native_fn_022068a0
    mov r11, r0
    mov r0, r7
    mov r1, #48
    mov r2, #168
    bl native_fn_022117e4
    mov r10, r0
    bl native_fn_021f1a44
    mov r9, r0
    ldr r2, =0x0223e120
    mov r0, #0
    mov r1, #127
ov001_0221157c_L3c:
    add r0, r0, #1
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    cmp r0, #3
    strb r1, [r2], #1
    blt ov001_0221157c_L3c
    mov r0, #0
    mov r1, r0
    bl ov001_side_slot_record_021db438
    ldr r5, =0x0223e120
    mov r4, r0
    mov r6, #0
ov001_0221157c_L6c:
    mov r0, r4
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_0221157c_Lfc
    mov r0, r4
    bl native_fn_021dbd24
    cmp r0, #0
    beq ov001_0221157c_Lfc
    mov r0, r6
    bl native_fn_0220723c
    mov r0, r0, lsl #24
    add r0, r11, r0, asr #19
    ldr r0, [r0, #0x28]
    ldrb r1, [r0, #0x5]
    ldrsb r0, [r0, #12]
    add r8, r1, #36
    bl native_fn_0206d250
    add r0, r0, r0, lsl #2
    mov r0, r0, asr #1
    mov r0, r0, lsl #3
    and r0, r0, #255
    add r8, r8, r0
    mov r0, #1
    bl native_fn_02212818
    mov r0, r8, lsl #16
    mov r3, r0, asr #16
    mov r0, r4
    mov r1, r7
    mov r2, #156
    bl native_fn_02204b5c
    mov r8, r0
    bl native_fn_02204250
    strb r10, [r0, #0x8]
    add r0, r9, r6
    strb r8, [r0, #0x9]
    strb r8, [r5]
ov001_0221157c_Lfc:
    add r0, r6, #1
    mov r0, r0, lsl #24
    mov r6, r0, asr #24
    cmp r6, #3
    add r5, r5, #1
    add r4, r4, #1088
    blt ov001_0221157c_L6c
    ldrsh r2, [r9, #22]
    ldr r0, [sp]
    mov r1, #160
    bl native_fn_02211860
    mov r4, r0
    bl native_fn_021f1a44
    strb r10, [r0, #0x8]
    mov r0, r10
    strb r4, [r9, #0xc]
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
