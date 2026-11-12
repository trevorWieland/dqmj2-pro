/* ov000 row 0x022270c0: 260 bytes.
 *
 * What it does: 63 instructions; 21 call(s) to 0x02227044, 0x02041814, 0x0205fd60, +18 more; loops (back edge at +0x20); returns through pop {r3, r4, r5, r6, r7, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xfc -> constant 0x022468b8 (image word 0x022468b8)
 *   pool +0x100 -> native_data_0222feb4 (image word 0x0222feb4)
 *   branch +0x4c -> +0x64
 *   branch +0x54 -> +0x78
 *   branch +0x5c -> +0x98
 *   branch +0x60 -> +0xb0
 *   branch +0x74 -> +0xb0
 *   branch +0x94 -> +0xb0
 *   branch +0xb8 -> +0xd8
 *   branch +0xc0 -> +0xd0
 *   branch +0xcc -> +0xe0
 *   branch +0xd4 -> +0xe0
 *   test +0x28 cmp r0, #1
 *   test +0x38 cmp r0, #0
 *   test +0x48 cmp r0, #1
 *   test +0x50 cmp r0, #3
 *   test +0x58 cmp r0, #4
 *   test +0xb4 cmp r0, #1
 *   test +0xbc cmp r0, #3
 *   test +0xc4 cmp r0, #4
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022270c0; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity fixes the instruction stream, not the field, block and callee semantics behind the addresses and strides it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_0222feb4[];
extern void native_fn_02227044(void);
extern void native_fn_02041814(void);
extern void native_fn_0205fd60(void);
extern void native_fn_021f34ac(void);
extern void native_fn_02227698(void);
extern void native_fn_01ffac28(void);
extern void native_fn_020c0210(void);
extern void native_fn_020c013c(void);
extern void native_fn_020693e0(void);
extern void native_fn_020c49e8(void);
extern void native_fn_020cab38(void);
extern void native_fn_020c9780(void);
extern void native_fn_020c5e88(void);
extern void native_fn_020c9830(void);
extern void native_fn_02048f6c(void);
extern void native_fn_02045680(void);
extern void native_fn_01ffa988(void);
extern void native_fn_02227648(void);
extern void native_fn_02224ee4(void);


asm u32 native_ov000_022270c0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    ldr r0, =0x022468b8
    ldr r7, =native_data_0222feb4
    ldrsb r1, [r0, #24]
    ldrsb r0, [r0, #26]
    mov r4, #0
    add r6, r1, r1, lsl #2
    add r5, r0, r0, lsl #2
    bl native_fn_02227044
    bl native_fn_02041814
    cmp r0, #1
    moveq r0, r4
    ldmeqia sp!, {r3, r4, r5, r6, r7, pc}
    bl native_fn_0205fd60
    cmp r0, #0
    movne r0, r4
    ldmneia sp!, {r3, r4, r5, r6, r7, pc}
    ldrsb r0, [r7, r6]
    cmp r0, #1
    beq ov000_022270c0_L64
    cmp r0, #3
    beq ov000_022270c0_L78
    cmp r0, #4
    beq ov000_022270c0_L98
    b ov000_022270c0_Lb0
ov000_022270c0_L64:
    mov r0, #2
    bl native_fn_021f34ac
    bl native_fn_02227698
    bl native_fn_01ffac28
    b ov000_022270c0_Lb0
ov000_022270c0_L78:
    bl native_fn_020c0210
    bl native_fn_020c013c
    bl native_fn_020693e0
    bl native_fn_020c49e8
    bl native_fn_020cab38
    bl native_fn_020c9780
    bl native_fn_020c5e88
    b ov000_022270c0_Lb0
ov000_022270c0_L98:
    bl native_fn_020693e0
    bl native_fn_020c9830
    bl native_fn_020c5e88
    mov r0, #1
    bl native_fn_02048f6c
    bl native_fn_02045680
ov000_022270c0_Lb0:
    ldrsb r0, [r7, r5]
    cmp r0, #1
    beq ov000_022270c0_Ld8
    cmp r0, #3
    beq ov000_022270c0_Ld0
    cmp r0, #4
    moveq r4, #2
    b ov000_022270c0_Le0
ov000_022270c0_Ld0:
    mov r4, #1
    b ov000_022270c0_Le0
ov000_022270c0_Ld8:
    bl native_fn_01ffa988
    bl native_fn_02227648
ov000_022270c0_Le0:
    mov r0, r4
    bl native_fn_02224ee4
    ldr r0, =0x022468b8
    mov r1, #5
    str r1, [r0, #0x14]
    mov r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
