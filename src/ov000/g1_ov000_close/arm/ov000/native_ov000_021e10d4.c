/* ov000 row 0x021e10d4: 596 bytes.
 *
 * What it does: 148 instructions; 23 call(s) to 0x021e07b8, 0x02210a64, 0x0205c008, +20 more; loops (back edge at +0x30); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x250 -> constant 0x022322d4 (image word 0x022322d4)
 *   branch +0x28 -> +0x244
 *   branch +0x48 -> +0x20c
 *   branch +0x5c -> +0x244
 *   branch +0xa4 -> +0x118
 *   branch +0x114 -> +0x17c
 *   branch +0x208 -> +0x244
 *   branch +0x218 -> +0x244
 *   branch +0x228 -> +0x238
 *   branch +0x234 -> +0x240
 *   test +0x24 cmp r0, #7
 *   test +0x58 cmp r1, #0
 *   test +0xa0 cmp r0, #0
 *   test +0x214 cmp r0, #0
 *   test +0x224 cmp r0, #0
 *   2 block transfer(s), 28 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e10d4; the literal pool and
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

extern void ov000_saved_world_position_get_021e07b8(void);
extern void native_fn_02210a64(void);
extern void native_fn_0205c008(void);
extern void native_fn_021dea78(void);
extern void native_fn_0205bfd4(void);
extern void native_fn_0205bf9c(void);
extern void native_fn_020c58c0(void);
extern void native_fn_02214d04(void);
extern void native_fn_02066d48(void);
extern void native_fn_02067024(void);
extern void native_fn_021e1038(void);
extern void native_fn_02040424(void);
extern void native_fn_021df3bc(void);
extern void native_fn_0205bd6c(void);
extern void native_fn_020404f0(void);
extern void native_fn_02212548(void);
extern void native_fn_021e4e9c(void);


asm u32 native_ov000_021e10d4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    sub sp, sp, #96
    mov r4, #0
    sub r1, r4, #1
    ldr r0, =0x022322d4
    strh r1, [sp, #62]
    strh r1, [sp, #60]
    strh r1, [sp, #58]
    ldrb r0, [r0, #0x278]
    cmp r0, #7
    beq ov000_021e10d4_L244
    mov r0, r4
    bl ov000_saved_world_position_get_021e07b8
    add r1, sp, #84
    add r2, sp, #80
    mov r6, r0
    bl native_fn_02210a64
    movs r5, r0
    beq ov000_021e10d4_L20c
    bl native_fn_0205c008
    add r0, r5, #512
    ldrsh r1, [r0, #118]
    cmp r1, #0
    blt ov000_021e10d4_L244
    mov r0, r6
    strh r1, [sp, #62]
    bl native_fn_021dea78
    mov r7, r0
    bl native_fn_0205bfd4
    ldr r1, =0x022322d4
    mov r6, r0
    ldr r0, [r1, #0x21c]
    ldrb r9, [r0, #0x41]
    ldrb r8, [r0, #0x40]
    bl native_fn_0205bf9c
    add r1, r5, #512
    mov r5, r0
    ldrsh r0, [r1, #118]
    bl native_fn_020c58c0
    bl native_fn_02214d04
    cmp r0, #0
    beq ov000_021e10d4_L118
    add r4, sp, #64
    str r8, [sp]
    mov r0, r7
    mov r1, r6
    mov r2, r5
    mov r3, r9
    str r4, [sp, #0x4]
    bl native_fn_02066d48
    add r1, sp, #56
    str r1, [sp]
    add r2, sp, #76
    str r2, [sp, #0x4]
    add r1, sp, #72
    str r1, [sp, #0x8]
    add r4, sp, #68
    add r1, sp, #62
    add r2, sp, #60
    add r3, sp, #58
    str r4, [sp, #0xc]
    bl native_fn_02067024
    mvn r0, #0
    mov r5, #1
    mov r4, r5
    strh r0, [sp, #60]
    strh r0, [sp, #58]
    mov r7, #43
    mov r6, #3
    b ov000_021e10d4_L17c
ov000_021e10d4_L118:
    add r12, sp, #64
    mov r0, r7
    mov r1, r6
    mov r2, r5
    mov r3, r9
    stmia sp, {r8, r12}
    bl native_fn_02066d48
    add r1, sp, #56
    str r1, [sp]
    add r2, sp, #76
    str r2, [sp, #0x4]
    add r1, sp, #72
    str r1, [sp, #0x8]
    add r5, sp, #68
    add r1, sp, #62
    add r2, sp, #60
    add r3, sp, #58
    str r5, [sp, #0xc]
    bl native_fn_02067024
    mov r5, r0
    ldr r1, [sp, #0x50]
    add r0, sp, #84
    mov r7, #42
    bl native_fn_021e1038
    mov r6, r0
ov000_021e10d4_L17c:
    bl native_fn_02040424
    bl native_fn_021df3bc
    mov r8, r0
    bl native_fn_0205bf9c
    add r0, r8, r0
    ldrb r8, [r0, #0xc]
    ldrb r1, [sp, #0x38]
    mov r3, #0
    mov r0, r5
    stmia sp, {r1, r6}
    ldrsh r5, [sp, #64]
    sub r2, r3, #1
    mov r1, #1
    str r5, [sp, #0x8]
    str r3, [sp, #0xc]
    str r8, [sp, #0x10]
    str r3, [sp, #0x14]
    str r4, [sp, #0x18]
    str r2, [sp, #0x1c]
    str r7, [sp, #0x20]
    str r3, [sp, #0x24]
    ldr r2, [sp, #0x4c]
    str r2, [sp, #0x28]
    ldr r2, [sp, #0x48]
    str r2, [sp, #0x2c]
    ldr r2, [sp, #0x44]
    str r2, [sp, #0x30]
    str r1, [sp, #0x34]
    ldrsh r1, [sp, #62]
    ldrsh r2, [sp, #60]
    ldrsh r3, [sp, #58]
    bl native_fn_0205bd6c
    mov r0, #22
    bl native_fn_020404f0
    mov r4, #1
    b ov000_021e10d4_L244
ov000_021e10d4_L20c:
    mov r0, r6
    bl native_fn_02212548
    cmp r0, #0
    beq ov000_021e10d4_L244
    mov r0, #142
    bl native_fn_021e4e9c
    cmp r0, #0
    beq ov000_021e10d4_L238
    mov r0, #49
    bl native_fn_020404f0
    b ov000_021e10d4_L240
ov000_021e10d4_L238:
    mov r0, #5
    bl native_fn_020404f0
ov000_021e10d4_L240:
    mov r4, #1
ov000_021e10d4_L244:
    mov r0, r4
    add sp, sp, #96
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
