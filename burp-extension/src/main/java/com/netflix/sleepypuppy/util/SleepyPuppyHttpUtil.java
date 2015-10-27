package com.netflix.sleepypuppy.util;

import com.netflix.sleepypuppy.truststore.SleepyPuppyTrustAllCerts;
import com.netflix.sleepypuppy.truststore.SleepyPuppyTrustStoreUtil;
import org.apache.http.HttpEntity;
import org.apache.http.HttpStatus;
import org.apache.http.client.config.RequestConfig;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.conn.ssl.SSLConnectionSocketFactory;
import org.apache.http.conn.ssl.SSLContextBuilder;
import org.apache.http.conn.ssl.SSLContexts;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;

import javax.net.ssl.SSLContext;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.charset.Charset;
import java.security.KeyManagementException;
import java.security.KeyStore;
import java.security.KeyStoreException;
import java.security.NoSuchAlgorithmException;

/**
 * Created by rperam on 9/14/15.
 */
public class SleepyPuppyHttpUtil {
    private static final int connectionTimeoutMillis = 5000;
    private static final int socketTimeoutMillis = 5000;
    private static final String TRUSTSTORE_LOCATION = "SLEEPYPUPPY_TRUSTSTORE_LOCATION";
    private static final String TRUSTSTORE_PASSWORD = "SLEEPYPUPPY_TRUSTSTORE_PASSWORD";
    private static final String INSECURE_HTTPS = "SLEEPYPUPPY_TRUST_ALL_CERTS";


    public static String sendGetRequest(PrintWriter stderr, String url,
                                        String token) {
        CloseableHttpResponse response = null;
        String data = "";

        CloseableHttpClient httpClient = getAppropriateHttpClient(stderr, url);
        if (httpClient != null) {
            try {
                HttpGet httpGet = new HttpGet(url);
                httpGet.addHeader("Content-Type", "application/json");
                httpGet.addHeader("Token", token);

                response = httpClient.execute(httpGet);
                if (response.getStatusLine().getStatusCode() != HttpStatus.SC_OK) {
                    stderr.println("Unable to fetch data from URL = " + url + " : " + data);
                    return data;
                }

                data = EntityUtils.toString(response.getEntity(), "UTF-8").trim();
            } catch (IOException e) {
                stderr.println("Unable to fetch data from URL = " + url + " : " + e.getMessage());
            } finally {
                closeResources(stderr, httpClient, response);
            }
        }
        return data;
    }

    public static String sendPostRequestWithJsonPayload(PrintWriter stderr,
                                                        String url, String jsonPayload, String token) {
        CloseableHttpResponse response = null;
        String data = "";

        CloseableHttpClient httpClient = getAppropriateHttpClient(stderr, url);
        if (httpClient != null) {
            try {
                HttpPost httpPost = new HttpPost(url);
                httpPost.addHeader("Content-Type", "application/json");
                httpPost.addHeader("Token", token);

                StringEntity params = new StringEntity(jsonPayload);
                httpPost.setEntity(params);
                response = httpClient.execute(httpPost);

                HttpEntity entity = response.getEntity();

                data = entity != null ? EntityUtils.toString(entity, Charset.forName("UTF-8")) : "";
            } catch (IOException e) {
                stderr.println("Error sending a POST request: " + e.getMessage());
            } finally {
                closeResources(stderr, httpClient, response);
            }
        }
        return data;
    }

    private static CloseableHttpClient getAppropriateHttpClient(PrintWriter stderr, String url) {
        if (url.startsWith("https:")) {
            String insecure = System.getProperty(INSECURE_HTTPS);
            if (insecure != null && !insecure.isEmpty() && insecure.equalsIgnoreCase("true")) {
                return getInSecureHttpsClient(stderr);
            } else {
                return getSecureHttpsClient(stderr);
            }
        } else if (url.startsWith("http:")) {
            return getHttpClient();
        } else {
            stderr.println("URL must start with http or https");
            return null;
        }
    }

