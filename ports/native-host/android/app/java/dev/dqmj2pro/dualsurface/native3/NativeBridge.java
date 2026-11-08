package dev.dqmj2pro.dualsurface.native3;

import android.view.Surface;

final class NativeBridge {
    static { System.loadLibrary("j2p_dualsurface"); }
    static native int init();
    static native boolean attach(int slot, long token, Surface surface);
    static native void detach(int slot, long token);
    static native void resize(int slot, long token, int width, int height, int rotation);
    static native boolean touch(int slot, long token, int x, int y);
    static native void frame();
    static native String state();
    private NativeBridge() {}
}
