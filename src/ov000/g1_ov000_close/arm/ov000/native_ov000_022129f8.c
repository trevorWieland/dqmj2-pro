/* ov000 row 0x022129f8: 296 bytes.
 *
 * What it does: 73 instructions; 13 call(s) to 0x02212804, 0x022127c4, 0x02212848, +10 more; loops (back edge at +0x14); returns through pop {r4, r5, r6, r7, r8, r9, r10, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x124 -> native_data_0222baf4 (image word 0x0222baf4)
 *   branch +0x1c -> +0x11c
 *   branch +0x40 -> +0x11c
 *   back edge +0x7c -> +0x4c
 *   back edge +0xb8 -> +0x88
 *   back edge +0x100 -> +0xd0
 *   test +0x18 cmp r0, #0
 *   test +0x3c cmp r0, #0
 *   test +0x74 cmp r6, #4
 *   test +0xb0 cmp r7, #4
 *   test +0xf8 cmp r9, #4
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022129f8; the literal pool and
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

extern void native_fn_02212804(void);
extern void native_fn_022127c4(void);
extern u8 native_data_0222baf4[];
extern void native_fn_02212848(void);
extern void native_fn_021dfb6c(void);
extern void native_fn_022128e4(void);
extern void native_fn_021dfc3c(void);
extern void native_fn_02212940(void);
extern void native_fn_021dfcd8(void);
extern void native_fn_0221299c(void);
extern void native_fn_021df950(void);


asm u32 native_ov000_022129f8 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, lr}
    mov r10, r0
    mov r0, r10, lsl #16
    mov r0, r0, asr #16
    mov r4, #0
    bl native_fn_02212804
    cmp r0, #0
    bne ov000_022129f8_L11c
    bl native_fn_022127c4
    ldr r1, =native_data_0222baf4
    mov r2, r10, lsl #1
    ldrsh r5, [r1, r2]
    mov r8, r0
    mov r1, r5
    bl native_fn_02212848
    cmp r0, #0
    beq ov000_022129f8_L11c
    add r7, r8, #92
    mov r6, r4
ov000_022129f8_L4c:
    mov r0, r5
    mov r1, r6
    bl native_fn_021dfb6c
    mov r4, r0
    mov r0, r7
    mov r1, r4
    bl native_fn_022128e4
    add r0, r8, r6, lsl #4
    add r6, r6, #1
    str r4, [r0, #0x5c]
    cmp r6, #4
    add r7, r7, #16
    blt ov000_022129f8_L4c
    add r6, r8, #156
    mov r7, #0
ov000_022129f8_L88:
    mov r0, r5
    mov r1, r7
    bl native_fn_021dfc3c
    mov r4, r0
    mov r0, r6
    mov r1, r4
    bl native_fn_02212940
    add r0, r8, r7, lsl #3
    add r7, r7, #1
    str r4, [r0, #0x9c]
    cmp r7, #4
    add r6, r6, #8
    blt ov000_022129f8_L88
    ldr r0, =native_data_0222baf4
    mov r1, r10, lsl #1
    ldrsh r7, [r0, r1]
    add r6, r8, #188
    mov r9, #0
ov000_022129f8_Ld0:
    mov r0, r7
    mov r1, r9
    bl native_fn_021dfcd8
    mov r4, r0
    mov r0, r6
    mov r1, r4
    bl native_fn_0221299c
    add r0, r8, r9, lsl #3
    add r9, r9, #1
    str r4, [r0, #0xbc]
    cmp r9, #4
    add r6, r6, #8
    blt ov000_022129f8_Ld0
    mov r0, #1
    strb r0, [r8, #0xdc]
    mov r0, r5
    strb r10, [r8, #0xdd]
    bl native_fn_021df950
    mov r4, #1
ov000_022129f8_L11c:
    mov r0, r4
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
}
