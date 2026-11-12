/* ov006 row 0x021e0454: 9704 bytes.
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

extern void native_fn_021df0a8(void);
extern void native_fn_0203d294(void);
extern void native_fn_021dfd34(void);
extern void native_fn_021da4f0(void);
extern void native_fn_021e2f38(void);
extern void native_fn_021df974(void);
extern void native_fn_021e00bc(void);
extern void native_fn_020677e0(void);
extern void native_fn_02067808(void);
extern void native_fn_02008e0c(void);
extern void native_fn_02067818(void);
extern void native_fn_02067a60(void);
extern void native_fn_02067b3c(void);
extern void native_fn_0203d0c0(void);
extern void native_fn_0206784c(void);
extern void native_fn_02067b58(void);
extern void native_fn_020678c8(void);
extern void native_fn_02067904(void);
extern void native_fn_02067968(void);
extern void native_fn_0206799c(void);
extern void native_fn_02008d78(void);
extern void native_fn_02064304(void);
extern void native_fn_020642f8(void);
extern void native_fn_02067bc4(void);
extern void native_fn_02063ed4(void);
extern void native_fn_02067748(void);
extern void native_fn_020679f0(void);
extern void native_fn_020684ac(void);
extern void native_fn_021e0000(void);
extern void native_fn_02067a30(void);
extern void native_fn_02067a40(void);
extern void native_fn_021df590(void);
extern void native_fn_021dee68(void);
extern void native_fn_02063eec(void);
extern void native_fn_020684e0(void);
extern void native_fn_021ded5c(void);
extern void native_fn_02068500(void);
extern void native_fn_021df150(void);
extern void native_fn_021dff30(void);
extern void native_fn_020644c0(void);
extern void native_fn_01ff8604(void);
extern void native_fn_021e2c2c(void);
extern void native_fn_0205e814(void);
extern void native_fn_021df960(void);
extern void native_fn_02068510(void);
extern void native_fn_021df524(void);
extern void native_fn_021dff78(void);
extern void native_fn_02063ee0(void);
extern void native_fn_021d77e8(void);
extern void native_fn_021dea9c(void);
extern void native_fn_020642cc(void);
extern void native_fn_021ddf58(void);
extern void native_fn_021d77d8(void);
extern void native_fn_020414c8(void);
extern void native_fn_02041538(void);
extern void native_fn_021df458(void);
extern void native_fn_021df15c(void);
extern void native_fn_021dfe74(void);
extern void native_fn_0205dc70(void);
extern void native_fn_02048034(void);
extern void native_fn_021dacb8(void);
extern void native_fn_021dfd70(void);
extern void native_fn_021df004(void);
extern void native_fn_021de8f0(void);
extern void native_fn_021ded04(void);
extern void native_fn_021e2a5c(void);
extern void native_fn_0206442c(void);
extern void native_fn_021d83c8(void);
extern void native_fn_02088e8c(void);
extern void native_fn_021d83e4(void);
extern void native_fn_020646d0(void);
extern void native_fn_020645b0(void);
extern void native_fn_020641ac(void);
extern void native_fn_021e2ab8(void);
extern void native_fn_021def28(void);
extern void native_fn_021dc3b8(void);
extern void native_fn_021def04(void);
extern void native_fn_021df16c(void);
extern void native_fn_02041814(void);
extern void native_fn_021d8384(void);
extern void native_fn_021dc108(void);
extern void native_fn_021dc178(void);
extern void native_fn_02062aa0(void);
extern void native_fn_0206258c(void);
extern void native_fn_021dc7cc(void);
extern void native_fn_021dc878(void);
extern void native_fn_02062a50(void);
extern void native_fn_0206dcd0(void);
extern void native_fn_020406c8(void);
extern void native_fn_020cf44c(void);
extern void native_fn_020cf43c(void);
extern void native_fn_02063b40(void);
extern void native_fn_0205e7a8(void);
extern void native_fn_020c40f4(void);
extern void native_fn_021dee98(void);
extern void native_fn_021db59c(void);
extern void native_fn_021dfe94(void);
extern void native_fn_021dbb88(void);
extern void native_fn_021db660(void);
extern void native_fn_021db3ac(void);
extern void native_fn_021db410(void);
extern void native_fn_021e2ba4(void);
extern void native_fn_021e2a40(void);


asm u32 native_ov006_021e0454 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    sub sp, sp, #8
    mov r4, #0
    bl native_fn_021df0a8
    cmp r0, #1
    addeq sp, sp, #8
    moveq r0, r4
    ldmeqia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
    ldr r0, [pc, #0xf9c]
    ldr r0, [r0, #0x14]
    cmp r0, #64
    addls pc, pc, r0, lsl #2
    b L_021e2a20
    dcd 0xea00003f
    dcd 0xea00004e
    dcd 0xea00005f
    dcd 0xea00006c
    dcd 0xea000095
    dcd 0xea0000a9
    dcd 0xea0000b3
    dcd 0xea0000c6
    dcd 0xea0000d1
    dcd 0xea0000df
    dcd 0xea0000ea
    dcd 0xea0000ff
    dcd 0xea000120
    dcd 0xea000142
    dcd 0xea000169
    dcd 0xea0001ec
    dcd 0xea000184
    dcd 0xea000195
    dcd 0xea00012c
    dcd 0xea0001a4
    dcd 0xea000950
    dcd 0xea000333
    dcd 0xea0001af
    dcd 0xea0002b2
    dcd 0xea0002c2
    dcd 0xea0002d0
    dcd 0xea0002e4
    dcd 0xea0002f6
    dcd 0xea000317
    dcd 0xea0001fe
    dcd 0xea00020a
    dcd 0xea000216
    dcd 0xea000222
    dcd 0xea000237
    dcd 0xea00024e
    dcd 0xea00032f
    dcd 0xea0003ee
    dcd 0xea0003ed
    dcd 0xea000430
    dcd 0xea000472
    dcd 0xea0004de
    dcd 0xea0004f1
    dcd 0xea000535
    dcd 0xea000557
    dcd 0xea0005bf
    dcd 0xea000603
    dcd 0xea00061c
    dcd 0xea000607
    dcd 0xea00064d
    dcd 0xea00068a
    dcd 0xea0003f7
    dcd 0xea0006af
    dcd 0xea000735
    dcd 0xea000748
    dcd 0xea000783
    dcd 0xea0007ae
    dcd 0xea0007ea
    dcd 0xea000819
    dcd 0xea000832
    dcd 0xea000880
    dcd 0xea0008a9
    dcd 0xea0008bc
    dcd 0xea0008ed
    dcd 0xea000922
    dcd 0xea000412
    mov r0, #100
    bl native_fn_0203d294
    bl native_fn_021dfd34
    cmp r0, #2
    bne L_021e2a20
    mvn r0, #0
    bl native_fn_021da4f0
    bl native_fn_021e2f38
    mov r2, r0
    mov r0, #1
    mov r1, #9
    mov r3, #24
    bl native_fn_021df974
    mov r0, #1
    bl native_fn_021e00bc
    b L_021e2a20
    bl native_fn_021dfd34
    cmp r0, #2
    blt L_021e2a20
    bl native_fn_021dfd34
    cmp r0, #2
    beq L_021e05f0
    bl native_fn_021e2f38
    mov r1, r4
    str r1, [r0]
L_021e05f0:
    bl native_fn_020677e0
    mov r2, r0
    mov r0, #3
    mov r1, #20
    mov r3, #4352
    bl native_fn_021df974
    mov r0, #2
    bl native_fn_021e00bc
    b L_021e2a20
    bl native_fn_021dfd34
    cmp r0, #2
    blt L_021e2a20
    ldr r5, [pc, #0xdf0]
    mov r6, r4
    ldr r2, [pc, #0xdec]
    mov r0, #3
    mov r1, #90
    mov r3, #4352
    str r6, [r5, #0x18]
    bl native_fn_021df974
    mov r0, #3
    bl native_fn_021e00bc
    b L_021e2a20
    bl native_fn_021dfd34
    cmp r0, #2
    blt L_021e2a20
    bl native_fn_021dfd34
    cmp r0, #2
    bne L_021e06a0
    mov r7, #368
    ldr r8, [pc, #0xdac]
    ldr r6, [pc, #0xda4]
    mov r9, r4
    mov r5, r7
L_021e0678:
    ldr r0, [r6, #0x18]
    bl native_fn_02067808
    mla r1, r9, r5, r0
    add r0, r9, r9, lsl #4
    mov r2, r7
    add r0, r8, r0, lsl #6
    bl native_fn_02008e0c
    add r9, r9, #1
    cmp r9, #4
    blt L_021e0678
L_021e06a0:
    ldr r0, [pc, #0xd70]
    ldr r1, [r0, #0x18]
    add r1, r1, #1
    str r1, [r0, #0x18]
    cmp r1, #9
    bne L_021e06dc
    bl native_fn_02067818
    mov r2, r0
    mov r0, #1
    mov r1, #6
    mov r3, #1088
    bl native_fn_021df974
    mov r0, #4
    bl native_fn_021e00bc
    b L_021e2a20
L_021e06dc:
    ldr r2, [pc, #0xd38]
    add r1, r1, #90
    mov r0, #3
    mov r3, #4352
    bl native_fn_021df974
    b L_021e2a20
    bl native_fn_021dfd34
    cmp r0, #2
    blt L_021e2a20
    bl native_fn_021dfd34
    cmp r0, #2
    bne L_021e0718
    mov r0, #1
    bl native_fn_02067a60
    b L_021e0724
L_021e0718:
    bl native_fn_02067818
    mov r1, r4
    str r1, [r0]
L_021e0724:
    bl native_fn_02067b3c
    mov r2, r0
    mov r0, #3
    mov r1, #7
    mov r3, #80
    bl native_fn_021df974
    mov r0, #5
    bl native_fn_021e00bc
    b L_021e2a20
    bl native_fn_021dfd34
    cmp r0, #2
    bne L_021e2a20
    ldr r2, [pc, #0xcc4]
    mov r0, #3
    mov r1, #24
    mov r3, #4
    bl native_fn_021df974
    mov r0, #6
    bl native_fn_021e00bc
    b L_021e2a20
    bl native_fn_021dfd34
    cmp r0, #2
    blt L_021e2a20
    bl native_fn_021dfd34
    cmp r0, #2
    bne L_021e07a0
    ldr r1, [pc, #0xc84]
    mov r0, #76
    ldr r1, [r1, #0x30]
    and r1, r1, #255
    bl native_fn_0203d0c0
L_021e07a0:
    bl native_fn_0206784c
    mov r2, r0
    mov r0, #3
    mov r1, #50
    mov r3, #512
    bl native_fn_021df974
    mov r0, #7
    bl native_fn_021e00bc
    b L_021e2a20
    bl native_fn_021dfd34
    cmp r0, #2
    bne L_021e2a20
    bl native_fn_02067b58
    mov r2, r0
    mov r0, #3
    mov r1, r0
    mov r3, #44
    bl native_fn_021df974
    mov r0, #8
    bl native_fn_021e00bc
    b L_021e2a20
    bl native_fn_021dfd34
    cmp r0, #2
    bne L_021e2a20
    mov r0, #5
    bl native_fn_0203d294
    mov r5, r0
    bl native_fn_020678c8
    mov r2, r0
    add r1, r5, #80
    mov r0, #3
    mov r3, #576
    bl native_fn_021df974
    mov r0, #9
    bl native_fn_021e00bc
    b L_021e2a20
    bl native_fn_021dfd34
    cmp r0, #2
    bne L_021e2a20
    bl native_fn_02067904
    mov r2, r0
    mov r0, #1
    mov r1, #12
    mov r3, #256
    bl native_fn_021df974
    mov r0, #10
    bl native_fn_021e00bc
    b L_021e2a20
    bl native_fn_021dfd34
    cmp r0, #2
    blt L_021e2a20
    bl native_fn_021dfd34
    cmp r0, #2
    bne L_021e0880
    mov r0, #4
    bl native_fn_02067a60
L_021e0880:
    ldr r1, [pc, #0xb90]
    mov r0, #0
    str r0, [r1, #0x18]
    bl native_fn_02067968
    ldr r1, [pc, #0xb80]
    mov r2, r0
    ldr r1, [r1, #0x18]
    mov r0, #3
    add r1, r1, #30
    mov r3, #3072
    bl native_fn_021df974
    mov r0, #11
    bl native_fn_021e00bc
    b L_021e2a20
    bl native_fn_021dfd34
    cmp r0, #2
    blt L_021e2a20
    bl native_fn_021dfd34
    cmp r0, #2
    bne L_021e08e0
    ldr r0, [pc, #0xb40]
    ldr r0, [r0, #0x18]
    add r0, r0, #8
    bl native_fn_02067a60
L_021e08e0:
    ldr r1, [pc, #0xb30]
    ldr r0, [r1, #0x18]
    add r0, r0, #1
    str r0, [r1, #0x18]
    cmp r0, #4
    bne L_021e091c
    bl native_fn_0206799c
    mov r2, r0
    mov r0, #3
    mov r1, #22
    mov r3, #256
    bl native_fn_021df974
    mov r0, #12
    bl native_fn_021e00bc
    b L_021e2a20
L_021e091c:
    bl native_fn_02067968
    ldr r1, [pc, #0xaf0]
    mov r2, r0
    ldr r1, [r1, #0x18]
    mov r0, #3
    add r1, r1, #30
    mov r3, #3072
    bl native_fn_021df974
    b L_021e2a20
    bl native_fn_021dfd34
    cmp r0, #2
    blt L_021e2a20
    ldr r0, [pc, #0xad0]
    mov r1, r4
    mov r2, #12
    bl native_fn_02008d78
    ldr r0, [pc, #0xac0]
    bl native_fn_02064304
    bl native_fn_020642f8
    mov r2, r0
    mov r0, #1
    mov r1, #14
    mov r3, #12
    bl native_fn_021df974
    mov r0, #18
    bl native_fn_021e00bc
    b L_021e2a20
    bl native_fn_021dfd34
    cmp r0, #2
    blt L_021e2a20
    ldr r1, [pc, #0xa7c]
    mov r0, r4
    str r0, [r1, #0x18]
    bl native_fn_02067bc4
    ldr r1, [pc, #0xa6c]
    mov r2, r0
    ldr r0, [r1, #0x18]
    ldr r3, [pc, #0xa70]
    add r1, r0, #45
    mov r0, #3
    bl native_fn_021df974
    mov r0, #13
    bl native_fn_021e00bc
    b L_021e2a20
    bl native_fn_021dfd34
    cmp r0, #2
    blt L_021e2a20
    ldr r1, [pc, #0xa38]
    ldr r0, [r1, #0x18]
    add r0, r0, #1
    str r0, [r1, #0x18]
    cmp r0, #4
    bne L_021e0a48
    bl native_fn_02063ed4
    ldr r0, [r0]
    cmp r0, #0
    bne L_021e0a24
    bl native_fn_02067748
    mov r2, r0
    mov r0, #2
    mov r1, #1
    mov r3, #56
    bl native_fn_021df974
    mov r0, #22
    bl native_fn_021e00bc
    b L_021e2a20
L_021e0a24:
    bl native_fn_02067748
    mov r2, r0
    mov r0, #1
    mov r1, r0
    mov r3, #56
    bl native_fn_021df974
    mov r0, #14
    bl native_fn_021e00bc
    b L_021e2a20
L_021e0a48:
    bl native_fn_02067bc4
    ldr r1, [pc, #0x9c4]
    mov r2, r0
    ldr r0, [r1, #0x18]
    ldr r3, [pc, #0x9c8]
    add r1, r0, #45
    mov r0, #3
    bl native_fn_021df974
    b L_021e2a20
    bl native_fn_021dfd34
    cmp r0, #3
    bne L_021e0a9c
    bl native_fn_02067748
    mov r2, r0
    mov r0, #2
    mov r1, #1
    mov r3, #56
    bl native_fn_021df974
    mov r0, #22
    bl native_fn_021e00bc
    b L_021e2a20
L_021e0a9c:
    bl native_fn_021dfd34
    cmp r0, #2
    bne L_021e2a20
    mov r0, r4
    bl native_fn_02067a60
    bl native_fn_020679f0
    mov r2, r0
    mov r0, #1
    mov r1, #5
    mov r3, #60
    bl native_fn_021df974
    mov r0, #16
    bl native_fn_021e00bc
    mov r0, r4
    mov r1, #1
    bl native_fn_020684ac
    b L_021e2a20
    bl native_fn_021dfd34
    cmp r0, #2
    blt L_021e2a20
    bl native_fn_021dfd34
    cmp r0, #2
    bne L_021e0b04
    mov r0, #2
    bl native_fn_02067a60
    bl native_fn_021e0000
L_021e0b04:
    bl native_fn_02067a30
    mov r2, r0
    mov r0, #1
    mov r1, #7
    mov r3, #80
    bl native_fn_021df974
    mov r0, #17
    bl native_fn_021e00bc
    b L_021e2a20
    bl native_fn_021dfd34
    cmp r0, #2
    blt L_021e2a20
    bl native_fn_021dfd34
    cmp r0, #2
    bne L_021e0b48
    mov r0, #3
    bl native_fn_02067a60
L_021e0b48:
    bl native_fn_02067a40
    mov r2, r0
    mov r0, #1
    mov r1, #4
    mov r3, #12
    bl native_fn_021df974
    mov r0, #19
    bl native_fn_021e00bc
    b L_021e2a20
    bl native_fn_021dfd34
    cmp r0, #2
    blt L_021e2a20
    bl native_fn_021dfd34
    cmp r0, #2
    bne L_021e0b8c
    mov r0, #6
    bl native_fn_02067a60
L_021e0b8c:
    mov r0, #87
    bl native_fn_021df590
    bl native_fn_021dee68
    mov r0, #33
    bl native_fn_021e00bc
    b L_021e2a20
    bl native_fn_021dfd34
    cmp r0, #2
    bne L_021e2a20
    mov r0, #87
    bl native_fn_021df590
    bl native_fn_021dee68
    bl native_fn_02063eec
    mov r1, r4
    mov r2, #256
    bl native_fn_02008d78
    bl native_fn_02067a40
    mov r1, r4
    mov r2, #12
    bl native_fn_02008d78
    bl native_fn_02063eec
    mov r1, r4
    strb r1, [r0]
    mov r0, #3
    bl native_fn_020684e0
    cmp r0, #0
    bne L_021e0c24
    mov r0, #1
    bl native_fn_020684e0
    cmp r0, #1
    bne L_021e0c24
    mov r0, #15
    mov r1, #4
    mov r2, #11
    bl native_fn_021ded5c
    mov r0, #15
    bl native_fn_021e00bc
    b L_021e2a20
L_021e0c24:
    mov r0, #3
    bl native_fn_020684e0
    cmp r0, #0
    bne L_021e0c44
    bl native_fn_02063ed4
    mov r1, #0
    str r1, [r0]
    b L_021e0c5c
L_021e0c44:
    bl native_fn_02063ed4
    mov r1, #0
    str r1, [r0]
    mov r0, #3
    mov r1, #1
    bl native_fn_020684ac
L_021e0c5c:
    mov r0, #0
    mov r1, #1
    bl native_fn_020684ac
    mov r0, #1
    bl native_fn_02068500
    mov r0, #33
    bl native_fn_021e00bc
    b L_021e2a20
    bl native_fn_021df150
    ldrh r1, [r0, #2]
    ldr r0, [pc, #0x7a0]
    tst r1, r0
    beq L_021e2a20
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_021dee68
    bl native_fn_02063ed4
    mov r1, r4
    str r1, [r0]
    mov r0, r1
    mov r1, #1
    bl native_fn_020684ac
    bl native_fn_02063eec
    mov r1, r4
    mov r2, #256
    bl native_fn_02008d78
    bl native_fn_02067a40
    mov r1, r4
    mov r2, #12
    bl native_fn_02008d78
    bl native_fn_02067748
    mov r1, r4
    mov r2, #56
    bl native_fn_02008d78
    bl native_fn_021dff30
    mov r0, #1
    bl native_fn_02068500
    mov r0, #33
    bl native_fn_021e00bc
    b L_021e2a20
    bl native_fn_021df150
    ldrh r1, [r0, #2]
    ldr r0, [pc, #0x720]
    tst r1, r0
    beq L_021e2a20
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_021dee68
    bl native_fn_020642f8
    mov r1, #9
    strb r1, [r0, #0x4]
    mov r4, #4
    b L_021e2a20
    bl native_fn_020644c0
    cmp r0, #0
    beq L_021e2a20
    mov r0, #1
    bl native_fn_01ff8604
    mov r0, #31
    bl native_fn_021e00bc
    ldr r2, [pc, #0x6d0]
    mov r0, #2
    mov r1, #14
    mov r3, #12
    bl native_fn_021df974
    b L_021e2a20
    bl native_fn_021dfd34
    cmp r0, #2
    bne L_021e2a20
    bl native_fn_021dee68
    mov r0, #87
    bl native_fn_021df590
    mov r0, #15
    mov r1, #3
    mov r2, #4
    bl native_fn_021ded5c
    mov r0, #32
    bl native_fn_021e00bc
    b L_021e2a20
    bl native_fn_021df150
    ldrh r1, [r0, #2]
    ldr r0, [pc, #0x684]
    tst r1, r0
    beq L_021e2a20
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_021dee68
    mov r0, #15
    mov r1, #4
    mov r2, #103
    bl native_fn_021ded5c
    mov r0, #34
    bl native_fn_021e00bc
    bl native_fn_021e2c2c
    cmp r0, #0
    bne L_021e2a20
    mov r0, r4
    mov r1, r0
    mov r2, #30
    bl native_fn_0205e814
    b L_021e2a20
    bl native_fn_021df960
    bl native_fn_020642f8
    ldrh r0, [r0]
    mov r1, #4
    cmp r0, #0
    mov r0, #15
    beq L_021e0e20
    mov r2, #24
    bl native_fn_021ded5c
    mov r0, #29
    bl native_fn_021e00bc
    b L_021e2a20
L_021e0e20:
    mov r2, #103
    bl native_fn_021ded5c
    mov r0, #34
    bl native_fn_021e00bc
    bl native_fn_021e2c2c
    cmp r0, #0
    bne L_021e2a20
    mov r0, r4
    mov r1, r0
    mov r2, #30
    bl native_fn_0205e814
    b L_021e2a20
    bl native_fn_021df150
    ldrh r1, [r0, #2]
    ldr r0, [pc, #0x5cc]
    tst r1, r0
    beq L_021e2a20
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_021dee68
    bl native_fn_02067748
    ldrb r0, [r0, #0x10]
    cmp r0, #0
    bne L_021e0e88
    mov r0, #1
    bl native_fn_02068500
L_021e0e88:
    bl native_fn_02068510
    cmp r0, #1
    bne L_021e0eb8
    mov r0, #33
    bl native_fn_021df524
    mov r0, #15
    mov r1, #4
    mov r2, #42
    bl native_fn_021ded5c
    mov r0, #23
    bl native_fn_021e00bc
    b L_021e2a20
L_021e0eb8:
    bl native_fn_021e2c2c
    cmp r0, #1
    cmpne r0, #2
    bne L_021e0ed4
    add sp, sp, #8
    mov r0, #5
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
L_021e0ed4:
    bl native_fn_02063eec
    ldrb r0, [r0, #0x1]
    cmp r0, #0
    bne L_021e0f1c
    bl native_fn_021dff78
    cmp r0, #0
    bne L_021e0f1c
    bl native_fn_02063eec
    ldrb r0, [r0]
    cmp r0, #0
    beq L_021e0f1c
    mov r0, #15
    mov r1, #4
    mov r2, #142
    bl native_fn_021ded5c
    mov r0, #21
    bl native_fn_021e00bc
    b L_021e2a20
L_021e0f1c:
    bl native_fn_021dff78
    cmp r0, #1
    bne L_021e0f7c
    bl native_fn_021dff30
    bl native_fn_02063eec
    mov r1, #0
    mov r2, #256
    bl native_fn_02008d78
    bl native_fn_02067a40
    mov r1, #0
    mov r2, #12
    bl native_fn_02008d78
    bl native_fn_02063ee0
    mov r5, r0
    bl native_fn_02067b58
    ldr r1, [r5]
    ldr r0, [r0, #0x24]
    cmp r1, r0
    bhs L_021e0f7c
    bl native_fn_02063ee0
    mov r5, r0
    bl native_fn_02067b58
    ldr r0, [r0, #0x24]
    str r0, [r5]
L_021e0f7c:
    mov r0, #33
    bl native_fn_021df524
    mov r0, #2
    bl native_fn_021d77e8
    mov r2, #2
    str r2, [sp]
    mov r3, #14
    mov r0, #5
    mov r1, #0
    str r3, [sp, #0x4]
    bl native_fn_021dea9c
    mov r0, #35
    bl native_fn_021e00bc
    b L_021e2a20
    bl native_fn_021df150
    ldrh r1, [r0, #2]
    ldr r0, [pc, #0x468]
    tst r1, r0
    beq L_021e2a20
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_021dee68
    mov r0, #15
    mov r1, #4
    mov r2, #43
    bl native_fn_021ded5c
    mov r0, #24
    bl native_fn_021e00bc
    mov r0, #2
    bl native_fn_021d77e8
    b L_021e2a20
    bl native_fn_021df150
    ldrh r1, [r0, #2]
    ldr r0, [pc, #0x424]
    tst r1, r0
    beq L_021e2a20
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_021dee68
    mov r0, #31
    bl native_fn_020642cc
    mov r0, r4
    mov r1, r0
    bl native_fn_021ddf58
    mov r4, #1
    b L_021e2a20
    bl native_fn_021df150
    ldrh r1, [r0, #2]
    ldr r0, [pc, #0x3e8]
    tst r1, r0
    beq L_021e2a20
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_021dee68
    mov r0, #33
    bl native_fn_020642cc
    mov r0, #13
    bl native_fn_021d77d8
    mov r0, #64
    bl native_fn_021e00bc
    mov r0, #63
    bl native_fn_020414c8
    mov r0, #1
    mov r1, #2
    mov r2, #10
    bl native_fn_02041538
    b L_021e2a20
    bl native_fn_021df150
    ldrh r1, [r0, #2]
    ldr r0, [pc, #0x394]
    tst r1, r0
    beq L_021e2a20
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_021dee68
    mov r2, #2
    str r2, [sp]
    mov r5, #34
    mov r0, #4
    mov r1, r4
    mov r3, #59
    str r5, [sp, #0x4]
    bl native_fn_021dea9c
    mov r0, #27
    bl native_fn_021e00bc
    b L_021e2a20
    bl native_fn_021df458
    bl native_fn_021df150
    ldrh r0, [r0, #2]
    tst r0, #1
    beq L_021e2a20
    mov r0, #82
    bl native_fn_021df590
    mov r0, r4
    bl native_fn_02068500
    bl native_fn_02067748
    mov r5, r0
    bl native_fn_021df15c
    str r0, [r5, #0x4]
    mov r0, #3
    mov r1, #2
    mov r2, #131
    bl native_fn_021dfe74
    bl native_fn_02067748
    ldr r1, [r0, #0x4]
    mov r0, #15
    add r1, r1, #59
    mov r1, r1, lsl #16
    mov r2, r1, lsr #16
    mov r1, #2
    bl native_fn_0205dc70
    mov r1, r4
    bl native_fn_02048034
    mov r0, #15
    mov r1, #4
    mov r2, #44
    bl native_fn_021ded5c
    mov r0, #28
    bl native_fn_021e00bc
    b L_021e2a20
    bl native_fn_021df150
    ldrh r1, [r0, #2]
    ldr r0, [pc, #0x2c0]
    tst r1, r0
    beq L_021e2a20
    bl native_fn_021dacb8
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_021dee68
    mov r0, r4
    bl native_fn_021dfd70
    mov r2, #2
    str r2, [sp]
    mov r3, #14
    mov r0, #5
    mov r1, r4
    str r3, [sp, #0x4]
    bl native_fn_021dea9c
    mov r0, #35
    bl native_fn_021e00bc
    b L_021e2a20
    bl native_fn_021df150
    ldrh r1, [r0, #2]
    ldr r0, [pc, #0x26c]
    tst r1, r0
    beq L_021e2a20
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_021dee68
    mov r4, #3
    b L_021e2a20
    mov r0, #5
    mov r1, r4
    bl native_fn_021df004
    cmp r0, #1
    beq L_021e2a20
    bl native_fn_021df458
    bl native_fn_021df150
    ldrh r0, [r0, #2]
    tst r0, #2
    beq L_021e1234
    bl native_fn_021de8f0
    bl native_fn_021df15c
    ldr r1, [pc, #0x208]
    str r0, [r1, #0x18]
    mov r0, #83
    bl native_fn_021df590
    mov r1, #10
    mov r2, r1
    mov r0, #15
    bl native_fn_021ded04
    mov r0, #50
    bl native_fn_021e00bc
    b L_021e2a20
L_021e1234:
    bl native_fn_021df150
    ldrh r0, [r0, #2]
    tst r0, #1
    beq L_021e2a20
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_021df15c
    cmp r0, #4
    addls pc, pc, r0, lsl #2
    b L_021e2a20
    b L_021e1270
    b L_021e13e0
    b L_021e1430
    b L_021e145c
    b L_021e14ac
L_021e1270:
    bl native_fn_021de8f0
    bl native_fn_021e2a5c
    cmp r0, #0
    bne L_021e129c
    mov r0, #15
    mov r1, #4
    mov r2, #55
    bl native_fn_021ded5c
    mov r0, #36
    bl native_fn_021e00bc
    b L_021e2a20
L_021e129c:
    bl native_fn_02067748
    ldrb r0, [r0, #0x10]
    cmp r0, #0
    bne L_021e12c8
    mov r0, #15
    mov r1, #4
    mov r2, #5
    bl native_fn_021ded5c
    mov r0, #36
    bl native_fn_021e00bc
    b L_021e2a20
L_021e12c8:
    bl native_fn_0206442c
    ldrh r0, [r0]
    cmp r0, #0
    bne L_021e12f4
    mov r0, #15
    mov r1, #4
    mov r2, #8
    bl native_fn_021ded5c
    mov r0, #36
    bl native_fn_021e00bc
    b L_021e2a20
L_021e12f4:
    bl native_fn_021d83c8
    mov r0, r4
    bl native_fn_02088e8c
    cmp r0, #0
    beq L_021e1328
    mov r0, #15
    mov r1, #4
    mov r2, #9
    bl native_fn_021ded5c
    mov r0, #36
    bl native_fn_021e00bc
    bl native_fn_021d83e4
    b L_021e2a20
L_021e1328:
    bl native_fn_021d83e4
    mov r0, r4
    bl native_fn_020646d0
    cmp r0, #0
    bne L_021e1358
    mov r0, #15
    mov r1, #4
    mov r2, #72
    bl native_fn_021ded5c
    mov r0, #36
    bl native_fn_021e00bc
    b L_021e2a20
L_021e1358:
    bl native_fn_02067748
    ldr r0, [r0, #0x4]
    mov r1, r4
    bl native_fn_020645b0
    cmp r0, #0
    bne L_021e138c
    mov r0, #15
    mov r1, #4
    mov r2, #40
    bl native_fn_021ded5c
    mov r0, #36
    bl native_fn_021e00bc
    b L_021e2a20
L_021e138c:
    mov r0, r4
    bl native_fn_020641ac
    cmp r0, #0
    beq L_021e13b8
    mov r0, #15
    mov r1, #4
    mov r2, #10
    bl native_fn_021ded5c
    mov r0, #36
    bl native_fn_021e00bc
    b L_021e2a20
L_021e13b8:
    bl native_fn_021e2ab8
    mov r0, #15
    mov r1, #4
    mov r2, #41
    bl native_fn_021ded5c
    mov r0, #1
    bl native_fn_021def28
    mov r0, #61
    bl native_fn_021e00bc
    b L_021e2a20
L_021e13e0:
    bl native_fn_021de8f0
    mov r0, #4
    bl native_fn_021dfd70
    mov r2, #2
    str r2, [sp]
    mov r5, #15
    mov r0, #3
    mov r1, r4
    mov r3, #27
    str r5, [sp, #0x4]
    bl native_fn_021dea9c
    mov r0, #39
    bl native_fn_021e00bc
    b L_021e2a20
    dcd 0x02216940
    dcd 0x02216ad8
    dcd 0x02216970
    dcd 0x0221698c
    dcd 0x00000c84
    dcd 0x00000ff7
L_021e1430:
    mov r2, #2
    str r2, [sp]
    mov r5, #16
    mov r0, #4
    mov r1, r4
    mov r3, #52
    str r5, [sp, #0x4]
    bl native_fn_021dea9c
    mov r0, #51
    bl native_fn_021e00bc
    b L_021e2a20
L_021e145c:
    bl native_fn_02067748
    ldr r0, [r0, #0x4]
    bl native_fn_021dc3b8
    bl native_fn_021de8f0
    mov r2, #2
    str r2, [sp]
    mov r0, #17
    str r0, [sp, #0x4]
    mov r0, #3
    mov r1, r4
    mov r3, #88
    bl native_fn_021dea9c
    mov r0, #38
    bl native_fn_021e00bc
    mov r0, #8
    bl native_fn_021d77e8
    ldr r0, [pc, #-0x8c]
    mov r1, r4
    str r1, [r0, #0x34]
    b L_021e2a20
L_021e14ac:
    bl native_fn_021de8f0
    bl native_fn_021df15c
    ldr r2, [pc, #-0xa4]
    mov r1, #10
    str r0, [r2, #0x18]
    mov r2, r1
    mov r0, #15
    bl native_fn_021ded04
    mov r0, #50
    bl native_fn_021e00bc
    b L_021e2a20
    bl native_fn_021df150
    ldrh r1, [r0, #2]
    ldr r0, [pc, #-0xbc]
    tst r1, r0
    beq L_021e2a20
    bl native_fn_021dee68
    mov r0, #82
    bl native_fn_021df590
    ldr r0, [pc, #-0xe8]
    ldr r0, [r0, #0x14]
    cmp r0, #37
    moveq r4, #2
    beq L_021e2a20
    mov r2, #2
    str r2, [sp]
    mov r3, #14
    mov r0, #5
    mov r1, r4
    str r3, [sp, #0x4]
    bl native_fn_021dea9c
    mov r0, #35
    bl native_fn_021e00bc
    b L_021e2a20
    bl native_fn_021def04
    bl native_fn_021df150
    ldrh r0, [r0, #2]
    tst r0, #1
    beq L_021e1590
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_021dee68
    bl native_fn_021df16c
    cmp r0, #0
    moveq r4, #2
    beq L_021e2a20
    mov r2, #2
    str r2, [sp]
    mov r3, #14
    ldr r0, [pc, #-0x160]
    str r3, [sp, #0x4]
    ldr r1, [r0, #0x18]
    mov r0, #5
    bl native_fn_021dea9c
    mov r0, #35
    bl native_fn_021e00bc
    b L_021e2a20
L_021e1590:
    bl native_fn_021df150
    ldrh r0, [r0, #2]
    tst r0, #2
    beq L_021e2a20
    bl native_fn_021dee68
    mov r0, #83
    bl native_fn_021df590
    mov r2, #2
    str r2, [sp]
    mov r3, #14
    ldr r0, [pc, #-0x1a8]
    str r3, [sp, #0x4]
    ldr r1, [r0, #0x18]
    mov r0, #5
    bl native_fn_021dea9c
    mov r0, #35
    bl native_fn_021e00bc
    b L_021e2a20
    bl native_fn_02041814
    cmp r0, #1
    movne r4, #6
    b L_021e2a20
    bl native_fn_021d8384
    cmp r0, #0
    beq L_021e2a20
    bl native_fn_021df458
    bl native_fn_021df15c
    ldr r1, [pc, #-0x1ec]
    ldr r1, [r1, #0x34]
    cmp r1, r0
    beq L_021e16ac
    bl native_fn_021df15c
    cmp r0, #0
    beq L_021e162c
    cmp r0, #1
    beq L_021e1638
    cmp r0, #2
    beq L_021e166c
    b L_021e169c
L_021e162c:
    mov r0, #8
    bl native_fn_021d77e8
    b L_021e169c
L_021e1638:
    bl native_fn_02067748
    ldr r1, [r0, #0x4]
    mov r0, r4
    bl native_fn_021dc108
    ldr r0, [pc, #-0x238]
    ldr r0, [r0, #0x34]
    cmp r0, #0
    bne L_021e1664
    mov r0, #10
    bl native_fn_021d77e8
    b L_021e169c
L_021e1664:
    bl native_fn_021dc178
    b L_021e169c
L_021e166c:
    bl native_fn_02067748
    ldr r1, [r0, #0x4]
    mov r0, #1
    bl native_fn_021dc108
    ldr r0, [pc, #-0x26c]
    ldr r0, [r0, #0x34]
    cmp r0, #0
    bne L_021e1698
    mov r0, #10
    bl native_fn_021d77e8
    b L_021e169c
L_021e1698:
    bl native_fn_021dc178
L_021e169c:
    bl native_fn_021df15c
    ldr r1, [pc, #-0x290]
    str r0, [r1, #0x34]
    b L_021e2a20
L_021e16ac:
    bl native_fn_021df150
    ldrh r0, [r0, #2]
    tst r0, #2
    beq L_021e2a20
    mov r0, #83
    bl native_fn_021df590
    mov r2, #2
    str r2, [sp]
    mov r3, #14
    mov r0, #5
    mov r1, #3
    str r3, [sp, #0x4]
    bl native_fn_021dea9c
    mov r0, #35
    bl native_fn_021e00bc
    mov r0, #2
    bl native_fn_021d77e8
    b L_021e2a20
    bl native_fn_021df458
    bl native_fn_021df150
    ldrh r0, [r0, #2]
    tst r0, #2
    beq L_021e1738
    mov r0, #83
    bl native_fn_021df590
    mov r2, #2
    str r2, [sp]
    mov r3, #14
    mov r0, #5
    mov r1, #1
    str r3, [sp, #0x4]
    bl native_fn_021dea9c
    mov r0, #35
    bl native_fn_021e00bc
    b L_021e2a20
L_021e1738:
    bl native_fn_021df150
    ldrh r0, [r0, #2]
    tst r0, #1
    beq L_021e2a20
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_021df15c
    cmp r0, #0
    beq L_021e1770
    cmp r0, #1
    beq L_021e17e8
    cmp r0, #2
    beq L_021e1848
    b L_021e2a20
L_021e1770:
    mov r0, #2
    bl native_fn_020684e0
    cmp r0, #1
    bne L_021e17c0
    mov r0, #4
    bl native_fn_021dfd70
    mov r2, #2
    str r2, [sp]
    mov r5, #27
    mov r0, #4
    mov r1, r4
    mov r3, #23
    str r5, [sp, #0x4]
    bl native_fn_021dea9c
    mov r0, #41
    bl native_fn_021e00bc
    ldr r0, [pc, #-0x3a0]
    mvn r1, #0
    str r1, [r0, #0x34]
    b L_021e2a20
L_021e17c0:
    mov r0, #15
    mov r1, #4
    mov r2, #66
    bl native_fn_021ded5c
    ldr r1, [pc, #-0x3c0]
    mov r2, r4
    mov r0, #40
    str r2, [r1, #0x18]
    bl native_fn_021e00bc
    b L_021e2a20
L_021e17e8:
    bl native_fn_021e2a5c
    cmp r0, #0
    bne L_021e181c
    mov r0, #15
    mov r1, #4
    mov r2, #55
    bl native_fn_021ded5c
    ldr r1, [pc, #-0x3f4]
    mov r2, #1
    mov r0, #40
    str r2, [r1, #0x18]
    bl native_fn_021e00bc
    b L_021e2a20
L_021e181c:
    mov r2, #2
    str r2, [sp]
    mov r5, #28
    mov r0, #5
    mov r1, r4
    mov r3, #30
    str r5, [sp, #0x4]
    bl native_fn_021dea9c
    mov r0, #43
    bl native_fn_021e00bc
    b L_021e2a20
L_021e1848:
    mov r0, #3
    bl native_fn_021d77e8
    mov r0, #42
    bl native_fn_021e00bc
    mov r0, #1
    bl native_fn_021dfd70
    bl native_fn_02062aa0
    mov r1, #2
    str r1, [sp]
    mov r1, #29
    str r1, [sp, #0x4]
    mov r1, r4
    and r0, r0, #255
    mov r2, r1
    mov r3, r1
    bl native_fn_021dea9c
    mov r0, #42
    bl native_fn_021e00bc
    mov r0, r4
    bl native_fn_0206258c
    ldr r0, [pc, #-0x488]
    mov r1, r4
    str r1, [r0, #0x34]
    b L_021e2a20
    bl native_fn_021df150
    ldrh r1, [r0, #2]
    ldr r0, [pc, #-0x48c]
    tst r1, r0
    beq L_021e2a20
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_021dee68
    mov r2, #2
    str r2, [sp]
    mov r1, #15
    ldr r0, [pc, #-0x4c4]
    str r1, [sp, #0x4]
    ldr r1, [r0, #0x18]
    mov r0, #3
    mov r3, #27
    bl native_fn_021dea9c
    mov r0, #39
    bl native_fn_021e00bc
    b L_021e2a20
    bl native_fn_021d8384
    cmp r0, #0
    beq L_021e2a20
    bl native_fn_021df458
    bl native_fn_021df15c
    ldr r1, [pc, #-0x4fc]
    ldr r1, [r1, #0x34]
    cmp r1, r0
    beq L_021e19b8
    bl native_fn_021df15c
    cmp r0, #3
    addls pc, pc, r0, lsl #2
    b L_021e19a8
    b L_021e193c
    b L_021e1948
    b L_021e1954
    b L_021e1980
L_021e193c:
    mov r0, #11
    bl native_fn_021d77e8
    b L_021e19a8
L_021e1948:
    mov r0, #13
    bl native_fn_021d77e8
    b L_021e19a8
L_021e1954:
    mov r0, r4
    bl native_fn_021dc7cc
    ldr r0, [pc, #-0x54c]
    ldr r0, [r0, #0x34]
    cmp r0, #1
    bne L_021e1978
    mov r0, #9
    bl native_fn_021d77e8
    b L_021e19a8
L_021e1978:
    bl native_fn_021dc878
    b L_021e19a8
L_021e1980:
    mov r0, #1
    bl native_fn_021dc7cc
    ldr r0, [pc, #-0x578]
    ldr r0, [r0, #0x34]
    cmp r0, #0
    bne L_021e19a4
    mov r0, #9
    bl native_fn_021d77e8
    b L_021e19a8
L_021e19a4:
    bl native_fn_021dc878
L_021e19a8:
    bl native_fn_021df15c
    ldr r1, [pc, #-0x59c]
    str r0, [r1, #0x34]
    b L_021e2a20
L_021e19b8:
    bl native_fn_021df150
    ldrh r0, [r0, #2]
    tst r0, #2
    beq L_021e2a20
    mov r0, #83
    bl native_fn_021df590
    mov r0, r4
    bl native_fn_021dfd70
    mov r2, #2
    str r2, [sp]
    mov r5, #15
    mov r0, #3
    mov r1, r4
    mov r3, #27
    str r5, [sp, #0x4]
    bl native_fn_021dea9c
    mov r0, #39
    bl native_fn_021e00bc
    mov r0, #2
    bl native_fn_021d77e8
    b L_021e2a20
    bl native_fn_021df458
    bl native_fn_021df150
    ldrh r0, [r0, #2]
    tst r0, #2
    beq L_021e1a6c
    mov r0, #83
    bl native_fn_021df590
    mov r0, r4
    bl native_fn_021dfd70
    mov r1, #2
    mov r2, r1
    str r1, [sp]
    mov r5, #15
    mov r0, #3
    mov r3, #27
    str r5, [sp, #0x4]
    bl native_fn_021dea9c
    mov r0, #39
    bl native_fn_021e00bc
    mov r0, #2
    bl native_fn_021d77e8
    mov r0, #1
    bl native_fn_0206258c
    b L_021e2a20
L_021e1a6c:
    bl native_fn_021df15c
    ldr r1, [pc, #-0x660]
    ldr r1, [r1, #0x34]
    cmp r1, r0
    beq L_021e2a20
    bl native_fn_021df15c
    ldr r1, [pc, #-0x674]
    str r0, [r1, #0x34]
    bl native_fn_02062a50
    bl native_fn_0206dcd0
    b L_021e2a20
    bl native_fn_021df458
    bl native_fn_021df150
    ldrh r0, [r0, #2]
    tst r0, #2
    beq L_021e1ae0
    mov r0, #83
    bl native_fn_021df590
    mov r2, #2
    str r2, [sp]
    mov r5, #15
    mov r0, #3
    mov r1, #1
    mov r3, #27
    str r5, [sp, #0x4]
    bl native_fn_021dea9c
    mov r0, #39
    bl native_fn_021e00bc
    b L_021e2a20
L_021e1ae0:
    bl native_fn_021df150
    ldrh r0, [r0, #2]
    tst r0, #1
    beq L_021e2a20
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_021df15c
    cmp r0, #5
    addls pc, pc, r0, lsl #2
    b L_021e2a20
    b L_021e1b20
    b L_021e1b54
    b L_021e1ba8
    b L_021e1bc4
    b L_021e1bf8
    b L_021e1c14
L_021e1b20:
    mov r0, #2
    mov r2, r0
    str r0, [sp]
    mov r5, #30
    mov r1, r4
    mov r3, #38
    str r5, [sp, #0x4]
    bl native_fn_021dea9c
    mov r0, #44
    bl native_fn_021e00bc
    mov r0, #6
    bl native_fn_021dfd70
    b L_021e2a20
L_021e1b54:
    mov r0, #30
    bl native_fn_020642cc
    mov r0, #5
    bl native_fn_020406c8
    mov r0, #15
    bl native_fn_020cf44c
    mov r0, #1
    bl native_fn_020cf43c
    mov r0, #16
    bl native_fn_021d77d8
    mov r0, #64
    bl native_fn_021e00bc
    mov r0, #63
    bl native_fn_020414c8
    mov r0, #1
    mov r1, #2
    mov r2, #10
    bl native_fn_02041538
    mov r0, r4
    bl native_fn_0206258c
    b L_021e2a20
L_021e1ba8:
    mov r0, #31
    bl native_fn_020642cc
    mov r0, r4
    mov r1, r0
    bl native_fn_021ddf58
    mov r4, #1
    b L_021e2a20
L_021e1bc4:
    mov r0, #33
    bl native_fn_020642cc
    mov r0, #13
    bl native_fn_021d77d8
    mov r0, #64
    bl native_fn_021e00bc
    mov r0, #63
    bl native_fn_020414c8
    mov r0, #1
    mov r1, #2
    mov r2, #10
    bl native_fn_02041538
    b L_021e2a20
L_021e1bf8:
    mov r0, #15
    mov r1, #4
    mov r2, #153
    bl native_fn_021ded5c
    mov r0, #47
    bl native_fn_021e00bc
    b L_021e2a20
L_021e1c14:
    mov r2, #2
    str r2, [sp]
    mov r3, #14
    mov r0, #5
    mov r1, #1
    str r3, [sp, #0x4]
    bl native_fn_021dea9c
    mov r0, #35
    bl native_fn_021e00bc
    b L_021e2a20
    mov r0, #6
    bl native_fn_021dfd70
    bl native_fn_021df458
    bl native_fn_021df150
    ldrh r0, [r0, #2]
    tst r0, #2
    beq L_021e1c94
    mov r0, #83
    bl native_fn_021df590
    mov r2, #2
    str r2, [sp]
    mov r5, #28
    mov r0, #5
    mov r1, r4
    mov r3, #30
    str r5, [sp, #0x4]
    bl native_fn_021dea9c
    mov r0, #43
    bl native_fn_021e00bc
    mov r0, r4
    bl native_fn_021dfd70
    b L_021e2a20
L_021e1c94:
    bl native_fn_021df150
    ldrh r0, [r0, #2]
    tst r0, #1
    beq L_021e2a20
    ldr r0, [pc, #0xd80]
    bl native_fn_02063b40
    cmp r0, #0
    bne L_021e1ce8
    bl native_fn_021df15c
    cmp r0, #1
    bne L_021e1ce8
    mov r0, #15
    mov r1, #11
    mov r2, #2
    bl native_fn_021ded5c
    mov r0, #45
    bl native_fn_021e00bc
    mvn r0, #0
    mov r1, #84
    bl native_fn_0205e7a8
    b L_021e2a20
L_021e1ce8:
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_021df15c
    add r0, r0, #28
    bl native_fn_020642cc
    mov r0, #1
    bl native_fn_020c40f4
    mov r0, #15
    bl native_fn_020cf44c
    mov r0, #3
    bl native_fn_020cf43c
    mov r0, #16
    bl native_fn_021d77d8
    mov r0, #64
    bl native_fn_021e00bc
    mov r0, #63
    bl native_fn_020414c8
    mov r0, #1
    mov r1, #2
    mov r2, #10
    bl native_fn_02041538
    mov r0, #0
    bl native_fn_0206258c
    mov r0, #0
    bl native_fn_021dfd70
    b L_021e2a20
    bl native_fn_021dee98
    cmp r0, #0
    beq L_021e2a20
    mov r0, #44
    bl native_fn_021e00bc
    b L_021e2a20
    bl native_fn_021df150
    ldrh r1, [r0, #2]
    ldr r0, [pc, #-0x94c]
    tst r1, r0
    beq L_021e2a20
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_021dee68
    bl native_fn_02067748
    mov r2, #2
    str r2, [sp]
    mov r1, #34
    str r1, [sp, #0x4]
    ldr r1, [r0, #0x4]
    mov r0, #4
    mov r3, #59
    bl native_fn_021dea9c
    mov r0, #46
    bl native_fn_021e00bc
    b L_021e2a20
    bl native_fn_021df458
    bl native_fn_021df150
    ldrh r0, [r0, #2]
    tst r0, #2
    beq L_021e1e04
    bl native_fn_021dee68
    mov r0, #83
    bl native_fn_021df590
    mov r2, #2
    str r2, [sp]
    mov r5, #28
    mov r0, #5
    mov r1, #4
    mov r3, #30
    str r5, [sp, #0x4]
    bl native_fn_021dea9c
    mov r0, #43
    bl native_fn_021e00bc
    b L_021e2a20
L_021e1e04:
    bl native_fn_021df150
    ldrh r0, [r0, #2]
    tst r0, #1
    beq L_021e2a20
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_021df15c
    ldr r1, [pc, #-0xa10]
    str r0, [r1, #0x18]
    bl native_fn_02067748
    ldr r1, [pc, #-0xa1c]
    ldr r0, [r0, #0x4]
    ldr r1, [r1, #0x18]
    cmp r1, r0
    mov r1, #4
    bne L_021e1e6c
    mov r2, #2
    str r2, [sp]
    mov r5, #28
    mov r0, #5
    mov r3, #30
    str r5, [sp, #0x4]
    bl native_fn_021dea9c
    mov r0, #43
    bl native_fn_021e00bc
    b L_021e2a20
L_021e1e6c:
    mov r0, #15
    mov r2, #154
    bl native_fn_021ded04
    mov r0, #48
    bl native_fn_021e00bc
    b L_021e2a20
    bl native_fn_021def04
    bl native_fn_021df150
    ldrh r0, [r0, #2]
    tst r0, #2
    beq L_021e1ed4
    mov r0, #83
    bl native_fn_021df590
    bl native_fn_021dee68
    mov r0, #46
    bl native_fn_021e00bc
    mov r2, #2
    str r2, [sp]
    mov r0, #34
    str r0, [sp, #0x4]
    mov r0, #4
    ldr r1, [pc, #-0xab0]
    mov r3, #59
    ldr r1, [r1, #0x18]
    bl native_fn_021dea9c
    b L_021e2a20
L_021e1ed4:
    bl native_fn_021df150
    ldrh r0, [r0, #2]
    tst r0, #1
    beq L_021e2a20
    bl native_fn_021dee68
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_021df16c
    cmp r0, #0
    bne L_021e1f4c
    bl native_fn_02067748
    ldr r1, [pc, #-0xaf0]
    ldr r1, [r1, #0x18]
    str r1, [r0, #0x4]
    bl native_fn_02067748
    ldr r0, [r0, #0x4]
    mov r1, r4
    bl native_fn_020645b0
    cmp r0, #0
    mov r0, #15
    mov r1, #4
    bne L_021e1f38
    mov r2, #155
    bl native_fn_021ded5c
    b L_021e1f40
L_021e1f38:
    mov r2, #157
    bl native_fn_021ded5c
L_021e1f40:
    mov r0, #49
    bl native_fn_021e00bc
    b L_021e2a20
L_021e1f4c:
    mov r2, #2
    str r2, [sp]
    mov r1, #34
    ldr r0, [pc, #-0xb48]
    str r1, [sp, #0x4]
    ldr r1, [r0, #0x18]
    mov r0, #4
    mov r3, #59
    bl native_fn_021dea9c
    mov r0, #46
    bl native_fn_021e00bc
    b L_021e2a20
    bl native_fn_021df150
    ldrh r1, [r0, #2]
    ldr r0, [pc, #-0xb60]
    tst r1, r0
    beq L_021e2a20
    bl native_fn_021dacb8
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_021dee68
    bl native_fn_02067748
    ldr r0, [r0, #0x4]
    mov r1, r4
    bl native_fn_020645b0
    cmp r0, #0
    bne L_021e1fec
    mov r0, #2
    mov r2, r0
    str r0, [sp]
    mov r5, #30
    mov r1, r4
    mov r3, #38
    str r5, [sp, #0x4]
    bl native_fn_021dea9c
    mov r0, #44
    bl native_fn_021e00bc
    mov r0, #6
    bl native_fn_021dfd70
    b L_021e2a20
L_021e1fec:
    mov r2, #2
    str r2, [sp]
    mov r5, #28
    mov r0, #5
    mov r1, #4
    mov r3, #30
    str r5, [sp, #0x4]
    bl native_fn_021dea9c
    mov r0, #43
    bl native_fn_021e00bc
    b L_021e2a20
    bl native_fn_021d8384
    cmp r0, #0
    beq L_021e2a20
    mov r0, #5
    mov r1, #8
    bl native_fn_021df004
    cmp r0, #1
    beq L_021e2a20
    bl native_fn_021df458
    bl native_fn_021df150
    ldrh r0, [r0, #2]
    tst r0, #2
    beq L_021e2080
    bl native_fn_021dee68
    mov r0, #83
    bl native_fn_021df590
    mov r1, #2
    mov r2, r1
    str r1, [sp]
    mov r3, #14
    mov r0, #5
    str r3, [sp, #0x4]
    bl native_fn_021dea9c
    mov r0, #35
    bl native_fn_021e00bc
    b L_021e2a20
L_021e2080:
    bl native_fn_021df150
    ldrh r0, [r0, #2]
    tst r0, #1
    beq L_021e2a20
    bl native_fn_021df15c
    ldr r1, [pc, #-0xc84]
    str r0, [r1, #0x1c]
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_021de8f0
    bl native_fn_021df15c
    cmp r0, #3
    addls pc, pc, r0, lsl #2
    b L_021e2a20
    b L_021e20c8
    b L_021e2130
    b L_021e2198
    b L_021e21f8
L_021e20c8:
    bl native_fn_02067b58
    ldr r0, [r0, #0x10]
    cmp r0, #0
    bne L_021e20f4
    mov r0, #15
    mov r1, #4
    mov r2, #139
    bl native_fn_021ded5c
    mov r0, #52
    bl native_fn_021e00bc
    b L_021e2a20
L_021e20f4:
    mov r0, #53
    bl native_fn_021e00bc
    mov r0, r4
    mov r1, #2
    mov r2, #52
    bl native_fn_021dfe74
    mov r2, #2
    str r2, [sp]
    mov r5, #16
    mov r0, #4
    mov r1, r4
    mov r3, #59
    str r5, [sp, #0x4]
    bl native_fn_021dea9c
    b L_021e2a20
L_021e2130:
    bl native_fn_02067b58
    ldr r0, [r0, #0x10]
    cmp r0, #0
    bne L_021e215c
    mov r0, #15
    mov r1, #4
    mov r2, #139
    bl native_fn_021ded5c
    mov r0, #52
    bl native_fn_021e00bc
    b L_021e2a20
L_021e215c:
    mov r0, #55
    bl native_fn_021e00bc
    mov r0, r4
    mov r1, #2
    mov r2, #53
    bl native_fn_021dfe74
    mov r2, #2
    str r2, [sp]
    mov r5, #16
    mov r0, #9
    mov r1, r4
    mov r3, #72
    str r5, [sp, #0x4]
    bl native_fn_021dea9c
    b L_021e2a20
L_021e2198:
    bl native_fn_02067b58
    ldr r0, [r0, #0x10]
    cmp r0, #0
    bne L_021e21c4
    mov r0, #15
    mov r1, #4
    mov r2, #134
    bl native_fn_021ded5c
    mov r0, #52
    bl native_fn_021e00bc
    b L_021e2a20
L_021e21c4:
    mov r0, #57
    bl native_fn_021e00bc
    mov r1, r4
    mov r2, r1
    mov r0, #1
    bl native_fn_021db59c
    mov r0, #4
    bl native_fn_021d77e8
    mov r1, #4
    mov r2, r1
    mov r0, #15
    bl native_fn_021ded5c
    b L_021e2a20
L_021e21f8:
    mov r0, r4
    mov r1, #2
    mov r2, #55
    bl native_fn_021dfe74
    mov r0, #58
    bl native_fn_021e00bc
    mov r2, #2
    str r2, [sp]
    mov r5, #16
    mov r0, #4
    mov r1, r4
    mov r3, #59
    str r5, [sp, #0x4]
    bl native_fn_021dea9c
    b L_021e2a20
    bl native_fn_021df150
    ldrh r1, [r0, #2]
    ldr r0, [pc, #-0xe18]
    tst r1, r0
    beq L_021e2a20
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_021dee68
    mov r2, #2
    str r2, [sp]
    mov r1, #16
    ldr r0, [pc, #-0xe50]
    str r1, [sp, #0x4]
    ldr r1, [r0, #0x1c]
    mov r0, #4
    mov r3, #52
    bl native_fn_021dea9c
    mov r0, #51
    bl native_fn_021e00bc
    b L_021e2a20
    bl native_fn_021df458
    bl native_fn_021d8384
    cmp r0, #0
    beq L_021e2a20
    bl native_fn_021df150
    ldrh r0, [r0, #2]
    tst r0, #2
    beq L_021e22e0
    mov r0, #83
    bl native_fn_021df590
    mov r0, r4
    bl native_fn_021dfe94
    mov r2, #2
    str r2, [sp]
    mov r5, #16
    mov r0, #4
    mov r1, r4
    mov r3, #52
    str r5, [sp, #0x4]
    bl native_fn_021dea9c
    mov r0, #51
    bl native_fn_021e00bc
    b L_021e2a20
L_021e22e0:
    bl native_fn_021df150
    ldrh r0, [r0, #2]
    tst r0, #1
    beq L_021e2a20
    bl native_fn_021df15c
    ldr r1, [pc, #-0xee4]
    mov r2, r4
    str r0, [r1, #0x10]
    mov r0, #82
    str r2, [r1, #0x18]
    bl native_fn_021df590
    ldr r1, [pc, #-0xefc]
    mov r0, #1
    ldr r2, [r1, #0x10]
    mov r1, #2
    add r2, r2, #59
    mov r2, r2, lsl #16
    mov r2, r2, lsr #16
    bl native_fn_021dfe74
    mov r2, #2
    str r2, [sp]
    mov r0, #16
    str r0, [sp, #0x4]
    mov r0, #3
    mov r1, r4
    mov r3, #66
    bl native_fn_021dea9c
    ldr r1, [pc, #-0xf3c]
    mov r0, r4
    ldr r1, [r1, #0x10]
    mov r2, r0
    bl native_fn_021db59c
    mov r0, #4
    bl native_fn_021d77e8
    mov r0, #54
    bl native_fn_021e00bc
    b L_021e2a20
    bl native_fn_021d8384
    cmp r0, #0
    beq L_021e2a20
    bl native_fn_021dbb88
    cmp r0, #1
    beq L_021e2a20
    bl native_fn_021df458
    bl native_fn_021df15c
    ldr r1, [pc, #-0xf84]
    ldr r1, [r1, #0x18]
    cmp r1, r0
    beq L_021e23cc
    bl native_fn_021df15c
    mov r1, #10
    ldr r3, [pc, #0x67c]
    mul r2, r0, r1
    str r0, [r3, #0x18]
    ldr r1, [r3, #0x10]
    mov r0, r4
    bl native_fn_021db59c
    bl native_fn_021db660
    b L_021e2a20
L_021e23cc:
    bl native_fn_021df150
    ldrh r0, [r0, #2]
    tst r0, #2
    beq L_021e2a20
    mov r0, #83
    bl native_fn_021df590
    mov r0, #53
    bl native_fn_021e00bc
    mov r0, #1
    bl native_fn_021dfe94
    mov r2, #2
    str r2, [sp]
    mov r0, #16
    str r0, [sp, #0x4]
    mov r0, #4
    ldr r1, [pc, #0x620]
    mov r3, #59
    ldr r1, [r1, #0x10]
    bl native_fn_021dea9c
    mov r0, #2
    bl native_fn_021d77e8
    b L_021e2a20
    bl native_fn_021df458
    bl native_fn_021d8384
    cmp r0, #0
    beq L_021e2a20
    bl native_fn_021df150
    ldrh r0, [r0, #2]
    tst r0, #2
    beq L_021e2480
    mov r0, #83
    bl native_fn_021df590
    mov r0, r4
    bl native_fn_021dfe94
    mov r2, #2
    str r2, [sp]
    mov r5, #16
    mov r0, #4
    mov r1, #1
    mov r3, #52
    str r5, [sp, #0x4]
    bl native_fn_021dea9c
    mov r0, #51
    bl native_fn_021e00bc
    b L_021e2a20
L_021e2480:
    bl native_fn_021df150
    ldrh r0, [r0, #2]
    tst r0, #1
    beq L_021e2a20
    bl native_fn_021df15c
    ldr r1, [pc, #0x594]
    mov r2, r4
    str r0, [r1, #0x10]
    mov r0, #82
    str r2, [r1, #0x18]
    bl native_fn_021df590
    ldr r1, [pc, #0x57c]
    mov r0, #1
    ldr r2, [r1, #0x10]
    mov r1, #2
    add r2, r2, #72
    mov r2, r2, lsl #16
    mov r2, r2, lsr #16
    bl native_fn_021dfe74
    mov r2, #2
    str r2, [sp]
    mov r0, #16
    str r0, [sp, #0x4]
    mov r0, #4
    mov r1, r4
    mov r3, #59
    bl native_fn_021dea9c
    ldr r0, [pc, #0x53c]
    mov r2, r4
    ldr r3, [r0, #0x10]
    ldr r1, [r0, #0x18]
    add r0, r3, #3
    bl native_fn_021db59c
    mov r0, #4
    bl native_fn_021d77e8
    mov r0, #56
    bl native_fn_021e00bc
    b L_021e2a20
    bl native_fn_021d8384
    cmp r0, #0
    beq L_021e2a20
    bl native_fn_021dbb88
    cmp r0, #1
    beq L_021e2a20
    bl native_fn_021df458
    bl native_fn_021df15c
    ldr r1, [pc, #0x4f0]
    ldr r1, [r1, #0x18]
    cmp r1, r0
    beq L_021e2570
    bl native_fn_021df15c
    ldr r2, [pc, #0x4dc]
    mov r1, r0
    str r1, [r2, #0x18]
    ldr r0, [r2, #0x10]
    mov r2, r4
    add r0, r0, #3
    bl native_fn_021db59c
    bl native_fn_021db660
    b L_021e2a20
L_021e2570:
    bl native_fn_021df150
    ldrh r0, [r0, #2]
    tst r0, #2
    beq L_021e2a20
    mov r0, #83
    bl native_fn_021df590
    mov r0, #1
    bl native_fn_021dfe94
    mov r0, #2
    bl native_fn_021d77e8
    mov r0, r4
    mov r1, #2
    mov r2, #53
    bl native_fn_021dfe74
    mov r2, #2
    str r2, [sp]
    mov r0, #16
    str r0, [sp, #0x4]
    ldr r1, [pc, #0x470]
    mov r0, #9
    ldr r1, [r1, #0x10]
    mov r3, #72
    bl native_fn_021dea9c
    mov r0, #55
    bl native_fn_021e00bc
    b L_021e2a20
    bl native_fn_021d8384
    cmp r0, #0
    beq L_021e2a20
    bl native_fn_021df150
    ldrh r1, [r0, #2]
    ldr r0, [pc, #0x440]
    tst r1, r0
    beq L_021e2a20
    mov r0, r4
    bl native_fn_021dfe94
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_021dee68
    mov r1, #2
    str r1, [sp]
    mov r0, #16
    str r0, [sp, #0x4]
    mov r0, #4
    mov r2, r1
    mov r3, #52
    bl native_fn_021dea9c
    mov r0, #51
    bl native_fn_021e00bc
    mov r0, #2
    bl native_fn_021d77e8
    b L_021e2a20
    bl native_fn_021df458
    bl native_fn_021df150
    ldrh r0, [r0, #2]
    tst r0, #2
    beq L_021e2690
    mov r0, #83
    bl native_fn_021df590
    mov r0, r4
    bl native_fn_021dfe94
    mov r2, #2
    str r2, [sp]
    mov r5, #16
    mov r0, #4
    mov r1, #3
    mov r3, #52
    str r5, [sp, #0x4]
    bl native_fn_021dea9c
    mov r0, #51
    bl native_fn_021e00bc
    b L_021e2a20
L_021e2690:
    bl native_fn_021df150
    ldrh r0, [r0, #2]
    tst r0, #1
    beq L_021e2a20
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_021df15c
    ldr r1, [pc, #0x37c]
    mov r2, r4
    str r0, [r1, #0x10]
    str r2, [r1, #0x18]
    bl native_fn_02067bc4
    ldr r0, [r0]
    cmp r0, #0
    bne L_021e26e8
    mov r0, #15
    mov r1, #4
    mov r2, #151
    bl native_fn_021ded5c
    mov r0, #60
    bl native_fn_021e00bc
    b L_021e2a20
L_021e26e8:
    ldr r1, [pc, #0x340]
    mov r0, #1
    ldr r2, [r1, #0x10]
    mov r1, #2
    add r2, r2, #59
    mov r2, r2, lsl #16
    mov r2, r2, lsr #16
    bl native_fn_021dfe74
    mov r0, #12
    bl native_fn_021d77e8
    ldr r0, [pc, #0x318]
    mov r1, r4
    ldr r0, [r0, #0x10]
    bl native_fn_021db3ac
    mov r0, #59
    bl native_fn_021e00bc
    mov r0, #3
    bl native_fn_021dfd70
    ldr r0, [pc, #0x2f8]
    ldr r0, [r0, #0x10]
    bl native_fn_02067bc4
    ldr r1, [r0]
    ldr r0, [pc, #0x2f0]
    add r1, r1, #9
    umull r0, r2, r1, r0
    mov r2, r2, lsr #3
    and r0, r2, #255
    mov r2, #2
    cmp r0, #10
    movhi r0, #10
    str r2, [sp]
    mov r5, #16
    mov r1, #0
    mov r3, #66
    str r5, [sp, #0x4]
    bl native_fn_021dea9c
    b L_021e2a20
    bl native_fn_021df458
    bl native_fn_021d8384
    cmp r0, #0
    beq L_021e2a20
    bl native_fn_021df15c
    ldr r1, [pc, #0x298]
    ldr r1, [r1, #0x18]
    cmp r1, r0
    beq L_021e27c4
    bl native_fn_021df15c
    mov r1, #10
    ldr r2, [pc, #0x280]
    mul r1, r0, r1
    str r0, [r2, #0x18]
    ldr r0, [r2, #0x10]
    bl native_fn_021db3ac
    bl native_fn_021db410
    b L_021e2a20
L_021e27c4:
    bl native_fn_021df150
    ldrh r0, [r0, #2]
    tst r0, #2
    beq L_021e2a20
    mov r0, #2
    bl native_fn_021d77e8
    mov r0, #83
    bl native_fn_021df590
    mov r0, #1
    bl native_fn_021dfe94
    mov r0, #58
    bl native_fn_021e00bc
    mov r0, r4
    bl native_fn_021dfd70
    mov r2, #2
    str r2, [sp]
    mov r0, #16
    str r0, [sp, #0x4]
    ldr r1, [pc, #0x21c]
    mov r0, #4
    ldr r1, [r1, #0x10]
    mov r3, #59
    bl native_fn_021dea9c
    b L_021e2a20
    bl native_fn_021df150
    ldrh r1, [r0, #2]
    ldr r0, [pc, #0x200]
    tst r1, r0
    beq L_021e2a20
    bl native_fn_021dee68
    mov r0, #82
    bl native_fn_021df590
    mov r0, #58
    bl native_fn_021e00bc
    mov r2, #2
    str r2, [sp]
    mov r0, #16
    str r0, [sp, #0x4]
    mov r0, #4
    ldr r1, [pc, #0x1c8]
    mov r3, #59
    ldr r1, [r1, #0x10]
    bl native_fn_021dea9c
    b L_021e2a20
    bl native_fn_021e2ba4
    ldr r2, [pc, #0x1b0]
    mvn r1, #1
    strb r0, [r2]
    ldrsb r0, [r2]
    cmp r0, r1
    beq L_021e2a20
    mov r0, #87
    bl native_fn_021df590
    bl native_fn_021dee68
    ldr r0, [pc, #0x18c]
    ldrsb r0, [r0]
    cmp r0, #3
    addls pc, pc, r0, lsl #2
    b L_021e28f8
    b L_021e28c0
    b L_021e28c0
    b L_021e28c0
    b L_021e28dc
L_021e28c0:
    mov r0, #15
    mov r1, #4
    mov r2, #7
    bl native_fn_021ded5c
    mov r0, #37
    bl native_fn_021e00bc
    b L_021e2a20
L_021e28dc:
    mov r0, #15
    mov r1, #4
    mov r2, #6
    bl native_fn_021ded5c
    mov r0, #37
    bl native_fn_021e00bc
    b L_021e2a20
L_021e28f8:
    mov r0, #62
    bl native_fn_021e00bc
    bl native_fn_02067748
    ldr r1, [r0, #0x4]
    mov r0, #15
    add r1, r1, #59
    mov r1, r1, lsl #16
    mov r2, r1, lsr #16
    mov r1, #2
    bl native_fn_0205dc70
    mov r1, #0
    bl native_fn_02048034
    mov r0, #15
    mov r1, #4
    mov r2, #13
    bl native_fn_021ded04
    b L_021e2a20
    bl native_fn_021def04
    bl native_fn_021df150
    ldrh r0, [r0, #2]
    tst r0, #2
    beq L_021e2984
    bl native_fn_021dee68
    mov r0, #83
    bl native_fn_021df590
    mov r2, #2
    str r2, [sp]
    mov r3, #14
    mov r0, #5
    mov r1, r4
    str r3, [sp, #0x4]
    bl native_fn_021dea9c
    mov r0, #35
    bl native_fn_021e00bc
    b L_021e2a20
L_021e2984:
    bl native_fn_021df150
    ldrh r0, [r0, #2]
    tst r0, #1
    beq L_021e2a20
    bl native_fn_021dee68
    mov r0, #82
    bl native_fn_021df590
    bl native_fn_021df16c
    cmp r0, #0
    bne L_021e29ec
    bl native_fn_021e2a40
    bl native_fn_02067748
    mov r2, r0
    mov r0, #2
    mov r1, #1
    mov r3, #56
    bl native_fn_021df974
    mov r0, #15
    mov r1, #4
    mov r2, #17
    bl native_fn_021ded5c
    mov r0, #1
    bl native_fn_021def28
    mov r0, #63
    bl native_fn_021e00bc
    b L_021e2a20
L_021e29ec:
    mov r2, #2
    str r2, [sp]
    mov r3, #14
    mov r0, #5
    mov r1, r4
    str r3, [sp, #0x4]
    bl native_fn_021dea9c
    mov r0, #35
    bl native_fn_021e00bc
    b L_021e2a20
    bl native_fn_021dfd34
    cmp r0, #2
    moveq r4, #3
L_021e2a20:
    mov r0, r4
    add sp, sp, #8
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
    dcd 0x0000011d
    dcd 0x02216940
    dcd 0x00000ff7
    dcd 0xcccccccd
}
