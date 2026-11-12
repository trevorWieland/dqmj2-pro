/* main row 0x02025578: 952 bytes.
 *
 * What it does: normalises a soft-float quotient through a 256-byte reciprocal table
 *
 * Carrier: mwccarm asm with dcd data runs.
 * The measured extent is code plus data inside the function. The data
 * runs are emitted as data, not decoded as instructions; every
 * instruction, branch target, pool word and table entry is read from
 * the image.
 *
 * Unknowns: the reciprocal table's producer and every call-site contract; the table content and bounds are measured.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;




asm u32 native_main_02025578 (register u32 a0)
{
    stmdb sp!, {lr}
    mov r12, #255
    ands r3, r12, r0, lsr #23
    cmpne r3, #255
    beq L_0202574c
    ands r12, r12, r1, lsr #23
    cmpne r12, #255
    beq L_02025788
    orr r1, r1, #8388608
    orr r0, r0, #8388608
    bic r2, r0, #-16777216
    bic lr, r1, #-16777216
L_020255a8:
    cmp r2, lr
    movlo r2, r2, lsl #1
    sublo r3, r3, #1
    teq r0, r1
    sub r0, pc, #148
    ldrb r1, [r0, lr, lsr #15]
    rsb lr, lr, #0
    mov r0, lr, asr #1
    mul r0, r1, r0
    add r0, r0, #-2147483648
    mov r0, r0, lsr #6
    mul r0, r1, r0
    mov r0, r0, lsr #14
    mul r1, r14, r0
    sub r12, r3, r12
    mov r1, r1, lsr #12
    mul r1, r0, r1
    mov r0, r0, lsl #14
    add r0, r0, r1, lsr #15
    umull r1, r0, r2, r0
    mov r3, r0
    orrmi r0, r0, #-2147483648
    adds r12, r12, #126
    bmi L_02025850
    cmp r12, #254
    bge L_02025904
    add r0, r0, r12, lsl #23
    mov r12, r1, lsr #28
    cmp r12, #7
    beq L_0202572c
    add r0, r0, r1, lsr #31
    ldmia sp!, {lr}
    bx lr
    dcd 0xfdfeffff
    dcd 0xf9fafbfc
    dcd 0xf5f6f7f8
    dcd 0xf1f2f3f4
    dcd 0xeeeff0f0
    dcd 0xeaebeced
    dcd 0xe7e8e9ea
    dcd 0xe4e5e6e6
    dcd 0xe1e2e2e3
    dcd 0xdedfdfe0
    dcd 0xdbdcdcdd
    dcd 0xd8d9d9da
    dcd 0xd5d6d7d7
    dcd 0xd2d3d4d4
    dcd 0xd0d0d1d2
    dcd 0xcdcececf
    dcd 0xcbcbcccc
    dcd 0xc8c9c9ca
    dcd 0xc6c6c7c8
    dcd 0xc3c4c5c5
    dcd 0xc1c2c2c3
    dcd 0xbfbfc0c0
    dcd 0xbdbdbebe
    dcd 0xbabbbcbc
    dcd 0xb8b9b9ba
    dcd 0xb6b7b7b8
    dcd 0xb4b5b5b6
    dcd 0xb2b3b3b4
    dcd 0xb0b1b1b2
    dcd 0xafafafb0
    dcd 0xadadaeae
    dcd 0xababacac
    dcd 0xa9aaaaaa
    dcd 0xa7a8a8a9
    dcd 0xa6a6a7a7
    dcd 0xa4a4a5a5
    dcd 0xa2a3a3a4
    dcd 0xa1a1a2a2
    dcd 0x9fa0a0a0
    dcd 0x9e9e9e9f
    dcd 0x9c9d9d9d
    dcd 0x9b9b9b9c
    dcd 0x999a9a9a
    dcd 0x98989999
    dcd 0x96979798
    dcd 0x95959696
    dcd 0x94949495
    dcd 0x92939393
    dcd 0x91919292
    dcd 0x90909191
    dcd 0x8f8f8f90
    dcd 0x8d8e8e8e
    dcd 0x8c8c8d8d
    dcd 0x8b8b8c8c
    dcd 0x8a8a8a8b
    dcd 0x8989898a
    dcd 0x88888888
    dcd 0x86878787
    dcd 0x85868686
    dcd 0x84858585
    dcd 0x83838484
    dcd 0x82828383
    dcd 0x81818282
    dcd 0x80808181
L_0202572c:
    mov r1, r3, lsl #1
    add r1, r1, #1
    rsb lr, lr, #0
    mul r1, r14, r1
    cmp r1, r2, lsl #24
    addmi r0, r0, #1
    ldmia sp!, {lr}
    bx lr
L_0202574c:
    eor lr, r0, r1
    and lr, lr, #-2147483648
    cmp r3, #0
    beq L_020257a4
    movs r0, r0, lsl #9
    bne L_020258ec
    mov r12, r1, lsr #23
    mov r1, r1, lsl #9
    ands r12, r12, #255
    beq L_020258dc
    cmp r12, #255
    blt L_020258dc
    cmp r1, #0
    beq L_020258f8
    b L_020258d4
L_02025788:
    eor lr, r0, r1
    and lr, lr, #-2147483648
    cmp r12, #0
    beq L_02025808
L_02025798:
    movs r1, r1, lsl #9
    bne L_020258d4
    b L_02025924
L_020257a4:
    movs r2, r0, lsl #9
    beq L_020257d8
    clz r3, r2
    movs r2, r2, lsl r3
    rsb r3, r3, #0
    mov r2, r2, lsr #8
    ands r12, r12, r1, lsr #23
    beq L_02025830
    cmp r12, #255
    beq L_02025798
    orr r1, r1, #8388608
    bic lr, r1, #-16777216
    b L_020255a8
L_020257d8:
    mov r12, r1, lsr #23
    mov r1, r1, lsl #9
    ands r12, r12, #255
    beq L_020257fc
    cmp r12, #255
    blt L_02025924
    cmp r1, #0
    beq L_02025924
    b L_020258d4
L_020257fc:
    cmp r1, #0
    beq L_020258f8
    b L_02025924
L_02025808:
    movs r12, r1, lsl #9
    beq L_020258dc
    mov lr, r12
    clz r12, lr
    movs lr, lr, lsl r12
    rsb r12, r12, #0
    mov lr, lr, lsr #8
    orr r0, r0, #8388608
    bic r2, r0, #-16777216
    b L_020255a8
L_02025830:
    movs r12, r1, lsl #9
    beq L_020258dc
    mov lr, r12
    clz r12, lr
    movs lr, lr, lsl r12
    rsb r12, r12, #0
    mov lr, lr, lsr #8
    b L_020255a8
L_02025850:
    and r0, r0, #-2147483648
    cmn r12, #24
    beq L_020258c4
    bmi L_0202591c
    add r1, r12, #23
    mov r2, r2, lsl r1
    rsb r12, r12, #0
    mov r3, r3, lsr r12
    orr r0, r0, r3
    rsb lr, lr, #0
    mul r1, r14, r3
    cmp r1, r2
    ldmeqia sp!, {lr}
    bxeq lr
    add r1, r1, lr
    cmp r1, r2
    beq L_020258b8
    addmi r0, r0, #1
    subpl r1, r1, lr
    add r1, lr, r1, lsl #1
    cmp r1, r2, lsl #1
    and r3, r0, #1
    addmi r0, r0, #1
    addeq r0, r0, r3
    ldmia sp!, {lr}
    bx lr
L_020258b8:
    add r0, r0, #1
    ldmia sp!, {lr}
    bx lr
L_020258c4:
    cmn r2, lr
    addne r0, r0, #1
    ldmia sp!, {lr}
    bx lr
L_020258d4:
    mov r0, r1
    b L_020258ec
L_020258dc:
    mov r0, #-16777216
    orr r0, lr, r0, lsr #1
    ldmia sp!, {lr}
    bx lr
L_020258ec:
    mvn r0, #-2147483648
    ldmia sp!, {lr}
    bx lr
L_020258f8:
    mvn r0, #-2147483648
    ldmia sp!, {lr}
    bx lr
L_02025904:
    tst r0, #-2147483648
    mov r0, #-16777216
    movne r0, r0, asr #1
    moveq r0, r0, lsr #1
    ldmia sp!, {lr}
    bx lr
L_0202591c:
    ldmia sp!, {lr}
    bx lr
L_02025924:
    mov r0, lr
    ldmia sp!, {lr}
    bx lr
}
