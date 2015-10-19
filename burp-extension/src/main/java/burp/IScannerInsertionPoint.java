package burp;

/*
 * @(#)IScannerInsertionPoint.java
 *
 * Copyright PortSwigger Ltd. All rights reserved.
 *
 * This code may be used to extend the functionality of Burp Suite Free Edition
 * and Burp Suite Professional, provided that this usage does not violate the
 * license terms for those products.
 */
/**
 * This interface is used to define an insertion point for use by active Scanner
 * checks. Extensions can obtain instances of this interface by registering an
 * <code>IScannerCheck</code>, or can create instances for use by Burp's own
 * scan checks by registering an
 * <code>IScannerInsertionPointProvider</code>.
 */
public interface IScannerInsertionPoint
{
    /**
     * Used to indicate where the payload is inserted into the value of a URL
     * parameter.
     */
    static final byte INS_PARAM_URL = 0x00;
    /**
     * Used to indicate where the payload is inserted into the value of a body
     * parameter.
     */
    static final byte INS_PARAM_BODY = 0x01;
    /**
     * Used to indicate where the payload is inserted into the value of an HTTP
     * cookie.
     */
    static final byte INS_PARAM_COOKIE = 0x02;
    /**
     * Used to indicate where the payload is inserted into the value of an item
     * of data within an XML data structure.
     */
    static final byte INS_PARAM_XML = 0x03;
    /**
     * Used to indicate where the payload is inserted into the value of a tag
     * attribute within an XML structure.
     */
    static final byte INS_PARAM_XML_ATTR = 0x04;
    /**
     * Used to indicate where the payload is inserted into the value of a
     * parameter attribute within a multi-part message body (such as the name of
     * an uploaded file).
     */
    static final byte INS_PARAM_MULTIPART_ATTR = 0x05;
    /**
     * Used to indicate where the payload is inserted into the value of an item
     * of data within a JSON structure.
     */
    static final byte INS_PARAM_JSON = 0x06;
    /**
     * Used to indicate where the payload is inserted into the value of an AMF
     * parameter.
     */
    static final byte INS_PARAM_AMF = 0x07;
    /**
     * Used to indicate where the payload is inserted into the value of an HTTP
     * request header.
     */
    static final byte INS_HEADER = 0x20;
    /**
     * Used to indicate where the payload is inserted into a REST parameter
     * within the URL file path.
     */
    static final byte INS_URL_REST = 0x21;
    /**
     * Used to indicate where the payload is inserted into the name of an added
     * URL parameter.
     */
    static final byte INS_PARAM_NAME_URL = 0x22;
    /**
     * Used to indicate where the payload is inserted into the name of an added
     * body parameter.
     */
    static final byte INS_PARAM_NAME_BODY = 0x23;
    /**
     * Used to indicate where the payload is inserted at a location manually
     * configured by the user.
     */
    static final byte INS_USER_PROVIDED = 0x40;
    /**
     * Used to indicate where the insertion point is provided by an
     * extension-registered
     * <code>IScannerInsertionPointProvider</code>.
     */
    static final byte INS_EXTENSION_PROVIDED = 0x41;
    /**
     * Used to indicate where the payload is inserted at an unknown location
     * within the request.
     */
    static final byte INS_UNKNOWN = 0x7f;

    /**
     * This method returns the name of the insertion point.
     *
     * @return The name of the insertion point (for example, a description of a
     * particular request parameter).
     */
    String getInsertionPointName();

    /**
     * This method returns the base value for this insertion point.
     *
     * @return the base value that appears in this insertion point in the base
     * request being scanned, or
     * <code>null</code> if there is no value in the base request that
     * corresponds to this insertion point.
     */
    String getBaseValue();

    /**
     * This method is used to build a request with the specified payload placed
     * into the insertion point. Any necessary adjustments to the Content-Length
     * header will be made by the Scanner itself when the request is issued, and
     * there is no requirement for the insertion point to do this. <b>Note:</b>
     * Burp's built-in scan checks do not apply any payload encoding (such as
     * URL-encoding) when dealing with an extension-provided insertion point.
     * Custom insertion points are responsible for performing any data encoding
     * that is necessary given the nature and location of the insertion point.
     *
     * @param payload The payload that should be placed into the insertion
     * point.
     * @return The resulting request.
     */
    byte[] buildRequest(byte[] payload);

    /**
     * This method is used to determine the offsets of the payload value within
     * the request, when it is placed into the insertion point. Scan checks may
     * invoke this method when reporting issues, so as to highlight the relevant
     * part of the request within the UI.
     *
     * @param payload The payload that should be placed into the insertion
     * point.
     * @return An int[2] array containing the start and end offsets of the
     * payload within the request, or null if this is not applicable (for
     * example, where the insertion point places a payload into a serialized
     * data structure, the raw payload may not literally appear anywhere within
     * the resulting request).
     */
    int[] getPayloadOffsets(byte[] payload);

    /**
     * This method returns the type of the insertion point.
     *
     * @return The type of the insertion point. Available types are defined in
     * this interface.
     */
    byte getInsertionPointType();
}
