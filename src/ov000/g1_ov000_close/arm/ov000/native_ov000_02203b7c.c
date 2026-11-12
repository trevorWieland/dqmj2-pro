/* ov000 row 0x02203b7c: 1072 bytes.
 *
 * What it does: 264 instructions and 28 call(s), then a 15-entry dispatch through an inline branch table at 0x02203c00 (dispatch word at 0x02203bf8)
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

extern void native_fn_02061944(void);
extern void native_fn_02061dcc(void);
extern void native_fn_02049ffc(void);
extern void native_fn_02008be0(void);
extern void native_fn_02072f48(void);
extern void native_fn_0204aaf0(void);
extern void native_fn_02044fcc(void);
extern void native_fn_02063520(void);
extern void native_fn_02044bac(void);
extern void native_fn_02066a6c(void);
extern void native_fn_02087a48(void);
extern void native_fn_0204ac20(void);
extern void native_fn_0204ab98(void);
extern void native_fn_020449d4(void);
extern void native_fn_0207b460(void);
extern u8 native_data_0222f564[];
extern u8 native_data_0222f568[];


asm u32 native_ov000_02203b7c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #144
    mov r5, r0
    bl native_fn_02061944
    mov r0, r5
    bl native_fn_02061dcc
    add r2, sp, #12
    mov r1, #0
    strh r1, [r2]
    strh r1, [r2, #2]
    ldr r0, [r0]
    mov r4, #1
    cmp r0, #0
    ldrne r8, [r0, #0x4]
    cmpne r8, #0
    addeq sp, sp, #144
    ldmeqia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    mov r0, r8
    bl native_fn_02049ffc
    add r1, sp, #80
    mov r0, #0
    mov r2, #64
    bl native_fn_02008be0
    ldr r0, [pc, #0x3bc]
    ldrsh r0, [r0, #12]
    cmp r0, #0
    ble L_02203bf4
    bl native_fn_02072f48
    cmp r0, #0
    movne r4, #0
L_02203bf4:
    cmp r5, #14
    addls pc, pc, r5, lsl #2
    b L_02203f94
    dcd 0xea0000e3
    dcd 0xea0000e2
    dcd 0xea0000e1
    dcd 0xea0000e0
    dcd 0xea0000df
    dcd 0xea0000de
    dcd 0xea000007
    dcd 0xea000015
    dcd 0xea00004d
    dcd 0xea000060
    dcd 0xea00008c
    dcd 0xea00009f
    dcd 0xea00009e
    dcd 0xea00009d
    dcd 0xea00009c
    mov r0, #22
    str r0, [sp]
    mov r2, #1
    str r2, [sp, #0x4]
    str r2, [sp, #0x8]
    add r1, sp, #12
    mov r0, r5
    mov r2, #9
    mov r3, #5
    bl native_fn_0204aaf0
    ldrsh r1, [sp, #12]
    add r0, r1, r0
    strh r0, [sp, #12]
    add sp, sp, #144
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    ldr r1, [pc, #0x31c]
    ldrsh r0, [r1, #12]
    ldrb r1, [r1, #0xe]
    bl native_fn_02044fcc
    cmp r0, #0
    bne L_02203d3c
    ldr r1, [pc, #0x304]
    ldrsh r0, [r1, #12]
    ldrb r1, [r1, #0xe]
    bl native_fn_02063520
    cmp r0, #0
    cmpne r4, #0
    beq L_02203d3c
    mov r10, #0
    ldr r7, [pc, #0x2e8]
    ldr r11, [pc, #0x2e0]
    mov r9, r10
    mov r6, #1
    add r5, sp, #80
    mov r4, r10
L_02203cc8:
    ldrsh r0, [r11, #12]
    and r1, r9, #255
    bl native_fn_02044bac
    cmp r0, #0
    beq L_02203d14
    add r0, r9, #2
    and r0, r0, #255
    bl native_fn_02066a6c
    add r0, r7, r0, lsl #1
    add r0, r0, #512
    ldrh r2, [r0, #246]
    mov r0, r8
    mov r1, r4
    strh r2, [sp, #80]
    str r6, [sp]
    str r5, [sp, #0x4]
    mov r2, r10
    mov r3, r4
    bl native_fn_02087a48
L_02203d14:
    add r0, r9, #1
    add r2, r10, #8
    mov r1, r0, lsl #16
    mov r0, r2, lsl #16
    mov r9, r1, lsr #16
    cmp r9, #7
    mov r10, r0, asr #16
    blo L_02203cc8
    add sp, sp, #144
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
L_02203d3c:
    mov r2, #1
    add r1, sp, #12
    mov r0, r5
    mov r3, #7
    str r2, [sp]
    bl native_fn_0204ac20
    add sp, sp, #144
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    mov r0, #18
    str r0, [sp]
    mov r3, #1
    str r3, [sp, #0x4]
    add r1, sp, #12
    mov r0, r5
    mov r2, #5
    str r3, [sp, #0x8]
    bl native_fn_0204aaf0
    mov r2, #40
    strh r2, [sp, #12]
    mov r4, #0
    ldr r3, [pc, #0x210]
    add r1, sp, #12
    mov r0, r5
    mov r2, #1
    str r4, [sp]
    bl native_fn_0204ab98
    add sp, sp, #144
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    ldr r1, [pc, #0x1e8]
    ldrsh r0, [r1, #12]
    ldrb r1, [r1, #0xe]
    bl native_fn_02044fcc
    cmp r0, #0
    bne L_02203e24
    ldr r1, [pc, #0x1d0]
    ldrsh r0, [r1, #12]
    ldrb r1, [r1, #0xe]
    bl native_fn_02063520
    cmp r0, #0
    cmpne r4, #0
    beq L_02203e24
    ldr r0, [pc, #0x1b4]
    ldrsh r0, [r0, #12]
    bl native_fn_020449d4
    ldrb r0, [r0, #0x5f]
    mov r2, #1
    add r1, sp, #12
    stmia sp, {r0, r2}
    str r2, [sp, #0x8]
    mov r0, r5
    mov r2, #8
    mov r3, #0
    bl native_fn_0204aaf0
    ldrsh r1, [sp, #12]
    add r0, r1, r0
    strh r0, [sp, #12]
    add sp, sp, #144
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
L_02203e24:
    mov r0, #42
    str r0, [sp]
    mov r2, #1
    str r2, [sp, #0x4]
    str r2, [sp, #0x8]
    add r1, sp, #12
    mov r0, r5
    mov r2, #5
    mov r3, #7
    bl native_fn_0204aaf0
    ldrsh r1, [sp, #12]
    add r0, r1, r0
    strh r0, [sp, #12]
    add sp, sp, #144
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    mov r0, #16
    str r0, [sp]
    mov r3, #1
    str r3, [sp, #0x4]
    add r1, sp, #12
    mov r0, r5
    mov r2, #5
    str r3, [sp, #0x8]
    bl native_fn_0204aaf0
    mov r2, #40
    strh r2, [sp, #12]
    mov r4, #0
    ldr r3, [pc, #0x110]
    add r1, sp, #12
    mov r0, r5
    mov r2, #1
    str r4, [sp]
    bl native_fn_0204ab98
    add sp, sp, #144
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    ldr r1, [pc, #0xe4]
    add r3, sp, #16
    ldrsh r0, [r1, #12]
    ldrb r1, [r1, #0xe]
    mov r2, #0
    bl native_fn_0207b460
    ldr r1, [pc, #0xcc]
    ldrsh r0, [r1, #12]
    ldrb r1, [r1, #0xe]
    bl native_fn_02044fcc
    cmp r0, #0
    bne L_02203f54
    ldr r1, [pc, #0xb4]
    ldrsh r0, [r1, #12]
    ldrb r1, [r1, #0xe]
    bl native_fn_02063520
    cmp r0, #0
    cmpne r4, #0
    beq L_02203f54
    add r0, sp, #16
    sub r1, r5, #11
    ldrb r0, [r0, r1]
    cmp r0, #0
    bne L_02203f1c
    cmp r5, #11
    addne sp, sp, #144
    ldmneia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
L_02203f1c:
    str r0, [sp]
    mov r2, #1
    str r2, [sp, #0x4]
    str r2, [sp, #0x8]
    add r1, sp, #12
    mov r0, r5
    mov r2, #11
    mov r3, #0
    bl native_fn_0204aaf0
    ldrsh r1, [sp, #12]
    add r0, r1, r0
    strh r0, [sp, #12]
    add sp, sp, #144
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
L_02203f54:
    cmp r5, #11
    addne sp, sp, #144
    ldmneia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    mov r0, #42
    str r0, [sp]
    mov r2, #1
    str r2, [sp, #0x4]
    str r2, [sp, #0x8]
    add r1, sp, #12
    mov r0, r5
    mov r2, #5
    mov r3, #7
    bl native_fn_0204aaf0
    ldrsh r1, [sp, #12]
    add r0, r1, r0
    strh r0, [sp, #12]
L_02203f94:
    add sp, sp, #144
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    dcd 0x02238190
    dcd 0x020dbc18
    dcd native_data_0222f564
    dcd native_data_0222f568
}
