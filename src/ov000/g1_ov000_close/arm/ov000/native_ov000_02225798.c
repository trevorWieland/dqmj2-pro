/* ov000 row 0x02225798: 880 bytes.
 *
 * What it does: 215 instructions and 20 call(s), then a 8-entry dispatch through an inline branch table at 0x022257f0 (dispatch word at 0x022257e8)
 *
 * Carrier: mwccarm asm with dcd data runs.
 * The measured extent is code plus data inside the function. The data
 * runs are emitted as data, not decoded as instructions; every
 * instruction, branch target, pool word and table entry is read from
 * the image.
 *
 * Unknowns: the field roles, the meaning of the table entries and every callee contract are not established by byte identity; the dispatch range and the table bounds are measured.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02049ae4(void);
extern void native_fn_02225714(void);
extern void native_fn_01ffac9c(void);
extern void native_fn_02225270(void);
extern void native_fn_01ffae70(void);
extern void native_fn_01ffb060(void);
extern void native_fn_02225738(void);
extern void native_fn_02225788(void);
extern void native_fn_02061260(void);
extern void native_fn_02223e70(void);
extern void native_fn_02062378(void);
extern void native_fn_021f51e8(void);
extern void native_fn_020620e8(void);
extern void native_fn_0208752c(void);
extern void native_fn_022276ac(void);
extern void native_fn_02225d1c(void);
extern void native_fn_02225b08(void);
extern void native_fn_02225df0(void);
extern void native_fn_02061284(void);
extern u8 native_data_0222feb4[];


asm u32 native_ov000_02225798 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    sub sp, sp, #8
    ldr r0, [pc, #0x34c]
    ldr r1, [pc, #0x34c]
    ldrsb r0, [r0, #24]
    ldr r5, [pc, #0x348]
    ldr r6, [pc, #0x348]
    add r0, r0, r0, lsl #2
    add r4, r1, r0
    bl native_fn_02049ae4
    ldr r1, [pc, #0x32c]
    mov r7, r0
    ldrsb r0, [r1, #24]
    ldrb r8, [r4, #0x1]
    cmp r0, #9
    cmpne r0, #10
    bne L_02225844
    ldr r1, [pc, #0x310]
    ldrsb r1, [r1, #31]
    cmp r1, #7
    addls pc, pc, r1, lsl #2
    b L_02225844
    dcd 0xea000013
    dcd 0xea000005
    dcd 0xea000006
    dcd 0xea000007
    dcd 0xea000008
    dcd 0xea000009
    dcd 0xea00000a
    dcd 0xea00000b
    mov r8, #18
    b L_02225844
    mov r8, #19
    b L_02225844
    mov r8, #10
    b L_02225844
    mov r8, #20
    b L_02225844
    mov r8, #21
    b L_02225844
    mov r8, #25
    b L_02225844
    mov r8, #29
L_02225844:
    ldrsb r1, [r4]
    cmp r1, #4
    addls pc, pc, r1, lsl #2
    b L_02225920
    b L_02225920
    b L_02225868
    b L_022258d0
    b L_02225914
    b L_0222591c
L_02225868:
    ldr r0, [pc, #0x284]
    ldr r1, [pc, #0x284]
    ldrsb r0, [r0, #25]
    add r0, r0, r0, lsl #2
    ldrsb r0, [r1, r0]
    sub r0, r0, #3
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    and r0, r0, #255
    cmp r0, #1
    bhi L_02225898
    bl native_fn_02225714
L_02225898:
    mov r1, #0
    str r1, [sp]
    mov r0, #2
    str r0, [sp, #0x4]
    ldrb r2, [r4, #0x3]
    ldrb r0, [r4, #0x4]
    mov r3, r8, lsl #16
    mov r8, r2, lsl #24
    mov r2, r0, lsl #28
    mov r0, r8, lsr #28
    mov r2, r2, lsr #28
    mov r3, r3, asr #16
    bl native_fn_01ffac9c
    b L_02225920
L_022258d0:
    bl native_fn_02225270
    mov r1, #0
    str r1, [sp]
    ldrb r1, [r4, #0x4]
    mov r3, r0
    mov r2, r8
    mov r0, r1, lsl #28
    mov r1, r0, lsr #28
    mov r0, #16
    bl native_fn_01ffae70
    ldrb r0, [r4, #0x3]
    mov r0, r0, lsl #28
    movs r0, r0, lsr #28
    beq L_02225920
    mov r0, #1
    bl native_fn_01ffb060
    b L_02225920
L_02225914:
    bl native_fn_02225738
    b L_02225920
L_0222591c:
    bl native_fn_02225788
L_02225920:
    ldr r0, [pc, #0x1cc]
    ldrsb r1, [r0, #24]
    cmp r1, #27
    addls pc, pc, r1, lsl #2
    b L_02225ac8
    b L_02225ac8
    b L_02225ac8
    b L_022259c4
    b L_02225ac8
    b L_02225ac8
    b L_02225a90
    b L_02225a90
    b L_02225ac8
    b L_02225a48
    b L_02225ac8
    b L_022259a4
    b L_022259d8
    b L_02225ac8
    b L_022259a4
    b L_022259a4
    b L_02225ac8
    b L_022259b8
    b L_02225a6c
    b L_02225a7c
    b L_02225ac8
    b L_02225a30
    b L_02225a08
    b L_02225a14
    b L_022259fc
    b L_02225ac8
    b L_02225aa4
    b L_02225aa4
    b L_02225ac0
L_022259a4:
    mov r2, #2
    mov r1, #0
    strb r2, [r5, #0x18c]
    strb r1, [r0, #0x1c]
    b L_02225ac8
L_022259b8:
    mov r0, #1
    bl native_fn_02061260
    b L_02225ac8
L_022259c4:
    bl native_fn_02223e70
    bl native_fn_02062378
    cmp r0, #19
    bne L_022259d8
    bl native_fn_021f51e8
L_022259d8:
    bl native_fn_02062378
    cmp r0, #19
    beq L_022259f0
    mov r0, #19
    mov r1, #1
    bl native_fn_020620e8
L_022259f0:
    mov r0, #127
    strb r0, [r5, #0x18c]
    b L_02225ac8
L_022259fc:
    mov r0, #127
    strb r0, [r5, #0x18c]
    b L_02225ac8
L_02225a08:
    mov r0, #127
    strb r0, [r6, #0x18c]
    b L_02225ac8
L_02225a14:
    ldrb r0, [r0, #0x20]
    cmp r0, #0
    bne L_02225ac8
    ldr r0, [r7, #0x4]
    mov r1, #0
    bl native_fn_0208752c
    b L_02225ac8
L_02225a30:
    mov r1, #0
    mov r0, #1
    strb r1, [r6, #0x18f]
    strb r0, [r5, #0x18f]
    bl native_fn_022276ac
    b L_02225ac8
L_02225a48:
    mov r3, #0
    strb r3, [r5, #0x190]
    strb r3, [r5, #0x18e]
    mov r2, #60
    ldr r1, [pc, #0xa4]
    str r2, [r0, #0x4]
    str r1, [r0, #0x10]
    strb r3, [r0, #0x1c]
    b L_02225ac8
L_02225a6c:
    mov r0, #0
    strb r0, [r5, #0x191]
    bl native_fn_02225d1c
    b L_02225ac8
L_02225a7c:
    mov r0, #0
    strb r0, [r6, #0x191]
    bl native_fn_02225b08
    bl native_fn_02225df0
    b L_02225ac8
L_02225a90:
    mov r1, #2
    strb r1, [r5, #0x18c]
    mov r1, #60
    str r1, [r0, #0x4]
    b L_02225ac8
L_02225aa4:
    mov r1, #1
    strb r1, [r5, #0x18c]
    mov r1, #60
    str r1, [r0, #0x4]
    mov r1, #0
    strb r1, [r0, #0x1c]
    b L_02225ac8
L_02225ac0:
    mov r0, #0
    strb r0, [r6, #0x193]
L_02225ac8:
    ldrsb r0, [r4, #2]
    cmp r0, #27
    bne L_02225adc
    mov r0, #1
    bl native_fn_02061284
L_02225adc:
    ldr r0, [pc, #0x10]
    mov r1, #3
    str r1, [r0, #0x14]
    mov r0, #0
    add sp, sp, #8
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
    dcd 0x022468b8
    dcd native_data_0222feb4
    dcd 0x02246c84
    dcd 0x02246aa8
    dcd 0x000001c2
}
