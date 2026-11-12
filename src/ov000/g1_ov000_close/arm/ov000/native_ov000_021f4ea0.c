/* ov000 row 0x021f4ea0: 584 bytes.
 *
 * What it does: 143 instructions; 31 call(s) to 0x02061944, 0x0206ea80, 0x020624c0, +28 more; loops (back edge at +0x08); returns through pop {r4, r5, r6, r7, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x23c -> constant 0x02236ee4 (image word 0x02236ee4)
 *   pool +0x240 -> native_data_0222eef0 (image word 0x0222eef0)
 *   pool +0x244 -> native_data_0222b986 (image word 0x0222b986)
 *   branch +0x40 -> +0x120
 *   branch +0x48 -> +0x164
 *   branch +0x50 -> +0x220
 *   branch +0x60 -> +0x120
 *   branch +0x70 -> +0x120
 *   back edge +0xb4 -> +0x8c
 *   branch +0x11c -> +0x220
 *   branch +0x12c -> +0x140
 *   branch +0x16c -> +0x220
 *   branch +0x178 -> +0x1b4
 *   branch +0x1c8 -> +0x204
 *   branch +0x214 -> +0x220
 *   test +0x3c cmp r1, #0
 *   test +0x44 cmp r1, #1
 *   test +0x4c cmp r1, #2
 *   test +0x5c cmp r0, #0
 *   test +0x6c cmp r0, #0
 *   test +0xb0 cmp r7, #12
 *   test +0x128 cmp r0, #19
 *   test +0x168 cmp r0, #0
 *   test +0x174 cmp r0, #0
 *   test +0x1f0 cmp r5, #1
 *   test +0x210 cmp r0, r1
 *   test +0x228 cmp r0, #42
 *   0 block transfer(s), 10 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f4ea0; the literal pool and
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

extern void native_fn_02061944(void);
extern void native_fn_0206ea80(void);
extern void native_fn_020624c0(void);
extern u8 native_data_0222eef0[];
extern void native_fn_020622ec(void);
extern u8 native_data_0222b986[];
extern void native_fn_02065d28(void);
extern void native_fn_02061250(void);
extern void native_fn_02045dc4(void);
extern void native_fn_02223d88(void);
extern void native_fn_02223e70(void);
extern void native_fn_0206dcd0(void);
extern void native_fn_0206de8c(void);
extern void native_fn_021f5308(void);
extern void native_fn_021f520c(void);
extern void native_fn_021f51d4(void);
extern void native_fn_0205fd60(void);
extern void native_fn_02062328(void);
extern void native_fn_02062144(void);
extern void native_fn_0206e214(void);
extern void native_fn_021f55b0(void);
extern void native_fn_021f53c0(void);
extern void native_fn_0206238c(void);
extern void native_fn_020620b4(void);
extern void native_fn_0206e1d8(void);
extern void native_fn_020624b0(void);
extern void native_fn_02062358(void);


asm u32 native_ov000_021f4ea0 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, lr}
    sub sp, sp, #12
    bl native_fn_02061944
    mov r4, r0
    bl native_fn_0206ea80
    add r1, r4, #512
    ldrsb r1, [r1, #105]
    mov r5, r0
    mov r0, #19
    strb r1, [sp, #0x8]
    mov r6, #0
    bl native_fn_020624c0
    add r1, r4, #512
    ldrsb r1, [r1, #106]
    mov r7, r0
    cmp r1, #0
    beq ov000_021f4ea0_L120
    cmp r1, #1
    beq ov000_021f4ea0_L164
    cmp r1, #2
    bne ov000_021f4ea0_L220
    ldr r0, =0x02236ee4
    ldrsb r0, [r0]
    cmp r0, #0
    beq ov000_021f4ea0_L120
    ldr r0, =native_data_0222eef0
    ldrsb r0, [r0]
    cmp r0, #0
    bne ov000_021f4ea0_L120
    mov r0, #6
    mov r1, #12
    mov r2, r6
    bl native_fn_020622ec
    ldr r5, =native_data_0222b986
    mov r7, r6
ov000_021f4ea0_L8c:
    mov r0, r7, lsl #1
    ldrsb r0, [r5, r0]
    bl native_fn_02065d28
    add r1, r7, #1
    ldr r2, [r4, #0x25c]
    mov r1, r1, lsl #24
    sub r0, r2, r0
    mov r7, r1, asr #24
    str r0, [r4, #0x25c]
    cmp r7, #12
    blt ov000_021f4ea0_L8c
    mov r0, #0
    bl native_fn_02061250
    mov r2, #5
    mov r1, r0
    str r2, [sp]
    mov r5, #15
    mov r0, #0
    mov r2, #1
    mov r3, #8
    str r5, [sp, #0x4]
    bl native_fn_02045dc4
    mov r0, #1
    bl native_fn_02061250
    mov r1, r0
    mov r0, #5
    str r0, [sp]
    mov r0, r5
    str r0, [sp, #0x4]
    mov r0, #0
    mov r2, #1
    mov r3, #8
    bl native_fn_02045dc4
    ldr r0, =native_data_0222eef0
    mov r1, #1
    strb r1, [r0]
    b ov000_021f4ea0_L220
ov000_021f4ea0_L120:
    add r0, r4, #512
    ldrsb r0, [r0, #109]
    cmp r0, #19
    beq ov000_021f4ea0_L140
    bl native_fn_02223d88
    bl native_fn_02223e70
    mov r0, #0
    bl native_fn_0206dcd0
ov000_021f4ea0_L140:
    bl native_fn_0206de8c
    bl native_fn_021f5308
    bl native_fn_021f520c
    mov r0, #1
    strb r0, [r4, #0x26a]
    bl native_fn_021f51d4
    ldr r0, =0x02236ee4
    mov r1, #1
    strb r1, [r0]
ov000_021f4ea0_L164:
    bl native_fn_0205fd60
    cmp r0, #0
    bne ov000_021f4ea0_L220
    ldrsb r0, [r5, #12]
    cmp r0, #0
    beq ov000_021f4ea0_L1b4
    bl native_fn_02062328
    add r0, r4, #512
    ldrsb r0, [r0, #111]
    mov r1, #0
    bl native_fn_02062144
    bl native_fn_0206e214
    bl native_fn_021f55b0
    bl native_fn_021f53c0
    bl native_fn_02223d88
    mov r0, #0
    bl native_fn_021f51d4
    ldr r0, =native_data_0222eef0
    mvn r1, #0
    strb r1, [r0]
ov000_021f4ea0_L1b4:
    mov r1, #19
    add r0, sp, #8
    mov r2, r1
    bl native_fn_0206238c
    movs r5, r0
    beq ov000_021f4ea0_L204
    ldrsb r0, [sp, #8]
    bl native_fn_020620b4
    bl native_fn_0206e1d8
    add r0, r7, #1
    and r0, r0, #1
    mov r0, r0, lsl #24
    mov r1, r0, asr #24
    mov r0, #19
    bl native_fn_020624b0
    cmp r5, #1
    movne r5, #0
    mov r0, r5
    bl native_fn_02062358
    mov r6, #1
ov000_021f4ea0_L204:
    add r1, r4, #512
    ldrsb r0, [sp, #8]
    ldrsb r1, [r1, #105]
    cmp r0, r1
    beq ov000_021f4ea0_L220
    bl native_fn_020620b4
    mov r6, #1
ov000_021f4ea0_L220:
    add r0, r4, #512
    ldrsb r0, [r0, #108]
    cmp r0, #42
    movne r6, #1
    mov r0, r6
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, pc}
}
