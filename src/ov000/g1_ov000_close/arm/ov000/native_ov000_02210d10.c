/* ov000 row 0x02210d10: 504 bytes.
 *
 * What it does: 124 instructions and 17 call(s), then a 8-entry dispatch through an inline branch table at 0x02210db8 (dispatch word at 0x02210db0)
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

extern void native_fn_02042cd0(void);
extern void native_fn_02025a28(void);
extern void native_fn_02025578(void);
extern void native_fn_02025a70(void);
extern void native_fn_02025504(void);
extern void ov000_saved_world_position_get_021e07b8(void);
extern void native_fn_0200236c(void);
extern void native_fn_021e7bbc(void);
extern void native_fn_02214b04(void);
extern void native_fn_02209bc0(void);
extern void native_fn_022104e8(void);


asm u32 native_ov000_02210d10 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #8
    mov r9, r0
    ldr r1, [r9, #0x60]
    ldr r0, [r9, #0x164]
    ldr r6, [r1]
    mov r11, #0
    bl native_fn_02042cd0
    movs r10, r0
    addeq sp, sp, #8
    moveq r0, r11
    ldmeqia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    ldr r5, [pc, #0x1b8]
    mov r8, r10
    mov r7, r11
L_02210d4c:
    mov r0, r6
    bl native_fn_02025a28
    mov r1, r5
    bl native_fn_02025578
    mov r4, r0
    ldrh r0, [r8]
    bl native_fn_02025a70
    mov r1, r0
    mov r0, r4
    bl native_fn_02025504
    bne L_02210d94
    mov r0, #6
    mla r2, r7, r0, r10
    ldrh r1, [r2, #2]
    ldr r0, [pc, #0x178]
    ldrh r11, [r2, #4]
    str r1, [r0, #0x4]
    b L_02210da4
L_02210d94:
    add r7, r7, #1
    cmp r7, #16
    add r8, r8, #6
    blt L_02210d4c
L_02210da4:
    ldr r0, [pc, #0x158]
    ldr r0, [r0, #0x4]
    cmp r0, #7
    addls pc, pc, r0, lsl #2
    b L_02210ef4
    dcd 0xea00004d
    dcd 0xea00004c
    dcd 0xea000004
    dcd 0xea00004a
    dcd 0xea000049
    dcd 0xea000033
    dcd 0xea000047
    dcd 0xea000039
    add r0, r9, #256
    ldrsb r1, [r0, #220]
    mvn r0, #0
    cmp r1, r0
    beq L_02210ef4
    mov r0, #0
    bl ov000_saved_world_position_get_021e07b8
    mov r8, r0
    mov r0, #0
    bl ov000_saved_world_position_get_021e07b8
    mov r7, r0
    mov r0, #0
    bl ov000_saved_world_position_get_021e07b8
    mov r5, r0
    mov r0, #0
    bl ov000_saved_world_position_get_021e07b8
    mov r4, r0
    mov r0, #0
    bl ov000_saved_world_position_get_021e07b8
    mov r6, r0
    mov r0, #0
    bl ov000_saved_world_position_get_021e07b8
    ldr r1, [r7, #0x8]
    ldr r3, [r6, #0x4]
    ldr r7, [r9, #0x78]
    ldr r2, [r8, #0x8]
    ldr r5, [r5]
    ldr r4, [r4]
    ldr r6, [r9, #0x70]
    sub r2, r7, r2
    sub r1, r7, r1
    sub r7, r6, r5
    sub r5, r6, r4
    ldr r4, [r9, #0x74]
    ldr r0, [r0, #0x4]
    sub r3, r4, r3
    sub r0, r4, r0
    smull r0, r4, r3, r0
    smlal r0, r4, r7, r5
    smlal r0, r4, r2, r1
    mov r0, r0, lsr #12
    orr r0, r0, r4, lsl #20
    bl native_fn_0200236c
    mov r0, r0, asr #12
    rsbs r1, r0, #135
    add r0, r9, #256
    ldrsb r0, [r0, #220]
    movmi r1, #0
    bl native_fn_021e7bbc
    b L_02210ef4
    mov r0, r9
    bl native_fn_02214b04
    cmp r0, #0
    bne L_02210ef4
    ldr r0, [pc, #0x4c]
    mov r1, #0
    str r1, [r0, #0x4]
    b L_02210ef4
    add r1, sp, #4
    add r2, sp, #0
    mov r0, r11
    bl native_fn_02209bc0
    cmp r0, #0
    beq L_02210ee8
    ldr r1, [sp, #0x4]
    ldr r2, [sp]
    mov r0, r9
    bl native_fn_022104e8
L_02210ee8:
    ldr r0, [pc, #0x14]
    mov r1, #0
    str r1, [r0, #0x4]
L_02210ef4:
    mov r0, #0
    add sp, sp, #8
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    dcd 0x45800000
    dcd 0x022385b8
}
