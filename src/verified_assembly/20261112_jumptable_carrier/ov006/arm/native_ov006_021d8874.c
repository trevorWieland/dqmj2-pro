/* ov006 row 0x021d8874: 5728 bytes.
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

extern void native_fn_021dfd34(void);
extern void native_fn_021d85d4(void);
extern void native_fn_020684e0(void);
extern void native_fn_02067748(void);
extern void native_fn_020679f0(void);
extern void native_fn_02067ae8(void);
extern void native_fn_02067adc(void);
extern void native_fn_021df974(void);
extern void native_fn_021d85b8(void);
extern void native_fn_021dee68(void);
extern void native_fn_021df590(void);
extern void native_fn_021d77e8(void);
extern void native_fn_021ded5c(void);
extern void native_fn_021df524(void);
extern void native_fn_021def28(void);
extern void native_fn_021e2ef4(void);
extern void native_fn_021da2c8(void);
extern void native_fn_02067a9c(void);
extern void native_fn_021df150(void);
extern void native_fn_02067b58(void);
extern void native_fn_020677c8(void);
extern void native_fn_0205e814(void);
extern void native_fn_02041510(void);
extern void native_fn_02041538(void);
extern void native_fn_021d8288(void);
extern void native_fn_02041800(void);
extern void native_fn_021d83b4(void);
extern void native_fn_021e9444(void);
extern void native_fn_021e9484(void);
extern void native_fn_021e2f28(void);
extern void native_fn_0202a164(void);
extern void native_fn_0206785c(void);
extern void native_fn_020642cc(void);
extern void native_fn_01ff8604(void);
extern void native_fn_02064488(void);
extern void native_fn_020644c0(void);
extern void native_fn_021dfd70(void);
extern void native_fn_021dea9c(void);
extern void native_fn_021df458(void);
extern void native_fn_021df15c(void);
extern void native_fn_021d9f5c(void);
extern void native_fn_021da3e8(void);
extern void native_fn_02067bd4(void);
extern void native_fn_02048094(void);
extern void native_fn_02048034(void);
extern void native_fn_021ded04(void);
extern void native_fn_021def04(void);
extern void native_fn_021df16c(void);
extern void native_fn_021df4c8(void);
extern void native_fn_021de1ec(void);
extern void native_fn_021de1a8(void);
extern void native_fn_021de2e8(void);
extern void native_fn_021de320(void);
extern void native_fn_020414c8(void);
extern void native_fn_021de340(void);
extern void native_fn_021da4f0(void);
extern void native_fn_0206258c(void);
extern void native_fn_021d77d8(void);
extern void native_fn_02041814(void);
extern void native_fn_020443c4(void);
extern void native_fn_0205e844(void);
extern void native_fn_020653d0(void);
extern void native_fn_020ba564(void);
extern void native_fn_021da15c(void);
extern u8 native_data_0220cb88[];
extern void native_fn_02063eec(void);
extern void native_fn_02067a40(void);
extern void native_fn_02063f04(void);
extern void native_fn_02063b60(void);
extern void native_fn_0207e564(void);
extern void native_fn_0207e690(void);
extern void native_fn_0207e6a0(void);
extern void native_fn_020684ac(void);
extern void native_fn_02063ee0(void);
extern void native_fn_021d8384(void);
extern void native_fn_021de358(void);
extern void native_fn_021dbda0(void);
extern void native_fn_021dbe64(void);
extern void native_fn_02064304(void);
extern u8 native_data_02207914[];


asm u32 native_ov006_021d8874 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, lr}
    sub sp, sp, #20
    ldr r0, [pc, #0xfa0]
    mov r4, #3
    ldr r1, [r0, #0x8]
    cmp r1, #51
    addls pc, pc, r1, lsl #2
    b L_021d9eb0
    dcd 0xea000032
    dcd 0xea00005f
    dcd 0xea0000d4
    dcd 0xea000097
    dcd 0xea000101
    dcd 0xea000111
    dcd 0xea00011c
    dcd 0xea00012d
    dcd 0xea00013b
    dcd 0xea00015d
    dcd 0xea000170
    dcd 0xea000186
    dcd 0xea0001b5
    dcd 0xea0001e7
    dcd 0xea000224
    dcd 0xea000232
    dcd 0xea000255
    dcd 0xea000267
    dcd 0xea00027b
    dcd 0xea00028e
    dcd 0xea000571
    dcd 0xea0002a2
    dcd 0xea0002ab
    dcd 0xea0002b3
    dcd 0xea0002dc
    dcd 0xea0002e2
    dcd 0xea000302
    dcd 0xea00031d
    dcd 0xea00032b
    dcd 0xea000371
    dcd 0xea000385
    dcd 0xea0003bb
    dcd 0xea0003c9
    dcd 0xea0003f0
    dcd 0xea00040e
    dcd 0xea00041d
    dcd 0xea000442
    dcd 0xea000452
    dcd 0xea00046b
    dcd 0xea00047f
    dcd 0xea00048d
    dcd 0xea00049f
    dcd 0xea0004b1
    dcd 0xea0004c5
    dcd 0xea000559
    dcd 0xea000558
    dcd 0xea00050e
    dcd 0xea000528
    dcd 0xea00052e
    dcd 0xea00053c
    dcd 0xea00054a
    dcd 0xea0003a0
    bl native_fn_021dfd34
    cmp r0, #3
    bne L_021d8988
    ldr r0, [pc, #0xeac]
    mov r1, #0
    ldr r0, [r0, #0x4]
    strb r1, [r0]
    bl native_fn_021d85d4
    b L_021d9eb0
L_021d8988:
    bl native_fn_021dfd34
    cmp r0, #2
    bne L_021d9eb0
    mov r0, #4
    bl native_fn_020684e0
    cmp r0, #1
    bne L_021d89e4
    bl native_fn_02067748
    mov r5, r0
    bl native_fn_020679f0
    ldr r1, [r5, #0x4]
    ldr r0, [r0]
    cmp r1, r0
    bne L_021d89e4
    bl native_fn_02067ae8
    mov r5, r0
    bl native_fn_02067adc
    mov r3, r0
    mov r2, r5
    mov r0, #1
    mov r1, #8
    bl native_fn_021df974
    b L_021d8a10
L_021d89e4:
    bl native_fn_02067748
    mov r6, r0
    bl native_fn_02067ae8
    mov r5, r0
    bl native_fn_02067adc
    ldr r1, [r6, #0x4]
    mov r2, r5
    add r1, r1, #40
    mov r3, r0
    mov r0, #3
    bl native_fn_021df974
L_021d8a10:
    mov r0, #1
    bl native_fn_021d85b8
    b L_021d9eb0
    bl native_fn_021dfd34
    cmp r0, #2
    blt L_021d9eb0
    bl native_fn_021dfd34
    cmp r0, #3
    bne L_021d8a64
    bl native_fn_02067748
    mov r6, r0
    bl native_fn_02067ae8
    mov r5, r0
    bl native_fn_02067adc
    ldr r1, [r6, #0x4]
    mov r3, r0
    mov r2, r5
    add r1, r1, #40
    mov r0, r4
    bl native_fn_021df974
    b L_021d9eb0
L_021d8a64:
    bl native_fn_021dee68
    mov r0, #87
    bl native_fn_021df590
    ldr r0, [pc, #0xdac]
    ldr r0, [r0, #0x4]
    ldrb r0, [r0]
    cmp r0, #5
    bne L_021d8ab0
    mov r0, #5
    bl native_fn_021d77e8
    mov r0, #15
    mov r1, #4
    mov r2, #100
    bl native_fn_021ded5c
    mov r0, #26
    bl native_fn_021d85b8
    mov r0, #50
    bl native_fn_021df524
    b L_021d9eb0
L_021d8ab0:
    cmp r0, #0
    beq L_021d8ae0
    mov r0, #15
    mov r1, #4
    mov r2, #21
    bl native_fn_021ded5c
    mov r0, #1
    bl native_fn_021def28
    mov r0, #7
    bl native_fn_021d85b8
    bl native_fn_021e2ef4
    b L_021d9eb0
L_021d8ae0:
    bl native_fn_021da2c8
    bl native_fn_02067a9c
    mov r0, #15
    mov r1, #4
    mov r2, #16
    bl native_fn_021ded5c
    mov r0, r4
    bl native_fn_021d85b8
    b L_021d9eb0
    bl native_fn_021df150
    ldrh r1, [r0, #2]
    ldr r0, [pc, #0xd14]
    tst r1, r0
    beq L_021d9eb0
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_021dee68
    bl native_fn_02067b58
    ldr r0, [r0, #0x10]
    cmp r0, #0
    bne L_021d8b60
    ldr r1, [pc, #0xce8]
    mov r2, r4
    str r2, [r1, #0x14]
    ldr r0, [pc, #0xce4]
    mov r1, #4
    ldrh r2, [r0, #6]
    mov r0, #15
    bl native_fn_021ded5c
    mov r0, #2
    bl native_fn_021d85b8
    b L_021d9eb0
L_021d8b60:
    bl native_fn_02067748
    ldr r0, [r0, #0x4]
    bl native_fn_020677c8
    ldr r0, [r0]
    mov r1, #4
    cmp r0, #0
    bne L_021d8ba4
    ldr r0, [pc, #0xca8]
    ldr r3, [pc, #0xc9c]
    ldrh r2, [r0]
    mov r5, #0
    mov r0, #15
    str r5, [r3, #0x14]
    bl native_fn_021ded5c
    mov r0, #2
    bl native_fn_021d85b8
    b L_021d9eb0
L_021d8ba4:
    mov r0, #15
    mov r2, #20
    bl native_fn_021ded5c
    mov r0, #4
    bl native_fn_021d85b8
    mov r0, #0
    mov r1, r0
    mov r2, #30
    bl native_fn_0205e814
    mov r0, #1
    mov r1, #2
    mov r2, #30
    bl native_fn_02041510
    mov r0, #1
    mov r1, #2
    mov r2, #30
    bl native_fn_02041538
    mov r0, #0
    bl native_fn_021d8288
    b L_021d9eb0
    bl native_fn_021df150
    ldrh r1, [r0, #2]
    ldr r0, [pc, #0xc24]
    tst r1, r0
    beq L_021d9eb0
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_021dee68
    ldr r3, [pc, #0xc08]
    ldr r1, [pc, #0xc10]
    ldr r0, [r3, #0x14]
    mov r2, r4
    add r12, r0, #1
    smull r0, r5, r1, r12
    add r5, r5, r12, lsr #31
    smull r0, r1, r2, r5
    str r12, [r3, #0x14]
    subs r5, r12, r0
    bne L_021d8c94
    mov r0, #15
    mov r1, #4
    mov r2, #20
    bl native_fn_021ded5c
    mov r0, #4
    bl native_fn_021d85b8
    mov r0, #0
    mov r1, r0
    mov r2, #10
    bl native_fn_0205e814
    mov r0, #1
    mov r1, #2
    mov r2, #10
    bl native_fn_02041510
    mov r0, #1
    mov r1, #2
    mov r2, #10
    bl native_fn_02041538
    mov r0, #0
    bl native_fn_021d8288
    b L_021d9eb0
L_021d8c94:
    ldr r0, [pc, #0xb98]
    mov r1, r12, lsl #1
    ldrh r2, [r0, r1]
    mov r0, #15
    mov r1, #4
    bl native_fn_021ded5c
    b L_021d9eb0
    bl native_fn_02041800
    cmp r0, #1
    beq L_021d9eb0
    bl native_fn_021df150
    ldrh r1, [r0, #2]
    ldr r0, [pc, #0xb5c]
    tst r1, r0
    beq L_021d9eb0
    bl native_fn_021dee68
    bl native_fn_021d83b4
    mov r0, #5
    bl native_fn_021d77e8
    mov r0, #5
    bl native_fn_021d85b8
    mov r0, #219
    bl native_fn_021e9444
    b L_021d9eb0
    bl native_fn_021e9484
    cmp r0, #0
    beq L_021d9eb0
    mov r0, #80
    bl native_fn_021df524
    mov r0, #6
    bl native_fn_021d85b8
    mov r0, #15
    mov r1, #4
    mov r2, #109
    bl native_fn_021ded5c
    b L_021d9eb0
    bl native_fn_021df150
    ldrh r1, [r0, #2]
    ldr r0, [pc, #0xaf4]
    tst r1, r0
    beq L_021d9eb0
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_021dee68
    mov r0, #15
    mov r1, #4
    mov r2, #21
    bl native_fn_021ded5c
    mov r0, #1
    bl native_fn_021def28
    mov r0, #7
    bl native_fn_021d85b8
    bl native_fn_021e2ef4
    b L_021d9eb0
    bl native_fn_021e2f28
    cmp r0, #1
    bne L_021d9eb0
    mov r0, #87
    bl native_fn_021df590
    bl native_fn_021dee68
    mov r0, #15
    mov r1, #10
    mov r2, #12
    bl native_fn_021ded5c
    mov r0, #8
    bl native_fn_021d85b8
    mov r0, #7
    bl native_fn_0202a164
    b L_021d9eb0
    bl native_fn_021df150
    ldrh r1, [r0, #2]
    ldr r0, [pc, #0xa70]
    tst r1, r0
    beq L_021d9eb0
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_021dee68
    ldr r0, [pc, #0xa54]
    ldr r0, [r0, #0x4]
    ldrb r0, [r0]
    cmp r0, #0
    bne L_021d8e28
    mov r0, r4
    bl native_fn_020684e0
    cmp r0, #1
    bne L_021d8e00
    mov r0, #0
    mov r2, r0
    mov r1, #7
    bl native_fn_0206785c
    b L_021d8e18
L_021d8e00:
    bl native_fn_02067b58
    mov r1, r0
    mov r0, #0
    ldr r1, [r1]
    mov r2, r0
    bl native_fn_0206785c
L_021d8e18:
    mov r0, #36
    bl native_fn_020642cc
    mov r4, #4
    b L_021d9eb0
L_021d8e28:
    mov r0, #9
    bl native_fn_021d85b8
    b L_021d9eb0
    mov r1, r4
    mov r2, r4
    mov r0, #15
    bl native_fn_021ded5c
    mov r0, #1
    bl native_fn_021def28
    mov r0, #10
    bl native_fn_021d85b8
    mov r0, #0
    bl native_fn_01ff8604
    ldr r0, [pc, #0x9c0]
    mov r1, #0
    str r1, [r0, #0x18]
    ldr r2, [r0, #0x4]
    mov r0, #2
    ldrb r1, [r2]
    add r1, r1, #1
    strb r1, [r2]
    bl native_fn_02064488
    b L_021d9eb0
    bl native_fn_020644c0
    cmp r0, #0
    beq L_021d9eb0
    mov r0, #1
    bl native_fn_01ff8604
    ldr r0, [pc, #0x984]
    ldr r1, [r0, #0x18]
    cmp r1, #0
    bne L_021d8eb8
    ldr r1, [r0, #0x4]
    ldrb r0, [r1]
    sub r0, r0, #1
    strb r0, [r1]
L_021d8eb8:
    bl native_fn_021dee68
    mov r0, #87
    bl native_fn_021df590
    mov r0, #15
    mov r1, #3
    mov r2, #4
    bl native_fn_021ded5c
    mov r0, #11
    bl native_fn_021d85b8
    b L_021d9eb0
    bl native_fn_021df150
    ldrh r1, [r0, #2]
    ldr r0, [pc, #0x938]
    tst r1, r0
    beq L_021d9eb0
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_021dee68
    ldr r0, [pc, #0x91c]
    ldr r0, [r0, #0x18]
    cmp r0, #1
    bne L_021d8f4c
    mov r0, #50
    bl native_fn_021df524
    mov r0, #5
    bl native_fn_021d77e8
    mov r0, #15
    mov r1, #4
    mov r2, #100
    bl native_fn_021ded5c
    ldr r0, [pc, #0x8ec]
    mov r2, #1
    ldr r1, [r0, #0x4]
    mov r0, #26
    strb r2, [r1, #0x1]
    bl native_fn_021d85b8
    b L_021d9eb0
L_021d8f4c:
    mov r0, #2
    bl native_fn_021dfd70
    ldr r0, [pc, #0x8c8]
    ldr r0, [r0, #0x4]
    ldrb r0, [r0]
    cmp r0, #0
    beq L_021d8f70
    mov r0, #80
    bl native_fn_021df524
L_021d8f70:
    mov r1, #0
    mov r0, #2
    str r1, [sp]
    mov r2, r0
    mov r3, #145
    str r0, [sp, #0x4]
    bl native_fn_021dea9c
    mov r0, #12
    bl native_fn_021d85b8
    mov r0, #5
    bl native_fn_021d77e8
    b L_021d9eb0
    bl native_fn_021df458
    bl native_fn_021df150
    ldrh r0, [r0, #2]
    tst r0, #1
    beq L_021d9eb0
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_021df15c
    ldr r1, [pc, #0x85c]
    str r0, [r1, #0x14]
    bl native_fn_021df15c
    cmp r0, #0
    beq L_021d8fe0
    cmp r0, #1
    beq L_021d9050
    b L_021d9eb0
L_021d8fe0:
    bl native_fn_021d9f5c
    mov r0, #34
    bl native_fn_020642cc
    mov r0, #2
    bl native_fn_021da3e8
    mov r0, #1
    bl native_fn_021d77e8
    ldr r0, [pc, #0x820]
    ldr r0, [r0, #0x4]
    ldrb r0, [r0]
    bl native_fn_02067bd4
    mov r5, r0
    ldr r0, [pc, #0x80c]
    mov r1, #0
    ldr r0, [r0, #0x4]
    ldrb r0, [r0]
    add r0, r0, #1
    bl native_fn_02048094
    add r0, r5, #20
    mov r1, #32
    bl native_fn_02048034
    mov r0, #15
    mov r1, #4
    mov r2, #98
    bl native_fn_021ded5c
    mov r0, #15
    bl native_fn_021d85b8
    b L_021d9eb0
L_021d9050:
    mov r0, #15
    mov r1, #4
    mov r2, #22
    bl native_fn_021ded04
    mov r0, #13
    bl native_fn_021d85b8
    b L_021d9eb0
    bl native_fn_021def04
    bl native_fn_021df150
    ldrh r0, [r0, #2]
    tst r0, #2
    beq L_021d90c4
    bl native_fn_021dee68
    mov r0, #83
    bl native_fn_021df590
    mov r0, #2
    bl native_fn_021dfd70
    mov r0, #0
    str r0, [sp]
    mov r0, #2
    str r0, [sp, #0x4]
    ldr r1, [pc, #0x778]
    mov r2, r0
    ldr r1, [r1, #0x14]
    mov r3, #145
    bl native_fn_021dea9c
    mov r0, #12
    bl native_fn_021d85b8
    b L_021d9eb0
L_021d90c4:
    bl native_fn_021df150
    ldrh r0, [r0, #2]
    tst r0, #1
    beq L_021d9eb0
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_021dee68
    bl native_fn_021df16c
    cmp r0, #0
    bne L_021d9130
    mov r0, #1
    bl native_fn_021da3e8
    mov r0, #1
    bl native_fn_021d77e8
    mov r0, #15
    mov r1, #4
    mov r2, #99
    bl native_fn_021ded5c
    mov r0, #14
    bl native_fn_021d85b8
    mov r0, #0
    mov r1, r0
    mov r2, #30
    bl native_fn_0205e814
    mvn r0, #0
    bl native_fn_021df4c8
    b L_021d9eb0
L_021d9130:
    mov r0, #2
    bl native_fn_021dfd70
    mov r1, #0
    mov r0, #2
    str r1, [sp]
    mov r2, r0
    mov r1, #1
    mov r3, #145
    str r0, [sp, #0x4]
    bl native_fn_021dea9c
    mov r0, #12
    bl native_fn_021d85b8
    b L_021d9eb0
    bl native_fn_021df150
    ldrh r1, [r0, #2]
    ldr r0, [pc, #0x6b4]
    tst r1, r0
    beq L_021d9eb0
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_021dee68
    mov r0, #15
    mov r1, #4
    mov r2, #100
    bl native_fn_021ded5c
    mov r0, #27
    bl native_fn_021d85b8
    b L_021d9eb0
    bl native_fn_021df150
    ldrh r1, [r0, #2]
    ldr r0, [pc, #0x678]
    tst r1, r0
    beq L_021d9eb0
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_021dee68
    ldr r0, [pc, #0x65c]
    ldr r0, [r0, #0x4]
    ldrb r0, [r0]
    bl native_fn_02067bd4
    add r0, r0, #20
    mov r1, #0
    bl native_fn_02048034
    ldr r0, [pc, #0x640]
    mov r1, #110
    strh r1, [r0]
    bl native_fn_021de1ec
    ldr r1, [pc, #0x630]
    mov r5, r0
    ldr r0, [r1, #0x4]
    ldrb r0, [r0]
    bl native_fn_021de1a8
    cmp r5, r0
    ldrgt r0, [pc, #0x618]
    movgt r1, #113
    strgth r1, [r0]
    ldr r1, [pc, #0x60c]
    mov r0, #15
    ldrh r2, [r1]
    mov r1, #4
    bl native_fn_021ded5c
    mov r0, #16
    bl native_fn_021d85b8
    b L_021d9eb0
    bl native_fn_021df150
    ldrh r1, [r0, #2]
    ldr r0, [pc, #0x5e8]
    tst r1, r0
    beq L_021d9eb0
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_021dee68
    ldr r1, [pc, #0x5cc]
    mov r0, #15
    ldrh r2, [r1]
    mov r1, #4
    add r2, r2, #1
    mov r2, r2, lsl #16
    mov r2, r2, lsr #16
    bl native_fn_021ded5c
    mov r0, #17
    bl native_fn_021d85b8
    b L_021d9eb0
    bl native_fn_021df150
    ldrh r1, [r0, #2]
    ldr r0, [pc, #0x59c]
    tst r1, r0
    beq L_021d9eb0
    bl native_fn_021dee68
    mov r0, #15
    mov r1, #4
    mov r2, #112
    bl native_fn_021ded5c
    mov r0, #18
    bl native_fn_021d85b8
    mov r0, #0
    ldr r3, [pc, #0x56c]
    mov r1, r0
    mov r2, #30
    str r0, [r3, #0xc]
    bl native_fn_0205e814
    ldr r0, [pc, #0x56c]
    bl native_fn_021de2e8
    b L_021d9eb0
    bl native_fn_021df150
    ldrh r1, [r0, #2]
    ldr r0, [pc, #0x548]
    tst r1, r0
    beq L_021d9eb0
    bl native_fn_021dee68
    mov r0, #30
    bl native_fn_021de320
    ldr r1, [pc, #0x52c]
    mov r2, #0
    mov r0, #19
    str r2, [r1, #0xc]
    bl native_fn_021d85b8
    mov r0, #63
    bl native_fn_020414c8
    mov r0, #1
    mov r1, #2
    mov r2, #10
    bl native_fn_02041538
    b L_021d9eb0
    ldr r2, [r0, #0xc]
    add r1, r2, #1
    str r1, [r0, #0xc]
    cmp r2, #30
    beq L_021d9340
    cmp r2, #90
    beq L_021d9358
    b L_021d9eb0
L_021d9340:
    bl native_fn_021de340
    mov r0, r4
    bl native_fn_021da4f0
    mov r0, #147
    bl native_fn_021de2e8
    b L_021d9eb0
L_021d9358:
    bl native_fn_021de340
    mov r0, #21
    bl native_fn_021d85b8
    mov r0, #0
    bl native_fn_0206258c
    mov r0, #2
    bl native_fn_021d77d8
    b L_021d9eb0
    bl native_fn_02041814
    cmp r0, #1
    beq L_021d9eb0
    bl native_fn_021de340
    mov r0, #0
    mov r4, #6
    bl native_fn_021dfd70
    mov r0, #15
    bl native_fn_020443c4
    b L_021d9eb0
    mov r0, #62
    bl native_fn_0205e844
    cmp r0, #0
    beq L_021d9eb0
    mov r0, #23
    bl native_fn_021d85b8
    mov r0, #0
    bl native_fn_021def28
    b L_021d9eb0
    bl native_fn_021df150
    ldrh r1, [r0, #2]
    ldr r0, [pc, #0x454]
    tst r1, r0
    beq L_021d9eb0
    bl native_fn_021dee68
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_020653d0
    cmp r0, #0
    bne L_021d9450
    mov r0, r4
    bl native_fn_020684e0
    cmp r0, #1
    bne L_021d9420
    ldr r1, [pc, #0x41c]
    mov r0, #1
    ldr r2, [r1, #0x4]
    mov r1, #7
    ldrb r2, [r2]
    add r2, r2, #1
    bl native_fn_0206785c
    b L_021d9440
L_021d9420:
    bl native_fn_02067b58
    ldr r1, [pc, #0x3f8]
    ldr r2, [r1, #0x4]
    ldr r1, [r0]
    ldrb r2, [r2]
    mov r0, #1
    add r2, r2, #1
    bl native_fn_0206785c
L_021d9440:
    mov r0, #36
    bl native_fn_020642cc
    mov r4, #4
    b L_021d9eb0
L_021d9450:
    mov r0, #15
    mov r1, #4
    mov r2, #116
    bl native_fn_021ded5c
    mov r0, #25
    bl native_fn_021d85b8
    b L_021d9eb0
    mov r0, #15
    mov r1, #4
    mov r2, #117
    bl native_fn_021ded5c
    mov r0, #25
    bl native_fn_021d85b8
    b L_021d9eb0
    bl native_fn_021df150
    ldrh r1, [r0, #2]
    ldr r0, [pc, #0x390]
    tst r1, r0
    beq L_021d9eb0
    bl native_fn_021dee68
    ldr r0, [pc, #0x37c]
    mov r1, #0
    ldr r3, [r0, #0x4]
    ldrb r2, [r3]
    add r2, r2, #1
    strb r2, [r3]
    str r1, [r0, #0x18]
    ldr r2, [r0, #0x4]
    ldrb r1, [r2]
    cmp r1, #5
    moveq r1, #1
    streq r1, [r0, #0x18]
    addne r0, r1, #1
    strneb r0, [r2]
    mov r1, #3
    mov r2, r1
    mov r0, #15
    bl native_fn_021ded5c
    mov r0, #1
    bl native_fn_021def28
    mov r0, #10
    bl native_fn_021d85b8
    mov r0, #0
    bl native_fn_01ff8604
    mov r0, #2
    bl native_fn_02064488
    b L_021d9eb0
    mov r0, #50
    bl native_fn_021df524
    bl native_fn_021df150
    ldrh r1, [r0, #2]
    ldr r0, [pc, #0x304]
    tst r1, r0
    beq L_021d9eb0
    bl native_fn_021dee68
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_020ba564
    cmp r0, #0
    mov r0, #15
    mov r1, #4
    bne L_021d955c
    mov r2, #118
    bl native_fn_021ded5c
    mov r0, #27
    bl native_fn_021d85b8
    b L_021d9eb0
L_021d955c:
    mov r2, #147
    bl native_fn_021ded04
    mov r0, #28
    bl native_fn_021d85b8
    ldr r0, [pc, #0x2b0]
    mov r1, #1
    str r1, [r0, #0x10]
    b L_021d9eb0
    bl native_fn_021df150
    ldrh r1, [r0, #2]
    ldr r0, [pc, #0x29c]
    tst r1, r0
    beq L_021d9eb0
    bl native_fn_021dee68
    mov r0, #82
    bl native_fn_021df590
    mov r0, #15
    mov r1, #4
    mov r2, #49
    bl native_fn_021ded04
    mov r0, #28
    bl native_fn_021d85b8
    b L_021d9eb0
    bl native_fn_021def04
    bl native_fn_021df150
    ldrh r0, [r0, #2]
    tst r0, #2
    beq L_021d960c
    bl native_fn_021dee68
    mov r0, #83
    bl native_fn_021df590
    bl native_fn_020ba564
    cmp r0, #0
    mov r0, #15
    mov r1, #4
    beq L_021d95f8
    mov r2, #149
    bl native_fn_021ded5c
    b L_021d9600
L_021d95f8:
    mov r2, #73
    bl native_fn_021ded5c
L_021d9600:
    mov r0, #29
    bl native_fn_021d85b8
    b L_021d9eb0
L_021d960c:
    bl native_fn_021df150
    ldrh r0, [r0, #2]
    tst r0, #1
    beq L_021d9eb0
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_021df16c
    cmp r0, #0
    bne L_021d969c
    bl native_fn_021dee68
    bl native_fn_020ba564
    cmp r0, #0
    beq L_021d9668
    bl native_fn_021da15c
    mov r0, #15
    mov r1, #4
    mov r2, #148
    bl native_fn_021ded5c
    mov r0, #1
    bl native_fn_021def28
    mov r0, #31
    bl native_fn_021d85b8
    b L_021d9eb0
L_021d9668:
    mov r0, #35
    bl native_fn_020642cc
    mov r0, r4
    bl native_fn_021d77d8
    mov r0, #63
    bl native_fn_020414c8
    mov r0, #1
    mov r1, #2
    mov r2, #10
    bl native_fn_02041538
    mov r0, #51
    bl native_fn_021d85b8
    b L_021d9eb0
L_021d969c:
    bl native_fn_021dee68
    bl native_fn_020ba564
    cmp r0, #0
    mov r0, #15
    mov r1, #4
    beq L_021d96c0
    mov r2, #149
    bl native_fn_021ded5c
    b L_021d96c8
L_021d96c0:
    mov r2, #73
    bl native_fn_021ded5c
L_021d96c8:
    mov r0, #29
    bl native_fn_021d85b8
    b L_021d9eb0
    bl native_fn_021df150
    ldrh r1, [r0, #2]
    ldr r0, [pc, #0x144]
    tst r1, r0
    beq L_021d9eb0
    bl native_fn_021dee68
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_020ba564
    cmp r0, #0
    mov r0, #15
    mov r1, #4
    beq L_021d9714
    mov r2, #150
    bl native_fn_021ded04
    b L_021d971c
L_021d9714:
    mov r2, #74
    bl native_fn_021ded04
L_021d971c:
    mov r0, #30
    bl native_fn_021d85b8
    b L_021d9eb0
    bl native_fn_021def04
    bl native_fn_021df150
    ldrh r0, [r0, #2]
    tst r0, #2
    beq L_021d977c
    bl native_fn_021dee68
    mov r0, #83
    bl native_fn_021df590
    bl native_fn_020ba564
    cmp r0, #0
    mov r0, #15
    mov r1, #4
    beq L_021d9768
    mov r2, #147
    bl native_fn_021ded04
    b L_021d9770
L_021d9768:
    mov r2, #49
    bl native_fn_021ded04
L_021d9770:
    mov r0, #28
    bl native_fn_021d85b8
    b L_021d9eb0
L_021d977c:
    bl native_fn_021df150
    ldrh r0, [r0, #2]
    tst r0, #1
    beq L_021d9eb0
    bl native_fn_021dee68
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_021df16c
    cmp r0, #0
    bne L_021d97cc
    bl native_fn_021da2c8
    ldr r0, [pc, #0x74]
    mov r3, #5
    ldr r2, [r0, #0x4]
    mov r1, #1
    strb r3, [r2]
    ldr r0, [r0, #0x4]
    mov r4, #2
    strb r1, [r0, #0x1]
    b L_021d9eb0
L_021d97cc:
    mov r0, #15
    mov r1, #4
    mov r2, #49
    bl native_fn_021ded04
    mov r0, #28
    bl native_fn_021d85b8
    b L_021d9eb0
    bl native_fn_02041814
    cmp r0, #1
    beq L_021d9eb0
    mov r0, #50
    bl native_fn_021df524
    mov r4, #6
    b L_021d9eb0
    ldr r2, [pc, #0x30]
    mov r0, r4
    mov r1, r4
    mov r3, #44
    bl native_fn_021df974
    mov r0, #32
    bl native_fn_021d85b8
    b L_021d9eb0
    dcd 0x0220f2f4
    dcd 0x00000ff7
    dcd native_data_0220cb88
    dcd 0x55555556
    dcd native_data_0220cb88
    dcd 0x00000213
    dcd 0x0220f310
    bl native_fn_021dfd34
    cmp r0, #2
    bne L_021d9eb0
    bl native_fn_02067b58
    ldr r1, [pc, #-0x34]
    ldrh r0, [r0, #4]
    ldrh r1, [r1, #32]
    cmp r1, r0
    bne L_021d9894
    bl native_fn_02067b58
    ldr r1, [pc, #-0x4c]
    ldrb r0, [r0, #0x6]
    ldrb r1, [r1, #0x22]
    cmp r1, r0
    bne L_021d9894
    bl native_fn_02067b58
    ldr r1, [pc, #-0x64]
    ldrb r0, [r0, #0x7]
    ldrb r1, [r1, #0x23]
    cmp r1, r0
    beq L_021d98bc
L_021d9894:
    mov r0, #87
    bl native_fn_021df590
    bl native_fn_021dee68
    mov r0, #15
    mov r1, #4
    mov r2, #156
    bl native_fn_021ded5c
    mov r0, #50
    bl native_fn_021d85b8
    b L_021d9eb0
L_021d98bc:
    bl native_fn_02063eec
    mov r2, r0
    mov r0, #2
    mov r1, r4
    mov r3, #256
    bl native_fn_021df974
    mov r0, #33
    bl native_fn_021d85b8
    b L_021d9eb0
    bl native_fn_021dfd34
    cmp r0, #2
    bne L_021d9eb0
    ldr r0, [pc, #-0xd0]
    ldr r0, [r0, #0x10]
    cmp r0, #1
    bne L_021d992c
    bl native_fn_021dee68
    mov r0, #87
    bl native_fn_021df590
    mov r0, #15
    mov r1, #4
    mov r2, #50
    bl native_fn_021ded5c
    mov r0, #1
    bl native_fn_021def28
    ldr r0, [pc, #-0x104]
    mov r1, #0
    str r1, [r0, #0x10]
L_021d992c:
    bl native_fn_02067a40
    mov r1, #0
    str r1, [r0]
    bl native_fn_02067a40
    mov r2, r0
    mov r0, #2
    mov r1, #4
    mov r3, #12
    bl native_fn_021df974
    mov r0, #34
    bl native_fn_021d85b8
    b L_021d9eb0
    bl native_fn_021dfd34
    cmp r0, #2
    bne L_021d9eb0
    bl native_fn_02067748
    mov r5, r0
    mov r0, #0
    bl native_fn_02063f04
    ldr r1, [r5, #0x4]
    mov r2, r0
    add r1, r1, #75
    mov r0, r4
    mov r3, #1776
    bl native_fn_021df974
    mov r0, #35
    bl native_fn_021d85b8
    b L_021d9eb0
    bl native_fn_021dfd34
    cmp r0, #2
    blt L_021d9eb0
    bl native_fn_021dfd34
    cmp r0, #2
    bne L_021d9a04
    mov r0, #1
    bl native_fn_02063f04
    ldrsh r0, [r0, #72]
    cmp r0, #0
    beq L_021d9a04
    ldr r0, [pc, #0x4ec]
    mov r1, #1
    bl native_fn_02063b60
    ldr r0, [pc, #0x4e4]
    mov r1, #1
    bl native_fn_02063b60
    ldr r0, [pc, #0x4dc]
    mov r1, #0
    bl native_fn_02063b60
    ldr r0, [pc, #0x4d4]
    mov r1, #0
    bl native_fn_02063b60
    ldr r0, [pc, #0x4cc]
    mov r1, #0
    bl native_fn_02063b60
L_021d9a04:
    mov r0, #2
    bl native_fn_0207e564
    mov r5, r0
    bl native_fn_0207e690
    mov r2, r0
    mov r3, r5
    mov r0, #2
    mov r1, #13
    bl native_fn_021df974
    mov r0, #36
    bl native_fn_021d85b8
    b L_021d9eb0
    bl native_fn_021dfd34
    cmp r0, #2
    blt L_021d9eb0
    mov r0, #87
    bl native_fn_021df590
    bl native_fn_021dee68
    mov r0, #15
    mov r1, #4
    mov r2, #50
    bl native_fn_021ded5c
    mov r0, #1
    bl native_fn_021def28
    bl native_fn_0207e6a0
    bl native_fn_021e2ef4
    mov r0, #37
    bl native_fn_021d85b8
    b L_021d9eb0
    bl native_fn_021e2f28
    cmp r0, #1
    bne L_021d9eb0
    mov r0, #7
    bl native_fn_0202a164
    mov r0, #1
    mov r1, r0
    bl native_fn_020684ac
    mov r0, #4
    mov r1, #1
    bl native_fn_020684ac
    bl native_fn_02063ee0
    mov r5, r0
    bl native_fn_02067b58
    ldr r0, [r0, #0x24]
    str r0, [r5]
    bl native_fn_021dee68
    mov r0, #87
    bl native_fn_021df590
    mov r0, #15
    mov r1, r4
    mov r2, #2
    bl native_fn_021ded5c
    mov r0, #38
    bl native_fn_021d85b8
    b L_021d9eb0
    bl native_fn_021df150
    ldrh r1, [r0, #2]
    ldr r0, [pc, #-0x2c8]
    tst r1, r0
    beq L_021d9eb0
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_021dee68
    mov r0, #0
    bl native_fn_01ff8604
    mov r0, #2
    bl native_fn_02064488
    mov r1, r4
    mov r0, #15
    mov r2, r1
    bl native_fn_021ded5c
    mov r0, #1
    bl native_fn_021def28
    mov r0, #39
    bl native_fn_021d85b8
    b L_021d9eb0
    bl native_fn_020644c0
    cmp r0, #0
    beq L_021d9eb0
    mov r0, #1
    bl native_fn_01ff8604
    bl native_fn_021dee68
    mov r0, #15
    mov r1, r4
    mov r2, #4
    bl native_fn_021ded5c
    mov r0, #87
    bl native_fn_021df590
    mov r0, #40
    bl native_fn_021d85b8
    b L_021d9eb0
    bl native_fn_021df150
    ldrh r1, [r0, #2]
    ldr r0, [pc, #-0x358]
    tst r1, r0
    beq L_021d9eb0
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_021dee68
    mov r0, #15
    mov r1, #4
    mov r2, #23
    bl native_fn_021ded5c
    mov r0, #41
    bl native_fn_021d85b8
    mov r0, #0
    mov r1, r0
    mov r2, #30
    bl native_fn_0205e814
    b L_021d9eb0
    bl native_fn_021df150
    ldrh r1, [r0, #2]
    ldr r0, [pc, #-0x3a4]
    tst r1, r0
    beq L_021d9eb0
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_021dee68
    mov r0, #6
    bl native_fn_021d77e8
    mov r0, #80
    bl native_fn_021df524
    mov r0, #15
    mov r1, #4
    mov r2, #115
    bl native_fn_021ded5c
    mov r0, #42
    bl native_fn_021d85b8
    b L_021d9eb0
    bl native_fn_021df150
    ldrh r1, [r0, #2]
    ldr r0, [pc, #-0x3f0]
    tst r1, r0
    beq L_021d9eb0
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_021dee68
    mov r0, #43
    bl native_fn_021d85b8
    mov r1, #0
    str r1, [sp]
    mov r2, #2
    str r2, [sp, #0x4]
    mov r0, #6
    mov r3, #109
    bl native_fn_021dea9c
    ldr r0, [pc, #-0x430]
    mov r1, #0
    str r1, [r0, #0x14]
    b L_021d9eb0
    bl native_fn_021d8384
    cmp r0, #0
    beq L_021d9eb0
    bl native_fn_021df458
    bl native_fn_021df150
    ldrh r0, [r0, #2]
    tst r0, #1
    beq L_021d9d24
    bl native_fn_021df15c
    cmp r0, #0
    bne L_021d9d18
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_02063eec
    ldr r1, [pc, #-0x478]
    mov r5, #0
    mov r2, r5
    str r0, [r1, #0x4]
L_021d9ca4:
    ldr r1, [r0, #0x34]
    add r2, r2, #1
    cmp r1, #0
    addne r5, r5, #1
    cmp r2, #5
    add r0, r0, #48
    blt L_021d9ca4
    mov r0, r5
    mov r1, #0
    bl native_fn_02048094
    rsb r0, r5, #5
    mov r1, #32
    bl native_fn_02048094
    bl native_fn_02063eec
    ldr r1, [pc, #-0x4c0]
    ldrb r0, [r0, #0x3]
    ldr r1, [r1, #0x4]
    ldr r1, [r1, #0xc]
    sub r0, r1, r0
    bl native_fn_021de358
    mov r1, #64
    bl native_fn_02048094
    mov r0, #15
    mov r1, #4
    mov r2, #83
    bl native_fn_021ded5c
    mov r0, #46
    bl native_fn_021d85b8
    b L_021d9eb0
L_021d9d18:
    mov r0, #84
    bl native_fn_021df590
    b L_021d9eb0
L_021d9d24:
    bl native_fn_021df15c
    ldr r1, [pc, #-0x50c]
    ldr r1, [r1, #0x14]
    cmp r1, r0
    beq L_021d9eb0
    bl native_fn_021df15c
    cmp r0, #0
    bne L_021d9d50
    mov r0, #6
    bl native_fn_021d77e8
    b L_021d9d7c
L_021d9d50:
    bl native_fn_021df15c
    sub r0, r0, #1
    bl native_fn_021dbda0
    ldr r0, [pc, #-0x540]
    ldr r0, [r0, #0x14]
    cmp r0, #0
    bne L_021d9d78
    mov r0, #7
    bl native_fn_021d77e8
    b L_021d9d7c
L_021d9d78:
    bl native_fn_021dbe64
L_021d9d7c:
    bl native_fn_021df15c
    ldr r1, [pc, #-0x564]
    str r0, [r1, #0x14]
    b L_021d9eb0
    bl native_fn_021df150
    ldrh r1, [r0, #2]
    ldr r0, [pc, #-0x574]
    tst r1, r0
    beq L_021d9eb0
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_021dee68
    ldr r1, [pc, #0x11c]
    add r0, sp, #8
    ldrh r4, [r1]
    ldrh r2, [r1, #2]
    ldrh r3, [r1, #4]
    strh r4, [sp, #8]
    strh r2, [sp, #10]
    ldrh r2, [r1, #6]
    strh r3, [sp, #12]
    strh r2, [sp, #14]
    ldrh r2, [r1, #8]
    ldrh r1, [r1, #10]
    strh r2, [sp, #16]
    strh r1, [sp, #18]
    bl native_fn_02064304
    mov r0, #36
    bl native_fn_020642cc
    mov r4, #4
    b L_021d9eb0
    mov r0, #15
    mov r1, #4
    mov r2, #84
    bl native_fn_021ded5c
    mov r0, #48
    bl native_fn_021d85b8
    b L_021d9eb0
    bl native_fn_021df150
    ldrh r1, [r0, #2]
    ldr r0, [pc, #-0x5fc]
    tst r1, r0
    beq L_021d9eb0
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_021dee68
    mov r0, #15
    mov r1, #4
    mov r2, #90
    bl native_fn_021ded5c
    mov r0, #49
    bl native_fn_021d85b8
    b L_021d9eb0
    bl native_fn_021df150
    ldrh r1, [r0, #2]
    ldr r0, [pc, #-0x638]
    tst r1, r0
    beq L_021d9eb0
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_021dee68
    mov r0, #15
    mov r1, #4
    mov r2, #85
    bl native_fn_021ded5c
    mov r0, #50
    bl native_fn_021d85b8
    b L_021d9eb0
    bl native_fn_021df150
    ldrh r1, [r0, #2]
    ldr r0, [pc, #-0x674]
    tst r1, r0
    beq L_021d9eb0
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_021dee68
    mov r4, #2
L_021d9eb0:
    mov r0, r4
    add sp, sp, #20
    ldmia sp!, {r3, r4, r5, r6, pc}
    dcd 0x00000216
    dcd 0x00000233
    dcd 0x00000221
    dcd 0x00000222
    dcd 0x00000223
    dcd native_data_02207914
}
