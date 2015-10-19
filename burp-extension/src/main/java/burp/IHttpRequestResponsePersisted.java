package burp;

/*
 * @(#)IHttpRequestResponsePersisted.java
 *
 * Copyright PortSwigger Ltd. All rights reserved.
 *
 * This code may be used to extend the functionality of Burp Suite Free Edition
 * and Burp Suite Professional, provided that this usage does not violate the
 * license terms for those products.
 */
/**
 * This interface is used for an
 * <code>IHttpRequestResponse</code> object whose request and response messages
 * have been saved to temporary files using
 * <code>IBurpExtenderCallbacks.saveBuffersToTempFiles()</code>.
 */
public interface IHttpRequestResponsePersisted extends IHttpRequestResponse
{
    /**
     * This method is used to permanently delete the saved temporary files. It
     * will no longer be possible to retrieve the request or response for this
     * item.
     */
    void deleteTempFiles();
}
