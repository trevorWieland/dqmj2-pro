/* ov000 row 0x021f72d0: 580 bytes.
 *
 * What it does: 142 instructions; 23 call(s) to 0x02061944, 0x0201d444, 0x0205ff80, +20 more; loops (back edge at +0x08); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x238 -> native_data_0222f338 (image word 0x0222f338)
 *   pool +0x23c -> native_data_0222b9a0 (image word 0x0222b9a0)
 *   pool +0x240 -> constant 0x00009999 (image word 0x00009999)
 *   back edge +0x78 -> +0x34
 *   branch +0xc0 -> +0xcc
 *   branch +0xf0 -> +0x160
 *   branch +0x108 -> +0x118
 *   back edge +0x15c -> +0xe8
 *   branch +0x198 -> +0x1a8
 *   branch +0x1b8 -> +0x204
 *   back edge +0x200 -> +0x1c4
 *   back edge +0x22c -> +0x180
 *   test +0x70 cmp r6, #15
 *   test +0xbc cmp r1, #28
 *   test +0xec cmp r9, r0
 *   test +0x104 cmp r1, #28
 *   test +0x154 cmp r10, #3
 *   test +0x16c cmp r0, #0
 *   test +0x194 cmp r1, #28
 *   test +0x1b4 cmp r0, #0
 *   test +0x1fc cmp r0, r4, asr #24
 *   test +0x21c cmp r0, r2, asr #24
 *   0 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f72d0; the literal pool and
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

extern void native_fn_02061944(void);
extern u8 native_data_0222f338[];
extern void native_fn_0201d444(void);
extern void native_fn_0205ff80(void);
extern u8 native_data_0222b9a0[];
extern void native_fn_02065730(void);
extern void native_fn_0205ff9c(void);
extern void native_fn_021f77b4(void);
extern void native_fn_02061de4(void);
extern void native_fn_02062aa0(void);
extern void native_fn_02062ad0(void);
extern void native_fn_02062a50(void);
extern void native_fn_02062a88(void);
extern void native_fn_02044cdc(void);


asm u32 native_ov000_021f72d0 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #44
    bl native_fn_02061944
    mov r7, r0
    ldr r1, =native_data_0222f338
    add r0, sp, #12
    bl native_fn_0201d444
    add r0, sp, #12
    bl native_fn_0205ff80
    mov r6, #0
    ldr r5, =native_data_0222b9a0
    add r8, r7, #16
    mov r4, r6
ov000_021f72d0_L34:
    ldr r0, [r7, #0x25c]
    mov r1, r6, lsl #1
    str r0, [sp]
    add r0, r5, r6, lsl #1
    ldrsb r1, [r5, r1]
    ldrb r3, [r0, #0x1]
    mov r0, r8
    mov r2, r4
    bl native_fn_02065730
    add r1, r6, #1
    ldr r2, [r7, #0x25c]
    mov r1, r1, lsl #24
    add r0, r2, r0
    mov r6, r1, asr #24
    str r0, [r7, #0x25c]
    cmp r6, #15
    add r8, r8, #12
    blt ov000_021f72d0_L34
    bl native_fn_0205ff9c
    mov r0, #1
    mov r1, r0
    mov r2, r0
    bl native_fn_021f77b4
    mov r4, #0
    ldr r1, =0x00009999
    add r0, r7, #28
    mov r2, #6
    mov r3, #1
    str r4, [sp]
    bl native_fn_02061de4
    bl native_fn_02062aa0
    add r1, r7, #512
    ldrsb r1, [r1, #105]
    str r0, [sp, #0x4]
    cmp r1, #28
    blt ov000_021f72d0_Lcc
    bl native_fn_02062ad0
    str r0, [sp, #0x4]
ov000_021f72d0_Lcc:
    mov r9, #0
    mov r10, r9
    add r6, r7, #16
    add r5, r7, #512
    mov r8, r9
    mov r11, #1
    mov r4, #12
ov000_021f72d0_Le8:
    ldr r0, [sp, #0x4]
    cmp r9, r0
    bge ov000_021f72d0_L160
    mov r0, r9
    bl native_fn_02062a50
    ldrsb r1, [r5, #105]
    mov r2, r0
    cmp r1, #28
    blt ov000_021f72d0_L118
    mov r0, r9
    bl native_fn_02062a88
    mov r2, r0
ov000_021f72d0_L118:
    add r1, r10, #2
    mla r0, r1, r4, r6
    str r8, [sp]
    ldrsh r1, [r2, #24]
    mov r2, r10
    mov r3, r11
    bl native_fn_02061de4
    add r0, r10, r0
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    add r0, r0, #1
    add r2, r9, #1
    mov r1, r0, lsl #24
    mov r0, r2, lsl #24
    mov r10, r1, asr #24
    cmp r10, #3
    mov r9, r0, asr #24
    blt ov000_021f72d0_Le8
ov000_021f72d0_L160:
    ldr r0, [sp, #0x4]
    mov r9, #0
    str r9, [sp, #0x8]
    cmp r0, #0
    mov r6, #8
    addle sp, sp, #44
    ldmleia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    mov r11, #1
ov000_021f72d0_L180:
    mov r0, r9
    bl native_fn_02062a50
    add r1, r7, #512
    ldrsb r1, [r1, #105]
    mov r10, r0
    cmp r1, #28
    blt ov000_021f72d0_L1a8
    mov r0, r9
    bl native_fn_02062a88
    mov r10, r0
ov000_021f72d0_L1a8:
    ldrsh r0, [r10, #24]
    mov r5, #0
    bl native_fn_02044cdc
    cmp r0, #0
    blt ov000_021f72d0_L204
    ldr r0, [sp, #0x8]
    add r8, r0, #2
ov000_021f72d0_L1c4:
    mov r0, r8, lsl #24
    mov r1, r11
    mov r2, r6
    mov r0, r0, asr #24
    bl native_fn_021f77b4
    add r1, r6, #5
    add r0, r5, #1
    mov r1, r1, lsl #24
    mov r4, r0, lsl #24
    ldrsh r0, [r10, #24]
    mov r6, r1, asr #24
    add r8, r8, #1
    mov r5, r4, asr #24
    bl native_fn_02044cdc
    cmp r0, r4, asr #24
    bge ov000_021f72d0_L1c4
ov000_021f72d0_L204:
    ldr r0, [sp, #0x8]
    add r1, r0, r5
    add r0, r9, #1
    mov r2, r0, lsl #24
    ldr r0, [sp, #0x4]
    mov r1, r1, lsl #24
    cmp r0, r2, asr #24
    mov r0, r1, asr #24
    str r0, [sp, #0x8]
    mov r9, r2, asr #24
    bgt ov000_021f72d0_L180
    add sp, sp, #44
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
