/* ov000 row 0x0221c0c4: 1004 bytes.
 *
 * What it does: 247 instructions and 55 call(s), then a 12-entry dispatch through an inline branch table at 0x0221c0e4 (dispatch word at 0x0221c0dc)
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

extern void native_fn_02221344(void);
extern void native_fn_02061944(void);
extern void native_fn_020620b4(void);
extern void native_fn_02062358(void);
extern void native_fn_02062a10(void);
extern void native_fn_021ead88(void);
extern void native_fn_0206dcd0(void);
extern void native_fn_02221358(void);
extern void native_fn_020620e8(void);
extern void native_fn_0222131c(void);
extern void native_fn_0207a2d0(void);
extern void native_fn_0221c0ac(void);
extern void native_fn_022213d8(void);
extern void native_fn_0221f6e8(void);
extern void native_fn_0207cd98(void);
extern void native_fn_0221befc(void);
extern void native_fn_0206be2c(void);
extern void native_fn_0206bf34(void);
extern void native_fn_020c1864(void);
extern void native_fn_020c1874(void);


asm u32 native_ov000_0221c0c4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    ldr r0, [pc, #0x3d0]
    ldr r1, [pc, #0x3d0]
    ldrsb r2, [r0, #16]
    ldr r4, [r1, #0x10]
    cmp r2, #11
    addls pc, pc, r2, lsl #2
    ldmia sp!, {r3, r4, r5, pc}
    dcd 0xe8bd8038
    dcd 0xea000009
    dcd 0xea0000bc
    dcd 0xe8bd8038
    dcd 0xe8bd8038
    dcd 0xe8bd8038
    dcd 0xea0000c4
    dcd 0xea0000c3
    dcd 0xe8bd8038
    dcd 0xe8bd8038
    dcd 0xea0000cf
    dcd 0xe8bd8038
    ldr r2, [r0]
    cmp r2, #0
    bne L_0221c1b0
    bl native_fn_02221344
    ldr r1, [pc, #0x378]
    str r0, [r1, #0x10]
    bl native_fn_02061944
    add r0, r0, #512
    ldrsb r0, [r0, #105]
    cmp r0, #8
    bne L_0221c164
    bl native_fn_02061944
    add r0, r0, #512
    ldrsb r0, [r0, #108]
    cmp r0, #1
    beq L_0221c164
    mov r0, #1
    bl native_fn_020620b4
    mov r0, #1
    bl native_fn_02062358
L_0221c164:
    ldr r0, [pc, #0x338]
    ldr r0, [r0, #0x10]
    bl native_fn_02062a10
    movs r5, r0
    beq L_0221c188
    ldrsh r0, [r5, #24]
    ldrb r1, [r5, #0x1a]
    bl native_fn_021ead88
    b L_0221c194
L_0221c188:
    mov r0, #0
    mov r1, r0
    bl native_fn_021ead88
L_0221c194:
    ldr r0, [pc, #0x308]
    ldr r0, [r0, #0x10]
    cmp r4, r0
    beq L_0221c3d4
    mov r0, r5
    bl native_fn_0206dcd0
    b L_0221c3d4
L_0221c1b0:
    cmp r2, #1
    bne L_0221c248
    bl native_fn_02221358
    ldr r1, [pc, #0x2e0]
    str r0, [r1, #0x10]
    bl native_fn_02061944
    add r0, r0, #512
    ldrsb r0, [r0, #105]
    cmp r0, #8
    bne L_0221c1fc
    bl native_fn_02061944
    add r0, r0, #512
    ldrsb r0, [r0, #108]
    cmp r0, #1
    beq L_0221c1fc
    mov r0, #1
    bl native_fn_020620b4
    mov r0, #1
    bl native_fn_02062358
L_0221c1fc:
    ldr r0, [pc, #0x2a0]
    ldr r0, [r0, #0x10]
    bl native_fn_02062a10
    movs r5, r0
    beq L_0221c220
    ldrsh r0, [r5, #24]
    ldrb r1, [r5, #0x1a]
    bl native_fn_021ead88
    b L_0221c22c
L_0221c220:
    mov r0, #0
    mov r1, r0
    bl native_fn_021ead88
L_0221c22c:
    ldr r0, [pc, #0x270]
    ldr r0, [r0, #0x10]
    cmp r4, r0
    beq L_0221c3d4
    mov r0, r5
    bl native_fn_0206dcd0
    b L_0221c3d4
L_0221c248:
    cmp r2, #2
    bne L_0221c2b4
    ldr r0, [r1, #0x20]
    cmp r0, #0
    beq L_0221c2b4
    bl native_fn_02061944
    add r0, r0, #512
    ldrsb r0, [r0, #105]
    cmp r0, #8
    bne L_0221c290
    bl native_fn_02061944
    add r0, r0, #512
    ldrsb r0, [r0, #108]
    cmp r0, #1
    beq L_0221c290
    mov r0, #1
    mov r1, r0
    bl native_fn_020620e8
L_0221c290:
    mov r0, #0
    mov r1, r0
    bl native_fn_021ead88
    mov r0, #0
    bl native_fn_0206dcd0
    ldr r0, [pc, #0x1f8]
    mov r1, #0
    str r1, [r0, #0x10]
    b L_0221c3d4
L_0221c2b4:
    cmp r2, #2
    blt L_0221c344
    ldr r0, [pc, #0x1e0]
    ldr r0, [r0, #0x20]
    cmp r0, #0
    bne L_0221c344
    bl native_fn_02061944
    add r0, r0, #512
    ldrsb r0, [r0, #105]
    cmp r0, #8
    beq L_0221c300
    bl native_fn_02061944
    add r0, r0, #512
    ldrsb r0, [r0, #108]
    cmp r0, #8
    beq L_0221c300
    mov r0, #8
    mov r1, #1
    bl native_fn_020620e8
L_0221c300:
    ldr r0, [pc, #0x198]
    ldr r3, [pc, #0x198]
    ldr r0, [r0]
    ldr r1, [pc, #0x194]
    mov r4, #0
    ldr r2, [pc, #0x190]
    sub r0, r0, #2
    str r4, [r3, #0x10]
    bl native_fn_0222131c
    mov r0, r4
    mov r1, r0
    bl native_fn_021ead88
    ldr r1, [pc, #0x16c]
    ldrsh r0, [r1, #8]
    ldrb r1, [r1, #0x1]
    bl native_fn_0207a2d0
    b L_0221c3d4
L_0221c344:
    cmp r2, #3
    blt L_0221c3d4
    ldr r0, [pc, #0x150]
    ldr r0, [r0, #0x20]
    cmp r0, #0
    beq L_0221c3d4
    bl native_fn_02061944
    add r0, r0, #512
    ldrsb r0, [r0, #105]
    cmp r0, #8
    beq L_0221c394
    bl native_fn_02061944
    add r0, r0, #512
    ldrsb r0, [r0, #108]
    cmp r0, #8
    beq L_0221c394
    mov r0, #8
    bl native_fn_020620b4
    mov r0, #1
    bl native_fn_02062358
L_0221c394:
    ldr r0, [pc, #0x104]
    ldr r3, [pc, #0x104]
    ldr r0, [r0]
    ldr r1, [pc, #0x100]
    mov r4, #0
    ldr r2, [pc, #0xfc]
    sub r0, r0, #3
    str r4, [r3, #0x10]
    bl native_fn_0222131c
    mov r0, r4
    mov r1, r0
    bl native_fn_021ead88
    ldr r1, [pc, #0xd8]
    ldrsh r0, [r1, #8]
    ldrb r1, [r1, #0x1]
    bl native_fn_0207a2d0
L_0221c3d4:
    ldr r0, [pc, #0xc8]
    ldr r0, [r0, #0x10]
    bl native_fn_0221c0ac
    ldmia sp!, {r3, r4, r5, pc}
    bl native_fn_022213d8
    ldr r2, [pc, #0xb0]
    mov r1, r0
    ldr r0, [r2]
    bl native_fn_0221f6e8
    bl native_fn_0207cd98
    mov r1, #0
    mov r4, r0
    bl native_fn_0221befc
    ldr r0, [pc, #0x94]
    str r4, [r0, #0x10]
    ldmia sp!, {r3, r4, r5, pc}
    ldr r0, [r1, #0xc]
    str r0, [r1, #0x10]
    cmp r4, r0
    ldmeqia sp!, {r3, r4, r5, pc}
    bl native_fn_02062a10
    mov r4, r0
    ldrsh r0, [r4, #24]
    ldrb r1, [r4, #0x1a]
    bl native_fn_021ead88
    mov r0, r4
    bl native_fn_0206dcd0
    ldr r0, [pc, #0x5c]
    ldr r0, [r0, #0x10]
    bl native_fn_0221c0ac
    ldmia sp!, {r3, r4, r5, pc}
    bl native_fn_0206be2c
    bl native_fn_0206bf34
    mov r1, #1
    mov r4, r0
    bl native_fn_0221befc
    cmp r0, #0
    beq L_0221c47c
    ldr r1, [pc, #0x30]
    mov r0, r4
    str r4, [r1, #0x10]
    bl native_fn_02062a10
L_0221c47c:
    bl native_fn_020c1864
    cmp r0, #0
    ldmeqia sp!, {r3, r4, r5, pc}
    ldr r0, [pc, #0x14]
    ldr r0, [r0, #0x2c]
    bl native_fn_02062a10
    bl native_fn_0206dcd0
    bl native_fn_020c1874
    ldmia sp!, {r3, r4, r5, pc}
    dcd 0x022460d4
    dcd 0x02246090
    dcd 0x02246098
    dcd 0x02246091
}
