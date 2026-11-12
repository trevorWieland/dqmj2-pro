/* ov000 row 0x02216fc4: 564 bytes.
 *
 * What it does: 137 instructions and 23 call(s), then a 15-entry dispatch through an inline branch table at 0x022170d0 (dispatch word at 0x022170c8)
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

extern void native_fn_02078cac(void);
extern void native_fn_0205f9e4(void);
extern void native_fn_0221576c(void);
extern void native_fn_02041538(void);
extern void native_fn_02041814(void);
extern void native_fn_02062520(void);
extern void native_fn_021fab0c(void);
extern void native_fn_02077938(void);
extern void native_fn_0220040c(void);
extern void native_fn_02074664(void);
extern void native_fn_02078c90(void);
extern void native_fn_022162b4(void);
extern void native_fn_0207973c(void);
extern void native_fn_022221d0(void);
extern void native_fn_021fc9bc(void);
extern void native_fn_021fed38(void);
extern void native_fn_02201eb8(void);
extern void native_fn_021fe378(void);
extern void native_fn_02217a54(void);
extern void native_fn_02217308(void);
extern void native_fn_022172dc(void);


asm u32 native_ov000_02216fc4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    ldr r0, [pc, #0x218]
    mov r4, #0
    ldrsb r0, [r0, #16]
    mov r5, #1
    cmp r0, #4
    bne L_02216fe4
    bl native_fn_02078cac
L_02216fe4:
    ldr r0, [pc, #0x200]
    ldr r0, [r0, #0x2c]
    cmp r0, #0
    beq L_02216ffc
    ldr r0, [pc, #0x1f4]
    bl native_fn_0205f9e4
L_02216ffc:
    ldr r0, [pc, #0x1f0]
    ldr r1, [r0, #0x20]
    cmp r1, #0
    bne L_02217064
    bl native_fn_0221576c
    cmp r0, #0
    bne L_02217050
    ldr r0, [pc, #0x1d4]
    ldr r1, [r0, #0xc]
    cmp r1, #0
    moveq r1, #20
    streq r1, [r0, #0x20]
    beq L_0221705c
    mov r0, #1
    mov r1, #2
    mov r2, #10
    bl native_fn_02041538
    ldr r0, [pc, #0x1ac]
    mov r1, #10
    str r1, [r0, #0x20]
    b L_0221705c
L_02217050:
    ldr r0, [pc, #0x19c]
    mov r1, #20
    str r1, [r0, #0x20]
L_0221705c:
    mov r4, #2
    b L_0221719c
L_02217064:
    cmp r1, #10
    bne L_022170b4
    bl native_fn_0221576c
    cmp r0, #0
    bne L_022170a4
    bl native_fn_02041814
    cmp r0, #1
    beq L_0221719c
    bl native_fn_02062520
    cmp r0, #0
    beq L_0221719c
    ldr r0, [pc, #0x15c]
    mov r1, #20
    str r1, [r0, #0x20]
    mov r4, #2
    b L_0221719c
L_022170a4:
    ldr r0, [pc, #0x148]
    mov r1, #20
    str r1, [r0, #0x20]
    b L_0221719c
L_022170b4:
    cmp r1, #20
    bne L_02217190
    ldr r0, [pc, #0x124]
    ldrsb r0, [r0, #16]
    cmp r0, #14
    addls pc, pc, r0, lsl #2
    b L_0221717c
    dcd 0xea00000d
    dcd 0xea000010
    dcd 0xea000011
    dcd 0xea00001c
    dcd 0xea000011
    dcd 0xea00001c
    dcd 0xea000009
    dcd 0xea000020
    dcd 0xea000013
    dcd 0xea00001a
    dcd 0xea00001b
    dcd 0xea00001e
    dcd 0xea00001d
    dcd 0xea00001c
    dcd 0xea00000f
    bl native_fn_021fab0c
    b L_02217180
    bl native_fn_02077938
    b L_02217180
    bl native_fn_0220040c
    b L_02217180
    bl native_fn_02074664
    b L_02217180
    bl native_fn_02078c90
    ldr r0, [pc, #0xb0]
    mov r1, #127
    ldrsb r0, [r0, #16]
    bl native_fn_022162b4
    b L_02217180
    bl native_fn_0207973c
    b L_02217180
    bl native_fn_022221d0
    b L_02217180
    bl native_fn_021fc9bc
    b L_02217180
    bl native_fn_021fed38
    b L_02217180
    bl native_fn_02201eb8
    b L_02217180
    bl native_fn_021fe378
    b L_02217180
    mov r1, #127
    bl native_fn_022162b4
L_0221717c:
    bl native_fn_02217a54
L_02217180:
    ldr r0, [pc, #0x6c]
    mov r1, #100
    str r1, [r0, #0x20]
    b L_0221719c
L_02217190:
    mov r5, #0
    str r5, [r0, #0x20]
    mov r4, #1
L_0221719c:
    cmp r5, #0
    bne L_022171e0
    ldr r0, [pc, #0x48]
    ldr r1, [pc, #0x38]
    ldrsb r0, [r0, #1]
    strb r0, [r1, #0x10]
    bl native_fn_02217308
    ldr r0, [pc, #0x34]
    ldrsb r0, [r0, #1]
    cmp r0, #127
    ldrne r0, [pc, #0x20]
    movne r1, #0
    ldreq r0, [pc, #0x18]
    moveq r1, #11
    strb r1, [r0, #0x494]
    bl native_fn_022172dc
    mov r4, #1
L_022171e0:
    mov r0, r4
    ldmia sp!, {r3, r4, r5, pc}
    dcd 0x0224536c
    dcd 0x022459b4
    dcd 0x022459c4
    dcd 0x0224532c
}
