/* ov006 row 0x021df5a4: 904 bytes.
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

extern void native_fn_021df134(void);
extern void native_fn_02049ad0(void);
extern void native_fn_02049f4c(void);
extern void native_fn_020679f0(void);
extern void native_fn_02048094(void);
extern void native_fn_02063eec(void);
extern void native_fn_021dfff0(void);
extern void native_fn_021df128(void);
extern void native_fn_0204a574(void);
extern void native_fn_02062a50(void);
extern void native_fn_020602ec(void);
extern void native_fn_021db390(void);
extern void native_fn_02063b40(void);
extern void native_fn_02049604(void);
extern u8 native_data_02207940[];


asm u32 native_ov006_021df5a4 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #20
    ldr r0, [pc, #0x36c]
    ldrh r1, [r0, #22]
    ldrh r0, [r0, #20]
    strh r1, [sp, #18]
    strh r0, [sp, #16]
    bl native_fn_021df134
    ldrb r0, [r0, #0x11]
    cmp r0, #0
    addeq sp, sp, #20
    ldmeqia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    bl native_fn_021df134
    ldrh r6, [r0, #12]
    bl native_fn_021df134
    mov r5, r0
    bl native_fn_021df134
    mov r4, r0
    bl native_fn_021df134
    ldrh r1, [r4, #12]
    ldr r2, [r5, #0x4]
    ldrh r0, [r0, #14]
    add r1, r2, r1
    cmp r1, r0
    ble L_021df628
    bl native_fn_021df134
    mov r4, r0
    bl native_fn_021df134
    ldrh r1, [r4, #14]
    ldr r0, [r0, #0x4]
    sub r0, r1, r0
    mov r0, r0, lsl #16
    mov r6, r0, lsr #16
L_021df628:
    cmp r6, #0
    mov r4, #0
    ble L_021df65c
L_021df634:
    add r0, r4, #5
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02049ad0
    bl native_fn_02049f4c
    add r0, r4, #1
    mov r0, r0, lsl #24
    cmp r6, r0, asr #24
    mov r4, r0, asr #24
    bgt L_021df634
L_021df65c:
    cmp r6, #0
    mov r7, #0
    ble L_021df8ac
    ldr r10, [pc, #0x2b4]
    add r9, sp, #16
    mov r11, #1
L_021df674:
    mov r4, #1
    bl native_fn_021df134
    ldr r1, [r0, #0x4]
    ldrb r0, [r10, #0x5]
    add r5, r7, r1
    cmp r0, #6
    addls pc, pc, r0, lsl #2
    b L_021df898
    dcd 0xea00001c
    dcd 0xea00002c
    dcd 0xea00000a
    dcd 0xea00003e
    dcd 0xea000001
    dcd 0xea00000f
    dcd 0xea000062
    cmp r5, #1
    bne L_021df6cc
    bl native_fn_020679f0
    ldr r0, [r0, #0xc]
    mov r1, #0
    add r0, r0, #1
    bl native_fn_02048094
L_021df6cc:
    cmp r5, #0
    bne L_021df6ec
    bl native_fn_02063eec
    bl native_fn_02063eec
    ldrb r0, [r0]
    mov r1, #0
    add r0, r0, #1
    bl native_fn_02048094
L_021df6ec:
    ldrb r0, [r10, #0x5]
    cmp r0, #5
    bne L_021df70c
    mov r0, r5
    bl native_fn_021dfff0
    cmp r0, #0
    moveq r4, #3
    movne r4, #1
L_021df70c:
    bl native_fn_021df128
    mov r8, r0
    bl native_fn_021df128
    ldrsh r2, [r0, #2]
    add r0, r7, #5
    mov r1, r0, lsl #24
    add r0, r5, r2
    mov r0, r0, lsl #16
    mov r0, r0, lsr #16
    str r0, [sp]
    stmib sp, {r4, r11}
    mov r0, r1, asr #24
    ldrb r3, [r8]
    mov r1, r9
    mov r2, #15
    bl native_fn_0204a574
    b L_021df898
    add r0, r5, #5
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02049ad0
    mov r5, r0
    mov r0, r7
    bl native_fn_02062a50
    mov r4, r0
    mov r0, r7
    bl native_fn_02062a50
    mov r2, r0
    ldrsh r0, [sp, #18]
    str r0, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    ldrsh r1, [r4, #24]
    ldrsh r3, [sp, #16]
    ldr r0, [r5]
    bl native_fn_020602ec
    b L_021df898
    bl native_fn_021db390
    mov r1, #10
    mul r1, r5, r1
    sub r5, r0, r1
    sub r4, r5, #9
    cmp r4, #1
    movlt r4, #1
    mov r0, r5
    mov r1, #0
    bl native_fn_02048094
    mov r0, r4
    mov r1, #32
    bl native_fn_02048094
    cmp r5, r4
    mov r2, #15
    mov r3, #2
    beq L_021df810
    mov r0, #84
    str r0, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    str r0, [sp, #0x8]
    add r0, r7, #5
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    mov r1, r9
    bl native_fn_0204a574
    b L_021df898
L_021df810:
    mov r0, #85
    str r0, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    str r0, [sp, #0x8]
    add r0, r7, #5
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    mov r1, r9
    bl native_fn_0204a574
    b L_021df898
    ldr r0, [pc, #0xe4]
    bl native_fn_02063b40
    cmp r0, #0
    addeq r0, r7, #5
    cmpeq r0, #6
    moveq r4, #3
    bl native_fn_021df128
    mov r8, r0
    bl native_fn_021df128
    ldrsh r2, [r0, #2]
    add r0, r7, #5
    mov r1, r0, lsl #24
    add r0, r5, r2
    mov r0, r0, lsl #16
    mov r0, r0, lsr #16
    stmia sp, {r0, r4}
    mov r0, r1, asr #24
    mov r1, #1
    str r1, [sp, #0x8]
    ldrb r3, [r8]
    mov r1, r9
    mov r2, #15
    bl native_fn_0204a574
L_021df898:
    add r0, r7, #1
    mov r0, r0, lsl #24
    cmp r6, r0, asr #24
    mov r7, r0, asr #24
    bgt L_021df674
L_021df8ac:
    ldr r0, [pc, #0x6c]
    ldrh r1, [r0, #10]
    ldrh r0, [r0, #8]
    strh r1, [sp, #14]
    strh r0, [sp, #12]
    bl native_fn_021df128
    ldrsh r1, [r0, #4]
    mvn r0, #0
    cmp r1, r0
    beq L_021df90c
    bl native_fn_021df128
    mov r4, r0
    bl native_fn_021df128
    ldrh r2, [r0, #6]
    mov r0, #1
    add r1, sp, #12
    str r2, [sp]
    str r0, [sp, #0x4]
    str r0, [sp, #0x8]
    ldrsh r3, [r4, #4]
    mov r0, #0
    mov r2, #15
    and r3, r3, #255
    bl native_fn_0204a574
L_021df90c:
    bl native_fn_021df134
    mov r1, #0
    bl native_fn_02049604
    add sp, sp, #20
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    dcd native_data_02207940
    dcd 0x0220f594
    dcd 0x0000011d
}
