/* ov001 row 0x021f0950: 668 bytes.
 *
 * What it does: 163 instructions; 19 call(s) to 0x021dbe68, 0x020444a8, 0x0207baa0, +16 more; loops (back edge at +0x30); returns through pop {r4, r5, r6, r7, r8, r9, r10, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: loop with 19 calls (163 instructions, 19 calls, 25 branches, 19 back edges, 4 literal slots).
 *
 *   pool +0x28c -> constant 0x66666667 (image word 0x66666667)
 *   pool +0x290 -> constant 0x51eb851f (image word 0x51eb851f)
 *   pool +0x294 -> native_data_0222df40 (image word 0x0222df40)
 *   pool +0x298 -> native_data_0222df4c (image word 0x0222df4c)
 *   branch +0x24 -> +0x40
 *   branch +0x4c -> +0x5c
 *   branch +0x88 -> +0xc0
 *   branch +0x9c -> +0xb0
 *   branch +0xac -> +0x26c
 *   branch +0xbc -> +0x26c
 *   branch +0xc8 -> +0xe8
 *   branch +0xe4 -> +0x26c
 *   branch +0xf0 -> +0x1b0
 *   branch +0xf8 -> +0x138
 *   branch +0x100 -> +0x26c
 *   branch +0x10c -> +0x26c
 *   branch +0x134 -> +0x26c
 *   branch +0x144 -> +0x158
 *   branch +0x154 -> +0x19c
 *   branch +0x160 -> +0x184
 *   branch +0x180 -> +0x19c
 *   branch +0x1ac -> +0x26c
 *   branch +0x1bc -> +0x26c
 *   branch +0x1c8 -> +0x208
 *   branch +0x204 -> +0x26c
 *   branch +0x218 -> +0x26c
 *   branch +0x22c -> +0x23c
 *   branch +0x238 -> +0x24c
 *   branch +0x248 -> +0x258
 *   test +0x44 cmp r0, #0
 *   test +0x50 cmp r7, #0
 *   test +0x84 cmp r8, r1
 *   test +0x98 cmp r0, #1
 *   test +0xc4 cmp r8, r0
 *   test +0xdc cmp r8, #1
 *   test +0xec cmp r8, r0
 *   test +0xf4 cmp r4, #215
 *   test +0xfc cmp r4, #247
 *   test +0x104 cmp r7, #0
 *   test +0x140 cmp r0, #5
 *   test +0x158 cmp r0, #8
 *   test +0x1b4 cmp r8, r0
 *   test +0x1c4 cmp r8, r0
 *   test +0x214 cmp r0, #0
 *   test +0x228 cmp r1, #0
 *   test +0x234 cmp r0, #0
 *   test +0x274 cmp r0, #0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f0950; the literal pool and
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

extern void native_fn_021dbe68(void);
extern void native_fn_020444a8(void);
extern void native_fn_0207baa0(void);
extern void native_fn_0207afec(void);
extern void native_fn_021dbcbc(void);
extern void ov001_record_field_1f2_021dbd30(void);
extern void native_fn_021dbcf0(void);
extern void native_fn_0203d294(void);
extern void native_fn_0207d198(void);
extern void native_fn_0207b004(void);
extern u8 native_data_0222df40[];
extern u8 native_data_0222df4c[];
extern void native_fn_021f0534(void);


asm u32 native_ov001_021f0950 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, lr}
    sub sp, sp, #8
    movs r7, r0
    moveq r9, #0
    mov r6, r1
    mov r5, r2
    mov r4, r3
    moveq r10, r9
    mvneq r8, #0
    beq ov001_021f0950_L40
    ldr r1, [r7, #0x1e8]
    ldrsh r8, [r1, #42]
    bl native_fn_021dbe68
    ldr r1, [r7, #0x1e8]
    mov r9, r0
    add r10, r1, #70
ov001_021f0950_L40:
    bl native_fn_020444a8
    cmp r0, #0
    movne r12, #0
    bne ov001_021f0950_L5c
    cmp r7, #0
    moveq r12, #0
    ldrneb r12, [r7, #0x31e]
ov001_021f0950_L5c:
    mov r0, r4
    mov r1, r8
    mov r2, r9
    mov r3, r10
    str r12, [sp]
    mov r8, #0
    str r8, [sp, #0x4]
    bl native_fn_0207baa0
    mov r8, r0
    mvn r1, #0
    cmp r8, r1
    bne ov001_021f0950_Lc0
    mov r0, r4
    bl native_fn_0207afec
    ldrb r0, [r0, #0x1e]
    cmp r0, #1
    bne ov001_021f0950_Lb0
    mov r0, r6
    bl native_fn_021dbcbc
    mov r8, r0
    b ov001_021f0950_L26c
ov001_021f0950_Lb0:
    mov r0, r7
    bl ov001_record_field_1f2_021dbd30
    mov r8, r0
    b ov001_021f0950_L26c
ov001_021f0950_Lc0:
    sub r0, r1, #1
    cmp r8, r0
    bne ov001_021f0950_Le8
    mov r0, r7
    bl ov001_record_field_1f2_021dbd30
    add r0, r0, #1
    mov r8, r0, asr #1
    cmp r8, #1
    movlt r8, #1
    b ov001_021f0950_L26c
ov001_021f0950_Le8:
    sub r0, r1, #3
    cmp r8, r0
    bne ov001_021f0950_L1b0
    cmp r4, #215
    beq ov001_021f0950_L138
    cmp r4, #247
    bne ov001_021f0950_L26c
    cmp r7, #0
    moveq r8, #0
    beq ov001_021f0950_L26c
    mov r0, r7
    bl native_fn_021dbcf0
    add r0, r0, #9
    ldr r3, =0x66666667
    mov r1, r0, lsr #31
    smull r2, r0, r3, r0
    add r0, r1, r0, asr #2
    bl native_fn_0203d294
    add r8, r0, #1
    b ov001_021f0950_L26c
ov001_021f0950_L138:
    mov r0, #10
    bl native_fn_0203d294
    cmp r0, #5
    bge ov001_021f0950_L158
    mov r0, r6
    bl native_fn_021dbcbc
    mov r2, r0
    b ov001_021f0950_L19c
ov001_021f0950_L158:
    cmp r0, #8
    mov r0, r6
    bge ov001_021f0950_L184
    bl native_fn_021dbcbc
    mov r1, #6
    mul r1, r0, r1
    ldr r3, =0x66666667
    mov r0, r1, lsr #31
    smull r1, r2, r3, r1
    add r2, r0, r2, asr #2
    b ov001_021f0950_L19c
ov001_021f0950_L184:
    bl native_fn_021dbcbc
    mov r1, r0, lsl #2
    ldr r3, =0x66666667
    mov r0, r1, lsr #31
    smull r1, r2, r3, r1
    add r2, r0, r2, asr #2
ov001_021f0950_L19c:
    mov r0, r10
    mov r1, r4
    bl native_fn_0207d198
    mov r8, r0
    b ov001_021f0950_L26c
ov001_021f0950_L1b0:
    sub r0, r1, #2
    cmp r8, r0
    moveq r8, r5
    beq ov001_021f0950_L26c
    sub r0, r1, #4
    cmp r8, r0
    bne ov001_021f0950_L208
    mov r0, #11
    bl native_fn_0203d294
    ldrb r2, [r7, #0x1fc]
    add r0, r0, #90
    ldr r1, =0x51eb851f
    mov r2, r2, lsl #1
    mul r3, r2, r0
    smull r0, r2, r1, r3
    mov r3, r3, lsr #31
    mov r0, r10
    mov r1, r4
    add r2, r3, r2, asr #5
    bl native_fn_0207d198
    mov r8, r0
    b ov001_021f0950_L26c
ov001_021f0950_L208:
    mov r0, r4
    mov r1, #536870912
    bl native_fn_0207b004
    cmp r0, #0
    beq ov001_021f0950_L26c
    ldrb r1, [r7, #0x31e]
    add r0, r7, #512
    ldrsb r5, [r0, #52]
    cmp r1, #0
    beq ov001_021f0950_L23c
    bl native_fn_020444a8
    cmp r0, #0
    beq ov001_021f0950_L24c
ov001_021f0950_L23c:
    ldr r0, =native_data_0222df40
    add r1, r5, #4
    ldrb r0, [r0, r1]
    b ov001_021f0950_L258
ov001_021f0950_L24c:
    ldr r0, =native_data_0222df4c
    add r1, r5, #4
    ldrb r0, [r0, r1]
ov001_021f0950_L258:
    mul r1, r8, r0
    ldr r2, =0x66666667
    mov r0, r1, lsr #31
    smull r1, r8, r2, r1
    add r8, r0, r8, asr #2
ov001_021f0950_L26c:
    ldr r0, [sp, #0x28]
    mov r1, r4
    cmp r0, #0
    movne r8, r8, lsl #1
    mov r0, r8
    bl native_fn_021f0534
    add sp, sp, #8
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
}
