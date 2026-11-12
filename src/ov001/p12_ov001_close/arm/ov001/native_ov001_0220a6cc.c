/* ov001 row 0x0220a6cc: 688 bytes.
 *
 * What it does: 170 instructions; 27 call(s) to 0x02068bd4, 0x02062a50, 0x021dc2f8, +24 more; loops (back edge at +0x1c); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: block fill (170 instructions, 27 calls, 13 branches, 27 back edges, 2 literal slots).
 *
 *   pool +0x2a8 -> constant 0x0223df2c (image word 0x0223df2c)
 *   pool +0x2ac -> native_data_0222f0dc (image word 0x0222f0dc)
 *   branch +0x44 -> +0xb0
 *   branch +0x58 -> +0x70
 *   branch +0x6c -> +0x7c
 *   branch +0x78 -> +0x84
 *   back edge +0xb8 -> +0x38
 *   branch +0xe4 -> +0x150
 *   branch +0xf8 -> +0x110
 *   branch +0x10c -> +0x11c
 *   branch +0x118 -> +0x124
 *   back edge +0x158 -> +0xd8
 *   branch +0x174 -> +0x1b8
 *   branch +0x17c -> +0x18c
 *   branch +0x188 -> +0x1b8
 *   branch +0x1b4 -> +0x1e0
 *   branch +0x264 -> +0x284
 *   back edge +0x28c -> +0x238
 *   test +0x54 cmp r0, #0
 *   test +0x68 cmp r0, #0
 *   test +0xb4 cmp r8, #3
 *   test +0xf4 cmp r0, #0
 *   test +0x108 cmp r0, #0
 *   test +0x154 cmp r10, #3
 *   test +0x170 cmp r1, #3
 *   test +0x178 cmp r0, #2
 *   test +0x184 cmp r0, #0
 *   test +0x250 cmp r0, #0
 *   test +0x258 cmpne r1, #0
 *   test +0x260 cmpne r0, #0
 *   test +0x288 cmp r5, #6
 *   2 block transfer(s), 13 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0220a6cc; the literal pool and
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

extern void native_fn_02068bd4(void);
extern void native_fn_02062a50(void);
extern void native_fn_021dc2f8(void);
extern void native_fn_020692b0(void);
extern void native_fn_02044cdc(void);
extern void native_fn_02062a88(void);
extern void native_fn_02062a10(void);
extern void native_fn_0203d128(void);
extern void native_fn_02068c14(void);
extern u8 native_data_0222f0dc[];
extern void native_fn_020451c4(void);
extern void native_fn_020482b4(void);
extern void native_fn_0204532c(void);
extern void native_fn_0206c0a0(void);
extern void native_fn_0206c718(void);
extern void native_fn_02048308(void);


asm u32 native_ov001_0220a6cc (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #20
    ldr r1, =0x0223df2c
    str r0, [sp, #0xc]
    ldr r0, [r1, #0x4]
    mov r1, #0
    str r1, [sp, #0x10]
    bl native_fn_02068bd4
    mov r9, #0
    mov r8, r9
    mov r5, #18
    mov r7, #12
    mov r6, #15
    mov r4, r9
ov001_0220a6cc_L38:
    mov r0, r8
    bl native_fn_02062a50
    movs r10, r0
    beq ov001_0220a6cc_Lb0
    ldr r0, [r10, #0x14]
    bl native_fn_021dc2f8
    ldrb r0, [r0, #0x31c]
    cmp r0, #0
    beq ov001_0220a6cc_L70
    ldr r0, [r10, #0x14]
    bl native_fn_021dc2f8
    ldrb r0, [r0, #0x1ff]
    cmp r0, #0
    bne ov001_0220a6cc_L7c
ov001_0220a6cc_L70:
    mov r0, r7
    mov r1, r6
    b ov001_0220a6cc_L84
ov001_0220a6cc_L7c:
    mov r0, r5
    mov r1, r5
ov001_0220a6cc_L84:
    str r4, [sp]
    stmib sp, {r0, r1}
    ldr r0, [r10, #0x14]
    mov r1, r4
    mov r2, r4
    and r3, r9, #255
    bl native_fn_020692b0
    ldrsh r0, [r10, #24]
    bl native_fn_02044cdc
    add r0, r0, #1
    add r9, r9, r0
ov001_0220a6cc_Lb0:
    add r8, r8, #1
    cmp r8, #3
    blt ov001_0220a6cc_L38
    mov r9, #0
    mov r10, r9
    mov r11, #18
    mov r7, #12
    mov r6, #15
    mov r5, r9
    mov r4, #1
ov001_0220a6cc_Ld8:
    mov r0, r10
    bl native_fn_02062a88
    movs r8, r0
    beq ov001_0220a6cc_L150
    ldr r0, [r8, #0x14]
    bl native_fn_021dc2f8
    ldrb r0, [r0, #0x31c]
    cmp r0, #0
    beq ov001_0220a6cc_L110
    ldr r0, [r8, #0x14]
    bl native_fn_021dc2f8
    ldrb r0, [r0, #0x1ff]
    cmp r0, #0
    bne ov001_0220a6cc_L11c
ov001_0220a6cc_L110:
    mov r0, r7
    mov r1, r6
    b ov001_0220a6cc_L124
ov001_0220a6cc_L11c:
    mov r0, r11
    mov r1, r11
ov001_0220a6cc_L124:
    str r5, [sp]
    stmib sp, {r0, r1}
    ldr r0, [r8, #0x14]
    mov r1, r4
    mov r2, r5
    and r3, r9, #255
    bl native_fn_020692b0
    ldrsh r0, [r8, #24]
    bl native_fn_02044cdc
    add r0, r0, #1
    add r9, r9, r0
ov001_0220a6cc_L150:
    add r10, r10, #1
    cmp r10, #3
    blt ov001_0220a6cc_Ld8
    ldr r0, [sp, #0xc]
    bl native_fn_02062a10
    ldrsh r0, [r0, #24]
    bl native_fn_02044cdc
    add r1, r9, r0
    cmp r1, #3
    bge ov001_0220a6cc_L1b8
    cmp r0, #2
    bne ov001_0220a6cc_L18c
    bl native_fn_0203d128
    cmp r0, #0
    beq ov001_0220a6cc_L1b8
ov001_0220a6cc_L18c:
    mov r2, #0
    str r2, [sp]
    mov r1, #12
    str r1, [sp, #0x4]
    mov r4, #15
    ldr r0, [sp, #0xc]
    and r3, r9, #255
    mov r1, #1
    str r4, [sp, #0x8]
    bl native_fn_020692b0
    b ov001_0220a6cc_L1e0
ov001_0220a6cc_L1b8:
    mov r2, #0
    str r2, [sp]
    mov r1, #12
    str r1, [sp, #0x4]
    mov r4, #15
    ldr r0, [sp, #0xc]
    mov r3, r2
    mov r1, #2
    str r4, [sp, #0x8]
    bl native_fn_020692b0
ov001_0220a6cc_L1e0:
    mov r0, #2
    mov r1, #36
    mov r2, #32
    mov r3, #0
    bl native_fn_02068c14
    ldr r0, =native_data_0222f0dc
    add r3, sp, #16
    mov r1, #17
    mov r2, #2
    bl native_fn_020451c4
    mov r4, r0
    mov r1, #352
    mov r2, #32
    bl native_fn_020482b4
    mov r1, r4
    mov r0, #2
    bl native_fn_0204532c
    mov r5, #0
    ldr r6, =0x0223df2c
    mov r9, r5
    mov r8, #18
    mov r7, #1
ov001_0220a6cc_L238:
    mov r0, r5, lsl #24
    mov r0, r0, asr #24
    bl native_fn_0206c0a0
    mov r4, r0
    ldr r0, [r4]
    bl native_fn_021dc2f8
    cmp r0, #0
    ldrneb r1, [r0, #0x31c]
    cmpne r1, #0
    ldrneb r0, [r0, #0x1ff]
    cmpne r0, #0
    beq ov001_0220a6cc_L284
    str r9, [sp]
    str r8, [sp, #0x4]
    ldrsb r2, [r4, #12]
    ldr r0, [r6, #0x4]
    mov r1, r7
    mov r3, r7
    bl native_fn_0206c718
ov001_0220a6cc_L284:
    add r5, r5, #1
    cmp r5, #6
    blt ov001_0220a6cc_L238
    bl native_fn_02048308
    ldr r0, =0x0223df2c
    mov r1, #1
    strb r1, [r0, #0x1]
    add sp, sp, #20
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
