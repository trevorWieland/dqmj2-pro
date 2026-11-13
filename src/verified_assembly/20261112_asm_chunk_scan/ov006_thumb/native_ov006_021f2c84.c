/* ov006 row 0x021f2c84: 616 bytes.
 *
 * What it does: Writes one block of 4 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x24c -> native_data_0221c05c (image word 0x0221c05c)
 *   pool +0x250 -> constant 0xc1fffcff (image word 0xc1fffcff)
 *   pool +0x254 -> constant 0xfffff3ff (image word 0xfffff3ff)
 *   pool +0x258 -> native_data_0220b164 (image word 0x0220b164)
 *   pool +0x25c -> native_data_0220b15c (image word 0x0220b15c)
 *   pool +0x260 -> native_data_0220d79c (image word 0x0220d79c)
 *   pool +0x264 -> native_fn_021f2f60+1 (image word 0x021f2f61)
 *   back edge +0x88 -> +0x50
 *   back edge +0xd6 -> +0x92
 *   back edge +0x122 -> +0xe0
 *   back edge +0x1a0 -> +0x16a
 *   branch +0x1a6 -> +0x1c0
 *   back edge +0x1d4 -> +0x13c
 *   back edge +0x1ea -> +0x132
 *   test +0x86 cmp r4, #0x2f
 *   test +0xd4 cmp r6, #0x4
 *   test +0x120 cmp r6, #0x2
 *   test +0x19e cmp r4, #0xc
 *   test +0x1a4 cmp r0, #0x0
 *   test +0x1d2 cmp r0, #0x4
 *   test +0x1e8 cmp r0, #0x3
 *   44 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f2c84; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void ov006_clear_buffer_02203c08(void);
extern u8 native_data9_0221c05c[];
extern void native_fn_0220303c(void);
extern u8 native_data_0220b164[];
extern u8 native_data_0220b15c[];
extern void native_fn_02203058(void);
extern void native_fn_02202dcc(void);
extern void native_fn_02202f54(void);
extern u8 native_data_0220d79c[];
extern void native_fn_0220342c(void);
extern void native_fn_022037c0(void);
extern void native_fn_02202c5c(void);
extern void native_fn_021f2f60(void);
extern void native_fn_0220490c(void);
extern void native_fn_021f37f0(void);


asm u32 native_ov006_021f2c84 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x38
    add r1, sp, #0x30
    mov r0, #0x0
    strh r0, [r1, #0]
    strh r0, [r1, #0x2]
    strh r0, [r1, #0x4]
    strh r0, [r1, #0x6]
    mov r1, #0x11
    add r0, sp, #0x28
    strh r1, [r0, #0xc]
    mov r1, #0x12
    strh r1, [r0, #0xe]
    mov r0, #0x4a
    lsl r0, r0, #0x2
    mov r1, #0x4
    bl ov006_clear_buffer_02203c08
    ldr r6, =native_data9_0221c05c
    mov r1, #0xff
    add r2, r1, #0x0
    mov r4, #0x0
    mov r7, #0x3
    str r0, [r6, #0]
    add r2, #0x1d
    strb r1, [r0, r2]
    add r0, r1, #0x0
    ldr r2, [r6, #0]
    add r0, #0x22
    strb r4, [r2, r0]
    add r0, r1, #0x0
    ldr r2, [r6, #0]
    mov r3, #0x1
    add r0, #0x24
    strb r3, [r2, r0]
    ldr r0, [r6, #0]
    add r1, #0x25
    strb r3, [r0, r1]
    add r5, r4, #0x0
    lsl r7, r7, #0xa
ov006_021f2c84_L50:
    mov r0, #0x0
    mov r1, #0x34
    bl native_fn_0220303c
    ldr r1, [r6, #0]
    add r4, r4, #0x1
    add r1, r1, r5
    str r0, [r1, #0x30]
    ldr r0, [r6, #0]
    ldr r1, =0xc1fffcff
    add r0, r0, r5
    ldr r0, [r0, #0x30]
    ldr r2, [r0, #0]
    and r2, r1
    mov r1, #0x2
    lsl r1, r1, #0x8
    orr r1, r2
    str r1, [r0, #0]
    ldr r0, [r6, #0]
    ldr r1, =0xfffff3ff
    add r0, r0, r5
    ldr r0, [r0, #0x30]
    add r5, r5, #0x4
    ldrh r2, [r0, #0x4]
    and r1, r2
    orr r1, r7
    strh r1, [r0, #0x4]
    cmp r4, #0x2f
    blt ov006_021f2c84_L50
    mov r6, #0x0
    ldr r4, =native_data_0220b164
    ldr r7, =native_data9_0221c05c
    add r5, r6, #0x0
ov006_021f2c84_L92:
    ldrb r1, [r4, #0]
    mov r0, #0x0
    bl native_fn_0220303c
    ldr r1, [r7, #0]
    add r6, r6, #0x1
    add r1, r1, r5
    add r1, #0xec
    str r0, [r1, #0]
    ldr r0, [r7, #0]
    ldr r1, =0xc1fffcff
    add r0, r0, r5
    add r0, #0xec
    ldr r0, [r0, #0]
    add r4, r4, #0x1
    ldr r2, [r0, #0]
    and r2, r1
    mov r1, #0x2
    lsl r1, r1, #0x8
    orr r1, r2
    str r1, [r0, #0]
    ldr r0, [r7, #0]
    ldr r1, =0xfffff3ff
    add r0, r0, r5
    add r0, #0xec
    ldr r0, [r0, #0]
    add r5, r5, #0x4
    ldrh r2, [r0, #0x4]
    and r2, r1
    mov r1, #0x3
    lsl r1, r1, #0xa
    orr r1, r2
    strh r1, [r0, #0x4]
    cmp r6, #0x4
    blt ov006_021f2c84_L92
    mov r6, #0x0
    ldr r4, =native_data_0220b15c
    ldr r7, =native_data9_0221c05c
    add r5, r6, #0x0
ov006_021f2c84_Le0:
    ldrb r1, [r4, #0]
    mov r0, #0x0
    mov r2, #0x1
    bl native_fn_02203058
    ldr r1, [r7, #0]
    mov r2, #0x2
    add r1, r1, r5
    add r1, #0xfc
    str r0, [r1, #0]
    ldr r0, [r7, #0]
    mov r1, #0x0
    add r0, r0, r5
    add r0, #0xfc
    ldr r0, [r0, #0]
    mvn r1, r1
    lsl r2, r2, #0x8
    mov r3, #0x0
    bl native_fn_02202dcc
    ldr r0, [r7, #0]
    mov r1, #0x0
    add r0, r0, r5
    add r0, #0xfc
    ldr r0, [r0, #0]
    mvn r1, r1
    mov r2, #0x3
    bl native_fn_02202f54
    add r6, r6, #0x1
    add r4, r4, #0x1
    add r5, r5, #0x4
    cmp r6, #0x2
    blt ov006_021f2c84_Le0
    mov r0, #0x0
    add r1, sp, #0x28
    str r0, [sp, #0x10]
    strh r0, [r1, #0x2]
    str r0, [sp, #0x20]
    ldr r0, =native_data_0220d79c
    str r0, [sp, #0x1c]
ov006_021f2c84_L132:
    mov r0, #0x0
    str r0, [sp, #0x24]
    str r0, [sp, #0x18]
    str r0, [sp, #0x14]
    add r6, sp, #0x28
ov006_021f2c84_L13c:
    add r0, sp, #0x2c
    str r0, [sp, #0]
    mov r0, #0x0
    mov r1, #0x1c
    mov r2, #0x2
    add r3, r0, #0x0
    str r0, [sp, #0x4]
    bl native_fn_0220342c
    ldr r1, =native_data9_0221c05c
    mov r4, #0x0
    ldr r2, [r1, #0]
    ldr r1, [sp, #0x20]
    add r2, r1, r2
    ldr r1, [sp, #0x18]
    str r0, [r1, r2]
    add r0, r4, #0x0
    strh r0, [r6, #0x8]
    ldr r0, [sp, #0x14]
    ldr r1, [sp, #0x20]
    lsl r5, r0, #0x1
    ldr r0, [sp, #0x18]
    add r7, r1, r0
ov006_021f2c84_L16a:
    ldr r0, [sp, #0x1c]
    ldr r0, [r0, #0]
    ldrh r0, [r0, r5]
    strh r0, [r6, #0]
    ldrh r0, [r6, #0xe]
    str r0, [sp, #0]
    mov r0, #0x2
    str r0, [sp, #0x4]
    mov r0, #0x12
    lsl r0, r0, #0x6
    str r0, [sp, #0x8]
    add r0, sp, #0x28
    str r0, [sp, #0xc]
    ldr r0, =native_data9_0221c05c
    ldrh r1, [r6, #0x8]
    ldr r0, [r0, #0]
    ldrh r2, [r6, #0xa]
    ldrh r3, [r6, #0xc]
    ldr r0, [r7, r0]
    bl native_fn_022037c0
    ldrh r0, [r6, #0x8]
    add r4, r4, #0x1
    add r5, r5, #0x2
    add r0, #0x12
    strh r0, [r6, #0x8]
    cmp r4, #0xc
    blt ov006_021f2c84_L16a
    ldr r0, [sp, #0x10]
    cmp r0, #0x0
    bne ov006_021f2c84_L1c0
    ldr r1, [sp, #0x2c]
    mov r0, #0x0
    mov r2, #0x1
    bl native_fn_02202c5c
    ldr r1, =native_data9_0221c05c
    ldr r2, [r1, #0]
    ldr r1, [sp, #0x18]
    add r2, r2, r1
    mov r1, #0x41
    lsl r1, r1, #0x2
    str r0, [r2, r1]
ov006_021f2c84_L1c0:
    ldr r0, [sp, #0x18]
    add r0, r0, #0x4
    str r0, [sp, #0x18]
    ldr r0, [sp, #0x14]
    add r0, #0xc
    str r0, [sp, #0x14]
    ldr r0, [sp, #0x24]
    add r0, r0, #0x1
    str r0, [sp, #0x24]
    cmp r0, #0x4
    blt ov006_021f2c84_L13c
    ldr r0, [sp, #0x20]
    add r0, #0x10
    str r0, [sp, #0x20]
    ldr r0, [sp, #0x1c]
    add r0, r0, #0x4
    str r0, [sp, #0x1c]
    ldr r0, [sp, #0x10]
    add r0, r0, #0x1
    str r0, [sp, #0x10]
    cmp r0, #0x3
    blt ov006_021f2c84_L132
    mov r0, #0x0
    mov r1, #0x40
    mov r2, #0x1
    bl native_fn_02203058
    ldr r1, =native_data9_0221c05c
    mov r2, #0x45
    ldr r3, [r1, #0]
    lsl r2, r2, #0x2
    str r0, [r3, r2]
    ldr r0, [r1, #0]
    mov r1, #0x0
    ldr r0, [r0, r2]
    mvn r1, r1
    add r2, #0xec
    mov r3, #0x0
    bl native_fn_02202dcc
    ldr r0, =native_data9_0221c05c
    mov r2, #0x2
    ldr r1, [r0, #0]
    mov r0, #0x45
    lsl r0, r0, #0x2
    ldr r0, [r1, r0]
    mov r1, #0x0
    mvn r1, r1
    bl native_fn_02202f54
    mov r0, #0x0
    ldr r1, =native_fn_021f2f60+1
    add r2, r0, #0x0
    mov r3, #0x78
    bl native_fn_0220490c
    ldr r2, =native_data9_0221c05c
    mov r1, #0x46
    ldr r3, [r2, #0]
    lsl r1, r1, #0x2
    str r0, [r3, r1]
    add r0, r1, #0x5
    ldr r2, [r2, #0]
    mov r1, #0x0
    ldrb r0, [r2, r0]
    mov r2, #0xc0
    bl native_fn_021f37f0
    add sp, #0x38
    pop {r3, r4, r5, r6, r7, pc}
}
