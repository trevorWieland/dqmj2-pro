/* ov006 row 0x021daaf0: 456 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x1b0 -> native_data_0220cdac (image word 0x0220cdac)
 *   pool +0x1b4 -> native_data_0220cdc0 (image word 0x0220cdc0)
 *   pool +0x1b8 -> native_data3_0220f358 (image word 0x0220f358)
 *   pool +0x1bc -> native_data_02207920 (image word 0x02207920)
 *   pool +0x1c0 -> constant 0x0220f34c (image word 0x0220f34c)
 *   pool +0x1c4 -> native_data_0220cb94 (image word 0x0220cb94)
 *   back edge +0xb0 -> +0x78
 *   branch +0xc4 -> +0x1a4
 *   branch +0x104 -> +0x184
 *   branch +0x130 -> +0x168
 *   back edge +0x180 -> +0x108
 *   back edge +0x1a0 -> +0xcc
 *   test +0xa4 cmp r8, #8
 *   test +0xc0 cmp r0, #0
 *   test +0x12c cmp r4, #0
 *   test +0x170 cmp r8, r0, asr #24
 *   test +0x19c cmp r0, r4, asr #24
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021daaf0; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity proves the instruction stream, not the meaning of the fields, blocks and callee contracts it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_0220cdac[];
extern void native_fn_0203cc2c(void);
extern void native_fn_0204518c(void);
extern void native_fn_020481b8(void);
extern void native_fn_0202a498(void);
extern void native_fn_02048308(void);
extern u8 native_data_0220cdc0[];
extern void native_fn_0201d444(void);
extern void native_fn_0205ff80(void);
extern u8 native_data3_0220f358[];
extern u8 native_data_02207920[];
extern void native_fn_02065730(void);
extern void native_fn_0205ff9c(void);
extern void native_fn_02062aa0(void);
extern void native_fn_02062a50(void);
extern void native_fn_02061de4(void);
extern void native_fn_02065818(void);
extern u8 native_data_0220cb94[];
extern void native_fn_021dacb8(void);


asm u32 native_ov006_021daaf0 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #44
    ldr r0, =native_data_0220cdac
    mov r6, #0
    mov r1, #2
    mov r7, r6
    mov r9, #64
    bl native_fn_0203cc2c
    mov r4, r0
    add r0, sp, #4
    mov r1, r4
    mov r2, #17
    bl native_fn_0204518c
    ldr r0, [sp, #0x4]
    mov r1, #352
    mov r2, #32
    bl native_fn_020481b8
    mov r1, r4
    mov r0, #2
    bl native_fn_0202a498
    bl native_fn_02048308
    ldr r1, =native_data_0220cdc0
    add r0, sp, #12
    bl native_fn_0201d444
    add r0, sp, #12
    bl native_fn_0205ff80
    ldr r10, =native_data3_0220f358
    ldr r5, =native_data_02207920
    mov r8, r6
    mov r4, r6
ov006_021daaf0_L78:
    str r9, [sp]
    mov r1, r8, lsl #1
    add r0, r5, r8, lsl #1
    ldrsb r1, [r5, r1]
    ldrb r3, [r0, #0x1]
    mov r0, r10
    mov r2, r4
    bl native_fn_02065730
    add r1, r8, #1
    mov r1, r1, lsl #24
    mov r8, r1, asr #24
    cmp r8, #8
    add r9, r9, r0
    add r10, r10, #12
    blt ov006_021daaf0_L78
    bl native_fn_0205ff9c
    mov r11, #0
    bl native_fn_02062aa0
    cmp r0, #0
    ble ov006_021daaf0_L1a4
    ldr r10, =native_data3_0220f358
ov006_021daaf0_Lcc:
    mov r0, r11
    bl native_fn_02062a50
    mov r1, #0
    mov r9, r0
    str r1, [sp]
    ldrsh r1, [r9, #24]
    mov r0, r10
    mov r2, r6
    mov r3, #1
    bl native_fn_02061de4
    movs r8, r0
    ldr r0, =0x0220f34c
    mov r4, #0
    str r8, [r0, r11, lsl #2]
    bmi ov006_021daaf0_L184
ov006_021daaf0_L108:
    add r0, r7, r4
    add r0, r0, r0, lsl #2
    add r0, r0, #8
    mov r0, r0, lsl #24
    mov r5, r0, asr #24
    mov r0, r10
    mov r1, #3
    mov r2, r5
    bl native_fn_02065818
    cmp r4, #0
    bne ov006_021daaf0_L168
    ldrb r0, [r9, #0x32]
    add r2, r5, #2
    mov r3, #12
    add r5, r0, #3
    ldr r0, =native_data3_0220f358
    mov r1, #9
    mla r0, r5, r3, r0
    ldr r3, =native_data_0220cb94
    ldrsb r3, [r3, r8]
    add r2, r2, r3
    mov r2, r2, lsl #24
    mov r2, r2, asr #24
    bl native_fn_02065818
ov006_021daaf0_L168:
    add r0, r4, #1
    mov r0, r0, lsl #24
    cmp r8, r0, asr #24
    add r10, r10, #12
    mov r4, r0, asr #24
    add r6, r6, #1
    bge ov006_021daaf0_L108
ov006_021daaf0_L184:
    add r0, r11, #1
    add r1, r8, #1
    mov r4, r0, lsl #24
    add r7, r7, r1
    mov r11, r4, asr #24
    bl native_fn_02062aa0
    cmp r0, r4, asr #24
    bgt ov006_021daaf0_Lcc
ov006_021daaf0_L1a4:
    bl native_fn_021dacb8
    add sp, sp, #44
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
