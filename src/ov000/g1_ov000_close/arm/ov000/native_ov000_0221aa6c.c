/* ov000 row 0x0221aa6c: 1080 bytes.
 *
 * What it does: 267 instructions and 65 call(s), then a 12-entry dispatch through an inline branch table at 0x0221aa88 (dispatch word at 0x0221aa80)
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

extern void native_fn_0221c980(void);
extern void native_fn_0221ca0c(void);
extern void native_fn_0221cdcc(void);
extern void native_fn_0221e7e8(void);
extern void native_fn_0221a9e4(void);
extern void native_fn_0221e6cc(void);
extern void native_fn_0221fa70(void);
extern void native_fn_0221ff50(void);
extern void native_fn_0221d05c(void);
extern void native_fn_0221c9e4(void);
extern void native_fn_0221d048(void);
extern void native_fn_0221e788(void);
extern void native_fn_02220160(void);
extern void native_fn_0221c9f8(void);
extern void native_fn_022211dc(void);
extern void native_fn_0221d8e0(void);
extern void native_fn_0221cf24(void);
extern void native_fn_0221d3fc(void);
extern void native_fn_0221da64(void);
extern void native_fn_0207e97c(void);
extern void native_fn_02062a10(void);
extern void native_fn_0207e720(void);
extern void native_fn_0204157c(void);
extern void native_fn_02041538(void);
extern void native_fn_0206dcd0(void);
extern void native_fn_0206de74(void);
extern void native_fn_020620e8(void);
extern void native_fn_0221cb10(void);
extern void native_fn_0221e81c(void);
extern void native_fn_02044cdc(void);
extern void native_fn_0221ebe0(void);
extern void native_fn_0221ed54(void);
extern void native_fn_0221f15c(void);
extern void native_fn_0221cc4c(void);
extern void native_fn_0221d6f8(void);
extern void native_fn_020c17e8(void);
extern void native_fn_0221d910(void);
extern void native_fn_02062aa0(void);
extern void native_fn_02062ad0(void);
extern void native_fn_02068ef8(void);
extern void native_fn_020c0200(void);
extern void native_fn_0221e7f8(void);
extern void native_fn_020bfe70(void);
extern void native_fn_0206be08(void);
extern void native_fn_020c4220(void);
extern void native_fn_0221c0ac(void);
extern void native_fn_0221c000(void);
extern void native_fn_0221d474(void);
extern u8 native_data_0222df24[];


asm u32 native_ov000_0221aa6c (register u32 a0)
{
    stmdb sp!, {r3, r4, lr}
    sub sp, sp, #36
    ldr r0, [pc, #0x41c]
    ldrsb r1, [r0, #16]
    cmp r1, #11
    addls pc, pc, r1, lsl #2
    b L_0221ae90
    dcd 0xea00000a
    dcd 0xea000027
    dcd 0xea000039
    dcd 0xea000046
    dcd 0xea0000fc
    dcd 0xea000049
    dcd 0xea0000fa
    dcd 0xea00005a
    dcd 0xea000078
    dcd 0xea0000a4
    dcd 0xea0000ab
    dcd 0xea0000d8
    ldr r0, [pc, #0x3dc]
    ldrsb r0, [r0]
    cmp r0, #1
    beq L_0221aae8
    mov r0, #0
    bl native_fn_0221c980
    ldr r0, [pc, #0x3c4]
    ldr r0, [r0, #0x20]
    cmp r0, #0
    beq L_0221aae8
    mov r0, #0
    bl native_fn_0221ca0c
L_0221aae8:
    ldr r0, [pc, #0x3b0]
    mov r1, #4
    ldrh r3, [r0, #10]
    ldrh r0, [r0, #8]
    add r2, sp, #16
    strh r3, [sp, #18]
    strh r0, [sp, #16]
    str r1, [sp]
    mov r4, #12
    ldr r0, [pc, #0x384]
    mov r1, #2
    mov r3, #1
    str r4, [sp, #0x4]
    bl native_fn_0221cdcc
    mov r0, #1
    bl native_fn_0221e7e8
    add sp, sp, #36
    ldmia sp!, {r3, r4, pc}
    ldr r0, [pc, #0x364]
    ldrsb r0, [r0]
    cmp r0, #2
    cmpne r0, #3
    beq L_0221ab5c
    cmp r0, #8
    addne sp, sp, #36
    ldmneia sp!, {r3, r4, pc}
    bl native_fn_0221a9e4
    add sp, sp, #36
    ldmia sp!, {r3, r4, pc}
L_0221ab5c:
    mov r0, #1
    bl native_fn_0221e7e8
    ldr r1, [pc, #0x330]
    ldr r0, [pc, #0x328]
    ldr r1, [r1, #0x20]
    bl native_fn_0221e6cc
    add sp, sp, #36
    ldmia sp!, {r3, r4, pc}
    mov r1, #1
    bl native_fn_0221fa70
    ldr r0, [pc, #0x30c]
    bl native_fn_0221ff50
    mov r0, #31
    mov r1, #1
    bl native_fn_0221d05c
    bl native_fn_0221c9e4
    mov r0, #31
    bl native_fn_0221d048
    mov r0, #1
    bl native_fn_0221e788
    add sp, sp, #36
    ldmia sp!, {r3, r4, pc}
    mov r1, #1
    bl native_fn_02220160
    bl native_fn_0221c9f8
    add sp, sp, #36
    ldmia sp!, {r3, r4, pc}
    ldr r1, [pc, #0x2d0]
    mov r0, #0
    ldrh r2, [r1, #2]
    ldrh r1, [r1]
    strh r2, [sp, #14]
    strh r1, [sp, #12]
    bl native_fn_0221c980
    bl native_fn_022211dc
    mov r4, #7
    mov r1, #2
    str r4, [sp]
    mov r4, #15
    ldr r0, [pc, #0x298]
    add r2, sp, #12
    mov r3, r1
    str r4, [sp, #0x4]
    bl native_fn_0221cdcc
    add sp, sp, #36
    ldmia sp!, {r3, r4, pc}
    bl native_fn_0221d8e0
    bl native_fn_0221cf24
    bl native_fn_0221d3fc
    bl native_fn_0221da64
    bl native_fn_0207e97c
    ldr r0, [pc, #0x26c]
    ldr r0, [r0, #0xc]
    bl native_fn_02062a10
    mov r1, #1
    strb r1, [sp, #0x14]
    ldrsh r3, [r0, #24]
    mov r2, #0
    mov r1, #16
    strh r3, [sp, #22]
    ldrb r3, [r0, #0x1a]
    strb r3, [sp, #0x18]
    ldrb r3, [r0, #0x1b]
    add r0, sp, #20
    strb r3, [sp, #0x19]
    strb r1, [sp, #0x20]
    str r2, [sp, #0x1c]
    strb r2, [sp, #0x21]
    bl native_fn_0207e720
    mov r0, #0
    bl native_fn_0204157c
    mov r0, #0
    mov r1, #2
    mov r2, #10
    bl native_fn_02041538
    add sp, sp, #36
    ldmia sp!, {r3, r4, pc}
    ldr r0, [pc, #0x204]
    ldrsb r0, [r0]
    cmp r0, #9
    beq L_0221acc8
    mov r0, #10
    bl native_fn_0221c980
    ldr r0, [pc, #0x1ec]
    ldr r0, [r0, #0x28]
    bl native_fn_0206dcd0
    mov r0, #1
    bl native_fn_0206de74
    mov r0, #1
    mov r1, r0
    bl native_fn_020620e8
L_0221acc8:
    bl native_fn_0221cb10
    ldr r0, [pc, #0x1c8]
    ldrsb r0, [r0]
    cmp r0, #9
    beq L_0221ad0c
    bl native_fn_0221e81c
    ldr r0, [pc, #0x1b4]
    ldrsh r0, [r0, #8]
    bl native_fn_02044cdc
    ldr r2, [pc, #0x1a8]
    mov r3, r0
    ldr r1, [r2, #0x24]
    ldr r2, [r2, #0x1c]
    ldr r0, [pc, #0x194]
    bl native_fn_0221ebe0
    add sp, sp, #36
    ldmia sp!, {r3, r4, pc}
L_0221ad0c:
    ldr r0, [pc, #0x184]
    mov r1, #0
    bl native_fn_0221ed54
    ldr r0, [pc, #0x17c]
    ldrsh r0, [r0, #8]
    bl native_fn_02044cdc
    ldr r2, [pc, #0x170]
    mov r3, r0
    ldr r1, [r2, #0x24]
    ldr r2, [r2, #0x1c]
    ldr r0, [pc, #0x15c]
    bl native_fn_0221ebe0
    add sp, sp, #36
    ldmia sp!, {r3, r4, pc}
    bl native_fn_0221f15c
    mov r0, #1
    bl native_fn_0221e7e8
    ldr r0, [pc, #0x144]
    mov r1, #0
    str r1, [r0, #0x30]
    add sp, sp, #36
    ldmia sp!, {r3, r4, pc}
    mov r0, #13
    bl native_fn_0221c980
    bl native_fn_0221cb10
    ldr r0, [pc, #0x120]
    bl native_fn_0221cc4c
    bl native_fn_0221da64
    bl native_fn_0221d6f8
    mov r0, #0
    mov r1, r0
    bl native_fn_020c17e8
    ldr r0, [pc, #0x108]
    ldr r0, [r0, #0xc]
    bl native_fn_0221d910
    bl native_fn_02062aa0
    mov r4, r0
    bl native_fn_02062ad0
    ldr r1, [pc, #0xf0]
    add r0, r4, r0
    ldr r2, [r1, #0xc]
    mov r0, r0, lsl #24
    mov r3, r0, asr #24
    mov r1, #0
    str r2, [sp]
    mov r0, #2
    mov r2, r1
    bl native_fn_02068ef8
    bl native_fn_020c0200
    bl native_fn_0221e7f8
    bl native_fn_020bfe70
    mov r0, #0
    mov r1, r0
    bl native_fn_0206be08
    mov r0, #5
    mov r1, #3
    bl native_fn_020c4220
    ldr r0, [pc, #0xa4]
    ldr r0, [r0, #0x10]
    bl native_fn_0221c0ac
    mov r0, #1
    bl native_fn_0221c000
    mov r0, #0
    mov r1, #2
    mov r2, #10
    bl native_fn_02041538
    add sp, sp, #36
    ldmia sp!, {r3, r4, pc}
    ldr r0, [pc, #0x7c]
    ldrh r1, [r0, #6]
    ldrh r0, [r0, #4]
    strh r1, [sp, #10]
    strh r0, [sp, #8]
    bl native_fn_0221d474
    mov r0, #0
    bl native_fn_0221c980
    mov r1, #4
    str r1, [sp]
    mov r12, #12
    ldr r0, [pc, #0x48]
    add r2, sp, #8
    mov r1, #2
    mov r3, #1
    str r12, [sp, #0x4]
    bl native_fn_0221cdcc
    mov r0, #2
    mov r1, #3
    bl native_fn_020c4220
    mov r0, #0
    mov r1, #2
    mov r2, #10
    bl native_fn_02041538
    mov r0, #1
    bl native_fn_0221e7e8
    mov r0, #16
    mov r1, #1
    bl native_fn_020620e8
L_0221ae90:
    add sp, sp, #36
    ldmia sp!, {r3, r4, pc}
    dcd 0x022460d4
    dcd 0x02246090
    dcd native_data_0222df24
}
