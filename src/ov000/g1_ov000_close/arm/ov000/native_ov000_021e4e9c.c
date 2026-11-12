/* ov000 row 0x021e4e9c: 1060 bytes.
 *
 * What it does: 261 instructions and 75 call(s), then a 16-entry dispatch through an inline branch table at 0x021e4ecc (dispatch word at 0x021e4ec4)
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

extern void native_fn_0204bd00(void);
extern void native_fn_021e4dec(void);
extern void native_fn_02025a28(void);
extern void native_fn_0205bfd4(void);
extern void native_fn_02025a70(void);
extern void native_fn_02040500(void);
extern void native_fn_02040534(void);
extern void native_fn_02040518(void);
extern void native_fn_0205be14(void);
extern void native_fn_0205be64(void);
extern void native_fn_02213f4c(void);
extern void native_fn_02213f5c(void);
extern void native_fn_02213f74(void);
extern void native_fn_02213f8c(void);
extern void native_fn_021e8c08(void);
extern void native_fn_021df3bc(void);
extern void native_fn_020c4104(void);
extern void native_fn_02040424(void);
extern void native_fn_02063e80(void);
extern void native_fn_022126ec(void);
extern u8 native_data_0222ebf4[];


asm u32 native_ov000_021e4e9c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    ldr r0, [pc, #0x404]
    mov r1, r5
    mov r4, #0
    bl native_fn_0204bd00
    cmp r0, #0
    beq L_021e52a8
    sub r0, r5, #128
    cmp r0, #15
    addls pc, pc, r0, lsl #2
    b L_021e52a8
    dcd 0xea00000e
    dcd 0xea000029
    dcd 0xea0000f3
    dcd 0xea000050
    dcd 0xea00005b
    dcd 0xea000033
    dcd 0xea0000ef
    dcd 0xea00006a
    dcd 0xea0000ab
    dcd 0xea0000b8
    dcd 0xea0000c5
    dcd 0xea000019
    dcd 0xea000088
    dcd 0xea0000d2
    dcd 0xea0000d7
    dcd 0xea00000d
    bl native_fn_021e4dec
    bl native_fn_02025a28
    ldr r1, [pc, #0x394]
    str r0, [r1, #0x450]
    bl native_fn_0205bfd4
    bl native_fn_02025a70
    ldr r1, [pc, #0x384]
    str r0, [r1, #0x454]
    mov r0, #2
    bl native_fn_02040500
    mvn r0, #0
    bl native_fn_02040534
    mov r4, #1
    b L_021e52a8
    mov r0, #3
    bl native_fn_02040500
    mvn r0, #0
    bl native_fn_02040534
    mov r0, #2
    bl native_fn_02040518
    mov r4, #1
    b L_021e52a8
    mov r0, #4
    bl native_fn_02040500
    mvn r0, #0
    bl native_fn_02040518
    mov r4, #1
    b L_021e52a8
    bl native_fn_0205be14
    bl native_fn_02025a70
    ldr r1, [pc, #0x324]
    str r0, [r1, #0x450]
    bl native_fn_0205be64
    bl native_fn_02025a28
    ldr r1, [pc, #0x314]
    str r0, [r1, #0x454]
    mov r0, #29
    bl native_fn_02040500
    mvn r0, #0
    bl native_fn_02040534
    mov r4, #1
    b L_021e52a8
    bl native_fn_02213f4c
    movs r5, r0
    bmi L_021e52a8
    bl native_fn_02025a28
    ldr r1, [pc, #0x2e4]
    str r0, [r1, #0x450]
    mov r0, r5
    bl native_fn_02213f5c
    bl native_fn_02025a28
    ldr r1, [pc, #0x2d0]
    str r0, [r1, #0x454]
    mov r0, r5
    bl native_fn_02213f74
    bl native_fn_02025a70
    ldr r1, [pc, #0x2bc]
    str r0, [r1, #0x458]
    mov r0, r5
    bl native_fn_02213f8c
    bl native_fn_02025a70
    ldr r1, [pc, #0x2a8]
    str r0, [r1, #0x45c]
    mov r0, #5
    bl native_fn_02040500
    mvn r0, #0
    bl native_fn_02040518
    mov r4, #1
    b L_021e52a8
    bl native_fn_021e8c08
    cmp r0, #0
    blt L_021e52a8
    bl native_fn_02025a28
    ldr r1, [pc, #0x278]
    str r0, [r1, #0x450]
    mov r0, #5
    bl native_fn_02040500
    mvn r0, #0
    bl native_fn_02040518
    mov r4, #1
    b L_021e52a8
    ldr r0, [pc, #0x25c]
    ldrh r0, [r0, #4]
    cmp r0, #0
    beq L_021e52a8
    bl native_fn_02025a70
    ldr r2, [pc, #0x244]
    ldr r1, [pc, #0x244]
    str r0, [r2, #0x450]
    ldrh r0, [r1, #2]
    bl native_fn_02025a70
    ldr r1, [pc, #0x230]
    str r0, [r1, #0x454]
    mov r0, #5
    bl native_fn_02040500
    mvn r0, #0
    bl native_fn_02040518
    mov r4, #1
    b L_021e52a8
    ldr r0, [pc, #0x218]
    ldrsh r2, [r0]
    cmp r2, #0
    blt L_021e52a8
    ldr r1, [pc, #0x20c]
    mov r0, #52
    smlabb r5, r2, r0, r1
    ldrb r0, [r5, #0x1c]
    cmp r0, #0
    beq L_021e52a8
    ldrb r0, [r5, #0x1d]
    cmp r0, #1
    bne L_021e52a8
    ldrb r0, [r5, #0x1f]
    bl native_fn_02025a70
    ldr r1, [pc, #0x1d4]
    str r0, [r1, #0x450]
    ldrb r0, [r5, #0x1f]
    bl native_fn_021df3bc
    ldrh r0, [r0]
    mov r0, r0, lsl #16
    mov r0, r0, lsr #27
    bl native_fn_02025a70
    ldr r1, [pc, #0x1b4]
    str r0, [r1, #0x454]
    ldrsb r0, [r5, #30]
    bl native_fn_02025a28
    ldr r1, [pc, #0x1a4]
    str r0, [r1, #0x458]
    mov r0, #5
    bl native_fn_02040500
    mvn r0, #0
    bl native_fn_02040518
    mov r4, #1
    b L_021e52a8
    ldr r0, [pc, #0x18c]
    ldrsh r2, [r0]
    cmp r2, #0
    blt L_021e52a8
    ldr r1, [pc, #0x180]
    mov r0, #52
    smlabb r5, r2, r0, r1
    ldrb r0, [r5, #0x1c]
    cmp r0, #0
    beq L_021e52a8
    ldrb r0, [r5, #0x1d]
    cmp r0, #0
    bne L_021e52a8
    ldrb r0, [r5, #0x1f]
    bl native_fn_02025a70
    ldr r1, [pc, #0x148]
    str r0, [r1, #0x450]
    ldrsb r0, [r5, #30]
    bl native_fn_02025a28
    ldr r1, [pc, #0x138]
    str r0, [r1, #0x454]
    ldrb r0, [r5, #0x2b]
    bl native_fn_02025a70
    ldr r1, [pc, #0x128]
    str r0, [r1, #0x458]
    mov r0, #18
    bl native_fn_02040500
    mvn r0, #0
    bl native_fn_02040518
    mov r4, #1
    b L_021e52a8
    bl native_fn_020c4104
    bl native_fn_02025a28
    ldr r1, [pc, #0x100]
    str r0, [r1, #0x450]
    bl native_fn_02040424
    bl native_fn_02025a70
    ldr r1, [pc, #0xf0]
    str r0, [r1, #0x454]
    mov r0, #5
    bl native_fn_02040500
    mvn r0, #0
    bl native_fn_02040518
    mov r4, #1
    b L_021e52a8
    bl native_fn_020c4104
    bl native_fn_02025a28
    ldr r1, [pc, #0xc8]
    str r0, [r1, #0x450]
    bl native_fn_02040424
    bl native_fn_02025a70
    ldr r1, [pc, #0xb8]
    str r0, [r1, #0x454]
    mov r0, #5
    bl native_fn_02040500
    mvn r0, #0
    bl native_fn_02040518
    mov r4, #1
    b L_021e52a8
    bl native_fn_02063e80
    ldr r0, [r0, #0x1c]
    bl native_fn_02025a70
    ldr r1, [pc, #0x8c]
    str r0, [r1, #0x450]
    bl native_fn_02063e80
    ldr r0, [r0, #0x20]
    bl native_fn_02025a70
    ldr r1, [pc, #0x78]
    str r0, [r1, #0x454]
    mov r0, #5
    bl native_fn_02040500
    mvn r0, #0
    bl native_fn_02040518
    mov r4, #1
    b L_021e52a8
    mov r0, #5
    bl native_fn_02040500
    mvn r0, #0
    bl native_fn_02040518
    mov r4, #1
    b L_021e52a8
    add r0, sp, #2
    add r1, sp, #0
    bl native_fn_022126ec
    ldrsh r0, [sp, #2]
    bl native_fn_02025a28
    ldr r1, [pc, #0x2c]
    str r0, [r1, #0x450]
    ldrsh r0, [sp]
    bl native_fn_02025a28
    ldr r1, [pc, #0x1c]
    str r0, [r1, #0x454]
    mov r0, #5
    bl native_fn_02040500
    mvn r0, #0
    bl native_fn_02040518
    mov r4, #1
L_021e52a8:
    mov r0, r4
    ldmia sp!, {r3, r4, r5, pc}
    dcd 0x02233ae8
    dcd 0x0223255c
    dcd native_data_0222ebf4
    dcd 0x02234388
}
