/* ov006 row 0x021dc3b8: 920 bytes.
 *
 * What it does: switch dispatch through an inline table
 *
 * Carrier: mwccarm asm with dcd data runs.
 * The measured extent is code plus data inside the function. The data
 * runs are emitted as data, not decoded as instructions; every
 * instruction, branch target, pool word and table entry is read from
 * the image.
 *
 * Unknowns: the field roles and the meaning of the table entries are not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02008d78(void);
extern void native_fn_02067a7c(void);
extern void native_fn_02067968(void);
extern void native_fn_021dc2a0(void);
extern void native_fn_0203d294(void);


asm u32 native_ov006_021dc3b8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #2080
    mov r11, r0
    ldr r0, [pc, #0x374]
    mov r1, #0
    mov r2, #128
    bl native_fn_02008d78
    ldr r0, [pc, #0x368]
    mov r1, #0
    mov r2, #128
    bl native_fn_02008d78
    add r0, r11, #8
    bl native_fn_02067a7c
    cmp r0, #0
    addeq sp, sp, #2080
    ldmeqia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    mov r0, r11
    bl native_fn_02067968
    str r0, [sp]
    mov r6, #0
L_021dc408:
    ldr r1, [pc, #0x330]
    mov r0, r6, lsl #2
    add r5, r1, r11, lsl #5
    mov r8, #1
    str r0, [sp, #0x8]
    add r0, r5, r6, lsl #2
    mov r7, #0
    str r0, [sp, #0xc]
    mov r4, r8
L_021dc42c:
    ldr r0, [sp]
    add r1, r8, r8, lsl #1
    mov r9, #0
    add r10, r0, r1, lsl #1
L_021dc43c:
    mov r0, r11
    mov r1, r8
    mov r2, r9
    bl native_fn_021dc2a0
    cmp r6, #0
    mov r1, #0
    ble L_021dc480
L_021dc458:
    mov r3, r1, lsl #2
    ldrh r2, [r3, r5]
    add r1, r1, #1
    cmp r8, r2
    addeq r2, r3, r5
    ldreqb r2, [r2, #0x2]
    cmpeq r9, r2
    moveq r0, r4
    cmp r1, r6
    blt L_021dc458
L_021dc480:
    mov r1, r9, lsl #1
    ldrh r2, [r1, r10]
    ldr r1, [pc, #0x2b8]
    cmp r2, r1
    movhi r0, #1
    cmp r0, #0
    bne L_021dc4b8
    cmp r2, r7
    blo L_021dc4b8
    ldr r0, [sp, #0x8]
    mov r7, r2
    strh r8, [r0, r5]
    ldr r0, [sp, #0xc]
    strb r9, [r0, #0x2]
L_021dc4b8:
    add r0, r9, #1
    mov r0, r0, lsl #16
    mov r9, r0, asr #16
    cmp r9, #3
    blt L_021dc43c
    add r0, r8, #1
    mov r0, r0, lsl #16
    mov r8, r0, lsr #16
    cmp r8, #512
    blo L_021dc42c
    add r6, r6, #1
    cmp r6, #8
    blt L_021dc408
    mov r2, #0
    add r0, sp, #1056
L_021dc4f4:
    mov r1, r2, lsl #1
    strh r2, [r0, r1]
    add r2, r2, #1
    cmp r2, #512
    blt L_021dc4f4
    mov r6, #0
    mov r5, #512
    add r4, sp, #1056
L_021dc514:
    mov r0, r5
    bl native_fn_0203d294
    mov r1, r6, lsl #16
    mov r0, r0, lsl #16
    mov r3, r1, lsr #15
    mov r1, r0, lsr #15
    add r6, r6, #1
    ldrh r2, [r4, r3]
    ldrh r0, [r4, r1]
    cmp r6, #256
    strh r0, [r4, r3]
    strh r2, [r4, r1]
    blt L_021dc514
    mov r6, #0
L_021dc54c:
    mov r0, #6
    ldr r10, [pc, #0x1f4]
    bl native_fn_0203d294
    cmp r0, #5
    addls pc, pc, r0, lsl #2
    b L_021dc620
    dcd 0xea000004
    dcd 0xea00000a
    dcd 0xea000010
    dcd 0xea000016
    dcd 0xea00001c
    dcd 0xea000022
    mov r2, #0
    mov r1, #1
    mov r0, #2
    strh r2, [sp, #32]
    strh r1, [sp, #34]
    strh r0, [sp, #36]
    b L_021dc620
    mov r2, #0
    mov r1, #2
    mov r0, #1
    strh r2, [sp, #32]
    strh r1, [sp, #34]
    strh r0, [sp, #36]
    b L_021dc620
    mov r2, #1
    mov r1, #0
    mov r0, #2
    strh r2, [sp, #32]
    strh r1, [sp, #34]
    strh r0, [sp, #36]
    b L_021dc620
    mov r2, #1
    mov r1, #2
    mov r0, #0
    strh r2, [sp, #32]
    strh r1, [sp, #34]
    strh r0, [sp, #36]
    b L_021dc620
    mov r2, #2
    mov r1, #0
    mov r0, #1
    strh r2, [sp, #32]
    strh r1, [sp, #34]
    strh r0, [sp, #36]
    b L_021dc620
    mov r2, #2
    mov r1, #1
    mov r0, #0
    strh r2, [sp, #32]
    strh r1, [sp, #34]
    strh r0, [sp, #36]
L_021dc620:
    ldr r1, [pc, #0x11c]
    mov r0, #0
    str r0, [sp, #0x4]
    mov r0, r6, lsl #2
    add r5, r1, r11, lsl #5
    str r0, [sp, #0x14]
    add r0, r5, r6, lsl #2
    str r0, [sp, #0x1c]
    mov r4, #1
L_021dc644:
    ldr r0, [sp, #0x4]
    mov r9, #0
    mov r1, r0, lsl #1
    add r0, sp, #32
    ldrsh r8, [r0, r1]
    ldr r0, [sp]
    add r0, r0, r8, lsl #1
    str r0, [sp, #0x10]
    and r0, r8, #255
    str r0, [sp, #0x18]
L_021dc66c:
    mov r1, r9, lsl #1
    add r0, sp, #1056
    ldrh r7, [r0, r1]
    cmp r7, #0
    moveq r0, #1
    beq L_021dc694
    mov r0, r11
    mov r1, r7
    mov r2, r8
    bl native_fn_021dc2a0
L_021dc694:
    cmp r6, #0
    mov r1, #0
    ble L_021dc6c8
L_021dc6a0:
    mov r3, r1, lsl #2
    ldrh r2, [r3, r5]
    add r1, r1, #1
    cmp r7, r2
    addeq r2, r3, r5
    ldreqb r2, [r2, #0x2]
    cmpeq r8, r2
    moveq r0, r4
    cmp r1, r6
    blt L_021dc6a0
L_021dc6c8:
    add r1, r7, r7, lsl #1
    mov r2, r1, lsl #1
    ldr r1, [sp, #0x10]
    ldrh r2, [r2, r1]
    ldr r1, [pc, #0x68]
    cmp r2, r1
    movhi r0, #1
    cmp r0, #0
    bne L_021dc70c
    cmp r2, r10
    bhs L_021dc70c
    ldr r0, [sp, #0x14]
    ldr r1, [sp, #0x18]
    strh r7, [r0, r5]
    ldr r0, [sp, #0x1c]
    mov r10, r2
    strb r1, [r0, #0x2]
L_021dc70c:
    add r9, r9, #1
    cmp r9, #512
    blt L_021dc66c
    ldr r0, [sp, #0x4]
    add r0, r0, #1
    str r0, [sp, #0x4]
    cmp r0, #3
    blt L_021dc644
    add r6, r6, #1
    cmp r6, #8
    blt L_021dc54c
    add sp, sp, #2080
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    dcd 0x0220f3d8
    dcd 0x0220f458
    dcd 0x00002710
    dcd 0x00007530
}
