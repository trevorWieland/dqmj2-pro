/* ov000 row 0x021d7b64: 556 bytes.
 *
 * What it does: 134 instructions; 27 call(s) to 0x01ffa824, 0x01ffb4ec, 0x01ffa84c, +24 more; loops (back edge at +0x0c); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 5 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x218 -> native_data_0222e184 (image word 0x0222e184)
 *   pool +0x21c -> constant 0x02230170 (image word 0x02230170)
 *   pool +0x220 -> native_data_0222b7e4 (image word 0x0222b7e4)
 *   pool +0x224 -> native_data_0222b7df (image word 0x0222b7df)
 *   pool +0x228 -> native_data_0222b7e0 (image word 0x0222b7e0)
 *   back edge +0x88 -> +0x50
 *   branch +0xc0 -> +0x118
 *   back edge +0x134 -> +0xb8
 *   back edge +0x164 -> +0x144
 *   branch +0x198 -> +0x1f4
 *   back edge +0x20c -> +0x190
 *   test +0x7c cmp r6, #6
 *   test +0xbc cmp r1, #0
 *   test +0x124 cmp r10, #3
 *   test +0x14c cmp r0, #0
 *   test +0x160 cmp r3, #3
 *   test +0x194 cmp r1, #0
 *   test +0x200 cmp r10, #3
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021d7b64; the literal pool and
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

extern void native_fn_01ffa824(void);
extern void native_fn_01ffb4ec(void);
extern void native_fn_01ffa84c(void);
extern void native_fn_021d7e44(void);
extern u8 native_data_0222e184[];
extern void native_fn_0201d444(void);
extern void native_fn_0205ff80(void);
extern u8 native_data_0222b7e4[];
extern void native_fn_02065730(void);
extern void native_fn_0205ff9c(void);
extern void native_fn_02062aa0(void);
extern u8 native_data_0222b7df[];
extern void native_fn_02061de4(void);
extern void native_fn_02065818(void);
extern void native_fn_021d7e58(void);
extern void native_fn_020bedf0(void);
extern void native_fn_021d811c(void);
extern u8 native_data_0222b7e0[];
extern void native_fn_020bedfc(void);


asm u32 native_ov000_021d7b64 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #40
    mov r7, #64
    bl native_fn_01ffa824
    and r0, r0, #255
    bl native_fn_01ffb4ec
    mov r8, r0
    bl native_fn_01ffa84c
    bl native_fn_01ffb4ec
    str r0, [sp, #0x4]
    bl native_fn_021d7e44
    ldr r1, =native_data_0222e184
    add r0, sp, #8
    bl native_fn_0201d444
    add r0, sp, #8
    bl native_fn_0205ff80
    mov r6, #0
    ldr r9, =0x02230170
    ldr r5, =native_data_0222b7e4
    mov r4, r6
ov000_021d7b64_L50:
    str r7, [sp]
    mov r1, r6, lsl #1
    add r0, r5, r6, lsl #1
    ldrsb r1, [r5, r1]
    ldrb r3, [r0, #0x1]
    mov r0, r9
    mov r2, r4
    bl native_fn_02065730
    add r1, r6, #1
    mov r1, r1, lsl #24
    mov r6, r1, asr #24
    cmp r6, #6
    add r7, r7, r0
    add r9, r9, #12
    blt ov000_021d7b64_L50
    bl native_fn_0205ff9c
    bl native_fn_02062aa0
    bl native_fn_02062aa0
    ldr r1, =native_data_0222b7df
    add r6, r8, #20
    mov r10, #0
    mov r8, #1
    ldrsb r9, [r1, r0]
    ldr r7, =0x02230170
    mov r4, r8
    mov r11, r10
ov000_021d7b64_Lb8:
    ldrsh r1, [r6, #4]
    cmp r1, #0
    ble ov000_021d7b64_L118
    mov r0, r7
    mov r2, r10
    mov r3, r11
    str r4, [sp]
    bl native_fn_02061de4
    add r0, r9, r8
    mov r0, r0, lsl #24
    mov r5, r0, asr #24
    mov r0, r7
    mov r1, r5
    mov r2, #4
    bl native_fn_02065818
    mov r0, r5
    mov r1, #4
    mov r2, #1
    bl native_fn_021d7e58
    bl native_fn_020bedf0
    add r0, r0, r10, lsl #2
    ldr r1, [r0, #0x4]
    mov r0, #0
    bl native_fn_021d811c
ov000_021d7b64_L118:
    add r0, r10, #1
    mov r0, r0, lsl #24
    mov r10, r0, asr #24
    cmp r10, #3
    add r6, r6, #52
    add r7, r7, #12
    add r8, r8, #5
    blt ov000_021d7b64_Lb8
    mov r1, #0
    ldr r2, [sp, #0x4]
    mov r3, r1
ov000_021d7b64_L144:
    ldrsh r0, [r2, #24]
    add r2, r2, #52
    cmp r0, #0
    add r0, r3, #1
    mov r0, r0, lsl #24
    mov r3, r0, asr #24
    addgt r1, r1, #1
    cmp r3, #3
    blt ov000_021d7b64_L144
    ldr r0, =native_data_0222b7e0
    sub r1, r1, #1
    ldrsb r9, [r0, r1]
    ldr r0, [sp, #0x4]
    ldr r6, =0x02230170
    add r7, r0, #20
    mov r10, #0
    mov r8, #16
    mov r4, #1
    mov r11, #12
ov000_021d7b64_L190:
    ldrsh r1, [r7, #4]
    cmp r1, #0
    ble ov000_021d7b64_L1f4
    add r2, r10, #3
    mul r5, r2, r11
    add r0, r6, r5
    mov r3, #0
    str r4, [sp]
    bl native_fn_02061de4
    add r1, r9, r8
    mov r1, r1, lsl #24
    add r0, r6, r5
    mov r5, r1, asr #24
    mov r1, r5
    mov r2, #15
    bl native_fn_02065818
    mov r0, r5
    mov r1, #15
    mov r2, #2
    bl native_fn_021d7e58
    bl native_fn_020bedfc
    add r0, r0, r10, lsl #2
    ldr r1, [r0, #0x4]
    mov r0, #1
    bl native_fn_021d811c
ov000_021d7b64_L1f4:
    add r0, r10, #1
    mov r0, r0, lsl #24
    mov r10, r0, asr #24
    cmp r10, #3
    add r7, r7, #52
    add r8, r8, #5
    blt ov000_021d7b64_L190
    add sp, sp, #40
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
