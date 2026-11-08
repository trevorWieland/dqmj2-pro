#include "host_session.h"
#include <android/log.h>
#include <android/native_window_jni.h>
#include <jni.h>
#include <pthread.h>
#include <stdio.h>

typedef struct { ANativeWindow *window; jlong token; int width, height, rotation; uint64_t frames; uint32_t hash; } Slot;
static J2pHostSession session;
static Slot slots[2];
static pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
static int initialized, probe_status = -1;
static uint64_t attached, detached, stale, refused;
int j2p_probe_run(void);

#define JNI(name) Java_dev_dqmj2pro_dualsurface_native3_NativeBridge_##name

JNIEXPORT jint JNICALL JNI(init)(JNIEnv *env, jclass type) {
    (void)env; (void)type;
    pthread_mutex_lock(&mutex);
    if (!initialized) { probe_status = j2p_probe_run(); initialized = j2p_host_init(&session); }
    pthread_mutex_unlock(&mutex);
    return initialized ? probe_status : -2;
}

JNIEXPORT jboolean JNICALL JNI(attach)(JNIEnv *env, jclass type, jint slot, jlong token, jobject surface) {
    ANativeWindow *window;
    (void)type;
    if (slot < 0 || slot > 1 || token <= 0 || !surface) return JNI_FALSE;
    window = ANativeWindow_fromSurface(env, surface);
    if (!window) return JNI_FALSE;
    pthread_mutex_lock(&mutex);
    if (token <= slots[slot].token) {
        ++stale; ANativeWindow_release(window); pthread_mutex_unlock(&mutex); return JNI_FALSE;
    }
    if (slots[slot].window) ANativeWindow_release(slots[slot].window);
    slots[slot].window = window; slots[slot].token = token;
    slots[slot].frames = 0; slots[slot].hash = 0;
    slots[slot].width = 0; slots[slot].height = 0;
    ANativeWindow_setBuffersGeometry(window, 256, 192, WINDOW_FORMAT_RGBA_8888);
    ++attached;
    pthread_mutex_unlock(&mutex);
    return JNI_TRUE;
}

JNIEXPORT void JNICALL JNI(detach)(JNIEnv *env, jclass type, jint slot, jlong token) {
    (void)env; (void)type;
    pthread_mutex_lock(&mutex);
    if (slot >= 0 && slot < 2 && slots[slot].token == token) {
        if (slots[slot].window) { ANativeWindow_release(slots[slot].window); slots[slot].window = NULL; ++detached; }
    } else ++stale;
    pthread_mutex_unlock(&mutex);
}

JNIEXPORT void JNICALL JNI(resize)(JNIEnv *env, jclass type, jint slot, jlong token, jint width, jint height, jint rotation) {
    (void)env; (void)type;
    pthread_mutex_lock(&mutex);
    if (slot >= 0 && slot < 2 && slots[slot].token == token && width > 0 && height > 0) {
        slots[slot].width = width; slots[slot].height = height; slots[slot].rotation = rotation;
        if (slots[slot].window) ANativeWindow_setBuffersGeometry(slots[slot].window, 256, 192, WINDOW_FORMAT_RGBA_8888);
    } else ++stale;
    pthread_mutex_unlock(&mutex);
}

JNIEXPORT jboolean JNICALL JNI(touch)(JNIEnv *env, jclass type, jint slot, jlong token, jint x, jint y) {
    int result = 0;
    (void)env; (void)type;
    pthread_mutex_lock(&mutex);
    if (slot >= 0 && slot < 2 && slots[slot].window && slots[slot].token == token) result = j2p_host_touch(&session, x, y);
    if (!result) ++refused;
    pthread_mutex_unlock(&mutex);
    return result ? JNI_TRUE : JNI_FALSE;
}

JNIEXPORT void JNICALL JNI(frame)(JNIEnv *env, jclass type) {
    unsigned i;
    (void)env; (void)type;
    pthread_mutex_lock(&mutex);
    j2p_host_step(&session);
    for (i = 0; i < 2; ++i) if (slots[i].window) {
        ANativeWindow_Buffer b;
        if (ANativeWindow_lock(slots[i].window, &b, NULL) == 0) {
            if (b.format == WINDOW_FORMAT_RGBA_8888 && b.width > 0 && b.height > 0 && b.stride >= b.width && b.stride <= 4096 && b.height <= 4096) {
                if (j2p_host_render(&session, i, b.bits, (size_t)b.stride * b.height * 4, b.width, b.height, b.stride * 4)) {
                    uint8_t *pixels = b.bits;
                    uint32_t hash = 2166136261u;
                    size_t n;
                    for (n = 0; n < (size_t)b.stride * b.height * 4; n += 31) hash = (hash ^ pixels[n]) * 16777619u;
                    slots[i].hash = hash; ++slots[i].frames;
                }
            }
            ANativeWindow_unlockAndPost(slots[i].window);
        }
    }
    pthread_mutex_unlock(&mutex);
}

JNIEXPORT jstring JNICALL JNI(state)(JNIEnv *env, jclass type) {
    char buffer[1536];
    (void)type;
    pthread_mutex_lock(&mutex);
    snprintf(buffer, sizeof(buffer), "{\"probeExit\":%d,\"frames\":%llu,\"touches\":%llu,\"revision\":%llu,\"xy\":[%d,%d],\"matrixXY\":[%d,%d],\"attached\":%llu,\"detached\":%llu,\"stale\":%llu,\"refused\":%llu,\"slots\":[{\"live\":%s,\"token\":%lld,\"frames\":%llu,\"hash\":%u,\"view\":[%d,%d],\"rotation\":%d},{\"live\":%s,\"token\":%lld,\"frames\":%llu,\"hash\":%u,\"view\":[%d,%d],\"rotation\":%d}]}",
        probe_status, (unsigned long long)session.frames, (unsigned long long)session.touches, (unsigned long long)session.revision, session.x, session.y,
        session.state.matrices[1][12], session.state.matrices[1][13], (unsigned long long)attached, (unsigned long long)detached, (unsigned long long)stale, (unsigned long long)refused,
        slots[0].window ? "true" : "false", (long long)slots[0].token, (unsigned long long)slots[0].frames, slots[0].hash, slots[0].width, slots[0].height, slots[0].rotation,
        slots[1].window ? "true" : "false", (long long)slots[1].token, (unsigned long long)slots[1].frames, slots[1].hash, slots[1].width, slots[1].height, slots[1].rotation);
    pthread_mutex_unlock(&mutex);
    return (*env)->NewStringUTF(env, buffer);
}
