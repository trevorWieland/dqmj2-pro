/* ov000 row 0x0220ae40: 1224 bytes.
 *
 * What it does: 306 instructions and 53 call(s), then a 7-entry dispatch through an inline branch table at 0x0220ae60 (dispatch word at 0x0220ae58)
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

extern void native_fn_021e5f48(void);
extern void native_fn_020c56b4(void);
extern void native_fn_02042bfc(void);
extern void native_fn_021e5f2c(void);
extern void native_fn_0220a2a4(void);
extern void native_fn_020430b4(void);
extern void native_fn_02042464(void);
extern void native_fn_0220a284(void);
extern void native_fn_021e5ed8(void);
extern void native_fn_021e5ef4(void);
extern void native_fn_021e5f10(void);
extern void native_fn_020420c4(void);
extern void native_fn_02000ce8(void);
extern void native_fn_020280a0(void);
extern void native_fn_02028044(void);
extern void native_fn_02027fe8(void);
extern void native_fn_02000e1c(void);
extern void ov000_saved_world_position_get_021e07b8(void);
extern void native_fn_02041f74(void);
extern void native_fn_020028d8(void);
extern void native_fn_0200235c(void);
extern void native_fn_021e5f6c(void);
extern void native_fn_02042c2c(void);
extern void native_fn_02028158(void);
extern void native_fn_02042104(void);
extern void native_fn_021e5fa4(void);
extern void native_fn_0205cba4(void);


asm u32 native_ov000_0220ae40 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    sub sp, sp, #144
    mov r5, r0
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5f48
    cmp r0, #6
    addls pc, pc, r0, lsl #2
    b L_0220b2f0
    dcd 0xea000005
    dcd 0xea00006e
    dcd 0xea000094
    dcd 0xea00011f
    dcd 0xea00011e
    dcd 0xea0000b2
    dcd 0xea0000fe
    ldrb r0, [r5, #0x279]
    cmp r0, #0
    bne L_0220af2c
    add r0, r5, #512
    ldrsh r0, [r0, #118]
    bl native_fn_020c56b4
    ldr r1, [r0, #0x14]
    mov r0, r5
    bl native_fn_02042bfc
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5f2c
    cmp r0, #1
    bne L_0220aec4
    mov r0, r5
    mov r1, #1
    mov r2, #0
    bl native_fn_0220a2a4
    b L_0220af04
L_0220aec4:
    mov r0, #0
    strb r0, [r5, #0x15f]
    add r0, r5, #256
    ldrsh r0, [r0, #106]
    bl native_fn_020430b4
    ldrsh r1, [r0, #6]
    mov r0, r5
    mov r2, #0
    bl native_fn_02042464
    cmp r0, #0
    beq L_0220aefc
    mov r0, #1
    bl native_fn_0220a284
    str r0, [r5, #0x264]
L_0220aefc:
    mov r0, #1
    strb r0, [r5, #0x15f]
L_0220af04:
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5ed8
    ldr r1, [r0]
    mov r0, r5
    bl native_fn_02042bfc
    add r0, r5, #512
    mov r1, #0
    strh r1, [r0, #122]
    mov r0, #10
    strb r0, [r5, #0x279]
L_0220af2c:
    add r0, r5, #512
    ldrsh r0, [r0, #122]
    tst r0, #3
    bne L_0220b2f0
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5ef4
    mov r4, r0
    ldr r1, [r5, #0x74]
    ldr r0, [r4, #0x4]
    ldr r3, [r5, #0x70]
    sub r12, r1, r0
    ldr r1, [r4]
    smull r0, r2, r12, r12
    sub r1, r3, r1
    smlal r0, r2, r1, r1
    ldr r12, [r5, #0x78]
    ldr r3, [r4, #0x8]
    mov r1, #0
    sub r3, r12, r3
    smlal r0, r2, r3, r3
    mov r0, r0, lsr #12
    orr r0, r0, r2, lsl #20
    subs r0, r0, #4096
    rscs r0, r1, r2, asr #12
    bge L_0220afb4
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5f10
    cmp r0, #255
    beq L_0220afb4
    mov r1, #0
    strb r1, [r5, #0x279]
    add sp, sp, #144
    strb r0, [r5, #0x2c0]
    ldmia sp!, {r4, r5, r6, pc}
L_0220afb4:
    mov r0, r5
    mov r1, r4
    bl native_fn_020420c4
    ldrb r0, [r5, #0x9]
    cmp r0, #0
    beq L_0220b2f0
    add r0, sp, #0
    bl native_fn_02000ce8
    ldr r1, [r5, #0x90]
    add r0, sp, #36
    bl native_fn_020280a0
    ldr r1, [r5, #0x8c]
    add r0, sp, #72
    bl native_fn_02028044
    ldr r1, [r5, #0x88]
    add r0, sp, #108
    bl native_fn_02027fe8
    add r0, sp, #72
    add r1, sp, #36
    add r2, sp, #0
    bl native_fn_02000e1c
    add r0, sp, #108
    add r1, sp, #0
    add r2, r5, #148
    bl native_fn_02000e1c
    mov r0, #0
    strb r0, [r5, #0x9]
    b L_0220b2f0
    ldrb r0, [r5, #0x279]
    cmp r0, #0
    bne L_0220b070
    mov r0, #0
    bl native_fn_0220a284
    str r0, [r5, #0x264]
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5f2c
    mov r1, r0
    mov r0, r5
    mov r2, #1
    bl native_fn_02042464
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5ed8
    ldr r1, [r0]
    mov r0, r5
    bl native_fn_02042bfc
    mov r0, #10
    strb r0, [r5, #0x279]
L_0220b070:
    ldrb r0, [r5, #0x279]
    cmp r0, #10
    bne L_0220b2f0
    ldr r1, [r5, #0x60]
    ldr r0, [r1, #0x8]
    ldr r1, [r1]
    ldrh r0, [r0, #4]
    mov r0, r0, lsl #12
    sub r0, r0, #1
    cmp r1, r0
    blt L_0220b2f0
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5f10
    cmp r0, #255
    beq L_0220b2f0
    mov r1, #0
    strb r1, [r5, #0x279]
    add sp, sp, #144
    strb r0, [r5, #0x2c0]
    ldmia sp!, {r4, r5, r6, pc}
    ldrb r0, [r5, #0x279]
    cmp r0, #0
    bne L_0220b104
    mov r1, #0
    mov r0, r5
    mov r2, r1
    bl native_fn_0220a2a4
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5ed8
    ldr r1, [r0]
    mov r0, r5
    bl native_fn_02042bfc
    add r0, r5, #512
    mov r1, #0
    strh r1, [r0, #122]
    mov r0, #10
    strb r0, [r5, #0x279]
L_0220b104:
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5f2c
    add r1, r5, #512
    ldrsh r1, [r1, #122]
    mov r0, r0, lsl #16
    cmp r1, r0, asr #16
    ble L_0220b2f0
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5f10
    cmp r0, #255
    beq L_0220b2f0
    mov r1, #0
    strb r1, [r5, #0x279]
    add sp, sp, #144
    strb r0, [r5, #0x2c0]
    ldmia sp!, {r4, r5, r6, pc}
    ldrb r0, [r5, #0x279]
    cmp r0, #0
    bne L_0220b1ec
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5ed8
    ldr r1, [r0]
    mov r0, r5
    bl native_fn_02042bfc
    mov r0, #0
    bl ov000_saved_world_position_get_021e07b8
    mov r4, r0
    mov r0, r5
    mov r1, #0
    bl native_fn_02041f74
    ldr r2, [r0]
    ldr r3, [r4]
    mov r0, r5
    mov r1, #0
    sub r6, r3, r2
    bl native_fn_02041f74
    mov r0, #0
    bl ov000_saved_world_position_get_021e07b8
    mov r0, #0
    bl ov000_saved_world_position_get_021e07b8
    mov r4, r0
    mov r0, r5
    mov r1, #0
    bl native_fn_02041f74
    ldr r1, [r0, #0x8]
    ldr r2, [r4, #0x8]
    mov r0, r6
    sub r1, r2, r1
    bl native_fn_020028d8
    str r0, [r5, #0x27c]
    mov r1, #71
    bl native_fn_0200235c
    str r0, [r5, #0x27c]
    mov r1, #0
    add r0, r5, #512
    strh r1, [r0, #122]
    mov r0, #10
    strb r0, [r5, #0x279]
L_0220b1ec:
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5f6c
    mov r4, r0
    mov r0, r5
    bl native_fn_02042c2c
    mov r6, r0
    ldr r1, [r5, #0x27c]
    add r0, r4, #4096
    subs r1, r6, r1
    rsbmi r1, r1, #0
    cmp r1, r0
    bge L_0220b240
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5f10
    cmp r0, #255
    beq L_0220b240
    mov r1, #0
    strb r1, [r5, #0x279]
    add sp, sp, #144
    strb r0, [r5, #0x2c0]
    ldmia sp!, {r4, r5, r6, pc}
L_0220b240:
    ldr r0, [r5, #0x27c]
    add r0, r0, #1474560
    sub r0, r0, r6
    bl native_fn_02028158
    cmp r0, #0
    mov r0, r5
    mov r2, #0
    ble L_0220b26c
    mov r1, r4
    bl native_fn_02042104
    b L_0220b2f0
L_0220b26c:
    rsb r1, r4, #0
    bl native_fn_02042104
    b L_0220b2f0
    ldrb r0, [r5, #0x279]
    cmp r0, #0
    bne L_0220b2c0
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5f2c
    mov r4, r0
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5fa4
    mov r2, r0, lsl #24
    mov r0, r4
    mov r1, r5
    mov r2, r2, asr #24
    bl native_fn_0205cba4
    add r0, r5, #512
    mov r1, #0
    strh r1, [r0, #122]
    mov r0, #10
    strb r0, [r5, #0x279]
L_0220b2c0:
    ldrb r0, [r5, #0x279]
    cmp r0, #10
    bne L_0220b2f0
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5f10
    cmp r0, #255
    beq L_0220b2f0
    mov r1, #0
    strb r1, [r5, #0x279]
    add sp, sp, #144
    strb r0, [r5, #0x2c0]
    ldmia sp!, {r4, r5, r6, pc}
L_0220b2f0:
    add r0, r5, #512
    ldrsh r1, [r0, #122]
    add r1, r1, #1
    strh r1, [r0, #122]
    add sp, sp, #144
    ldmia sp!, {r4, r5, r6, pc}
}
