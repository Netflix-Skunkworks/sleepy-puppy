package com.netflix.sleepypuppy.truststore;

import java.io.*;
import java.security.KeyStore;
import java.security.KeyStoreException;
import java.security.NoSuchAlgorithmException;
import java.security.cert.CertificateException;

/**
 * Created by rperam on 9/30/15.
 */
public class SleepyPuppyTrustStoreUtil {
    public static KeyStore getKeyStore(PrintWriter stderr, String trustStoreLocation, String password)
            throws KeyStoreException {
        InputStream trustStoreInputStream = null;
        try {
            trustStoreInputStream = getFileInputStream(trustStoreLocation);

            KeyStore trustStore = KeyStore.getInstance(KeyStore.getDefaultType());
            trustStore.load(trustStoreInputStream, password.toCharArray());

            return trustStore;
        } catch (CertificateException | KeyStoreException | NoSuchAlgorithmException | IOException kse) {
            stderr.println("Error loading TrustStore: " + kse.getMessage());
            throw new KeyStoreException(kse);
        } finally {
            if (trustStoreInputStream != null) {
                try {
                    trustStoreInputStream.close();
                } catch (IOException ignore) {
                    stderr.println("Error closing InputStream: " + ignore.getMessage());
                }
            }
        }
    }

    private static InputStream getFileInputStream(String fileLocation)
            throws FileNotFoundException {
        // Look for file in classpath in the war file (relative path)
        InputStream inputStream = Thread.currentThread().getContextClassLoader().getResourceAsStream(fileLocation);
        // file not found in classpath
        if (inputStream == null) {
            // Look for file in disk (absolute path)
            File file = new File(fileLocation);
            inputStream = new FileInputStream(file);
        }

        return inputStream;
    }
}
