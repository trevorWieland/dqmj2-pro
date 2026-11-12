/* ov000 row 0x022089b4: 448 bytes.
 *
 * What it does: 111 instructions and 23 call(s), then a 6-entry dispatch through an inline branch table at 0x022089ec (dispatch word at 0x022089e4)
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

extern void native_fn_02208b74(void);
extern void native_fn_0204157c(void);
extern void native_fn_020418b0(void);
extern void native_fn_02008d78(void);
extern void native_fn_0207e720(void);
extern void native_fn_02041538(void);
extern void native_fn_0207e874(void);
extern void native_fn_0207f390(void);
extern void native_fn_02205e80(void);
extern void native_fn_02205e70(void);
extern void native_fn_0207f254(void);
extern void native_fn_02041814(void);
extern void native_fn_0207f3b0(void);
extern void native_fn_02063a74(void);
extern void native_fn_0207e948(void);
extern void native_fn_02208b8c(void);
extern void native_fn_022063f8(void);
extern void native_fn_02207bc0(void);


asm u32 native_ov000_022089b4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #16
    mov r5, #0
    ldr r4, [pc, #0x1a8]
    mov r8, #2
    add r6, sp, #0
    mov r10, #16
    mov r11, #1
    mov r7, r5
L_022089d8:
    ldrb r0, [r4, #0x1]
    mov r9, r7
    cmp r0, #5
    addls pc, pc, r0, lsl #2
    b L_02208b50
    dcd 0xea000004
    dcd 0xea000056
    dcd 0xea000006
    dcd 0xea000054
    dcd 0xea000053
    dcd 0xea000048
    mov r0, #2
    bl native_fn_02208b74
    mov r9, #1
    b L_02208b5c
    ldrb r0, [r4]
    cmp r0, #4
    addls pc, pc, r0, lsl #2
    b L_02208b5c
    b L_02208a38
    b L_02208a58
    b L_02208aa0
    b L_02208ae8
    b L_02208b1c
L_02208a38:
    mov r0, r7
    bl native_fn_0204157c
    mov r0, #2
    bl native_fn_020418b0
    mov r0, #1
    strb r0, [r4]
    mov r9, r0
    b L_02208b5c
L_02208a58:
    mov r0, r6
    mov r1, r7
    mov r2, #16
    bl native_fn_02008d78
    mov r0, r6
    strb r5, [sp]
    str r5, [sp, #0x8]
    strb r10, [sp, #0xc]
    strb r11, [sp, #0xd]
    bl native_fn_0207e720
    mov r0, #0
    mov r1, #2
    mov r2, #10
    bl native_fn_02041538
    mov r0, #2
    strb r0, [r4]
    mov r9, #1
    b L_02208b5c
L_02208aa0:
    bl native_fn_0207e874
    cmp r0, #0
    beq L_02208b5c
    bl native_fn_0207f390
    cmp r0, #0
    beq L_02208ac8
    mov r0, #1
    bl native_fn_02205e80
    mov r0, #0
    bl native_fn_02205e70
L_02208ac8:
    mov r0, #1
    mov r1, #2
    mov r2, #10
    bl native_fn_02041538
    mov r0, #3
    strb r0, [r4]
    mov r9, #1
    b L_02208b5c
L_02208ae8:
    bl native_fn_0207f254
    bl native_fn_02041814
    cmp r0, #1
    beq L_02208b5c
    bl native_fn_0207f390
    cmp r0, #0
    beq L_02208b0c
    bl native_fn_0207f3b0
    bl native_fn_02063a74
L_02208b0c:
    bl native_fn_0207e948
    mov r0, #4
    strb r0, [r4]
    b L_02208b5c
L_02208b1c:
    mov r0, #5
    bl native_fn_02208b74
    b L_02208b5c
    bl native_fn_0207f390
    cmp r0, #0
    beq L_02208b40
    bl native_fn_02208b8c
    mov r8, #4
    b L_02208b5c
L_02208b40:
    mov r8, #1
    bl native_fn_022063f8
    bl native_fn_02207bc0
    b L_02208b5c
L_02208b50:
    mov r0, #0
    bl native_fn_02208b74
    mov r9, #1
L_02208b5c:
    cmp r9, #0
    bne L_022089d8
    mov r0, r8
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    dcd 0x0223850c
}
