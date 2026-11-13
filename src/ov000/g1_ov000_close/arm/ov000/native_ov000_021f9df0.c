/* ov000 row 0x021f9df0: 1584 bytes.
 *
 * What it does: 392 instructions and 94 call(s), then a 12-entry dispatch through an inline branch table at 0x021f9f48 (dispatch word at 0x021f9f40)
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

extern void ov000_display_context_02215698(void);
extern void native_fn_0202a634(void);
extern void native_fn_02217440(void);
extern void native_fn_022156c4(void);
extern void native_fn_02062378(void);
extern void native_fn_02061260(void);
extern void native_fn_020620b4(void);
extern void native_fn_021f95b0(void);
extern void native_fn_021f9614(void);
extern void native_fn_021f9948(void);
extern void native_fn_021f8e4c(void);
extern void native_fn_021f99b0(void);
extern void native_fn_02063b60(void);
extern void native_fn_022156a4(void);
extern void native_fn_02062074(void);
extern void native_fn_021e7b9c(void);
extern void native_fn_02217814(void);
extern void native_fn_02062aa0(void);
extern void native_fn_021f9cdc(void);
extern void native_fn_021fbddc(void);
extern void native_fn_021fbdec(void);
extern void native_fn_021f8b0c(void);
extern void native_fn_02215814(void);
extern void native_fn_0221573c(void);
extern void native_fn_0221570c(void);
extern void native_fn_02219480(void);
extern void native_fn_021f9d50(void);
extern void native_fn_02062368(void);
extern void native_fn_021f933c(void);
extern void native_fn_021f9484(void);
extern void native_fn_0204b2d0(void);
extern void native_fn_0206d250(void);
extern void native_fn_021f85c8(void);
extern void native_fn_021f8f70(void);
extern void native_fn_021f96a8(void);
extern void native_fn_021f8990(void);
extern void native_fn_021f8588(void);
extern void native_fn_0204b414(void);
extern void native_fn_0205f98c(void);
extern void native_fn_02048a94(void);
extern void native_fn_0204b380(void);
extern void native_fn_021f8aac(void);
extern void native_fn_021f9768(void);
extern void native_fn_021f9148(void);
extern void native_fn_0206cfe4(void);
extern void native_fn_021f97ec(void);
extern void native_fn_02062a50(void);
extern void native_fn_0206dcd0(void);
extern void native_fn_021faba8(void);


asm u32 native_ov000_021f9df0 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, lr}
    sub sp, sp, #12
    bl ov000_display_context_02215698
    mov r4, r0
    bl native_fn_0202a634
    mov r7, r0
    bl native_fn_02217440
    mov r5, r0
    bl native_fn_022156c4
    add r1, r4, #1024
    ldrsb r1, [r1, #154]
    mov r6, r0
    cmp r1, #1
    bne L_021f9e54
    bl native_fn_02062378
    cmp r0, #0
    beq L_021f9e48
    mov r0, #1
    bl native_fn_02061260
    mov r0, #0
    bl native_fn_020620b4
    b L_021f9e5c
L_021f9e48:
    mov r0, #0
    bl native_fn_02061260
    b L_021f9e5c
L_021f9e54:
    mov r0, #0
    bl native_fn_02061260
L_021f9e5c:
    ldrh r1, [r7, #2]
    ldr r0, [pc, #0x5a8]
    tst r1, r0
    beq L_021f9ed0
    add r0, r4, #1024
    ldrsb r1, [r0, #154]
    cmp r1, #1
    bne L_021f9ebc
    ldrsb r1, [r0, #144]
    ldrsb r0, [r0, #145]
    add r0, r1, r0, lsl #2
    and r0, r0, #255
    bl native_fn_021f95b0
    bl native_fn_021f9614
    mov r4, r0
    bl native_fn_021f9948
    mov r1, #0
    bl native_fn_021f8e4c
    mov r0, r4
    bl native_fn_021f99b0
    cmp r0, #0
    ble L_021f9ebc
    mov r1, #0
    bl native_fn_02063b60
L_021f9ebc:
    mov r0, #127
    bl native_fn_022156a4
    mov r0, #0
    bl native_fn_02062074
    b L_021fa404
L_021f9ed0:
    tst r1, #1
    beq L_021fa144
    add r0, r4, #1024
    ldrsb r1, [r0, #154]
    cmp r1, #0
    beq L_021fa138
    cmp r1, #1
    bne L_021fa404
    ldrsb r1, [r0, #144]
    ldrsb r0, [r0, #145]
    add r0, r1, r0, lsl #2
    and r0, r0, #255
    bl native_fn_021f95b0
    bl native_fn_021f9614
    mov r4, r0
    bl native_fn_02062378
    cmp r0, #0
    bne L_021fa404
    cmp r4, #127
    bne L_021f9f2c
    mov r0, #84
    bl native_fn_021e7b9c
    b L_021fa404
L_021f9f2c:
    mov r0, r4
    bl native_fn_02217814
    cmp r0, #0
    bne L_021fa010
    cmp r4, #11
    addls pc, pc, r4, lsl #2
    b L_021fa004
    dcd 0xea00002d
    dcd 0xea00002c
    dcd 0xea00002b
    dcd 0xea00002a
    dcd 0xea000029
    dcd 0xea000028
    dcd 0xea000018
    dcd 0xea00000d
    dcd 0xea000025
    dcd 0xea000024
    dcd 0xea000014
    dcd 0xeaffffff
    bl native_fn_02062aa0
    cmp r0, #0
    beq L_021fa004
    mov r3, #1
    mov r0, #5
    mov r1, #6
    mov r2, #41
    str r3, [sp]
    bl native_fn_021f9cdc
    b L_021fa004
    bl native_fn_02062aa0
    cmp r0, #0
    beq L_021fa004
    mov r3, #1
    mov r0, #5
    mov r1, #6
    mov r2, #40
    str r3, [sp]
    bl native_fn_021f9cdc
    b L_021fa004
    mov r0, r4
    bl native_fn_021f9948
    mov r1, #0
    bl native_fn_021f8e4c
    mov r0, r4
    bl native_fn_021f99b0
    mov r1, #0
    bl native_fn_02063b60
    mov r0, r4
    bl native_fn_021fbddc
    mov r0, #0
    mov r1, #1
    mov r2, r1
    bl native_fn_021fbdec
    bl native_fn_021f8b0c
L_021fa004:
    mov r0, #84
    bl native_fn_021e7b9c
    b L_021fa404
L_021fa010:
    str r4, [r5]
    bl native_fn_02215814
    mov r0, #0
    bl native_fn_02061260
    cmp r4, #10
    addls pc, pc, r4, lsl #2
    b L_021fa078
    b L_021fa078
    b L_021fa078
    b L_021fa078
    b L_021fa078
    b L_021fa078
    b L_021fa078
    b L_021fa058
    b L_021fa058
    b L_021fa058
    b L_021fa058
    b L_021fa058
L_021fa058:
    mov r0, r4
    bl native_fn_021f9948
    mov r1, #0
    bl native_fn_021f8e4c
    mov r0, r4
    bl native_fn_021f99b0
    mov r1, #0
    bl native_fn_02063b60
L_021fa078:
    cmp r4, #15
    addls pc, pc, r4, lsl #2
    b L_021fa11c
    b L_021fa11c
    b L_021fa11c
    b L_021fa11c
    b L_021fa11c
    b L_021fa11c
    b L_021fa11c
    b L_021fa0fc
    b L_021fa11c
    b L_021fa11c
    b L_021fa11c
    b L_021fa0fc
    b L_021fa114
    b L_021fa0c4
    b L_021fa11c
    b L_021fa11c
    b L_021fa0c4
L_021fa0c4:
    mov r0, r4, lsl #24
    mov r0, r0, asr #24
    bl native_fn_0221573c
    mov r0, #127
    bl native_fn_022156a4
    mov r0, #0
    bl native_fn_02062074
    mov r0, #1
    bl native_fn_0221570c
    cmp r4, #15
    beq L_021fa404
    mov r0, #1
    bl native_fn_02219480
    b L_021fa404
L_021fa0fc:
    ldr r2, [pc, #0x310]
    ldr r1, [pc, #0x310]
    mov r0, r4
    str r2, [r1, #0x4]
    bl native_fn_021fbddc
    b L_021fa404
L_021fa114:
    bl native_fn_021f9d50
    b L_021fa404
L_021fa11c:
    add r0, r4, #1
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_022156a4
    mov r0, #1
    bl native_fn_0221570c
    b L_021fa404
L_021fa138:
    mov r0, #1
    bl native_fn_02062368
    b L_021fa404
L_021fa144:
    bl native_fn_021f933c
    cmp r0, #0
    beq L_021fa1e0
    add r0, r4, #1024
    ldrsb r1, [r0, #144]
    ldrsb r0, [r0, #145]
    add r0, r1, r0, lsl #2
    and r0, r0, #255
    bl native_fn_021f95b0
    bl native_fn_021f9614
    add r0, r4, #1024
    ldrsb r1, [r0, #154]
    cmp r1, #1
    bne L_021fa1a0
    ldrsb r1, [r0, #144]
    ldrsb r2, [r0, #145]
    add r0, sp, #8
    bl native_fn_021f9484
    add r2, sp, #8
    add r0, r4, #16
    mov r1, #0
    bl native_fn_0204b2d0
    b L_021fa1d4
L_021fa1a0:
    ldrsb r0, [r0, #145]
    add r1, r4, #160
    add r1, r1, r0, lsl #3
    ldrb r0, [r1, #0x4]
    strh r0, [sp, #8]
    ldrb r0, [r1, #0x5]
    strh r0, [sp, #10]
    ldrsb r0, [r1, #6]
    bl native_fn_0206d250
    mov r1, r0
    add r2, sp, #8
    add r0, r4, #16
    bl native_fn_0204b2d0
L_021fa1d4:
    bl native_fn_021f85c8
    bl native_fn_021f8f70
    b L_021fa404
L_021fa1e0:
    bl native_fn_021f96a8
    mov r5, r0
    mvn r0, #0
    cmp r5, r0
    beq L_021fa324
    add r0, r4, #1024
    ldrsb r0, [r0, #154]
    cmp r0, #1
    beq L_021fa214
    mov r1, #1
    mov r0, #0
    strb r1, [r4, #0x49a]
    bl native_fn_020620b4
L_021fa214:
    strb r5, [r4, #0x492]
    add r0, r4, #1024
    ldrsb r1, [r0, #146]
    and r7, r5, #255
    mov r0, r7
    strb r1, [r4, #0x493]
    bl native_fn_021f95b0
    add r1, r4, #1024
    ldrsb r12, [r1, #146]
    add r1, r4, #184
    mov r2, #80
    mov r5, r12, lsr #31
    rsb r3, r5, r12, lsl #30
    add r3, r5, r3, ror #30
    mov r5, r12, asr #1
    mla r8, r0, r2, r1
    mov r3, r3, lsl #24
    add r12, r12, r5, lsr #30
    mov r5, r3, asr #24
    mov r3, r12, lsl #22
    mov r0, r7
    strb r5, [r4, #0x490]
    mov r9, r3, asr #24
    strb r9, [r4, #0x491]
    bl native_fn_021f95b0
    bl native_fn_021f9614
    bl native_fn_021f8990
    mov r1, r5
    mov r2, r9
    add r0, sp, #4
    bl native_fn_021f9484
    add r0, sp, #4
    bl native_fn_021f8588
    add r2, r4, #1024
    ldrsb r1, [r2, #144]
    ldrsb r2, [r2, #145]
    add r0, sp, #8
    bl native_fn_021f9484
    add r0, r4, #16
    mov r1, #0
    add r2, sp, #8
    bl native_fn_0204b2d0
    add r0, r4, #16
    mov r1, #15
    bl native_fn_0204b414
    ldr r0, [r8, #0x1c]
    mov r1, #0
    bl native_fn_0205f98c
    ldrb r1, [r8, #0x20]
    sub r1, r1, #2
    and r1, r1, #255
    bl native_fn_02048a94
    add r0, r4, #16
    mov r1, #0
    bl native_fn_0204b380
    mov r0, #101
    bl native_fn_021e7b9c
    mov r0, #7
    strb r0, [r4, #0x494]
    mov r0, #1
    strb r0, [r4, #0x49a]
    bl native_fn_021f85c8
    bl native_fn_021f8f70
    mov r0, r7
    bl native_fn_021f95b0
    mov r1, #1
    bl native_fn_021f8aac
    b L_021fa404
L_021fa324:
    bl native_fn_021f9768
    mov r5, r0
    mvn r0, #0
    cmp r5, r0
    beq L_021fa404
    add r0, r4, #1024
    ldrsb r0, [r0, #154]
    cmp r0, #0
    beq L_021fa358
    mov r1, #0
    mov r0, #1
    strb r1, [r4, #0x49a]
    bl native_fn_020620b4
L_021fa358:
    mov r0, r5
    bl native_fn_021f9148
    add r0, r4, #1024
    ldrsb r0, [r0, #145]
    add r1, r4, #160
    add r7, r1, r0, lsl #3
    ldrb r0, [r7, #0x4]
    strh r0, [sp, #8]
    ldrb r0, [r7, #0x5]
    strh r0, [sp, #10]
    ldrsb r0, [r7, #6]
    bl native_fn_0206d250
    mov r1, r0
    add r2, sp, #8
    add r0, r4, #16
    bl native_fn_0204b2d0
    add r0, r4, #16
    mov r1, #15
    bl native_fn_0204b414
    ldrsb r0, [r7, #6]
    mov r1, #2
    bl native_fn_0206cfe4
    add r0, r4, #16
    mov r1, #0
    bl native_fn_0204b380
    strb r5, [r4, #0x497]
    bl native_fn_021f97ec
    add r0, r4, #1024
    ldrsb r2, [r0, #151]
    ldr r0, [pc, #0x48]
    mov r1, #2
    ldrsb r0, [r0, r2]
    bl native_fn_0206cfe4
    mov r0, #8
    strb r0, [r4, #0x494]
    mov r0, #101
    bl native_fn_021e7b9c
    bl native_fn_021f85c8
    bl native_fn_021f8f70
    add r0, r4, #1024
    ldrsb r0, [r0, #145]
    bl native_fn_02062a50
    bl native_fn_0206dcd0
L_021fa404:
    mov r0, r6
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, r8, r9, pc}
    dcd 0x00000402
    dcd native_fn_021faba8
    dcd 0x02236f14
    dcd 0x02236f28
}
