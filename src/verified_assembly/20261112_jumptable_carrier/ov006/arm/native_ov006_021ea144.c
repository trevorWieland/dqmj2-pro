/* ov006 row 0x021ea144: 360 bytes.
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

extern void native_fn_02062328(void);
extern void native_fn_020406a8(void);
extern void native_fn_02041510(void);
extern void native_fn_020418e8(void);
extern void native_fn_020414b0(void);
extern void native_fn_02041800(void);
extern void native_fn_0206dec8(void);
extern void native_fn_0206157c(void);
extern void native_fn_0204bb18(void);
extern void native_fn_0204bb08(void);
extern void native_fn_0204bb28(void);
extern void native_fn_020bb3f4(void);
extern void native_fn_0204617c(void);
extern void native_fn_02084920(void);
extern void native_fn_021e69a4(void);
extern void native_fn_021e6c44(void);
extern void native_fn_020ba574(void);
extern void native_fn_021e7fe0(void);
extern void native_fn_021e7ff0(void);
extern void native_fn_021ebb08(void);


asm u32 native_ov006_021ea144 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r0, [pc, #0x158]
    ldr r0, [r0, #0x8]
    cmp r0, #7
    addls pc, pc, r0, lsl #2
    b L_021ea2a0
    dcd 0xea000006
    dcd 0xea000015
    dcd 0xea00001b
    dcd 0xea00001f
    dcd 0xea00002c
    dcd 0xea000030
    dcd 0xea000037
    dcd 0xea000041
    bl native_fn_02062328
    mov r0, #0
    bl native_fn_020406a8
    mov r0, #1
    mov r1, #2
    mov r2, #5
    bl native_fn_02041510
    mov r0, #5
    mov r1, #10
    bl native_fn_020418e8
    mov r0, #63
    bl native_fn_020414b0
    ldr r0, [pc, #0xf4]
    mov r1, #1
    str r1, [r0, #0x8]
    b L_021ea2a0
    bl native_fn_02041800
    cmp r0, #1
    beq L_021ea2a0
    ldr r0, [pc, #0xd8]
    mov r1, #2
    str r1, [r0, #0x8]
    b L_021ea2a0
    bl native_fn_0206dec8
    ldr r0, [pc, #0xc4]
    mov r1, #3
    str r1, [r0, #0x8]
    b L_021ea2a0
    bl native_fn_0206157c
    cmp r0, #0
    beq L_021ea2a0
    bl native_fn_0204bb18
    cmp r0, #0
    bne L_021ea214
    mov r0, #1
    bl native_fn_0204bb08
    mov r0, #0
    bl native_fn_0204bb28
L_021ea214:
    ldr r0, [pc, #0x8c]
    mov r1, #4
    str r1, [r0, #0x8]
    b L_021ea2a0
    bl native_fn_020bb3f4
    ldr r0, [pc, #0x78]
    mov r1, #5
    str r1, [r0, #0x8]
    b L_021ea2a0
    mov r0, #0
    mov r1, #2
    bl native_fn_0204617c
    bl native_fn_02084920
    ldr r0, [pc, #0x58]
    mov r1, #6
    str r1, [r0, #0x8]
    b L_021ea2a0
    bl native_fn_021e69a4
    bl native_fn_021e6c44
    bl native_fn_020ba574
    cmp r0, #0
    blt L_021ea274
    bl native_fn_021e7fe0
    b L_021ea278
L_021ea274:
    bl native_fn_021e7ff0
L_021ea278:
    ldr r0, [pc, #0x28]
    mov r1, #7
    str r1, [r0, #0x8]
    mov r0, #0
    bl native_fn_021ebb08
    ldr r0, [pc, #0x14]
    mov r1, #0
    str r1, [r0, #0x8]
    mov r0, #1
    ldmia sp!, {r3, pc}
L_021ea2a0:
    mov r0, #0
    ldmia sp!, {r3, pc}
    dcd 0x02219290
}
