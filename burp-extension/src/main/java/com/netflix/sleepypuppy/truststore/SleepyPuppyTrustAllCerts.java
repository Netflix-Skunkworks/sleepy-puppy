package com.netflix.sleepypuppy.truststore;

import org.apache.http.conn.ssl.TrustStrategy;

import java.security.cert.CertificateException;
import java.security.cert.X509Certificate;

/**
 * Created by rperam on 9/14/15.
 */
public class SleepyPuppyTrustAllCerts implements TrustStrategy {

    public boolean isTrusted(
            final X509Certificate[] chain, final String authType) throws CertificateException {
        return true;
    }
}
