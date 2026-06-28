package com.caijaihang.pharmacycompare;

import android.content.Context;
import android.util.Log;
import java.io.IOException;
import java.net.ServerSocket;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;

public class PythonServer {

    private static final String TAG = "PythonServer";
    private final Context context;
    private int port;
    private Thread serverThread;
    private volatile boolean running = false;
    private final ExecutorService executor = Executors.newSingleThreadExecutor();

    public PythonServer(Context context) {
        this.context = context;
    }

    public int start() {
        port = findFreePort(5000);
        final int finalPort = port;

        running = true;
        serverThread = new Thread(() -> {
            try {
                if (!Python.isStarted()) {
                    Python.start(new AndroidPlatform(context));
                }
            } catch (Exception e) {
                Log.e(TAG, "Python start failed", e);
                return;
            }

            executor.execute(() -> {
                try {
                    Python py = Python.getInstance();
                    py.getModule("android_server").callAttr("start_server", finalPort);
                } catch (Exception e) {
                    Log.e(TAG, "Flask server start failed", e);
                }
            });
        });
        serverThread.start();

        try { Thread.sleep(3000); } catch (InterruptedException ignored) {}
        return finalPort;
    }

    public void stop() {
        running = false;
        if (serverThread != null) {
            serverThread.interrupt();
        }
        executor.shutdownNow();
    }

    private int findFreePort(int startPort) {
        for (int port = startPort; port < startPort + 20; port++) {
            try (ServerSocket socket = new ServerSocket(port)) {
                return port;
            } catch (IOException ignored) {
            }
        }
        return startPort;
    }
}
