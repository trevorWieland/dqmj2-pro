/* ov000 row 0x021f2008: 1132 bytes.
 *
 * What it does: 277 instructions and 40 call(s), then a 7-entry dispatch through an inline branch table at 0x021f2038 (dispatch word at 0x021f2030)
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

extern void native_fn_021f32b4(void);
extern void native_fn_021f30e4(void);
extern void native_fn_021f32d4(void);
extern void native_fn_02049ad0(void);
extern void native_fn_02049f4c(void);
extern void native_fn_02049ffc(void);
extern void native_fn_020635d4(void);
extern void native_fn_02044ff4(void);
extern void native_fn_020602ec(void);
extern void native_fn_021f1854(void);
extern void native_fn_02065818(void);
extern void native_fn_0205dc70(void);
extern void native_fn_0204a858(void);
extern void native_fn_020636e0(void);
extern void native_fn_0204a574(void);
extern void native_fn_02063798(void);
extern void native_fn_02060738(void);
extern u8 native_data_0222b918[];
extern u8 native_data_0222b940[];
extern u8 native_data_0222b924[];
extern u8 native_data_0222b930[];


asm u32 native_ov000_021f2008 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #48
    ldr r0, [pc, #0x444]
    add r2, sp, #12
    mov r1, #0
    ldr r6, [r0, #0x8]
    strh r1, [r2]
    strh r1, [r2, #2]
    ldrsb r0, [r6, #32]
    cmp r0, #6
    addls pc, pc, r0, lsl #2
    b L_021f2454
    dcd 0xea000005
    dcd 0xea00000f
    dcd 0xea000019
    dcd 0xea000071
    dcd 0xea00007b
    dcd 0xea0000bc
    dcd 0xea0000c6
    mov r1, #16
    add r0, r6, #16
    strh r1, [sp, #12]
    bl native_fn_021f32b4
    ldr r1, [pc, #0x3f4]
    add r2, sp, #12
    add r0, r6, #16
    bl native_fn_021f30e4
    bl native_fn_021f32d4
    add sp, sp, #48
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    mov r1, #16
    add r0, r6, #16
    strh r1, [sp, #12]
    bl native_fn_021f32b4
    ldr r1, [pc, #0x3cc]
    add r2, sp, #12
    add r0, r6, #16
    bl native_fn_021f30e4
    bl native_fn_021f32d4
    add sp, sp, #48
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    mov r0, #16
    strh r0, [sp, #12]
    add r0, r6, #16
    bl native_fn_021f32b4
    bl native_fn_021f32d4
    ldrh r0, [r6, #28]
    mov r5, #0
    cmp r0, #0
    addle sp, sp, #48
    ldmleia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    mov r7, #8
    add r11, sp, #16
L_021f20dc:
    add r9, r5, #3
    mov r0, r9, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02049ad0
    ldr r1, [r6, #0x14]
    movs r4, r0
    add r8, r1, r5
    ldrne r1, [r4]
    cmpne r1, #0
    beq L_021f2114
    bl native_fn_02049f4c
    ldr r0, [r4]
    ldr r0, [r0, #0x4]
    bl native_fn_02049ffc
L_021f2114:
    ldr r0, [pc, #0x340]
    ldr r1, [r0, #0x8]
    add r0, r1, #6400
    ldrh r0, [r0, #24]
    cmp r8, r0
    bge L_021f21ec
    add r0, r1, r8, lsl #2
    ldr r1, [r0, #0x10c]
    mov r0, r1, lsl #16
    mov r8, r0, asr #16
    mov r0, r1, lsr #16
    and r10, r0, #255
    mov r0, r8
    mov r1, r10
    bl native_fn_020635d4
    cmp r0, #0
    beq L_021f21b8
    mov r1, r8, lsl #16
    mov r0, r11
    mov r1, r1, lsr #16
    mov r2, r10
    bl native_fn_02044ff4
    mov r0, #0
    str r0, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    ldrsh r3, [sp, #12]
    ldr r0, [r4]
    mov r1, r8
    mov r2, r11
    bl native_fn_020602ec
    mov r0, r8
    mov r1, r10
    bl native_fn_021f1854
    cmp r0, #0
    beq L_021f21ec
    mov r2, r7, lsl #24
    mov r1, #3
    mov r2, r2, asr #24
    bl native_fn_02065818
    b L_021f21ec
L_021f21b8:
    mov r0, #5
    mov r1, #7
    mov r2, #42
    bl native_fn_0205dc70
    mov r1, r9, lsl #24
    str r0, [sp]
    mov r0, r1, asr #24
    mov r1, #1
    str r1, [sp, #0x4]
    ldr r1, [pc, #0x284]
    add r2, sp, #12
    mov r3, #1
    bl native_fn_0204a858
L_021f21ec:
    add r7, r7, #2
    add r0, r5, #1
    mov r0, r0, lsl #24
    mov r5, r0, asr #24
    ldrh r1, [r6, #28]
    cmp r1, r0, asr #24
    bgt L_021f20dc
    add sp, sp, #48
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    mov r1, #16
    add r0, r6, #16
    strh r1, [sp, #12]
    bl native_fn_021f32b4
    ldr r1, [pc, #0x244]
    add r2, sp, #12
    add r0, r6, #16
    bl native_fn_021f30e4
    bl native_fn_021f32d4
    add sp, sp, #48
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    mov r0, #16
    strh r0, [sp, #12]
    add r0, r6, #16
    bl native_fn_021f32b4
    bl native_fn_021f32d4
    ldrh r0, [r6, #28]
    mov r9, #0
    cmp r0, #0
    addle sp, sp, #48
    ldmleia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    mov r11, #1
    mov r4, r11
L_021f226c:
    add r8, r9, #3
    mov r0, r8, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02049ad0
    ldr r1, [r6, #0x14]
    mov r5, r0
    add r10, r1, r9
    ldr r1, [pc, #0x1cc]
    ldr r1, [r1, #0x8]
    add r1, r1, r10, lsl #2
    ldr r7, [r1, #0x10c]
    bl native_fn_02049f4c
    ldr r0, [r5]
    ldr r0, [r0, #0x4]
    bl native_fn_02049ffc
    ldr r0, [pc, #0x1ac]
    ldr r0, [r0, #0x8]
    add r0, r0, #6400
    ldrh r0, [r0, #24]
    cmp r10, r0
    bge L_021f2324
    mov r0, r7
    bl native_fn_020636e0
    cmp r0, #0
    add r1, sp, #12
    beq L_021f2300
    mov r0, r7, lsl #16
    mov r0, r0, lsr #16
    str r0, [sp]
    mov r0, r8, lsl #24
    str r4, [sp, #0x4]
    mov r2, #8
    mov r0, r0, asr #24
    mov r3, #0
    str r4, [sp, #0x8]
    bl native_fn_0204a574
    b L_021f2324
L_021f2300:
    mov r0, #42
    str r0, [sp]
    mov r0, r8, lsl #24
    str r11, [sp, #0x4]
    mov r2, #5
    mov r0, r0, asr #24
    mov r3, #7
    str r11, [sp, #0x8]
    bl native_fn_0204a574
L_021f2324:
    ldrh r1, [r6, #28]
    add r0, r9, #1
    mov r0, r0, lsl #24
    cmp r1, r0, asr #24
    mov r9, r0, asr #24
    bgt L_021f226c
    add sp, sp, #48
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    mov r1, #16
    add r0, r6, #16
    strh r1, [sp, #12]
    bl native_fn_021f32b4
    ldr r1, [pc, #0x114]
    add r2, sp, #12
    add r0, r6, #16
    bl native_fn_021f30e4
    bl native_fn_021f32d4
    add sp, sp, #48
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    mov r0, #16
    strh r0, [sp, #12]
    add r0, r6, #16
    bl native_fn_021f32b4
    bl native_fn_021f32d4
    ldrh r0, [r6, #28]
    mov r9, #0
    cmp r0, #0
    addle sp, sp, #48
    ldmleia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    ldr r11, [pc, #0xbc]
    mov r4, #1
L_021f23a0:
    add r8, r9, #3
    mov r0, r8, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02049ad0
    ldr r2, [r6, #0x14]
    ldr r1, [r11, #0x8]
    add r10, r2, r9
    add r1, r1, r10, lsl #2
    mov r5, r0
    ldr r7, [r1, #0x10c]
    bl native_fn_02049f4c
    ldr r0, [r5]
    ldr r0, [r0, #0x4]
    bl native_fn_02049ffc
    ldr r0, [r11, #0x8]
    add r0, r0, #6400
    ldrh r0, [r0, #24]
    cmp r10, r0
    bge L_021f243c
    mov r0, r7
    bl native_fn_02063798
    cmp r0, #0
    beq L_021f2414
    ldr r0, [r5]
    mov r1, r7
    add r2, sp, #12
    mov r3, #1
    bl native_fn_02060738
    b L_021f243c
L_021f2414:
    mov r0, #42
    str r0, [sp]
    mov r0, r8, lsl #24
    str r4, [sp, #0x4]
    add r1, sp, #12
    mov r2, #5
    mov r3, #7
    mov r0, r0, asr #24
    str r4, [sp, #0x8]
    bl native_fn_0204a574
L_021f243c:
    ldrh r1, [r6, #28]
    add r0, r9, #1
    mov r0, r0, lsl #24
    cmp r1, r0, asr #24
    mov r9, r0, asr #24
    bgt L_021f23a0
L_021f2454:
    add sp, sp, #48
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    dcd 0x02236d98
    dcd native_data_0222b918
    dcd native_data_0222b940
    dcd 0x021c9698
    dcd native_data_0222b924
    dcd native_data_0222b930
}
