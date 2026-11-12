/* ov001 row 0x0220f600: 616 bytes.
 *
 * What it does: 154 instructions; 17 call(s) to 0x0220e910, 0x02209490, 0x0207b004, +14 more; loops (back edge at +0x20); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: loop with 17 calls (154 instructions, 17 calls, 15 branches, 12 back edges, 0 literal slots).
 *
 *   branch +0x3c -> +0x238
 *   branch +0x44 -> +0x8c
 *   branch +0x58 -> +0x8c
 *   branch +0x68 -> +0x8c
 *   branch +0x9c -> +0xe4
 *   branch +0xb0 -> +0xe4
 *   branch +0xc0 -> +0xe4
 *   branch +0xf8 -> +0x134
 *   branch +0x148 -> +0x184
 *   branch +0x194 -> +0x1e4
 *   branch +0x1a0 -> +0x1e4
 *   branch +0x1a8 -> +0x1e4
 *   branch +0x1f8 -> +0x234
 *   branch +0x23c -> +0x254
 *   back edge +0x250 -> +0x40
 *   test +0x40 cmp r0, #10
 *   test +0x54 cmp r0, #0
 *   test +0x64 cmp r0, #0
 *   test +0x7c cmp r0, #0
 *   test +0x98 cmp r0, #49
 *   test +0xac cmp r0, #0
 *   test +0xbc cmp r0, #0
 *   test +0xd4 cmp r0, #0
 *   test +0xf0 cmp r0, #11
 *   test +0xf4 cmpeq r8, #0
 *   test +0x120 cmp r0, #0
 *   test +0x124 cmpne r7, #0
 *   test +0x140 cmp r0, #12
 *   test +0x144 cmpeq r8, #0
 *   test +0x170 cmp r0, #0
 *   test +0x174 cmpne r7, #0
 *   test +0x190 cmp r0, #63
 *   test +0x19c cmp r0, #0
 *   test +0x1a4 cmp r8, #0
 *   test +0x1d0 cmp r0, #0
 *   test +0x1d4 cmpne r7, #0
 *   test +0x1f0 cmp r0, #67
 *   test +0x1f4 cmpeq r8, #0
 *   test +0x220 cmp r0, #0
 *   test +0x224 cmpne r7, #0
 *   test +0x238 cmp r6, #64
 *   test +0x24c cmp r0, #0
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0220f600; the literal pool and
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

extern void native_fn_0220e910(void);
extern void native_fn_02209490(void);
extern void native_fn_0207b004(void);
extern void native_fn_0220f470(void);
extern void native_fn_02210ad0(void);
extern void native_fn_021d908c(void);
extern void native_fn_0220f530(void);


asm u32 native_ov001_0220f600 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r10, r0
    ldrb r0, [r10, #0x31e]
    mov r9, r1
    mov r8, r2
    mov r1, #8
    mov r2, #3
    mov r7, r3
    bl native_fn_0220e910
    mov r5, r0
    add r0, r10, #556
    bl native_fn_02209490
    mov r4, r0
    mov r6, #0
    add r11, r9, #512
    b ov001_0220f600_L238
ov001_0220f600_L40:
    cmp r0, #10
    bne ov001_0220f600_L8c
    mov r0, r8
    mov r1, #4194304
    bl native_fn_0207b004
    cmp r0, #0
    beq ov001_0220f600_L8c
    mov r0, r9
    bl native_fn_0220f470
    cmp r0, #0
    beq ov001_0220f600_L8c
    mov r0, r9
    mov r1, #2
    mov r2, #1
    bl native_fn_02210ad0
    cmp r0, #0
    ldrne r0, [r9, #0x33c]
    orrne r0, r0, #512
    strne r0, [r9, #0x33c]
ov001_0220f600_L8c:
    ldr r0, [r9, #0x1e8]
    add r0, r0, r6
    ldrb r0, [r0, #0x46]
    cmp r0, #49
    bne ov001_0220f600_Le4
    mov r0, r8
    mov r1, #4194304
    bl native_fn_0207b004
    cmp r0, #0
    beq ov001_0220f600_Le4
    mov r0, r9
    bl native_fn_0220f470
    cmp r0, #0
    beq ov001_0220f600_Le4
    mov r0, r9
    mov r1, #4
    mov r2, #1
    bl native_fn_02210ad0
    cmp r0, #0
    ldrne r0, [r9, #0x33c]
    orrne r0, r0, #8388608
    strne r0, [r9, #0x33c]
ov001_0220f600_Le4:
    ldr r0, [r9, #0x1e8]
    add r0, r0, r6
    ldrb r0, [r0, #0x46]
    cmp r0, #11
    cmpeq r8, #0
    bne ov001_0220f600_L134
    ldr r1, [r10, #0x1e8]
    mov r0, r5
    ldrb r1, [r1, #0x91]
    mov r2, r4
    bl native_fn_021d908c
    mov r2, r0
    mov r0, r9
    mov r1, #100
    bl native_fn_02210ad0
    cmp r0, #0
    cmpne r7, #0
    ldrne r0, [r9, #0x33c]
    orrne r0, r0, #8
    strne r0, [r9, #0x33c]
ov001_0220f600_L134:
    ldr r0, [r9, #0x1e8]
    add r0, r0, r6
    ldrb r0, [r0, #0x46]
    cmp r0, #12
    cmpeq r8, #0
    bne ov001_0220f600_L184
    ldr r1, [r10, #0x1e8]
    mov r0, r5
    ldrb r1, [r1, #0x98]
    mov r2, r4
    bl native_fn_021d908c
    mov r2, r0
    mov r0, r9
    mov r1, #100
    bl native_fn_02210ad0
    cmp r0, #0
    cmpne r7, #0
    ldrne r0, [r9, #0x33c]
    orrne r0, r0, #16
    strne r0, [r9, #0x33c]
ov001_0220f600_L184:
    ldr r0, [r9, #0x1e8]
    add r0, r0, r6
    ldrb r0, [r0, #0x46]
    cmp r0, #63
    bne ov001_0220f600_L1e4
    ldrsb r0, [r11, #53]
    cmp r0, #0
    beq ov001_0220f600_L1e4
    cmp r8, #0
    bne ov001_0220f600_L1e4
    ldr r1, [r10, #0x1e8]
    mov r0, r5
    ldrb r1, [r1, #0x98]
    mov r2, r4
    bl native_fn_021d908c
    mov r2, r0
    mov r0, r9
    mov r1, #100
    bl native_fn_02210ad0
    cmp r0, #0
    cmpne r7, #0
    ldrne r0, [r9, #0x33c]
    orrne r0, r0, #32
    strne r0, [r9, #0x33c]
ov001_0220f600_L1e4:
    ldr r0, [r9, #0x1e8]
    add r0, r0, r6
    ldrb r0, [r0, #0x46]
    cmp r0, #67
    cmpeq r8, #0
    bne ov001_0220f600_L234
    ldr r1, [r10, #0x1e8]
    mov r0, r5
    ldrb r1, [r1, #0x92]
    mov r2, r4
    bl native_fn_021d908c
    mov r2, r0
    mov r0, r9
    mov r1, #100
    bl native_fn_02210ad0
    cmp r0, #0
    cmpne r7, #0
    ldrne r0, [r9, #0x33c]
    orrne r0, r0, #16777216
    strne r0, [r9, #0x33c]
ov001_0220f600_L234:
    add r6, r6, #1
ov001_0220f600_L238:
    cmp r6, #64
    bge ov001_0220f600_L254
    ldr r0, [r9, #0x1e8]
    add r0, r0, r6
    ldrb r0, [r0, #0x46]
    cmp r0, #0
    bne ov001_0220f600_L40
ov001_0220f600_L254:
    ldr r1, [sp, #0x28]
    mov r0, r9
    bl native_fn_0220f530
    ldr r0, [r9, #0x33c]
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
