/* ov001 row 0x021ffc00: 824 bytes.
 *
 * What it does: 205 instructions; 29 call(s) to 0x02202360, 0x022042c4, 0x021db530, +26 more; loops (back edge at +0x7c); returns through pop {r4, r5, r6, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 29 calls (205 instructions, 29 calls, 21 branches, 11 back edges, 1 literal slot).
 *
 *   pool +0x334 -> constant 0x02239c10 (image word 0x02239c10)
 *   branch +0x30 -> +0x2f0
 *   branch +0x34 -> +0x2f0
 *   branch +0x38 -> +0x54
 *   branch +0x3c -> +0x4c
 *   branch +0x40 -> +0x2a0
 *   branch +0x44 -> +0x200
 *   branch +0x48 -> +0x2f0
 *   branch +0x5c -> +0xbc
 *   branch +0x74 -> +0xb0
 *   branch +0xb8 -> +0x1f4
 *   branch +0xcc -> +0xd8
 *   branch +0x118 -> +0x12c
 *   branch +0x128 -> +0x164
 *   branch +0x138 -> +0x1f4
 *   branch +0x160 -> +0x1f4
 *   branch +0x170 -> +0x1f4
 *   branch +0x1a0 -> +0x1f0
 *   branch +0x1fc -> +0x2f0
 *   branch +0x218 -> +0x254
 *   branch +0x250 -> +0x288
 *   branch +0x29c -> +0x2f0
 *   test +0x28 cmp r1, #5
 *   test +0x58 cmp r0, #2
 *   test +0x64 cmp r0, #1
 *   test +0xc4 cmp r0, #5
 *   test +0x114 cmp r5, r1
 *   test +0x124 cmp r0, #0
 *   test +0x130 cmp r5, r0
 *   test +0x168 cmp r6, r0
 *   test +0x19c cmp r0, r5
 *   test +0x214 cmp r0, #0
 *   test +0x2fc cmp r1, #0
 *   0 block transfer(s), 40 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021ffc00; the literal pool and
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

extern void native_fn_02202360(void);
extern void native_fn_022042c4(void);
extern void native_fn_021db530(void);
extern void native_fn_022029a8(void);
extern void native_fn_02049748(void);
extern void native_fn_022023f8(void);
extern void native_fn_022011c0(void);
extern void native_fn_0220451c(void);
extern void native_fn_021fe3dc(void);
extern void native_fn_022023c4(void);
extern void native_fn_022028fc(void);
extern void native_fn_022043f0(void);
extern void native_fn_021fe2b8(void);
extern void native_fn_021feeb4(void);


asm u32 native_ov001_021ffc00 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    sub sp, sp, #8
    ldr r0, =0x02239c10
    ldrsb r0, [r0, #12]
    bl native_fn_02202360
    ldr r1, =0x02239c10
    mov r2, #0
    strb r2, [r1, #0x7]
    ldrsb r1, [r1, #12]
    mov r4, r0
    cmp r1, #5
    addls pc, pc, r1, lsl #2
    b ov001_021ffc00_L2f0
    b ov001_021ffc00_L2f0
    b ov001_021ffc00_L54
    b ov001_021ffc00_L4c
    b ov001_021ffc00_L2a0
    b ov001_021ffc00_L200
    b ov001_021ffc00_L2f0
ov001_021ffc00_L4c:
    add r0, r4, #96
    bl native_fn_022042c4
ov001_021ffc00_L54:
    ldrb r0, [r4, #0x13]
    cmp r0, #2
    bne ov001_021ffc00_Lbc
    ldrb r0, [r4, #0x14]
    cmp r0, #1
    ldrne r0, =0x02239c10
    movne r1, #0
    strneb r1, [r0, #0x7]
    bne ov001_021ffc00_Lb0
    mov r0, #1
    bl native_fn_021db530
    strb r0, [r4, #0xb]
    mov r1, #1
    str r1, [sp]
    mov r2, #0
    str r2, [sp, #0x4]
    ldrb r3, [r4, #0xb]
    mov r0, r4
    bl native_fn_022029a8
    strb r0, [r4, #0xa]
    ldr r1, =0x02239c10
    mov r0, #1
    strb r0, [r1, #0x7]
ov001_021ffc00_Lb0:
    mov r0, #3
    strb r0, [r4, #0x13]
    b ov001_021ffc00_L1f4
ov001_021ffc00_Lbc:
    ldr r0, [r4, #0x60]
    ldrsb r5, [r4, #18]
    cmp r0, #5
    ldrsb r6, [r4, #8]
    bne ov001_021ffc00_Ld8
    add r0, r4, #96
    bl native_fn_022042c4
ov001_021ffc00_Ld8:
    mov r0, r4
    bl native_fn_02049748
    ldr r1, =0x02239c10
    mov r0, #0
    ldrsb r2, [r1, #12]
    mov r1, #1
    strb r2, [r4, #0x10]
    strb r0, [r4, #0x14]
    strb r1, [r4, #0x13]
    bl native_fn_021db530
    mov r3, #0
    sub r1, r3, #1
    ldr r2, =0x02239c10
    strb r0, [r4, #0x9]
    strb r3, [r2, #0x7]
    cmp r5, r1
    beq ov001_021ffc00_L12c
    mov r0, #64
    bl native_fn_022023f8
    cmp r0, #0
    bne ov001_021ffc00_L164
ov001_021ffc00_L12c:
    mvn r0, #0
    cmp r5, r0
    strneb r5, [r4, #0x8]
    bne ov001_021ffc00_L1f4
    mov r0, #1
    str r0, [sp]
    str r0, [sp, #0x4]
    ldrb r3, [r4, #0x9]
    mov r1, #0
    mov r0, r4
    mov r2, r1
    bl native_fn_022029a8
    strb r0, [r4, #0x8]
    b ov001_021ffc00_L1f4
ov001_021ffc00_L164:
    mvn r0, #0
    cmp r6, r0
    streqb r5, [r4, #0x8]
    beq ov001_021ffc00_L1f4
    mov r0, #1
    str r0, [sp]
    str r0, [sp, #0x4]
    add r0, r5, #1
    mov r1, r0, lsl #24
    ldrb r3, [r4, #0x9]
    mov r0, r4
    mov r2, r1, asr #24
    mov r1, #0
    bl native_fn_022029a8
    cmp r0, r5
    bgt ov001_021ffc00_L1f0
    mov r0, #0
    bl native_fn_02202360
    mov r5, r0
    bl native_fn_022011c0
    mov r2, #0
    str r2, [r5]
    ldr r1, [r5, #0x4]
    mov r4, r0
    add r0, r5, #24
    rsb r1, r1, #0
    bl native_fn_0220451c
    mov r0, #1
    mov r1, #0
    bl native_fn_021fe3dc
    mov r0, #141
    bl native_fn_022023c4
    add sp, sp, #8
    mov r0, r4
    ldmia sp!, {r4, r5, r6, pc}
ov001_021ffc00_L1f0:
    strb r0, [r4, #0x8]
ov001_021ffc00_L1f4:
    mov r0, #141
    bl native_fn_022023c4
    b ov001_021ffc00_L2f0
ov001_021ffc00_L200:
    bl native_fn_02049748
    ldr r0, =0x02239c10
    ldrsb r0, [r0, #12]
    strb r0, [r4, #0x10]
    ldrb r0, [r4, #0x14]
    cmp r0, #0
    bne ov001_021ffc00_L254
    mov r0, #0
    bl native_fn_021db530
    strb r0, [r4, #0x9]
    mov r0, #1
    str r0, [sp]
    mov r1, #0
    ldrb r3, [r4, #0x9]
    mov r0, r4
    mov r2, r1
    bl native_fn_022028fc
    strb r0, [r4, #0x8]
    ldr r1, =0x02239c10
    mov r0, #0
    b ov001_021ffc00_L288
ov001_021ffc00_L254:
    mov r0, #1
    bl native_fn_021db530
    strb r0, [r4, #0xb]
    mov r1, #1
    str r1, [sp]
    mov r2, #0
    str r2, [sp, #0x4]
    ldrb r3, [r4, #0xb]
    mov r0, r4
    bl native_fn_022029a8
    strb r0, [r4, #0xa]
    ldr r1, =0x02239c10
    mov r0, #1
ov001_021ffc00_L288:
    strb r0, [r1, #0x7]
    mov r1, #1
    mov r0, #141
    strb r1, [r4, #0x13]
    bl native_fn_022023c4
    b ov001_021ffc00_L2f0
ov001_021ffc00_L2a0:
    bl native_fn_02049748
    ldr r1, =0x02239c10
    mov r0, #1
    ldrsb r1, [r1, #12]
    strb r1, [r4, #0x10]
    bl native_fn_021db530
    strb r0, [r4, #0xb]
    mov r1, #1
    str r1, [sp]
    mov r2, #0
    str r2, [sp, #0x4]
    ldrb r3, [r4, #0xb]
    mov r0, r4
    bl native_fn_022029a8
    strb r0, [r4, #0xa]
    mov r1, #1
    strb r1, [r4, #0x14]
    mov r0, #141
    strb r1, [r4, #0x13]
    bl native_fn_022023c4
ov001_021ffc00_L2f0:
    ldrb r1, [r4, #0x14]
    add r0, r4, #168
    mov r3, #107
    cmp r1, #0
    ldreqsb r2, [r4, #8]
    ldrnesb r2, [r4, #10]
    bl native_fn_022043f0
    mov r0, #1
    mov r1, r0
    bl native_fn_021fe2b8
    bl native_fn_021feeb4
    ldr r0, =0x02239c10
    mov r1, #7
    strb r1, [r0, #0xa]
    mov r0, #1
    add sp, sp, #8
    ldmia sp!, {r4, r5, r6, pc}
}