    private static CloseableHttpClient getHttpClient() {

        RequestConfig requestConfig = RequestConfig.custom()
                .setConnectTimeout(connectionTimeoutMillis)
                .setSocketTimeout(socketTimeoutMillis)
                .setStaleConnectionCheckEnabled(true)
                .build();

        return HttpClients.custom()
                .setDefaultRequestConfig(requestConfig)
                .build();

    }

    private static CloseableHttpClient getInSecureHttpsClient(PrintWriter stderr) {
        CloseableHttpClient httpClient = null;
        try {
            SSLContextBuilder builder = new SSLContextBuilder();
            builder.loadTrustMaterial(null, new SleepyPuppyTrustAllCerts());
            SSLConnectionSocketFactory sslConnectionSocketFactory = new SSLConnectionSocketFactory(
                    builder.build(), SSLConnectionSocketFactory.ALLOW_ALL_HOSTNAME_VERIFIER);

            httpClient = HttpClients.custom()
                    .setSSLSocketFactory(sslConnectionSocketFactory).build();
        } catch (Exception e) {
            stderr.println("Error while creating an Insecure HTTPS Client" + e.getMessage());
        }
        return httpClient;
    }

    private static CloseableHttpClient getSecureHttpsClient(PrintWriter stderr) {

        CloseableHttpClient httpClient = null;
        String trustStoreLocation = getPropertyValue(TRUSTSTORE_LOCATION, stderr);
        String password = getPropertyValue(TRUSTSTORE_PASSWORD, stderr);

        if (trustStoreLocation != null && !trustStoreLocation.isEmpty() && password != null && !password.isEmpty()) {
            try {
                // Load the truststore
                KeyStore trustStore = SleepyPuppyTrustStoreUtil.getKeyStore(stderr, trustStoreLocation, password);
                if (trustStore == null) {
                    stderr.println("Unable to load TrustStore file");
                }

                final SSLContext sslContext = SSLContexts.custom()
                        .loadTrustMaterial(trustStore)
                        .useTLS()
                        .build();

                RequestConfig requestConfig = RequestConfig.custom()
                        .setConnectTimeout(connectionTimeoutMillis)
                        .setSocketTimeout(socketTimeoutMillis)
                        .setStaleConnectionCheckEnabled(true)
                        .build();

                httpClient = HttpClients.custom()
                        .setSSLSocketFactory(new SSLConnectionSocketFactory(sslContext,
                                SSLConnectionSocketFactory.ALLOW_ALL_HOSTNAME_VERIFIER))
                        .setDefaultRequestConfig(requestConfig)
                        .setMaxConnPerRoute(4)
                        .setMaxConnTotal(24)
                        .build();

            } catch (KeyStoreException | KeyManagementException | NoSuchAlgorithmException e) {
                stderr.println("Error while creating a secure HTTP Client" + e.getMessage());
            }
        }
        return httpClient;
    }

    private static String getPropertyValue(String propertyName, PrintWriter stderr) {
        String value = null;

        // Get property value from VM Options (set using "-Dproperty=value" in command line as part of burp startup command)
        value = System.getProperty(propertyName);
        if (value == null || value.isEmpty()) {
            // Get property value from Environment variable (set using "export property=value" in command line)
            value = System.getenv(propertyName);
            if (value == null || value.isEmpty()) {
                stderr.println(propertyName + " must be set as either an environment variable or a jvm startup option");
            }
        }
        return value;
    }

    private static void closeResources(PrintWriter stderr, CloseableHttpClient httpClient,
                                       CloseableHttpResponse response) {
        try {
            if (response != null) {
                response.close();
            }
            if (httpClient != null) {
                httpClient.close();
            }
        } catch (IOException ioe) {
            stderr.println("Error closing InputStream: " + ioe.getMessage());
        }
    }

}
